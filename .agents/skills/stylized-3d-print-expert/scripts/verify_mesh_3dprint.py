#!/usr/bin/env python3
"""
verify_mesh_3dprint.py
----------------------
Script de verificación técnica e inspección de mallas para impresión 3D (FDM/SLA).
Ejecución headless en Blender 5.x / 4.x:
  /Applications/Blender.app/Contents/MacOS/Blender -b --python verify_mesh_3dprint.py -- --input modelo.stl [opciones]

Verifica:
1. Estanqueidad (Watertight / 2-Manifold). Cero aristas abiertas, cero aristas no manifold.
2. Dimensiones físicas (X, Y, Z en mm) contra volumen de impresión de la máquina (ej. Ender-3 S1 Pro: 220x220x270 mm).
3. Volumen cerrado macizo (cm³) y cálculo exacto de masa en filamento PLA/PETG (g).
4. Caras degeneradas (área cero o vértices colineales).
5. Análisis de voladizos (Overhangs) a >45° y >60° diferenciando superficie de contacto con la cama vs voladizos al aire.
"""

import sys
import os
import math
import json
import argparse

try:
    import bpy
    import bmesh
    from mathutils import Vector
except ImportError:
    print("[ERROR] Este script debe ejecutarse dentro del entorno de Blender:")
    print("  /Applications/Blender.app/Contents/MacOS/Blender -b --python verify_mesh_3dprint.py -- --input <archivo>")
    sys.exit(1)


def parse_args():
    argv = sys.argv
    if "--" in argv:
        args_to_parse = argv[argv.index("--") + 1:]
    else:
        args_to_parse = []

    parser = argparse.ArgumentParser(description="Auditoría y verificación de mallas STL/OBJ/GLB para impresión 3D")
    parser.add_argument("--input", "-i", required=True, help="Ruta al archivo 3D (.stl, .obj, .glb, .gltf)")
    parser.add_argument("--output-json", "-o", default=None, help="Ruta para guardar el reporte en formato JSON")
    parser.add_argument("--bed-x", type=float, default=220.0, help="Ancho máximo de cama en mm (default: 220.0 para Ender-3 S1 Pro)")
    parser.add_argument("--bed-y", type=float, default=220.0, help="Profundidad máxima de cama en mm (default: 220.0 para Ender-3 S1 Pro)")
    parser.add_argument("--bed-z", type=float, default=270.0, help="Altura máxima en mm (default: 270.0 para Ender-3 S1 Pro)")
    parser.add_argument("--density", type=float, default=1.24, help="Densidad del material en g/cm³ (default: 1.24 para PLA)")
    return parser.parse_args(args_to_parse)


def reset_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for block in bpy.data.meshes:
        bpy.data.meshes.remove(block)


def import_model(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".stl":
        bpy.ops.wm.stl_import(filepath=filepath)
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=filepath)
    elif ext in [".glb", ".gltf"]:
        bpy.ops.import_scene.gltf(filepath=filepath)
    else:
        raise ValueError(f"Extensión no soportada: {ext}. Utilice .stl, .obj, .glb o .gltf")

    selected = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    if not selected:
        selected = [obj for obj in bpy.data.objects if obj.type == 'MESH']
        if not selected:
            raise RuntimeError(f"No se encontró ningún objeto de tipo MESH tras la importación de {filepath}.")

    # Si hay múltiples mallas importadas, unirlas para análisis conjunto
    if len(selected) > 1:
        bpy.context.view_layer.objects.active = selected[0]
        for o in selected:
            o.select_set(True)
        bpy.ops.object.join()
        obj = selected[0]
    else:
        obj = selected[0]
        bpy.context.view_layer.objects.active = obj

    obj.select_set(True)
    # Aplicar transformaciones para mediciones en espacio de mundo
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def analyze_mesh(obj, bed_x, bed_y, bed_z, density):
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # 1. Conteo básico
    n_verts = len(bm.verts)
    n_edges = len(bm.edges)
    n_faces = len(bm.faces)

    # 2. Dimensiones de la caja envolvente (Bounding Box en mm)
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    min_x = min(c.x for c in bbox_corners)
    max_x = max(c.x for c in bbox_corners)
    min_y = min(c.y for c in bbox_corners)
    max_y = max(c.y for c in bbox_corners)
    min_z = min(c.z for c in bbox_corners)
    max_z = max(c.z for c in bbox_corners)

    dim_x = max_x - min_x
    dim_y = max_y - min_y
    dim_z = max_z - min_z

    fits_bed = (dim_x <= bed_x) and (dim_y <= bed_y) and (dim_z <= bed_z)

    # 3. Manifold / Estanqueidad
    non_manifold_edges = [e for e in bm.edges if not e.is_manifold]
    boundary_edges = [e for e in bm.edges if e.is_boundary]
    zero_area_faces = [f for f in bm.faces if f.calc_area() < 1e-7]

    is_watertight = (len(non_manifold_edges) == 0) and (len(boundary_edges) == 0)

    # 4. Volumen macizo y masa estimada
    volume_mm3 = 0.0
    try:
        volume_mm3 = abs(bm.calc_volume())
    except Exception:
        pass

    volume_cm3 = volume_mm3 / 1000.0
    mass_g = volume_cm3 * density

    # 5. Área y Análisis de Voladizos (Overhangs)
    total_area_mm2 = sum(f.calc_area() for f in bm.faces)
    bed_contact_area_mm2 = 0.0
    overhang_45_area_mm2 = 0.0
    overhang_60_area_mm2 = 0.0

    # Umbral Z para contacto con la cama (primeros 0.3 mm sobre min_z)
    bed_threshold_z = min_z + 0.3

    for face in bm.faces:
        area = face.calc_area()
        normal = face.normal
        # Si la cara apunta hacia abajo (normal.z < -0.01)
        if normal.z < -0.01:
            face_center_z = face.calc_center_median().z
            # ¿Es cara de apoyo en la cama?
            if face_center_z <= bed_threshold_z and normal.z <= -0.95:
                bed_contact_area_mm2 += area
            else:
                overhang_deg = math.degrees(math.asin(min(1.0, abs(normal.z))))
                if overhang_deg >= 45.0:
                    overhang_45_area_mm2 += area
                if overhang_deg >= 60.0:
                    overhang_60_area_mm2 += area

    bm.free()

    # Veredicto de imprimibilidad
    verdict = "PASS"
    issues = []

    if not is_watertight:
        verdict = "FAIL"
        issues.append(f"Malla NO estanca: {len(boundary_edges)} bordes abiertos y {len(non_manifold_edges)} aristas no manifold.")
    if not fits_bed:
        verdict = "FAIL"
        issues.append(f"Excede la cama ({dim_x:.1f}x{dim_y:.1f}x{dim_z:.1f} mm vs límite {bed_x}x{bed_y}x{bed_z} mm).")
    if len(zero_area_faces) > 0:
        if verdict == "PASS":
            verdict = "WARNING"
        issues.append(f"Contiene {len(zero_area_faces)} caras degeneradas de área nula.")
    if bed_contact_area_mm2 < 10.0 and dim_z > 20.0:
        if verdict == "PASS":
            verdict = "WARNING"
        issues.append(f"Área de contacto con cama muy reducida ({bed_contact_area_mm2:.1f} mm²). Riesgo de despegue (requiere balsa o borde/brim).")

    report = {
        "verdict": verdict,
        "fits_bed": fits_bed,
        "is_watertight": is_watertight,
        "poly_counts": {
            "vertices": n_verts,
            "edges": n_edges,
            "faces": n_faces
        },
        "dimensions_mm": {
            "width_x": round(dim_x, 2),
            "depth_y": round(dim_y, 2),
            "height_z": round(dim_z, 2)
        },
        "bed_limits_mm": {
            "max_x": bed_x,
            "max_y": bed_y,
            "max_z": bed_z
        },
        "solid_volume_cm3": round(volume_cm3, 3),
        "estimated_mass_g": round(mass_g, 2),
        "surface_area_mm2": round(total_area_mm2, 2),
        "bed_contact_area_mm2": round(bed_contact_area_mm2, 2),
        "overhangs": {
            "area_gt_45_deg_mm2": round(overhang_45_area_mm2, 2),
            "pct_gt_45_deg": round((overhang_45_area_mm2 / max(1e-5, total_area_mm2)) * 100.0, 2),
            "area_gt_60_deg_mm2": round(overhang_60_area_mm2, 2),
            "pct_gt_60_deg": round((overhang_60_area_mm2 / max(1e-5, total_area_mm2)) * 100.0, 2)
        },
        "non_manifold_edges": len(non_manifold_edges),
        "boundary_edges": len(boundary_edges),
        "zero_area_faces": len(zero_area_faces),
        "issues": issues
    }
    return report


def print_human_report(filepath, report):
    print("\n" + "=" * 70)
    print(f"📊 REPORTE DE AUDITORÍA 3D PRINT: {os.path.basename(filepath)}")
    print("=" * 70)
    
    v = report["verdict"]
    badge = "✅ APROBADO (LISTO PARA IMPRESIÓN)" if v == "PASS" else ("⚠️ ADVERTENCIA (REVISAR AJUSTES)" if v == "WARNING" else "❌ NO APTO (REQUIERE REPARACIÓN)")
    print(f"ESTADO GENERAL: {badge}")
    print("-" * 70)

    d = report["dimensions_mm"]
    b = report["bed_limits_mm"]
    print(f"📐 Dimensiones (X × Y × Z): {d['width_x']} × {d['depth_y']} × {d['height_z']} mm")
    print(f"🛏️ Compatibilidad con cama ({b['max_x']}×{b['max_y']}×{b['max_z']} mm): {'SÍ (Cabe perfectamente)' if report['fits_bed'] else 'NO (Excede volumen)'}")
    
    print(f"📦 Volumen macizo: {report['solid_volume_cm3']} cm³")
    print(f"⚖️ Masa estimada (PLA 1.24 g/cm³): {report['estimated_mass_g']} gramos")
    
    watertight_str = "SÍ (Sólido estanco / 2-Manifold puro)" if report['is_watertight'] else f"NO ({report['boundary_edges']} huecos abiertos, {report['non_manifold_edges']} no-manifold)"
    print(f"🛡️ Geometría Estanca (Watertight): {watertight_str}")
    print(f"🔹 Densidad de polígonos: {report['poly_counts']['faces']:,} caras, {report['poly_counts']['vertices']:,} vértices")

    print(f"📍 Contacto con la cama: {report['bed_contact_area_mm2']} mm²")
    ov = report["overhangs"]
    print(f"🧗 Voladizos >45° (Soporte suave): {ov['area_gt_45_deg_mm2']} mm² ({ov['pct_gt_45_deg']}% de la piel)")
    print(f"🚨 Voladizos >60° (Soporte crítico): {ov['area_gt_60_deg_mm2']} mm² ({ov['pct_gt_60_deg']}% de la piel)")

    if report["issues"]:
        print("\n⚠️ DIAGNÓSTICO Y OBSERVACIONES:")
        for idx, issue in enumerate(report["issues"], 1):
            print(f"   [{idx}] {issue}")
    else:
        print("\n🎉 La geometría no presenta aristas no manifold ni defectos críticos. Puede importarse en Cura/PrusaSlicer directamente.")

    print("=" * 70 + "\n")


def run():
    args = parse_args()
    reset_scene()
    obj = import_model(args.input)
    report = analyze_mesh(obj, args.bed_x, args.bed_y, args.bed_z, args.density)
    print_human_report(args.input, report)

    if args.output_json:
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"[OK] Reporte JSON guardado en: {args.output_json}")

    if report["verdict"] == "FAIL":
        sys.exit(2)
    sys.exit(0)


def main():
    try:
        run()
    except SystemExit:
        raise
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
