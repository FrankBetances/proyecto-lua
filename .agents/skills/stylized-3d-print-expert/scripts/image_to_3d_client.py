#!/usr/bin/env python3
"""
image_to_3d_client.py
---------------------
Cliente CLI automatizado para la generación de modelos 3D a partir de imágenes 2D/fotos.
Soporta:
1. Motores Neuronales en la Nube (Tripo3D v2 API y Meshy 4 API).
2. Generador Orgánico Local Offline (sin APIs ni costos, utilizando Blender 5.1).
3. Modo Mock / Simulación que genera geometría real para pruebas de integración desatendidas.

Flujo de trabajo:
1. Valida la imagen de entrada (.png, .jpg, .webp).
2. Procesa la reconstrucción volumétrica (vía API o generador local).
3. Verifica empíricamente la integridad física y tamaño del archivo generado.
4. Opcional: Ejecuta 'clean_and_watertight.py' para entregar un STL listo para imprimir en la Ender-3 S1 Pro.

Uso:
  # Modo local offline (cero costo, sin claves de API):
  python3 image_to_3d_client.py --image foto.png --service local --auto-stl modelo.stl

  # Modo neuronal en la nube:
  export TRIPO_API_KEY="tu_token"
  python3 image_to_3d_client.py --image foto.png --service tripo --output modelo.glb --auto-stl modelo.stl

  # Modo mock para pruebas automatizadas:
  python3 image_to_3d_client.py --image foto.png --mock --output /tmp/mock.glb --auto-stl /tmp/mock.stl
"""

import os
import sys
import time
import json
import base64
import urllib.request
import urllib.error
import argparse
import subprocess

TRIPO_API_BASE = "https://api.tripo3d.ai/v2/openapi"
MESHY_API_BASE = "https://api.meshy.ai/v2/image-to-3d"
BLENDER_BIN = "/Applications/Blender.app/Contents/MacOS/Blender"


def parse_args():
    parser = argparse.ArgumentParser(description="Conversión de imagen 2D a modelo 3D para impresión")
    parser.add_argument("--image", "-i", required=True, help="Ruta a la imagen 2D (.png, .jpg, .webp)")
    parser.add_argument("--service", choices=["tripo", "meshy", "local"], default="tripo", help="Motor de reconstrucción (tripo, meshy o local)")
    parser.add_argument("--output", "-o", default=None, help="Ruta de descarga del modelo crudo (.glb o .stl)")
    parser.add_argument("--auto-stl", default=None, help="Si se especifica, genera el STL estanco y verificado con Blender")
    parser.add_argument("--target-height-mm", type=float, default=120.0, help="Altura deseada para el modelo en mm")
    parser.add_argument("--mock", action="store_true", help="Modo simulación con generación de geometría real para pruebas sin gastar créditos")
    return parser.parse_args()


def read_image_base64(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Imagen no encontrada: {filepath}")
    with open(filepath, "rb") as f:
        data = f.read()
    ext = os.path.splitext(filepath)[1].lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:image/{ext};base64,{b64}"


def generate_mock_glb(output_glb, target_height_mm=120.0):
    """
    Genera un archivo GLB de prueba válido con geometría estilizada chibi real usando Blender headless.
    Garantiza que el modo mock no sea un cascarón vacío sino un pipeline 100% verificable.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_glb)), exist_ok=True)
    py_code = f"""
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for b in bpy.data.meshes: bpy.data.meshes.remove(b)

# Cabeza esférica achatada (Chibi)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=30.0, location=(0, 0, 75.0))
head = bpy.context.active_object
head.scale = (1.0, 0.9, 0.85)
bpy.ops.object.transform_apply(scale=True)

# Torso compacto
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=24.0, location=(0, 0, 35.0))
body = bpy.context.active_object
body.scale = (0.9, 0.8, 1.1)
bpy.ops.object.transform_apply(scale=True)

# Orejas
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=16, radius=10.0, location=(-28.0, 0, 95.0))
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=16, radius=10.0, location=(28.0, 0, 95.0))

# Unir todo
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
obj = bpy.context.active_object
obj.name = "MockStylizedMascot"

# Exportar a GLB
bpy.ops.export_scene.gltf(filepath=r'{output_glb}', export_format='GLB')
"""
    cmd = [BLENDER_BIN, "-b", "--python-expr", py_code]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not os.path.exists(output_glb) or os.path.getsize(output_glb) == 0:
        raise RuntimeError(f"Fallo al generar geometría mock en Blender:\n{res.stderr}")
    print(f"[MOCK] Geometría 3D de prueba generada con éxito ({os.path.getsize(output_glb):,} bytes) en: {output_glb}")
    return output_glb


def run_tripo_pipeline(image_path, output_glb, mock=False):
    if mock:
        print("[MOCK] Ejecutando simulación de pipeline Tripo3D con geometría real...")
        return generate_mock_glb(output_glb)

    api_key = os.environ.get("TRIPO_API_KEY")
    if not api_key:
        print("[ERROR] Falta la variable de entorno TRIPO_API_KEY.", file=sys.stderr)
        print("  Obtén tu API key en https://platform.tripo3d.ai/", file=sys.stderr)
        print("  O utiliza el motor local sin costo: --service local", file=sys.stderr)
        sys.exit(1)

    data_uri = read_image_base64(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "type": "image_to_model",
        "file": {
            "type": "image",
            "data": data_uri
        },
        "model_seed": 42
    }
    
    print("🚀 [1/3] Enviando imagen a Tripo3D para reconstrucción volumétrica...")
    req = urllib.request.Request(f"{TRIPO_API_BASE}/task", data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            if res_data.get("code") != 0:
                raise RuntimeError(f"Error devuelto por Tripo: {res_data}")
            task_id = res_data["data"]["task_id"]
            print(f"      Tarea registrada en la nube. ID: {task_id}")
    except urllib.error.HTTPError as e:
        print(f"[HTTP ERROR] {e.code}: {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)

    # Polling con límite de tiempo
    print("⏳ [2/3] Generando geometría estilizada 3D...")
    status_url = f"{TRIPO_API_BASE}/task/{task_id}"
    start_time = time.time()
    max_wait_seconds = 600  # 10 minutos máximo

    while True:
        if time.time() - start_time > max_wait_seconds:
            raise TimeoutError(f"Tiempo de espera excedido ({max_wait_seconds}s) para tarea Tripo {task_id}")

        req = urllib.request.Request(status_url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                task_info = json.loads(resp.read().decode("utf-8"))["data"]
                status = task_info.get("status")
                progress = task_info.get("progress", 0)
                print(f"      Estado: {status} ({progress}%)")
                if status == "success":
                    model_url = task_info["output"]["model"]
                    break
                elif status in ["failed", "cancelled"]:
                    raise RuntimeError(f"La tarea falló en el servidor: {task_info}")
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"      [Reintento] Error de red transitorio: {e}")

        time.sleep(3)

    # Descarga
    print(f"⬇️ [3/3] Descargando modelo GLB en: {output_glb}...")
    os.makedirs(os.path.dirname(os.path.abspath(output_glb)), exist_ok=True)
    urllib.request.urlretrieve(model_url, output_glb)

    if not os.path.exists(output_glb) or os.path.getsize(output_glb) == 0:
        raise RuntimeError(f"Fallo al descargar el archivo GLB desde {model_url}")

    print(f"[OK] Modelo 3D descargado exitosamente ({os.path.getsize(output_glb):,} bytes).")
    return output_glb


def run_meshy_pipeline(image_path, output_glb, mock=False):
    if mock:
        print("[MOCK] Ejecutando simulación de pipeline Meshy con geometría real...")
        return generate_mock_glb(output_glb)

    api_key = os.environ.get("MESHY_API_KEY")
    if not api_key:
        print("[ERROR] Falta la variable de entorno MESHY_API_KEY.", file=sys.stderr)
        print("  Obtén tu API key en https://meshy.ai/", file=sys.stderr)
        print("  O utiliza el motor local sin costo: --service local", file=sys.stderr)
        sys.exit(1)

    data_uri = read_image_base64(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "image_url": data_uri,
        "enable_pbr": False,
        "surface_mode": "hard",
        "ai_model": "meshy-4"
    }

    print("🚀 [1/3] Enviando imagen a Meshy 4 Image-to-3D...")
    req = urllib.request.Request(MESHY_API_BASE, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            task_data = json.loads(resp.read().decode("utf-8"))
            task_id = task_data.get("result")
            print(f"      Tarea registrada. ID: {task_id}")
    except urllib.error.HTTPError as e:
        print(f"[HTTP ERROR] {e.code}: {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)

    status_url = f"{MESHY_API_BASE}/{task_id}"
    start_time = time.time()
    max_wait = 600

    while True:
        if time.time() - start_time > max_wait:
            raise TimeoutError(f"Tiempo de espera excedido para tarea Meshy {task_id}")

        req = urllib.request.Request(status_url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                status = data.get("status")
                progress = data.get("progress", 0)
                print(f"      Estado: {status} ({progress}%)")
                if status == "SUCCEEDED":
                    model_url = data.get("model_urls", {}).get("glb")
                    if not model_url:
                        raise ValueError(f"Respuesta de Meshy no contiene URL de GLB: {data}")
                    break
                elif status in ["FAILED", "EXPIRED"]:
                    raise RuntimeError(f"Error en Meshy: {data}")
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"      [Reintento] Error de red: {e}")

        time.sleep(3)

    print(f"⬇️ Descargando modelo: {output_glb}...")
    os.makedirs(os.path.dirname(os.path.abspath(output_glb)), exist_ok=True)
    urllib.request.urlretrieve(model_url, output_glb)

    if not os.path.exists(output_glb) or os.path.getsize(output_glb) == 0:
        raise RuntimeError(f"Fallo al descargar modelo desde Meshy: {model_url}")

    return output_glb


def run_local_pipeline(image_path, output_stl, target_height_mm):
    """
    Ejecuta el generador local offline 'local_image_to_3d.py' en Blender.
    """
    script_path = os.path.join(os.path.dirname(__file__), "local_image_to_3d.py")
    if not os.path.exists(BLENDER_BIN):
        raise FileNotFoundError(f"Blender no encontrado en {BLENDER_BIN}")

    print("\n🛠️ Ejecutando generador local offline con Blender...")
    cmd = [
        BLENDER_BIN, "-b", "--python", script_path, "--",
        "--image", image_path,
        "--output", output_stl,
        "--target-height-mm", str(target_height_mm),
        "--orientation", "standing"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not os.path.exists(output_stl) or os.path.getsize(output_stl) == 0:
        raise RuntimeError(f"Fallo en generador local de Blender:\n{res.stderr}\n{res.stdout}")
    print(f"[EXITO] STL generado localmente con éxito: {output_stl} ({os.path.getsize(output_stl):,} bytes)")
    return output_stl


def auto_convert_to_stl(glb_path, stl_path, target_height_mm):
    script_path = os.path.join(os.path.dirname(__file__), "clean_and_watertight.py")
    if not os.path.exists(BLENDER_BIN):
        print(f"[AVISO] Blender no encontrado en {BLENDER_BIN}. Omite conversión automática a STL.")
        return

    print("\n🛠️ Ejecutando acondicionamiento estanco y escalado con Blender...")
    cmd = [
        BLENDER_BIN, "-b", "--python", script_path, "--",
        "--input", glb_path,
        "--output", stl_path,
        "--target-height-mm", str(target_height_mm),
        "--align-bed", "--center-xy"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if res.returncode != 0 or not os.path.exists(stl_path) or os.path.getsize(stl_path) == 0:
        raise RuntimeError(f"Error al procesar en Blender. El STL no se generó:\n{res.stderr}\n{res.stdout}")

    print(f"[EXITO] STL final 100% estanco generado en: {stl_path} ({os.path.getsize(stl_path):,} bytes)")


def main():
    args = parse_args()

    if not os.path.exists(args.image):
        print(f"[ERROR] Imagen no encontrada: {args.image}", file=sys.stderr)
        sys.exit(1)

    # Modo 1: Motor local directo
    if args.service == "local":
        stl_out = args.auto_stl or args.output or f"{os.path.splitext(args.image)[0]}_local.stl"
        run_local_pipeline(args.image, stl_out, args.target_height_mm)
        return

    # Modo 2 y 3: Cloud APIs o Mock
    if not args.output:
        base = os.path.splitext(args.image)[0]
        args.output = f"{base}_model.glb"

    if args.service == "tripo":
        glb = run_tripo_pipeline(args.image, args.output, mock=args.mock)
    else:
        glb = run_meshy_pipeline(args.image, args.output, mock=args.mock)

    if args.auto_stl:
        auto_convert_to_stl(glb, args.auto_stl, args.target_height_mm)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}", file=sys.stderr)
        sys.exit(1)
