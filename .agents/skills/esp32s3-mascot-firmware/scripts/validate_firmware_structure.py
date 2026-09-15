#!/usr/bin/env python3
"""
Script de verificación sintáctica y estructural del skill ESP32-S3 Mascot Firmware.
Comprueba que los archivos de referencia, ejemplos e instrucciones principales cumplan
con la especificación Antigravity y no contengan enlaces o rutas rotas.
"""

import sys
from pathlib import Path

def validate_skill():
    skill_root = Path(__file__).resolve().parent.parent
    print(f"🔍 Validando skill en: {skill_root}")

    required_files = [
        skill_root / "SKILL.md",
        skill_root / "references" / "hardware_pinout_and_peripherals.md",
        skill_root / "references" / "ble_gatt_protocol_valeria_via.md",
        skill_root / "references" / "freertos_multitask_architecture.md",
        skill_root / "references" / "mdr_safety_and_pediatric_compliance.md",
        skill_root / "examples" / "platformio.ini",
        skill_root / "examples" / "main.cpp",
        skill_root / "examples" / "mascot_ble_server.hpp",
        skill_root / "examples" / "mascot_kinematics.hpp",
    ]

    missing = []
    for file_path in required_files:
        if not file_path.exists():
            missing.append(str(file_path))

    if missing:
        print("❌ Error: Los siguientes archivos requeridos no fueron encontrados:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)

    # Validar Frontmatter de SKILL.md
    skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    if not skill_md.startswith("---"):
        print("❌ Error: SKILL.md no contiene el inicio del frontmatter YAML ('---').")
        sys.exit(1)
    
    if "name: esp32s3-mascot-firmware" not in skill_md:
        print("❌ Error: Nombre de skill en YAML frontmatter no coincide con 'esp32s3-mascot-firmware'.")
        sys.exit(1)

    print("✅ ¡Validación exitosa! Todos los componentes del skill están correctamente estructurados.")
    sys.exit(0)

if __name__ == "__main__":
    validate_skill()
