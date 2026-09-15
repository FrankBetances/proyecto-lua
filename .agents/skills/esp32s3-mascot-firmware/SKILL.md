---
name: esp32s3-mascot-firmware
description: >-
  Especialista en el desarrollo, arquitectura de firmware, control cinemático de servos, audio I2S,
  servidor BLE GATT y animación para la mascota robótica interactiva basada en ESP32-S3 para las
  plataformas Valeria+ v10.2 y VIA+. Utilizar este skill al desarrollar, depurar o configurar el
  código embebido (PlatformIO / ESP-IDF / Arduino Framework) del dispositivo físico de la mascota.
---

# ESP32-S3 Mascot Firmware Expert (Valeria+ & VIA+)

Este skill define la guía arquitectónica, patrones de código en C/C++, pinouts de hardware, protocolo de comunicación Bluetooth Low Energy (BLE GATT) y normas de seguridad pediátrica para programar la mascota robótica interactiva (**ESP32-S3**) asociada a **Valeria+ v10.2** y **VIA+**.

---

## 🐻 1. Especificación General del Sistema Embebido

- **Microcontrolador**: ESP32-S3 (Xtensa Dual-Core 32-bit LX7 @ 240 MHz, 8 MB PSRAM, 16 MB Flash, BLE 5.0).
- **Entorno Recomendado**: PlatformIO con framework Arduino o ESP-IDF v5.x.
- **Arquitectura de Software**: Multitarea en **FreeRTOS** fijando afinidad de núcleos (Core 0 para BLE y Audio, Core 1 para Animación, Touch y Cinemática).
- **Protocolo Inalámbrico**: Servidor BLE GATT nativo para sincronización bidireccional en tiempo real con las aplicaciones React Native / Expo (`react-native-ble-plx`).
- **Seguridad Pediátrica (MDR / ISO 14971)**:
  - Límite de volumen por software y hardware a <75 dBA a 10 cm.
  - Rampas de aceleración suave en servos para evitar enganches o atrapamientos.
  - Watchdog de tarea (TWDT) habilitado en ambos núcleos con recuperación a estado seguro neutro si se pierde la conexión BLE.

---

## 🔌 2. Diagrama de Conexiones y Mapeo de Pines (Hardware Pinout)

Para la asignación completa de pines GPIO y periferia I2S/I2C/PWM, consulta la referencia dedicada:
📄 [hardware_pinout_and_peripherals.md](./references/hardware_pinout_and_peripherals.md)

### Resumen de Buses Principales:
- **Audio DAC (I2S Output - MAX98357A)**: `BCLK=GPIO 7`, `LRCK=GPIO 6`, `DIN=GPIO 5`, `SD_MODE=GPIO 4`.
- **Micrófono (I2S Input - INMP441)**: `SCK=GPIO 15`, `WS=GPIO 16`, `SD=GPIO 17`.
- **Actuadores PWM (Servos SG90/MG90S)**: `Oreja Izq=GPIO 8`, `Oreja Der=GPIO 18`, `Cabeza Pan=GPIO 19`, `Cabeza Tilt=GPIO 20`.
- **Expresiones Oculares (WS2812B NeoPixels)**: `Ojos & Corazón=GPIO 38` (Línea de datos en cascada).
- **Pines Táctiles Capacitivos**: `Cabeza=TOUCH1 (GPIO 1)`, `Oreja Izq=TOUCH2 (GPIO 2)`, `Oreja Der=TOUCH3 (GPIO 3)`, `Pecho=TOUCH4 (GPIO 4)`.

---

## 📶 3. Protocolo BLE GATT para Valeria+ y VIA+

La comunicación entre el teléfono/tablet y la mascota utiliza un servicio BLE personalizado.
Para la especificación formal de características y payloads binarios/JSON, consulta:
📄 [ble_gatt_protocol_valeria_via.md](./references/ble_gatt_protocol_valeria_via.md)

### Servicios y Características Clave:
- **Mascot Service UUID**: `0000FA10-0000-1000-8000-00805F9B34FB`
- **Control & Animation (UUID `...FA11`) [WRITE]**: Recibe comandos de estado emocional (`HAPPY`, `LISTENING`, `CELEBRATE`, `TALKING`, `SLEEPING`).
- **Telemetry & Touch (UUID `...FA12`) [NOTIFY]**: Emite eventos de toques del niño, porcentaje de batería y acelerómetro.
- **Audio VAD Stream (UUID `...FA13`) [NOTIFY]**: Transmite eventos de presencia de voz o nivel acústico en dB.

---

## 🧵 4. Arquitectura Multitarea FreeRTOS

Para asegurar una fluidez de 60 FPS en la animación oculofacial y evitar tirones en el audio I2S o pérdida de paquetes BLE, el firmware distribuye el trabajo entre los dos núcleos de la ESP32-S3.
Revisa la arquitectura de hilos completa en:
📄 [freertos_multitask_architecture.md](./references/freertos_multitask_architecture.md)

- **Core 0 (Comunicaciones & Procesamiento DSP)**:
  - `Task_BLE_Server` (Prioridad 5): Atiende eventos de conexión/subscripción BLE.
  - `Task_Audio_I2S` (Prioridad 4): Stream I2S y cálculo de envolvente RMS / VAD.
- **Core 1 (Animaciones, Percepción Táctil & Cinemática)**:
  - `Task_Kinematics` (Prioridad 3): Interpolación de movimiento de servos con curvas S (S-curve).
  - `Task_NeoPixels` (Prioridad 2): Renderizado de pupilas, pestañeos y patrones de respiración LED.
  - `Task_Touch_Sensors` (Prioridad 3): Lectura de capacitancia con antirrebote (debounce) y eventos táctiles.

---

## 🛡️ 5. Normas de Seguridad y Cumplimiento Pediátrico

Dado que la mascota interactúa directamente con niñas y niños en entornos de terapia del lenguaje o audiometría, el firmware implementa reglas estrictas de seguridad:
📄 [mdr_safety_and_pediatric_compliance.md](./references/mdr_safety_and_pediatric_compliance.md)

1. **Límite de Torque en Servos**: Desactivación del pulso PWM si el movimiento se bloquea físicamente por más de 500 ms.
2. **Protección Auditiva**: Atenuación automática del volumen I2S según la distancia o tiempo continuo de emisión.
3. **Fail-Safe Disconnect**: Si la app pierde conexión BLE por más de 3 segundos, la mascota adopta la postura neutra de reposo y enciende respiración suave azul.

---

## 💻 6. Archivos de Ejemplo e Implementación

Puedes partir de los siguientes ejemplos ubicados en `examples/`:
- Configuración de proyecto: [`examples/platformio.ini`](./examples/platformio.ini)
- Punto de entrada FreeRTOS: [`examples/main.cpp`](./examples/main.cpp)
- Servidor BLE GATT: [`examples/mascot_ble_server.hpp`](./examples/mascot_ble_server.hpp)
- Cinemática de servos y LEDs: [`examples/mascot_kinematics.hpp`](./examples/mascot_kinematics.hpp)

---

## 🧪 7. Verificación del Proyecto

Para validar la sintaxis y estructura de cualquier desarrollo en este repositorio, ejecuta el script de comprobación:
```bash
python3 .agents/skills/esp32s3-mascot-firmware/scripts/validate_firmware_structure.py
```
