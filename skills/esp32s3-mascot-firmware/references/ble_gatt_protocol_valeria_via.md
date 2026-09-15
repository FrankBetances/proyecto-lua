# Protocolo de Comunicación BLE GATT: Valeria+ / VIA+ Mascot

Este documento especifica la arquitectura del servidor **Bluetooth Low Energy (BLE GATT)** que implementa el firmware de la mascota para dialogar con las aplicaciones móviles de **Valeria+ v10.2** y **VIA+** a través de la librería `react-native-ble-plx`.

---

## 📡 1. Identificación del Dispositivo y Anuncio (Advertising)

- **Device Name**: `VALERIA-MASCOT-S3` (o `VIAPLUS-MASCOT-S3`)
- **Advertising Data**:
  - Service UUID: `0000FA10-0000-1000-8000-00805F9B34FB`
  - Tx Power Level.
  - Manufacturer Data: `0x02E5` (ID Espressif) + 2 bytes versión de firmware (`0x0100` = v1.0).

---

## 🔐 2. Estructura de Servicios y Características GATT

### Primary Service: `Mascot Therapy Service`
UUID Base: `0000FA10-0000-1000-8000-00805F9B34FB`

| Característica | UUID Suffix | Propiedades | Payload Format | Descripción |
|---|---|---|---|---|
| **Command / Expression** | `...FA11` | `WRITE`, `WRITE_WITHOUT_RESPONSE` | JSON o ByteArray | Recibe comandos de animación visual, auditiva y posicional |
| **Telemetry & Touch** | `...FA12` | `READ`, `NOTIFY` | ByteArray (6 bytes) | Notifica toques detectados, nivel de batería y aceleración |
| **Acoustic Level / VAD**| `...FA13` | `NOTIFY` | ByteArray (4 bytes) | Notifica nivel de ruido LAeq y flag VAD de detección de habla |
| **System Info & Config** | `...FA14` | `READ`, `WRITE` | JSON | Lee/Escribe límites de volumen, calibración táctil y firmware info |

---

## 📦 3. Formato de Payloads y Protocolo de Comandos

### A. Comando de Expresión y Estado Animado (`...FA11` - WRITE)

#### Ejemplo Payload JSON:
```json
{
  "cmd": "SET_STATE",
  "state": "HAPPY",
  "duration_ms": 3000,
  "audio_id": "CHEER_01"
}
```

#### Lista de Estados Animados Disponibles:
- `IDLE`: Parpadeo suave cada 4 segundos, respiración de corazón azul.
- `LISTENING`: Orejas orientadas adelante (Pan: 90°, Tilt: 105°), ojos amarillos atentos.
- `TALKING`: Movimiento sutil de orejas en sincronía con envolvente de audio, ojos verde brillante.
- `HAPPY`: Orejas batiendo alternadamente, ojos verdes festivos, destellos en NeoPixels.
- `CONFUSED`: Cabeza inclinada (Tilt: 75°), una oreja abajo y otra arriba, ojos naranjas.
- `CELEBRATE`: Rotación pan de cabeza, batido rápido de orejas, fuegos artificiales de colores en NeoPixels.
- `SLEEPING`: Cabeza abajo, ojos apagados, respiración lenta violeta en corazón.

---

### B. Notificación de Telemetría y Eventos Táctiles (`...FA12` - NOTIFY)

Notificación binaria de 6 bytes transmitida al ocurrir un evento o periódicamente cada 5 segundos:

```text
[ Byte 0 ] : Event Code (0x01=Touch, 0x02=Battery, 0x03=IMU_Tilt)
[ Byte 1 ] : Touch Zone (0x00=None, 0x01=Head, 0x02=EarLeft, 0x03=EarRight, 0x04=Chest)
[ Byte 2 ] : Battery Level Percentage (0 - 100 %)
[ Byte 3 ] : Battery Status (0x00=Discharging, 0x01=Charging, 0x02=Full)
[ Byte 4 ] : Servo Angle Head Pan (0 - 180°)
[ Byte 5 ] : Reserved / Checksum (XOR bytes 0..4)
```

---

### C. Notificación Acústica y VAD (`...FA13` - NOTIFY)

Notificación binaria de 4 bytes emitida cada 250 ms durante la terapia del lenguaje / audiometría:

```text
[ Byte 0 ] : Nivel de Ruido LAeq en dB(A) (30 - 100 dB)
[ Byte 1 ] : Flag VAD (0x00=Silencio, 0x01=Voz Detectada)
[ Byte 2 ] : Valor Pico Envolvente RMS (0 - 255)
[ Byte 3 ] : Reserved
```

---

## ⚡ 4. Reconexión y Timeouts

1. **Keep-Alive Heartbeat**: La app React Native envía un comando nulo a `...FA11` cada 2000 ms.
2. **Timeout de Desconexión**: Si la mascota no recibe comunicación en 4000 ms, la tarea BLE gatilla un evento de desconexión preventiva, entrando en modo `IDLE_UNCONNECTED`.
