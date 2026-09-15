#!/usr/bin/env python3
"""
test_pipeline.py
----------------
Suite de pruebas automatizadas y verificación técnica rigurosa para el skill
'stylized-3d-print-expert'.

Ejecución:
  python3 test_pipeline.py
"""

import os
import sys
import tempfile
import subprocess
import unittest

BLENDER_BIN = "/Applications/Blender.app/Contents/MacOS/Blender"
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
VERIFY_SCRIPT = os.path.join(SCRIPTS_DIR, "verify_mesh_3dprint.py")
CLEAN_SCRIPT = os.path.join(SCRIPTS_DIR, "clean_and_watertight.py")
SPLIT_SCRIPT = os.path.join(SCRIPTS_DIR, "generate_keyed_split.py")
LOCAL_SCRIPT = os.path.join(SCRIPTS_DIR, "local_image_to_3d.py")
CLIENT_SCRIPT = os.path.join(SCRIPTS_DIR, "image_to_3d_client.py")

# Búsqueda dinámica de la raíz del espacio de trabajo (donde reside la carpeta stl)
cur = SCRIPTS_DIR
while cur != "/" and not os.path.exists(os.path.join(cur, "stl")):
    cur = os.path.dirname(cur)
WORKSPACE_DIR = cur
SAMPLE_STL = os.path.join(WORKSPACE_DIR, "stl", "boton.stl")
SAMPLE_IMG = os.path.join(WORKSPACE_DIR, "lua-firmware", "docs", "cad", "muneco-frente.png")


class TestStylized3DPipeline(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="test_3d_")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_verify_mesh_valid(self):
        """Verifica que verify_mesh_3dprint apruebe un modelo STL válido con código 0."""
        cmd = [BLENDER_BIN, "-b", "--python", VERIFY_SCRIPT, "--", "--input", SAMPLE_STL]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Debe retornar 0. Salida:\n{res.stdout}\n{res.stderr}")
        self.assertIn("ESTADO GENERAL: ✅ APROBADO", res.stdout)
        self.assertIn("Sólido estanco / 2-Manifold puro", res.stdout)

    def test_02_verify_mesh_not_found_exits_with_error(self):
        """Verifica que un archivo inexistente provoque código de salida 1 (no salida 0 silenciosa)."""
        cmd = [BLENDER_BIN, "-b", "--python", VERIFY_SCRIPT, "--", "--input", "no_existe_9999.stl"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0, "Blender no debe salir con código 0 ante error")
        self.assertIn("[FATAL ERROR]", res.stderr)

    def test_03_clean_and_watertight_valid(self):
        """Verifica que clean_and_watertight procese, remalle y exporte un STL estanco."""
        out_stl = os.path.join(self.temp_dir, "clean_boton.stl")
        cmd = [
            BLENDER_BIN, "-b", "--python", CLEAN_SCRIPT, "--",
            "--input", SAMPLE_STL,
            "--output", out_stl,
            "--voxel-size", "0.35"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Fallo en clean_and_watertight:\n{res.stderr}")
        self.assertTrue(os.path.exists(out_stl))
        self.assertGreater(os.path.getsize(out_stl), 1000)

    def test_04_clean_and_watertight_error_exit_code(self):
        """Verifica que un archivo inexistente en clean_and_watertight provoque código de salida 1."""
        out_stl = os.path.join(self.temp_dir, "out.stl")
        cmd = [
            BLENDER_BIN, "-b", "--python", CLEAN_SCRIPT, "--",
            "--input", "no_existe_archivo.stl",
            "--output", out_stl
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("[FATAL ERROR]", res.stderr)

    def test_05_generate_keyed_split_inverted_pin(self):
        """Verifica que --invert-pin genere la espiga macho en TOP extendiéndose hacia abajo (-Z)."""
        out_top = os.path.join(self.temp_dir, "inv_top.stl")
        out_bot = os.path.join(self.temp_dir, "inv_bot.stl")
        cmd = [
            BLENDER_BIN, "-b", "--python", SPLIT_SCRIPT, "--",
            "--input", SAMPLE_STL,
            "--cut-z", "1.7",
            "--output-top", out_top,
            "--output-bottom", out_bot,
            "--pin-diameter", "3.0",
            "--pin-height", "2.0",
            "--invert-pin"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Fallo en split invert:\n{res.stderr}")
        self.assertTrue(os.path.exists(out_top) and os.path.exists(out_bot))

        # Auditar con verify_mesh
        cmd_audit = [BLENDER_BIN, "-b", "--python", VERIFY_SCRIPT, "--", "--input", out_top]
        res_audit = subprocess.run(cmd_audit, capture_output=True, text=True)
        self.assertEqual(res_audit.returncode, 0)
        self.assertIn("Sólido estanco / 2-Manifold puro", res_audit.stdout)

    def test_06_generate_keyed_split_off_center_autocenter(self):
        """Verifica que piezas descentradas en XY coloquen los pines en el corte y no en (0,0)."""
        # Crear un cubo en (60, 60, 20)
        cube_stl = os.path.join(self.temp_dir, "offset_cube.stl")
        py_make = f"""
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for b in bpy.data.meshes: bpy.data.meshes.remove(b)
bpy.ops.mesh.primitive_cube_add(size=20, location=(60, 60, 20))
bpy.ops.wm.stl_export(filepath=r'{cube_stl}')
"""
        subprocess.run([BLENDER_BIN, "-b", "--python-expr", py_make], check=True, capture_output=True)

        out_top = os.path.join(self.temp_dir, "offset_top.stl")
        out_bot = os.path.join(self.temp_dir, "offset_bot.stl")
        cmd = [
            BLENDER_BIN, "-b", "--python", SPLIT_SCRIPT, "--",
            "--input", cube_stl,
            "--cut-z", "20.0",
            "--output-top", out_top,
            "--output-bottom", out_bot,
            "--pin-diameter", "4.0",
            "--pin-height", "4.0"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("(60.00, 60.00)", res.stdout)

    def test_07_local_image_to_3d_standing(self):
        """Verifica que el generador local offline cree un STL estanco con Z = altura vertical."""
        out_stl = os.path.join(self.temp_dir, "mascot_local.stl")
        cmd = [
            BLENDER_BIN, "-b", "--python", LOCAL_SCRIPT, "--",
            "--image", SAMPLE_IMG,
            "--output", out_stl,
            "--target-height-mm", "90.0",
            "--depth-mm", "16.0",
            "--orientation", "standing"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Fallo en local_image_to_3d:\n{res.stderr}")
        self.assertTrue(os.path.exists(out_stl))
        self.assertGreater(os.path.getsize(out_stl), 10000)

        # Auditar con verify_mesh
        cmd_audit = [BLENDER_BIN, "-b", "--python", VERIFY_SCRIPT, "--", "--input", out_stl]
        res_audit = subprocess.run(cmd_audit, capture_output=True, text=True)
        self.assertEqual(res_audit.returncode, 0)
        self.assertIn("Sólido estanco / 2-Manifold puro", res_audit.stdout)

    def test_08_image_to_3d_client_mock_end_to_end(self):
        """Verifica que el cliente en modo mock genere geometría real y convierta a STL estanco."""
        mock_glb = os.path.join(self.temp_dir, "mock.glb")
        mock_stl = os.path.join(self.temp_dir, "mock.stl")
        cmd = [
            sys.executable, CLIENT_SCRIPT,
            "--image", SAMPLE_IMG,
            "--mock",
            "--output", mock_glb,
            "--auto-stl", mock_stl,
            "--target-height-mm", "100.0"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Fallo en mock client:\n{res.stderr}")
        self.assertTrue(os.path.exists(mock_glb))
        self.assertTrue(os.path.exists(mock_stl))
        self.assertGreater(os.path.getsize(mock_stl), 50000)

        # Auditar
        cmd_audit = [BLENDER_BIN, "-b", "--python", VERIFY_SCRIPT, "--", "--input", mock_stl]
        res_audit = subprocess.run(cmd_audit, capture_output=True, text=True)
        self.assertEqual(res_audit.returncode, 0)
        self.assertIn("Sólido estanco / 2-Manifold puro", res_audit.stdout)

    def test_09_generate_keyed_split_dual_pins_and_bed_placement(self):
        """Verifica que --dual-pins y --place-on-bed alineen ambas piezas en Z=0."""
        out_top = os.path.join(self.temp_dir, "dual_top.stl")
        out_bot = os.path.join(self.temp_dir, "dual_bot.stl")
        cmd = [
            BLENDER_BIN, "-b", "--python", SPLIT_SCRIPT, "--",
            "--input", SAMPLE_STL,
            "--cut-z", "1.7",
            "--output-top", out_top,
            "--output-bottom", out_bot,
            "--pin-diameter", "2.5",
            "--pin-height", "2.0",
            "--dual-pins",
            "--pin-spacing", "6.0",
            "--pin-axis", "y",
            "--place-on-bed"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertTrue(os.path.exists(out_top) and os.path.exists(out_bot))

        # Auditar ambas piezas
        for p in [out_top, out_bot]:
            res_audit = subprocess.run([BLENDER_BIN, "-b", "--python", VERIFY_SCRIPT, "--", "--input", p], capture_output=True, text=True)
            self.assertEqual(res_audit.returncode, 0)
            self.assertIn("Sólido estanco / 2-Manifold puro", res_audit.stdout)

    def test_10_local_image_to_3d_flat_mode(self):
        """Verifica que local_image_to_3d en modo 'flat' cree una figura acostada en cama sin soportes."""
        out_stl = os.path.join(self.temp_dir, "flat_mascot.stl")
        cmd = [
            BLENDER_BIN, "-b", "--python", LOCAL_SCRIPT, "--",
            "--image", SAMPLE_IMG,
            "--output", out_stl,
            "--target-height-mm", "80.0",
            "--depth-mm", "14.0",
            "--orientation", "flat"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertTrue(os.path.exists(out_stl))
        res_audit = subprocess.run([BLENDER_BIN, "-b", "--python", VERIFY_SCRIPT, "--", "--input", out_stl], capture_output=True, text=True)
        self.assertEqual(res_audit.returncode, 0)
        self.assertIn("ESTADO GENERAL: ✅ APROBADO", res_audit.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
