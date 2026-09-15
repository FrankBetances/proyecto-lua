#!/usr/bin/env python3
"""
local_image_to_3d.py
--------------------
Generador local y desatendido de modelos 3D estilizados a partir de imágenes/fotos 2D.
Ejecución en Blender 5.x / 4.x sin necesidad de conexión a internet ni claves de API:

  /Applications/Blender.app/Contents/MacOS/Blender -b --python local_image_to_3d.py -- \\
      --image "personaje.png" \\
      --output "personaje_estilizado.stl" \\
      --target-height-mm 120.0 \\
      --depth-mm 22.0

Algoritmo de Inflado Orgánico (Toy-Art / Chibi / Kindchenschema):
1. Segmenta el sujeto detectando fondos transparentes o lisos (detección adaptativa de color en esquinas).
2. Calcula el campo de distancia euclidiana (EDT / SDF) desde el contorno exterior de la silueta.
3. Aplica un perfil de elevación sinusoidal suave (continuidad de curvatura G2) para inflar la masa
   como un juguete o figura coleccionable, eliminando aristas vivas y cortes en ángulo recto (CSG).
4. Opcional: Proyecta el mapa de luminancia para estampar en relieve suave los detalles interiores (ojos, boca, costuras).
5. Construye una malla cerrada, ejecuta Voxel Remesh unificado y suavizado laplaciano.
6. Entrega un archivo STL 100% estanco (2-Manifold) con base plana en Z=0 para impresión inmediata sin soportes.
"""

import sys
import os
import math
import argparse

try:
    import bpy
    import bmesh
    import numpy as np
    from mathutils import Vector
except ImportError:
    print("[ERROR] Este script debe ejecutarse dentro de Blender:")
    print("  /Applications/Blender.app/Contents/MacOS/Blender -b --python local_image_to_3d.py -- [opciones]")
    sys.exit(1)


def parse_args():
    argv = sys.argv
    if "--" in argv:
        args_to_parse = argv[argv.index("--") + 1:]
    else:
        args_to_parse = []

    parser = argparse.ArgumentParser(description="Generador local de modelos 3D estilizados para impresión FDM")
    parser.add_argument("--image", "-i", required=True, help="Ruta a la imagen o foto 2D (.png, .jpg, .webp)")
    parser.add_argument("--output", "-o", required=True, help="Ruta de exportación del archivo STL (.stl)")
    parser.add_argument("--target-height-mm", type=float, default=120.0, help="Altura deseada del modelo en mm (default: 120.0)")
    parser.add_argument("--depth-mm", type=float, default=20.0, help="Grosor máximo de inflado orgánico en mm (default: 20.0)")
    parser.add_argument("--voxel-size", type=float, default=0.35, help="Resolución de vóxel para remallado en mm (default: 0.35)")
    parser.add_argument("--grid-res", type=int, default=140, help="Resolución horizontal de la grilla de muestreo (default: 140)")
    parser.add_argument("--orientation", choices=["flat", "standing"], default="standing", help="Orientación del modelo: 'standing' (vertical, Z=altura para corte modular) o 'flat' (acostado en cama para imprimir en 1 sola pieza sin soporte)")
    parser.add_argument("--double-sided", action="store_true", help="Crea un modelo inflado simétrico en ambas caras (tipo juguete de vinilo)")
    parser.add_argument("--emboss-details", action="store_true", default=True, help="Relieve sutil de rasgos faciales/interiores basado en luminancia")
    parser.add_argument("--bg-threshold", type=float, default=0.12, help="Umbral de tolerancia de color para detección de fondo (default: 0.12)")
    return parser.parse_args(args_to_parse)


def reset_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for block in bpy.data.meshes:
        bpy.data.meshes.remove(block)
    for img in bpy.data.images:
        bpy.data.images.remove(img)


def compute_distance_transform(fg_mask):
    """
    Transformada de distancia euclidiana rápida de dos pasadas sobre una máscara booleana 2D.
    """
    h, w = fg_mask.shape
    dist = np.zeros((h, w), dtype=np.float32)
    inf = 1e6
    dist[~fg_mask] = 0.0
    dist[fg_mask] = inf

    # Pasada 1: Arriba-Izquierda a Abajo-Derecha
    for r in range(h):
        for c in range(w):
            if not fg_mask[r, c]:
                continue
            v = dist[r, c]
            if r > 0:
                v = min(v, dist[r - 1, c] + 1.0)
                if c > 0:
                    v = min(v, dist[r - 1, c - 1] + 1.4142)
                if c < w - 1:
                    v = min(v, dist[r - 1, c + 1] + 1.4142)
            if c > 0:
                v = min(v, dist[r, c - 1] + 1.0)
            dist[r, c] = v

    # Pasada 2: Abajo-Derecha a Arriba-Izquierda
    for r in range(h - 1, -1, -1):
        for c in range(w - 1, -1, -1):
            if not fg_mask[r, c]:
                continue
            v = dist[r, c]
            if r < h - 1:
                v = min(v, dist[r + 1, c] + 1.0)
                if c > 0:
                    v = min(v, dist[r + 1, c - 1] + 1.4142)
                if c < w - 1:
                    v = min(v, dist[r + 1, c + 1] + 1.4142)
            if c < w - 1:
                v = min(v, dist[r, c + 1] + 1.0)
            dist[r, c] = v

    return dist


def generate_stylized_mesh(args):
    if not os.path.exists(args.image):
        raise FileNotFoundError(f"Imagen no encontrada: {args.image}")

    print(f"\n[1/5] Cargando y analizando imagen: {args.image}...")
    img = bpy.data.images.load(args.image)
    orig_w, orig_h = img.size
    if orig_w == 0 or orig_h == 0:
        raise ValueError(f"Imagen inválida o vacía: {args.image}")

    raw_pixels = np.empty(orig_w * orig_h * 4, dtype=np.float32)
    img.pixels.foreach_get(raw_pixels)
    img_array = raw_pixels.reshape((orig_h, orig_w, 4))

    # Muestreo a grilla de trabajo conservando relación de aspecto
    grid_w = args.grid_res
    grid_h = max(20, int(grid_w * (orig_h / orig_w)))
    print(f"      Resolución de muestreo geométrico: {grid_w} × {grid_h} vóxeles")

    ys = np.linspace(0, orig_h - 1, grid_h).astype(int)
    xs = np.linspace(0, orig_w - 1, grid_w).astype(int)
    sampled = img_array[np.ix_(ys, xs)]

    # Detección de fondo: color de esquinas o transparencia alfa
    bg_candidates = [
        sampled[0, 0, :3],
        sampled[0, -1, :3],
        sampled[-1, 0, :3],
        sampled[-1, -1, :3]
    ]
    bg_color = np.mean(bg_candidates, axis=0)

    color_distance = np.linalg.norm(sampled[:, :, :3] - bg_color, axis=2)
    fg_mask = (color_distance > args.bg_threshold)

    # Si hay canal alfa con transparencia
    if sampled.shape[2] == 4:
        alpha_mask = sampled[:, :, 3] > 0.4
        # Si el alfa contiene información discriminante
        if np.sum(~alpha_mask) > (grid_w * grid_h * 0.05):
            fg_mask = alpha_mask

    fg_count = np.sum(fg_mask)
    if fg_count < 50:
        raise RuntimeError(
            "No se detectó sujeto en la imagen. Verifique que el fondo sea blanco, transparente o contrastado."
        )
    print(f"      Sujeto detectado con éxito: {fg_count:,} píxeles de silueta ({fg_count / (grid_w * grid_h) * 100:.1f}%)")

    # 2. Transformada de distancia euclidiana para inflado orgánico continuo
    print(f"[2/5] Calculando campo de distancia euclidiana para inflado orgánico suave...")
    dist_map = compute_distance_transform(fg_mask)
    max_d = np.max(dist_map)
    if max_d < 1e-3:
        raise RuntimeError("Error en el cálculo del campo de distancias de la silueta.")

    # Normalización con perfil sinusoidal (Continuidad G2 tipo cojín/chibi)
    norm_dist = np.clip(dist_map / max_d, 0.0, 1.0)
    z_elevation = args.depth_mm * np.sin(norm_dist * (np.pi / 2.0))

    # Grabado sutil de rasgos interiores si está habilitado
    if args.emboss_details:
        # Luminancia relativa
        lum = 0.299 * sampled[:, :, 0] + 0.587 * sampled[:, :, 1] + 0.114 * sampled[:, :, 2]
        # Rasgos oscuros (ojos, boca, contornos) se hunden sutilmente (-0.8 mm)
        lum_feature = (1.0 - lum) * norm_dist
        z_elevation -= (lum_feature * 0.8)
        z_elevation = np.maximum(0.0, z_elevation)

    # 3. Construcción topológica de la malla
    print(f"[3/5] Generando geometría estanca hermética (2-Manifold)...")
    bm = bmesh.new()

    # Dimensiones físicas en mm basadas en target_height_mm
    actual_height_mm = args.target_height_mm
    pixel_pitch_mm = actual_height_mm / float(grid_h)

    v_top = {}
    v_bot = {}

    for r in range(grid_h):
        for c in range(grid_w):
            if fg_mask[r, c]:
                x = (c - grid_w / 2.0) * pixel_pitch_mm
                elevation = float(z_elevation[r, c])
                
                if args.orientation == "standing":
                    # X = ancho, Y = espesor/profundidad, Z = altura vertical
                    z = (r - grid_h / 2.0) * pixel_pitch_mm
                    y_t = elevation
                    y_b = -elevation if args.double_sided else 0.0
                    v_top[(r, c)] = bm.verts.new((x, y_t, z))
                    v_bot[(r, c)] = bm.verts.new((x, y_b, z))
                else:
                    # Flat en cama: X = ancho, Y = altura sobre cama, Z = espesor vertical
                    y = (r - grid_h / 2.0) * pixel_pitch_mm
                    z_t = elevation
                    z_b = -elevation if args.double_sided else 0.0
                    v_top[(r, c)] = bm.verts.new((x, y, z_t))
                    v_bot[(r, c)] = bm.verts.new((x, y, z_b))

    bm.verts.ensure_lookup_table()

    # Creación de caras en malla estructurada (quiring)
    for r in range(grid_h - 1):
        for c in range(grid_w - 1):
            quad = [(r, c), (r + 1, c), (r + 1, c + 1), (r, c + 1)]
            if all(p in v_top for p in quad):
                # Cara superior
                bm.faces.new([v_top[p] for p in quad])
                # Cara inferior (invertida para normales hacia afuera)
                bm.faces.new([v_bot[p] for p in reversed(quad)])

    bm.faces.ensure_lookup_table()
    bm.edges.ensure_lookup_table()

    # Cierre hermético perimetral (paredes laterales continuas)
    top_to_bot = {v_top[k]: v_bot[k] for k in v_top}
    boundary_edges = [
        e for e in bm.edges
        if e.is_boundary and e.verts[0] in top_to_bot and e.verts[1] in top_to_bot
    ]

    for e in boundary_edges:
        vt1, vt2 = e.verts[0], e.verts[1]
        vb1, vb2 = top_to_bot[vt1], top_to_bot[vt2]
        bm.faces.new([vt1, vb1, vb2, vt2])

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    mesh_data = bpy.data.meshes.new("StylizedOrganicMesh")
    bm.to_mesh(mesh_data)
    bm.free()

    obj = bpy.data.objects.new("StylizedOrganicObject", mesh_data)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # 4. Remallado unificado de vóxeles y alisado laplaciano
    print(f"[4/5] Aplicando Voxel Remesh unificado ({args.voxel_size} mm) y relajación laplaciana...")
    obj.data.remesh_voxel_size = args.voxel_size
    bpy.ops.object.voxel_remesh()

    mod_smooth = obj.modifiers.new(name="OrganicSmooth", type='SMOOTH')
    mod_smooth.factor = 0.45
    mod_smooth.iterations = 3
    bpy.ops.object.modifier_apply(modifier="OrganicSmooth")

    # Si no es doble cara, apoyar base exactamente en Z=0
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    min_z = min(c.z for c in bbox_corners)
    min_x = min(c.x for c in bbox_corners)
    max_x = max(c.x for c in bbox_corners)
    min_y = min(c.y for c in bbox_corners)
    max_y = max(c.y for c in bbox_corners)

    obj.location.x -= (min_x + max_x) / 2.0
    obj.location.y -= (min_y + max_y) / 2.0
    obj.location.z -= min_z
    bpy.ops.object.transform_apply(location=True)

    # Verificación final
    bm_audit = bmesh.new()
    bm_audit.from_mesh(obj.data)
    non_man = len([e for e in bm_audit.edges if not e.is_manifold])
    bound = len([e for e in bm_audit.edges if e.is_boundary])
    vol_cm3 = abs(bm_audit.calc_volume()) / 1000.0
    bm_audit.free()

    # 5. Exportar STL
    print(f"[5/5] Exportando archivo STL final...")
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    bpy.ops.wm.stl_export(filepath=args.output, export_selected_objects=True)

    if not os.path.exists(args.output) or os.path.getsize(args.output) == 0:
        raise RuntimeError(f"Fallo al escribir el archivo STL: {args.output}")

    print("\n" + "=" * 65)
    print("✨ GENERACIÓN DE FIGURA ESTILIZADA COMPLETADA:")
    print(f"   - Archivo STL: {args.output} ({os.path.getsize(args.output):,} bytes)")
    print(f"   - Dimensiones: {obj.dimensions.x:.1f} × {obj.dimensions.y:.1f} × {obj.dimensions.z:.1f} mm")
    print(f"   - Volumen macizo: {vol_cm3:.2f} cm³ (Masa PLA: ~{vol_cm3 * 1.24:.1f} g)")
    print(f"   - Estanqueidad: {'✅ 100% Watertight (2-Manifold puro)' if non_man == 0 and bound == 0 else f'⚠️ Revisión ({bound} huecos, {non_man} no-manifold)'}")
    print("=" * 65 + "\n")


def run():
    args = parse_args()
    reset_scene()
    generate_stylized_mesh(args)


def main():
    try:
        run()
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
