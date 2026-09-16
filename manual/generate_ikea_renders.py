#!/usr/bin/env python3
"""
Generate True IKEA-Style Line-Art Assembly Diagrams for Lúa Mascot
Using Blender 5.1 Cycles CPU + Freestyle Line-Art Engine with Real STLs.
Refined coordinate alignments, camera framings, and materials.
"""

import bpy
import math
import mathutils
import os
import sys

OUTPUT_DIR = os.path.abspath('manual/diagrams')
os.makedirs(OUTPUT_DIR, exist_ok=True)
STL_DIR = os.path.abspath('stl')

def reset_scene(bg_color=(1.0, 1.0, 1.0, 1.0)):
    bpy.ops.wm.read_factory_settings(use_empty=False)
    for o in list(bpy.data.objects):
        if o.name in ['Cube', 'Light']:
            bpy.data.objects.remove(o, do_unlink=True)

    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 24
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1100
    scene.render.film_transparent = True

    world = scene.world
    world.node_tree.nodes['Background'].inputs['Color'].default_value = bg_color
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0

    # Key light: Sun 1 (clean technical CAD illumination)
    l1 = bpy.data.lights.new('Sun1', type='SUN')
    l1.energy = 2.4
    o1 = bpy.data.objects.new('Sun1', l1)
    scene.collection.objects.link(o1)
    o1.rotation_euler = (math.radians(50), math.radians(25), math.radians(45))

    # Fill light: Sun 2
    l2 = bpy.data.lights.new('Sun2', type='SUN')
    l2.energy = 1.2
    o2 = bpy.data.objects.new('Sun2', l2)
    scene.collection.objects.link(o2)
    o2.rotation_euler = (math.radians(-30), math.radians(-40), math.radians(-30))

    # Freestyle line art setup
    scene.render.use_freestyle = True
    rl = scene.view_layers['ViewLayer']
    rl.use_freestyle = True
    rl.freestyle_settings.crease_angle = math.radians(135)
    lineset = rl.freestyle_settings.linesets['LineSet']
    lineset.select_silhouette = True
    lineset.select_border = True
    lineset.select_crease = True
    lineset.linestyle.thickness = 2.6
    lineset.linestyle.color = (0.05, 0.05, 0.08)

    return scene

def get_mat(name, color, roughness=0.55):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name=name)
    bsdf = mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = roughness
    return mat

def load_stl(filename, name, mat, location=(0,0,0), rotation=(0,0,0), scale=(1,1,1)):
    path = os.path.join(STL_DIR, filename)
    bpy.ops.wm.stl_import(filepath=path)
    obj = bpy.context.selected_objects[0]
    obj.name = name
    obj.location = location
    obj.rotation_euler = [math.radians(r) for r in rotation]
    obj.scale = scale
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj

def create_insert(name, mat, location=(0,0,0), rotation=(90,0,0)):
    # Brass knurled cylinder M2 (OD 3.2mm, length 4mm)
    bpy.ops.mesh.primitive_cylinder_add(radius=1.6, depth=4.0, vertices=24)
    ins = bpy.context.selected_objects[0]
    ins.name = name
    ins.location = location
    ins.rotation_euler = [math.radians(r) for r in rotation]
    ins.data.materials.append(mat)
    return ins

def create_screw(name, mat, location=(0,0,0), rotation=(90,0,0)):
    # M2 screw: head Ø3.8mm H 1.5mm, shaft Ø2.0mm H 8mm
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=8.0, vertices=16)
    shaft = bpy.context.selected_objects[0]
    bpy.ops.mesh.primitive_cylinder_add(radius=1.9, depth=1.5, vertices=20)
    head = bpy.context.selected_objects[0]
    head.location = (0, 0, 4.0)
    bpy.ops.object.select_all(action='DESELECT')
    shaft.select_set(True)
    head.select_set(True)
    bpy.context.view_layer.objects.active = shaft
    bpy.ops.object.join()
    screw = shaft
    screw.name = name
    screw.location = location
    screw.rotation_euler = [math.radians(r) for r in rotation]
    screw.data.materials.append(mat)
    return screw

def setup_camera(cam_loc, target_loc, ortho_scale=140):
    cam = bpy.data.objects['Camera']
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = ortho_scale
    cam.data.clip_end = 2000.0
    cam.location = cam_loc
    
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=target_loc)
    target = bpy.context.selected_objects[0]
    
    tt = cam.constraints.new(type='TRACK_TO')
    tt.target = target
    tt.track_axis = 'TRACK_NEGATIVE_Z'
    tt.up_axis = 'UP_Y'
    return cam

def render(scene, filename):
    out_path = os.path.join(OUTPUT_DIR, filename)
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {out_path}")

# ==========================================
# REFINED STEP RENDERS
# ==========================================

def render_step1():
    # Paso 1: Cuerpo espalda + 2 insertos de latón alineados con los agujeros
    scene = reset_scene()
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_brass = get_mat('Brass', (0.85, 0.68, 0.22, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    # Holes at X = +/- 20.50, Y = 20.57, Z = 38.04
    # Exploded hovering along +Y at Y = 46.0
    create_insert('Insert_L', mat_brass, location=(-20.5, 46.0, 38.0), rotation=(90, 0, 0))
    create_insert('Insert_R', mat_brass, location=(20.5, 46.0, 38.0), rotation=(90, 0, 0))

    setup_camera(cam_loc=(-110, 140, 85), target_loc=(0, 15, 38), ortho_scale=135)
    render(scene, 'step1_inserts.png')

def render_step2():
    # Paso 2: Cuerpo + collar deslizándose en el cuello
    scene = reset_scene()
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    # Collar hovering above neck (neck is Z=66..80), hovering at Z=105
    load_stl('collar.stl', 'Collar', mat_cyan, location=(0, 0, 105))

    setup_camera(cam_loc=(120, -120, 110), target_loc=(0, 0, 55), ortho_scale=155)
    render(scene, 'step2_collar.png')

def render_step3():
    # Paso 3: Cabeza frente vista interior + PCB + anillo de placa roscado
    scene = reset_scene()
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_pcb = get_mat('PCB', (0.15, 0.55, 0.35, 1.0))
    mat_ring = get_mat('RingWhite', (0.90, 0.92, 0.95, 1.0))

    load_stl('cabeza_frente.stl', 'Frente', mat_white, location=(0, 0, 0), rotation=(0, 0, 0))

    bpy.ops.mesh.primitive_cylinder_add(radius=18.5, depth=3.0, vertices=32)
    pcb = bpy.context.selected_objects[0]
    pcb.name = 'PCB'
    pcb.location = (0, 0, 34)
    pcb.data.materials.append(mat_pcb)

    load_stl('anillo_placa.stl', 'Anillo', mat_ring, location=(0, 0, 56))

    setup_camera(cam_loc=(70, -85, 120), target_loc=(0, 0, 25), ortho_scale=120)
    render(scene, 'step3_pcb_thread.png')

def render_step4():
    # Paso 4: Cierre del casco (cabeza_frente y cabeza_dorso enfrentados)
    scene = reset_scene()
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))

    load_stl('cabeza_frente.stl', 'Frente', mat_white, location=(0, 0, -22), rotation=(0, 0, 0))
    load_stl('cabeza_dorso.stl', 'Dorso', mat_white, location=(0, 0, 42), rotation=(0, 0, 0))

    setup_camera(cam_loc=(120, -100, 45), target_loc=(0, 0, 12), ortho_scale=160)
    render(scene, 'step4_head_halves.png')

def render_step5():
    # Paso 5: Casco montado + aro visor + orejas + botón de sien
    scene = reset_scene()
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))
    mat_dark = get_mat('Dark', (0.15, 0.16, 0.18, 1.0))

    load_stl('cabeza_frente.stl', 'Frente', mat_white, location=(0, -8, 0), rotation=(-90, 0, 0))
    load_stl('cabeza_dorso.stl', 'Dorso', mat_white, location=(0, 13, 0), rotation=(-90, 0, 0))
    load_stl('aro_visor.stl', 'Aro', mat_dark, location=(0, -38, 0), rotation=(-90, 0, 0))
    load_stl('oreja_izq.stl', 'Oreja_L', mat_cyan, location=(-20, 0, 56), rotation=(0, 0, 20))
    load_stl('oreja_der.stl', 'Oreja_R', mat_cyan, location=(20, 0, 56), rotation=(0, 0, -20))
    load_stl('boton.stl', 'Boton', mat_cyan, location=(52, 0, 0), rotation=(0, 90, 0))

    setup_camera(cam_loc=(115, -115, 60), target_loc=(0, 0, 10), ortho_scale=155)
    render(scene, 'step5_head_accessories.png')

def render_step6():
    # Paso 6: Emblema y logo en el pecho de cuerpo.stl
    scene = reset_scene()
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    # Chest socket center: X = 0.0, Z = 38.25. Emblema rotated +90 deg around X
    load_stl('emblema.stl', 'Emblema', mat_cyan, location=(0, -44, 38.25), rotation=(90, 0, 0))
    load_stl('logo.stl', 'Logo', mat_white, location=(0, -56, 38.25), rotation=(90, 0, 0))

    setup_camera(cam_loc=(80, -100, 60), target_loc=(0, -20, 38.25), ortho_scale=105)
    render(scene, 'step6_chest_emblem.png')

def render_step7():
    # Paso 7: Espalda - Cartucho batería + Mochila + 2 tornillos M2
    scene = reset_scene()
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))
    mat_steel = get_mat('Steel', (0.65, 0.68, 0.72, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    # Cartucho sits upright, sliding back into cavity
    load_stl('cartucho.stl', 'Cartucho', mat_white, location=(0, 38, 27))
    # Mochila rotated -90 around X: holes at X = +/- 20.5, Z = 38.0
    load_stl('mochila.stl', 'Mochila', mat_cyan, location=(0, 56, 38), rotation=(-90, 0, 0))
    create_screw('Screw_L', mat_steel, location=(-20.5, 76, 38), rotation=(90, 0, 0))
    create_screw('Screw_R', mat_steel, location=(20.5, 76, 38), rotation=(90, 0, 0))

    setup_camera(cam_loc=(-110, 140, 80), target_loc=(0, 30, 38), ortho_scale=145)
    render(scene, 'step7_battery_backpack.png')

def render_step8():
    # Paso 8: Extremidades bicolor (brazos y piernas)
    scene = reset_scene()
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))

    # Limbs exploded outward from sockets
    # Left arm (-X), Right arm (+X)
    load_stl('brazo_izq.stl', 'Brazo_L', mat_white, location=(-48, -5, 36), rotation=(180, 0, 0))
    load_stl('brazo_der.stl', 'Brazo_R', mat_white, location=(48, -5, 36), rotation=(180, 0, 0))

    # Left leg (-X), Right leg (+X)
    load_stl('pierna_izq.stl', 'Pierna_L', mat_white, location=(-42, -18, 5), rotation=(180, 0, 0))
    load_stl('pierna_der.stl', 'Pierna_R', mat_white, location=(42, -18, 5), rotation=(180, 0, 0))

    setup_camera(cam_loc=(110, -120, 70), target_loc=(0, 0, 35), ortho_scale=155)
    render(scene, 'step8_limbs.png')

def render_step9():
    # Paso 9: Túnel de carga USB-C bajo la barbilla y pulsadores
    scene = reset_scene()
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))
    mat_dark = get_mat('Dark', (0.15, 0.16, 0.18, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    load_stl('collar.stl', 'Collar', mat_cyan, location=(0,0,66))
    load_stl('cabeza_frente.stl', 'Frente', mat_white, location=(0, -8, 85), rotation=(-90, 0, 0))
    load_stl('pulsadores.stl', 'Pulsadores', mat_dark, location=(0, -28, 76), rotation=(0, 0, 0))

    setup_camera(cam_loc=(50, -85, 55), target_loc=(0, -12, 72), ortho_scale=85)
    render(scene, 'step9_chin_port.png')

def render_step10():
    # Paso 10: Acople final de cabeza sobre el cuerpo (sin pegamento)
    scene = reset_scene()
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))
    mat_dark = get_mat('Dark', (0.15, 0.16, 0.18, 1.0))

    # Torso assembled
    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    load_stl('collar.stl', 'Collar', mat_cyan, location=(0,0,66))
    load_stl('emblema.stl', 'Emblema', mat_cyan, location=(0, -28.5, 38.25), rotation=(90, 0, 0))
    load_stl('logo.stl', 'Logo', mat_white, location=(0, -30.0, 38.25), rotation=(90, 0, 0))
    load_stl('brazo_izq.stl', 'Brazo_L', mat_white, location=(-25, -5, 42))
    load_stl('brazo_der.stl', 'Brazo_R', mat_white, location=(25, -5, 42))
    load_stl('pierna_izq.stl', 'Pierna_L', mat_white, location=(-20, -15, 12))
    load_stl('pierna_der.stl', 'Pierna_R', mat_white, location=(20, -15, 12))
    load_stl('mochila.stl', 'Mochila', mat_cyan, location=(0, 24, 38), rotation=(-90, 0, 0))

    # Assembled head hovering above neck at Z = 135
    load_stl('cabeza_frente.stl', 'Frente', mat_white, location=(0, -8, 135), rotation=(-90, 0, 0))
    load_stl('cabeza_dorso.stl', 'Dorso', mat_white, location=(0, 13, 135), rotation=(-90, 0, 0))
    load_stl('aro_visor.stl', 'Aro', mat_dark, location=(0, -29, 135), rotation=(-90, 0, 0))
    load_stl('oreja_izq.stl', 'Oreja_L', mat_cyan, location=(-20, 2, 175), rotation=(0, 0, 20))
    load_stl('oreja_der.stl', 'Oreja_R', mat_cyan, location=(20, 2, 175), rotation=(0, 0, -20))
    load_stl('boton.stl', 'Boton', mat_cyan, location=(39, 2, 135), rotation=(0, 90, 0))

    setup_camera(cam_loc=(120, -120, 100), target_loc=(0, 0, 75), ortho_scale=190)
    render(scene, 'step10_final_assembly.png')

def render_mascot_full():
    # Muñeco montado completo (Portada / Cover)
    scene = reset_scene()
    mat_white = get_mat('White', (0.95, 0.96, 0.98, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))
    mat_dark = get_mat('Dark', (0.15, 0.16, 0.18, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    load_stl('collar.stl', 'Collar', mat_cyan, location=(0,0,66))
    load_stl('emblema.stl', 'Emblema', mat_cyan, location=(0, -28.5, 38.25), rotation=(90, 0, 0))
    load_stl('logo.stl', 'Logo', mat_white, location=(0, -30.0, 38.25), rotation=(90, 0, 0))
    load_stl('brazo_izq.stl', 'Brazo_L', mat_white, location=(-25, -5, 42))
    load_stl('brazo_der.stl', 'Brazo_R', mat_white, location=(25, -5, 42))
    load_stl('pierna_izq.stl', 'Pierna_L', mat_white, location=(-20, -15, 12))
    load_stl('pierna_der.stl', 'Pierna_R', mat_white, location=(20, -15, 12))
    load_stl('mochila.stl', 'Mochila', mat_cyan, location=(0, 24, 38), rotation=(-90, 0, 0))

    # Head on neck (Z = 85)
    load_stl('cabeza_frente.stl', 'Frente', mat_white, location=(0, -8, 85), rotation=(-90, 0, 0))
    load_stl('cabeza_dorso.stl', 'Dorso', mat_white, location=(0, 13, 85), rotation=(-90, 0, 0))
    load_stl('aro_visor.stl', 'Aro', mat_dark, location=(0, -29, 85), rotation=(-90, 0, 0))
    load_stl('oreja_izq.stl', 'Oreja_L', mat_cyan, location=(-20, 2, 125), rotation=(0, 0, 20))
    load_stl('oreja_der.stl', 'Oreja_R', mat_cyan, location=(20, 2, 125), rotation=(0, 0, -20))
    load_stl('boton.stl', 'Boton', mat_cyan, location=(39, 2, 85), rotation=(0, 90, 0))

    setup_camera(cam_loc=(120, -120, 85), target_loc=(0, 0, 55), ortho_scale=165)
    render(scene, 'mascot_full_cover.png')

def render_parts_overview():
    # Overview de todas las piezas sobre fondo limpio (Catálogo)
    scene = reset_scene()
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))
    mat_dark = get_mat('Dark', (0.15, 0.16, 0.18, 1.0))

    load_stl('cuerpo.stl', 'A_Cuerpo', mat_white, location=(-60, 20, 0))
    load_stl('cabeza_frente.stl', 'B_Frente', mat_white, location=(15, -40, 0))
    load_stl('cabeza_dorso.stl', 'C_Dorso', mat_white, location=(-60, -50, 0))
    load_stl('collar.stl', 'J_Collar', mat_cyan, location=(-85, 70, 0))
    load_stl('mochila.stl', 'K_Mochila', mat_cyan, location=(65, -10, 0))
    load_stl('anillo_placa.stl', 'P_Anillo', mat_white, location=(15, 15, 0))
    load_stl('cartucho.stl', 'Q_Cartucho', mat_white, location=(-10, 85, 0))
    load_stl('aro_visor.stl', 'O_Aro', mat_dark, location=(80, -60, 0))
    load_stl('emblema.stl', 'M_Emblema', mat_cyan, location=(40, 85, 0))
    load_stl('logo.stl', 'N_Logo', mat_white, location=(65, 85, 0))
    load_stl('boton.stl', 'L_Boton', mat_cyan, location=(20, 85, 0))
    load_stl('oreja_izq.stl', 'H_OrejaL', mat_cyan, location=(-45, 55, 0))
    load_stl('oreja_der.stl', 'I_OrejaR', mat_cyan, location=(-10, 55, 0))
    load_stl('brazo_izq.stl', 'D_BrazoL', mat_white, location=(85, 55, 0))
    load_stl('brazo_der.stl', 'E_BrazoR', mat_white, location=(-40, 95, 0))
    load_stl('pierna_izq.stl', 'F_PiernaL', mat_white, location=(25, 55, 0))
    load_stl('pierna_der.stl', 'G_PiernaR', mat_white, location=(55, 55, 0))

    setup_camera(cam_loc=(0, -180, 160), target_loc=(0, 20, 15), ortho_scale=240)
    render(scene, 'parts_overview_plate.png')

if __name__ == '__main__':
    print("Executing refined rendering pipeline...")
    render_parts_overview()
    render_mascot_full()
    render_step1()
    render_step2()
    render_step3()
    render_step4()
    render_step5()
    render_step6()
    render_step7()
    render_step8()
    render_step9()
    render_step10()
    print("Refined rendering complete!")
