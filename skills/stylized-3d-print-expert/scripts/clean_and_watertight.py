#!/usr/bin/env python3
"""
clean_and_watertight.py
-----------------------
Post-procesado y acondicionamiento automatizado de mallas 3D para impresión 3D (FDM/SLA).
Transforma modelos crudos procedentes de generadores IA (Trellis, Tripo, Meshy, Rodin) o
esculturas digitales en mallas sólidas 100% estancas (Watertight / 2-Manifold), escaladas
a milímetros reales y optimizadas para laminadores (Cura, PrusaSlicer, Bambu Studio).

Uso:
  /Applications/Blender.app/Contents/MacOS/Blender -b --python clean_and_watertight.py -- \\
      --input modelo_ia_crudo.glb \\
      --output modelo_imprimible.stl \\
      --target-height-mm 160.0 \\
      --voxel-size 0.30 \\
      --align-bed \\
      --center-xy
"""

import sys
import os
import argparse

try:
    import bpy
    import bmesh
    from mathutils import Vector
except ImportError:
    print("[ERROR] Este script debe ejecutarse dentro del entorno de Blender:")
    print("  /Applications/Blender.app/Contents/MacOS/Blender -b --python clean_and_watertight.py -- [opciones]")
    sys.exit(1)


def parse_args():
    argv = sys.argv
    if "--" in argv:
        args_to_parse = argv[argv.index("--") + 1:]
    else:
        args_to_parse = []

    parser = argparse.ArgumentParser(description="Limpieza, solidificación y remallado estanco para impresión 3D")
    parser.add_argument("--input", "-i", required=True, help="Ruta al archivo 3D de entrada (.glb, .gltf, .obj, .stl)")
    parser.add_argument("--output", "-o", required=True, help="Ruta de salida del STL (.stl)")
    parser.add_argument("--target-height-mm", type=float, default=None, help="Altura deseada en mm (eje Z)")
    parser.add_argument("--voxel-size", type=float, default=0.30, help="Tamaño de vóxel en mm para el remallado unificado (default: 0.30)")
    parser.add_argument("--smooth-factor", type=float, default=0.40, help="Factor de suavizado para eliminar ruido de alta frecuencia (default: 0.40)")
    parser.add_argument("--smooth-repeat", type=int, default=2, help="Iteraciones de suavizado laplaciano (default: 2)")
    parser.add_argument("--target-faces", type=int, default=120000, help="Máximo de triángulos objetivo tras remallado (default: 120000)")
    
    # Flags con capacidad de desactivación mediante --no-*
    if hasattr(argparse, "BooleanOptionalAction"):
        parser.add_argument("--auto-scale-mm", action=argparse.BooleanOptionalAction, default=True, help="Detecta si el modelo está en metros (<2.5) y lo multiplica por 1000")
        parser.add_argument("--align-bed", action=argparse.BooleanOptionalAction, default=True, help="Apoya la base del modelo exactamente en Z = 0 (cama de impresión)")
        parser.add_argument("--center-xy", action=argparse.BooleanOptionalAction, default=True, help="Centra el modelo en el origen horizontal (X=0, Y=0)")
    else:
        parser.add_argument("--auto-scale-mm", dest="auto_scale_mm", action="store_true", default=True)
        parser.add_argument("--no-auto-scale-mm", dest="auto_scale_mm", action="store_false")
        parser.add_argument("--align-bed", dest="align_bed", action="store_true", default=True)
        parser.add_argument("--no-align-bed", dest="align_bed", action="store_false")
        parser.add_argument("--center-xy", dest="center_xy", action="store_true", default=True)
        parser.add_argument("--no-center-xy", dest="center_xy", action="store_false")

    return parser.parse_args(args_to_parse)


def reset_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for block in bpy.data.meshes:
        bpy.data.meshes.remove(block)


def import_and_join(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Archivo de entrada inexistente: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".stl":
        bpy.ops.wm.stl_import(filepath=filepath)
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=filepath)
    elif ext in [".glb", ".gltf"]:
        bpy.ops.import_scene.gltf(filepath=filepath)
    else:
        raise ValueError(f"Formato no soportado: {ext}. Solo se admiten .glb, .gltf, .obj y .stl")

    mesh_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    if not mesh_objs:
        # Fallback a buscar en todos los objetos de la escena por si el importador no seleccionó
        mesh_objs = [obj for obj in bpy.data.objects if obj.type == 'MESH']
        if not mesh_objs:
            raise RuntimeError(f"No se encontró ninguna geometría de malla importada en {filepath}.")

    # Unificar si el modelo viene dividido en múltiples mallas o piezas
    if len(mesh_objs) > 1:
        bpy.context.view_layer.objects.active = mesh_objs[0]
        for o in mesh_objs:
            o.select_set(True)
        bpy.ops.object.join()
        obj = mesh_objs[0]
    else:
        obj = mesh_objs[0]
        bpy.context.view_layer.objects.active = obj

    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def process_mesh(obj, args):
    print(f"\n[1/6] Analizando geometría original: {len(obj.data.polygons):,} polígonos, dimensiones: {obj.dimensions}")

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Detección de escala metros -> milímetros
    max_dim = max(obj.dimensions) if len(obj.dimensions) > 0 else 0.0
    if args.auto_scale_mm and 0.0 < max_dim < 2.5:
        print(f"      Detectada escala en metros (dimensión máxima: {max_dim:.3f} m). Escalando x1000 a milímetros...")
        obj.scale = (1000.0, 1000.0, 1000.0)
        bpy.ops.object.transform_apply(scale=True)

    # Escalado a altura objetivo en mm
    if args.target_height_mm and args.target_height_mm > 0:
        current_z = obj.dimensions.z
        if current_z > 1e-4:
            scale_factor = args.target_height_mm / current_z
            print(f"[2/6] Escalando altura de {current_z:.1f} mm a {args.target_height_mm:.1f} mm (factor: {scale_factor:.4f})...")
            obj.scale = (scale_factor, scale_factor, scale_factor)
            bpy.ops.object.transform_apply(scale=True)

    # Voxel Remesh para fusionar conchas interiores, cerrar agujeros y garantizar estanqueidad
    print(f"[3/6] Ejecutando Voxel Remesh (vóxel: {args.voxel_size} mm) para consolidación estanca (Watertight)...")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    obj.data.remesh_voxel_size = args.voxel_size
    bpy.ops.object.voxel_remesh()
    print(f"      Polígonos tras Voxel Remesh: {len(obj.data.polygons):,}")

    # Suavizado suave de ruido de escaneo/reconstrucción IA
    if args.smooth_repeat > 0 and args.smooth_factor > 0:
        print(f"[4/6] Aplicando filtro de relajación superficial (Factor: {args.smooth_factor}, Iteraciones: {args.smooth_repeat})...")
        mod_smooth = obj.modifiers.new(name="Surface_Smooth", type='SMOOTH')
        mod_smooth.factor = args.smooth_factor
        mod_smooth.iterations = args.smooth_repeat
        bpy.ops.object.modifier_apply(modifier="Surface_Smooth")

    # Decimación inteligente si excede el número objetivo de polígonos
    current_faces = len(obj.data.polygons)
    if current_faces > args.target_faces:
        ratio = float(args.target_faces) / float(current_faces)
        print(f"[5/6] Optimizando densidad de polígonos ({current_faces:,} -> ~{args.target_faces:,}, ratio: {ratio:.3f})...")
        mod_dec = obj.modifiers.new(name="Poly_Decimate", type='DECIMATE')
        mod_dec.decimate_type = 'COLLAPSE'
        mod_dec.ratio = ratio
        bpy.ops.object.modifier_apply(modifier="Poly_Decimate")
        print(f"      Polígonos tras decimación: {len(obj.data.polygons):,}")

    # Limpieza post-decimación para eliminar cualquier cara colapsada o degenerada
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.dissolve_degenerate(bm, dist=0.0001, edges=bm.edges)
    bm.to_mesh(obj.data)
    bm.free()

    # Alineación con la cama y centrado
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    min_x = min(c.x for c in bbox_corners)
    max_x = max(c.x for c in bbox_corners)
    min_y = min(c.y for c in bbox_corners)
    max_y = max(c.y for c in bbox_corners)
    min_z = min(c.z for c in bbox_corners)

    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0

    offset_x = -center_x if args.center_xy else 0.0
    offset_y = -center_y if args.center_xy else 0.0
    offset_z = -min_z if args.align_bed else 0.0

    print(f"[6/6] Ajustando coordenadas: Centrado XY ({offset_x:+.2f}, {offset_y:+.2f} mm), Base en Z=0 ({offset_z:+.2f} mm)")
    obj.location.x += offset_x
    obj.location.y += offset_y
    obj.location.z += offset_z
    bpy.ops.object.transform_apply(location=True)

    # Verificación final de estanqueidad
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    non_manifold = [e for e in bm.edges if not e.is_manifold]
    boundaries = [e for e in bm.edges if e.is_boundary]
    is_manifold = (len(non_manifold) == 0) and (len(boundaries) == 0)
    vol_cm3 = abs(bm.calc_volume()) / 1000.0 if is_manifold else 0.0
    bm.free()

    print(f"\n" + "=" * 60)
    print(f"✨ RESULTADO DE PROCESAMIENTO:")
    print(f"   - Estanqueidad: {'✅ 100% Watertight (2-Manifold)' if is_manifold else '⚠️ Requiere revisión'}")
    print(f"   - Dimensiones finales: {obj.dimensions.x:.1f} × {obj.dimensions.y:.1f} × {obj.dimensions.z:.1f} mm")
    print(f"   - Volumen sólido: {vol_cm3:.2f} cm³")
    print(f"   - Peso estimado PLA: {vol_cm3 * 1.24:.1f} g")
    print("=" * 60)

    if not is_manifold:
        print(f"[AVISO] La malla contiene {len(boundaries)} bordes abiertos y {len(non_manifold)} aristas no manifold.", file=sys.stderr)


def export_stl(obj, filepath):
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.stl_export(filepath=filepath, export_selected_objects=True)
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        raise RuntimeError(f"Fallo al escribir el archivo STL de salida: {filepath}")
    print(f"[OK] Archivo STL exportado con éxito ({os.path.getsize(filepath):,} bytes): {filepath}\n")


def run():
    args = parse_args()
    reset_scene()
    obj = import_and_join(args.input)
    process_mesh(obj, args)
    export_stl(obj, args.output)


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
