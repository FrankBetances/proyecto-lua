#!/usr/bin/env python3
"""
Generate Official IKEA-Style Line-Art Assembly Diagrams for Lúa Mascot (V15)
Using Blender 5.1 Cycles CPU + Freestyle Line-Art Engine with Real V15 STLs.
Supports 21 parts: Φ87 head, media-vuelta bayoneta, press-fit Lego limbs,
press-fit backpack pins (no M2 screws, no brass inserts).
"""

import bpy
import math
import os
import subprocess
import sys
from math import radians
from mathutils import Euler, Vector

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
DIAGRAMS_PNG_DIR = os.path.join(PROJECT_DIR, 'manual/diagrams')
DIAGRAMS_JPG_DIR = os.path.join(PROJECT_DIR, 'manual/diagrams_jpg')
STL_DIR = os.path.join(PROJECT_DIR, 'stl')

os.makedirs(DIAGRAMS_PNG_DIR, exist_ok=True)
os.makedirs(DIAGRAMS_JPG_DIR, exist_ok=True)

# Exact V15 CAD dimensions from lua-muneco.scad
Y_CARA = -29.2415
Y_CORTE = -10.3415
Z_CAB = 114.0
RXn = Euler((radians(-90), 0, 0), 'YXZ').to_matrix().to_4x4()

def clean_scene():
    """Clean all objects, meshes, materials, and lights without triggering userpref reload."""
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.materials):
        bpy.data.materials.remove(m, do_unlink=True)
    for me in list(bpy.data.meshes):
        bpy.data.meshes.remove(me, do_unlink=True)

def setup_scene(res_x=1400, res_y=1100):
    clean_scene()
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 24
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.render.film_transparent = False

    world = scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    bg.inputs['Strength'].default_value = 1.0

    # Key light: Technical illumination
    l1 = bpy.data.lights.new('Sun1', type='SUN')
    l1.energy = 2.4
    o1 = bpy.data.objects.new('Sun1', l1)
    scene.collection.objects.link(o1)
    o1.rotation_euler = (radians(50), radians(25), radians(45))

    # Fill light: Soft fill
    l2 = bpy.data.lights.new('Sun2', type='SUN')
    l2.energy = 1.2
    o2 = bpy.data.objects.new('Sun2', l2)
    scene.collection.objects.link(o2)
    o2.rotation_euler = (radians(-30), radians(-40), radians(-30))

    # Freestyle line art setup
    scene.render.use_freestyle = True
    rl = scene.view_layers['ViewLayer']
    rl.use_freestyle = True
    rl.freestyle_settings.crease_angle = radians(135)
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
    mat.use_nodes = True
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
    obj.rotation_euler = [radians(r) for r in rotation]
    obj.scale = scale
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj

def head_place(path_filename, name, y0, mat, dy=0, z_offset=0):
    path = os.path.join(STL_DIR, path_filename)
    bpy.ops.wm.stl_import(filepath=path)
    o = bpy.context.selected_objects[0]
    o.name = name
    o.rotation_mode = 'YXZ'
    o.rotation_euler = RXn.to_euler('YXZ')
    o.location = Vector((0, y0 + dy, Z_CAB + z_offset))
    o.data.materials.clear()
    o.data.materials.append(mat)
    return o

def ear_place(path_filename, name, sx, mat, out=0, z_offset=0):
    path = os.path.join(STL_DIR, path_filename)
    bpy.ops.wm.stl_import(filepath=path)
    o = bpy.context.selected_objects[0]
    o.name = name
    R1 = Euler((radians(-90), 0, 0), 'YXZ').to_matrix()
    R2 = Euler((radians(14), radians(sx * 30), 0), 'YXZ').to_matrix()
    R = (R2 @ R1.inverted()).to_4x4()
    n = R2 @ Vector((0.485 * sx, -0.242, 0.840))
    L = (R2 @ R1.inverted() @ Vector((0, 0, -6.0))
         + R2 @ Vector((0, 0, 43.5)) + Vector((0, 0, Z_CAB + z_offset)) + n * out)
    o.rotation_mode = 'YXZ'
    o.rotation_euler = R.to_euler('YXZ')
    o.location = L
    o.data.materials.clear()
    o.data.materials.append(mat)
    return o

def create_pin(name, mat, location=(0,0,0), rotation=(90,0,0)):
    """Cilindro perno press-fit Ø4mm x 6.6mm"""
    bpy.ops.mesh.primitive_cylinder_add(radius=2.0, depth=6.6, vertices=24)
    pin = bpy.context.selected_objects[0]
    pin.name = name
    pin.location = location
    pin.rotation_euler = [radians(r) for r in rotation]
    pin.data.materials.clear()
    pin.data.materials.append(mat)
    return pin

def setup_camera(cam_loc, target_loc, ortho_scale=140):
    cam_data = bpy.data.cameras.new('Camera')
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = ortho_scale
    cam_data.clip_end = 2000.0
    cam = bpy.data.objects.new('Camera', cam_data)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = cam_loc

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=target_loc)
    target = bpy.context.selected_objects[0]

    tt = cam.constraints.new(type='TRACK_TO')
    tt.target = target
    tt.track_axis = 'TRACK_NEGATIVE_Z'
    tt.up_axis = 'UP_Y'
    bpy.context.scene.camera = cam
    return cam

def render_and_convert(scene, png_name, jpg_name):
    png_path = os.path.join(DIAGRAMS_PNG_DIR, png_name)
    jpg_path = os.path.join(DIAGRAMS_JPG_DIR, jpg_name)
    scene.render.filepath = png_path
    bpy.ops.render.render(write_still=True)
    print(f"Rendered PNG: {png_path}")

    # Convert to JPEG 95% via sips
    cmd = ['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '95', png_path, '--out', jpg_path]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    print(f"Converted JPG: {jpg_path} ({os.path.getsize(jpg_path)} bytes)")

# ==========================================
# 12 V15 DIAGRAM RENDERS
# ==========================================

def render_mascot_full():
    """Portada Oficial IKEA: Muñeco montado completo V15 (Cabeza Φ87, press-fit, sin tornillos)"""
    scene = setup_scene(1400, 1100)
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
    load_stl('mochila.stl', 'Mochila', mat_cyan, location=(0, 23.5, 38), rotation=(-90, 0, 0))

    head_place('cabeza_frente.stl', 'Frente', Y_CARA, mat_white)
    head_place('cabeza_dorso.stl', 'Dorso', Y_CORTE, mat_white)
    load_stl('aro_visor.stl', 'Aro', mat_dark, location=(0, -38.5, Z_CAB), rotation=(-90, 0, 0))
    ear_place('oreja_izq.stl', 'Oreja_L', -1, mat_cyan)
    ear_place('oreja_der.stl', 'Oreja_R', +1, mat_cyan)
    load_stl('boton.stl', 'Boton', mat_cyan, location=(43, 2, Z_CAB), rotation=(0, 90, 0))

    setup_camera(cam_loc=(120, -120, 85), target_loc=(0, 0, 55), ortho_scale=165)
    render_and_convert(scene, 'mascot_full_cover.png', 'mascot_full_cover.jpg')

def render_parts_overview():
    """Catálogo Oficial de 19 piezas V15 en la cama 220x220 mm con pernos_mochila.stl"""
    scene = setup_scene(1400, 1100)
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))
    mat_dark = get_mat('Dark', (0.15, 0.16, 0.18, 1.0))
    mat_bed = get_mat('Bed', (0.90, 0.91, 0.93, 1.0))

    # Print bed 220x220 mm
    bpy.ops.mesh.primitive_plane_add(size=220, location=(0, 0, -0.5))
    bed = bpy.context.selected_objects[0]
    bed.data.materials.append(mat_bed)

    # Disposición exacta del plato() de lua-muneco.scad
    load_stl('cabeza_dorso.stl', 'Dorso', mat_white, location=(-61.0, -61.0, 0))
    load_stl('cabeza_frente.stl', 'Frente', mat_white, location=(25.4, -62.3, 0))
    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(-66.9, 14.4, 0))
    load_stl('anillo_placa.stl', 'Anillo', mat_white, location=(3.7, 13.9, 0))
    load_stl('aro_visor.stl', 'Aro', mat_dark, location=(58.5, 3.8, 0))
    load_stl('collar.stl', 'Collar', mat_cyan, location=(85.6, -85.1, 0))
    load_stl('mochila.stl', 'Mochila', mat_cyan, location=(-80.5, 65.9, 0))
    load_stl('oreja_izq.stl', 'Oreja_L', mat_cyan, location=(-40.8, 51.9, 0))
    load_stl('oreja_der.stl', 'Oreja_R', mat_cyan, location=(-10.0, 51.9, 0))
    load_stl('pierna_izq.stl', 'Pierna_L', mat_white, location=(51.4, 59.8, 0))
    load_stl('pierna_der.stl', 'Pierna_R', mat_white, location=(17.4, 59.8, 0))
    load_stl('cartucho.stl', 'Cartucho', mat_white, location=(-27.4, 89.3, 0))
    load_stl('emblema.stl', 'Emblema', mat_cyan, location=(92.3, -7.2, 0))
    load_stl('brazo_izq.stl', 'Brazo_L', mat_white, location=(94.4, 57.9, 0))
    load_stl('brazo_der.stl', 'Brazo_R', mat_white, location=(73.7, 57.0, 0))
    load_stl('boton.stl', 'Boton', mat_cyan, location=(-97.0, 92.2, 0))
    load_stl('logo.stl', 'Logo', mat_white, location=(-81.3, 92.1, 0))
    load_stl('pulsadores.stl', 'Pulsadores', mat_dark, location=(-58.9, 91.8, 0))
    load_stl('pernos_mochila.stl', 'Pernos', mat_cyan, location=(0.2, 86.7, 0))

    setup_camera(cam_loc=(0, -180, 160), target_loc=(0, 15, 10), ortho_scale=240)
    render_and_convert(scene, 'parts_overview_plate.png', 'parts_overview_plate.jpg')

def render_step1():
    """Paso 1: Cuerpo espalda + 2 pernos press-fit Ø4x6.6 mm (sin tornillos M2)"""
    scene = setup_scene(1400, 1400)
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    create_pin('Perno_L', mat_cyan, location=(-20.5, 48.0, 38.0), rotation=(90, 0, 0))
    create_pin('Perno_R', mat_cyan, location=(20.5, 48.0, 38.0), rotation=(90, 0, 0))

    setup_camera(cam_loc=(-105, 135, 80), target_loc=(0, 20, 38), ortho_scale=135)
    render_and_convert(scene, 'step1_pernos.png', 'step1_pernos.jpg')

def render_step2():
    """Paso 2: Cuerpo + collar turquesa deslizándose por la espiga del cuello"""
    scene = setup_scene(1400, 1100)
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    load_stl('collar.stl', 'Collar', mat_cyan, location=(0, 0, 105))

    setup_camera(cam_loc=(120, -120, 110), target_loc=(0, 0, 55), ortho_scale=155)
    render_and_convert(scene, 'step2_collar.png', 'step2_collar.jpg')

def render_step3():
    """Paso 3: Cabeza frente vista interior + PCB con carcasa (cajetín 42x43.5x15) + anillo M55 roscado"""
    scene = setup_scene(1400, 1100)
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_pcb = get_mat('PCB', (0.12, 0.50, 0.30, 1.0))
    mat_ring = get_mat('RingWhite', (0.90, 0.92, 0.95, 1.0))

    load_stl('cabeza_frente.stl', 'Frente', mat_white, location=(0, 0, 0), rotation=(0, 0, 0))

    # Carcasa de placa 42 x 43.5 x 15 mm
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 36))
    pcb = bpy.context.selected_objects[0]
    pcb.name = 'PCB_Carcasa'
    pcb.scale = (42.0, 43.5, 8.0)
    pcb.data.materials.append(mat_pcb)

    load_stl('anillo_placa.stl', 'Anillo', mat_ring, location=(0, 0, 58))

    setup_camera(cam_loc=(70, -85, 120), target_loc=(0, 0, 25), ortho_scale=120)
    render_and_convert(scene, 'step3_pcb_thread.png', 'step3_pcb_thread.jpg')

def render_step4():
    """Paso 4: Bayoneta de media vuelta (cabeza_frente y cabeza_dorso enfrentados en el eje)"""
    scene = setup_scene(1400, 1400)
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))

    head_place('cabeza_frente.stl', 'Frente', Y_CARA, mat_white)
    head_place('cabeza_dorso.stl', 'Dorso', Y_CORTE, mat_white, dy=38)

    setup_camera(cam_loc=(115, 100, 155), target_loc=(0, 2, 106), ortho_scale=155)
    render_and_convert(scene, 'step4_bayoneta.png', 'step4_bayoneta.jpg')

def render_step5():
    """Paso 5: Casco cerrado + orejas con bayoneta 1/4 vuelta + aro visor + botón"""
    scene = setup_scene(1400, 1400)
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))
    mat_dark = get_mat('Dark', (0.15, 0.16, 0.18, 1.0))

    head_place('cabeza_frente.stl', 'Frente', Y_CARA, mat_white)
    head_place('cabeza_dorso.stl', 'Dorso', Y_CORTE, mat_white)
    load_stl('aro_visor.stl', 'Aro', mat_dark, location=(0, -48, Z_CAB), rotation=(-90, 0, 0))
    ear_place('oreja_izq.stl', 'Oreja_L', -1, mat_cyan, out=15)
    ear_place('oreja_der.stl', 'Oreja_R', +1, mat_cyan, out=15)
    load_stl('boton.stl', 'Boton', mat_cyan, location=(55, 2, Z_CAB), rotation=(0, 90, 0))

    setup_camera(cam_loc=(115, -115, 135), target_loc=(0, 0, 114), ortho_scale=160)
    render_and_convert(scene, 'step5_oreja.png', 'step5_oreja.jpg')

def render_step6():
    """Paso 6: Emblema turquesa y logo blanco a presión (press-fit Lego) en el pecho"""
    scene = setup_scene(1400, 1100)
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    load_stl('emblema.stl', 'Emblema', mat_cyan, location=(0, -44, 38.25), rotation=(90, 0, 0))
    load_stl('logo.stl', 'Logo', mat_white, location=(0, -56, 38.25), rotation=(90, 0, 0))

    setup_camera(cam_loc=(80, -100, 60), target_loc=(0, -20, 38.25), ortho_scale=105)
    render_and_convert(scene, 'step6_chest_emblem.png', 'step6_chest_emblem.jpg')

def render_step7():
    """Paso 7: Espalda - Cartucho batería + Mochila press-fit sobre los 2 pernos (sin tornillos)"""
    scene = setup_scene(1400, 1400)
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    create_pin('Perno_L', mat_cyan, location=(-20.5, 23.5, 38.0), rotation=(90, 0, 0))
    create_pin('Perno_R', mat_cyan, location=(20.5, 23.5, 38.0), rotation=(90, 0, 0))
    load_stl('cartucho.stl', 'Cartucho', mat_white, location=(0, 38, 27))
    load_stl('mochila.stl', 'Mochila', mat_cyan, location=(0, 56, 38), rotation=(-90, 0, 0))

    setup_camera(cam_loc=(-105, 135, 75), target_loc=(0, 28, 38), ortho_scale=140)
    render_and_convert(scene, 'step7_mochila.png', 'step7_mochila.jpg')

def render_step8():
    """Paso 8: Extremidades a presión (brazos y piernas en cajetas press-fit)"""
    scene = setup_scene(1400, 1100)
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    load_stl('brazo_izq.stl', 'Brazo_L', mat_white, location=(-48, -5, 36), rotation=(180, 0, 0))
    load_stl('brazo_der.stl', 'Brazo_R', mat_white, location=(48, -5, 36), rotation=(180, 0, 0))
    load_stl('pierna_izq.stl', 'Pierna_L', mat_white, location=(-42, -18, 5), rotation=(180, 0, 0))
    load_stl('pierna_der.stl', 'Pierna_R', mat_white, location=(42, -18, 5), rotation=(180, 0, 0))

    setup_camera(cam_loc=(110, -120, 70), target_loc=(0, 0, 35), ortho_scale=155)
    render_and_convert(scene, 'step8_limbs.png', 'step8_limbs.jpg')

def render_step9():
    """Paso 9: Túnel de carga USB-C bajo la barbilla y pulsadores en cabeza Φ87"""
    scene = setup_scene(1400, 1100)
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))
    mat_dark = get_mat('Dark', (0.15, 0.16, 0.18, 1.0))

    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    load_stl('collar.stl', 'Collar', mat_cyan, location=(0,0,66))
    head_place('cabeza_frente.stl', 'Frente', Y_CARA, mat_white, z_offset=-25)
    load_stl('pulsadores.stl', 'Pulsadores', mat_dark, location=(0, -28, 76), rotation=(0, 0, 0))

    setup_camera(cam_loc=(50, -85, 55), target_loc=(0, -12, 72), ortho_scale=85)
    render_and_convert(scene, 'step9_chin_port.png', 'step9_chin_port.jpg')

def render_step10():
    """Paso 10: Acople final de cabeza Φ87 sobre el cuerpo (sin pegamento, giro libre)"""
    scene = setup_scene(1400, 1100)
    mat_white = get_mat('White', (0.94, 0.95, 0.97, 1.0))
    mat_cyan = get_mat('Cyan', (0.28, 0.72, 0.72, 1.0))
    mat_dark = get_mat('Dark', (0.15, 0.16, 0.18, 1.0))

    # Torso montado
    load_stl('cuerpo.stl', 'Cuerpo', mat_white, location=(0,0,0))
    load_stl('collar.stl', 'Collar', mat_cyan, location=(0,0,66))
    load_stl('emblema.stl', 'Emblema', mat_cyan, location=(0, -28.5, 38.25), rotation=(90, 0, 0))
    load_stl('logo.stl', 'Logo', mat_white, location=(0, -30.0, 38.25), rotation=(90, 0, 0))
    load_stl('brazo_izq.stl', 'Brazo_L', mat_white, location=(-25, -5, 42))
    load_stl('brazo_der.stl', 'Brazo_R', mat_white, location=(25, -5, 42))
    load_stl('pierna_izq.stl', 'Pierna_L', mat_white, location=(-20, -15, 12))
    load_stl('pierna_der.stl', 'Pierna_R', mat_white, location=(20, -15, 12))
    load_stl('mochila.stl', 'Mochila', mat_cyan, location=(0, 23.5, 38), rotation=(-90, 0, 0))

    # Cabeza completa suspendida en Z=145 mm
    head_place('cabeza_frente.stl', 'Frente', Y_CARA, mat_white, z_offset=30)
    head_place('cabeza_dorso.stl', 'Dorso', Y_CORTE, mat_white, z_offset=30)
    load_stl('aro_visor.stl', 'Aro', mat_dark, location=(0, -38.5, Z_CAB + 30), rotation=(-90, 0, 0))
    ear_place('oreja_izq.stl', 'Oreja_L', -1, mat_cyan, z_offset=30)
    ear_place('oreja_der.stl', 'Oreja_R', +1, mat_cyan, z_offset=30)
    load_stl('boton.stl', 'Boton', mat_cyan, location=(43, 2, Z_CAB + 30), rotation=(0, 90, 0))

    setup_camera(cam_loc=(120, -120, 100), target_loc=(0, 0, 75), ortho_scale=190)
    render_and_convert(scene, 'step10_final_assembly.png', 'step10_final_assembly.jpg')

if __name__ == '__main__':
    print("==================================================")
    print("Rendering 12 V15 Line-Art Assembly Diagrams...")
    print("==================================================")
    render_mascot_full()
    render_parts_overview()
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
    print("==================================================")
    print("ALL 12 V15 DIAGRAMS SUCCESSFULLY RENDERED & CONVERTED!")
    print("==================================================")
