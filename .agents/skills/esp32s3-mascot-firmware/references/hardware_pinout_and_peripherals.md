# Especificación de Hardware y Pinout: ESP32-S3 Mascota Valeria+ / VIA+

Este documento define la asignación de pines GPIO y la configuración de periféricos físicos del microcontrolador **ESP32-S3** para la mascota interactiva.

---

## 📍 1. Tabla de Asignación de Pines (GPIO Map)

| Periférico | Función | Pin ESP32-S3 | Tipo Signal | Notas Hardware |
|---|---|---|---|---|
| **I2S Audio Output** | `BCLK` (Bit Clock) | `GPIO 7` | Digital Out | Conectado a MAX98357A / PCM5102 |
| | `LRCK` (Word Select) | `GPIO 6` | Digital Out | Frame Clock (44.1 kHz / 16-bit) |
| | `DIN` (Data In) | `GPIO 5` | Digital Out | Datos de audio PCM I2S |
| | `SD_MODE` (Shutdown) | `GPIO 4` | Digital Out | `HIGH` = Enable, `LOW` = Mute / Sleep |
| **I2S Audio Input** | `SCK` (Serial Clock) | `GPIO 15` | Digital Out | Conectado a Micrófono INMP441 |
| | `WS` (Word Select) | `GPIO 16` | Digital Out | Configuración de canal I2S mic |
| | `SD` (Serial Data) | `GPIO 17` | Digital In | Captura de audio digital MEMS |
| **Servomotores PWM** | `Oreja Izquierda` | `GPIO 8` | PWM (LEDC Ch 0)| Servo SG90 / MG90S (0° - 180°) |
| | `Oreja Derecha` | `GPIO 18` | PWM (LEDC Ch 1)| Servo SG90 / MG90S (0° - 180°) |
| | `Cabeza Pan (Giro)` | `GPIO 19` | PWM (LEDC Ch 2)| Servo SG90 / MG90S (0° - 180°) |
| | `Cabeza Tilt (Inclinación)`| `GPIO 20` | PWM (LEDC Ch 3)| Servo SG90 / MG90S (0° - 180°) |
| **Iluminación WS2812B**| `Matriz Ojos / Pecho`| `GPIO 38` | Data Out (RMT) | 2x Ojos (12 LEDs) + 1x Corazón (1 LED) |
| **Touch Capacitivo** | `Touch Cabeza` | `TOUCH1 / GPIO 1` | Analog/Touch | Detección de caricia superior |
| | `Touch Oreja Izq` | `TOUCH2 / GPIO 2` | Analog/Touch | Detección de toque en oreja izquierda |
| | `Touch Oreja Der` | `TOUCH3 / GPIO 3` | Analog/Touch | Detección de toque en oreja derecha |
| | `Touch Pecho` | `TOUCH4 / GPIO 4` | Analog/Touch | Detección de abrazo / toque pectoral |
| **Sensor Batería** | `VBAT_SENSE` | `ADC1_CH0 / GPIO 1` | Analog In (ADC) | Divisor de tensión 100k/100k a LiPo |
| **Estado y Diagnóstico**| `LED Status Integrado`| `GPIO 21` | Digital Out | LED RGB interno ESP32-S3 DevKit |

---

## 🔊 2. Configuración del Bus I2S de Audio Output (MAX98357A)

- **Frecuencia de Muestreo**: 44100 Hz (o 22050 Hz para ahorro de memoria Flash).
- **Resolución**: 16 bits por muestra, estéreo o mono duplicado.
- **Modo I2S**: Master Mode, TX.
- **Modo SD_MODE**: Se habilita solo durante la reproducción de tonos/prompts para eliminar soplido o zumbido de fondo (Zero-Noise Idle).

---

## 🎙️ 3. Configuración del Bus I2S de Audio Input (INMP441)

- **Frecuencia de Muestreo**: 16000 Hz.
- **Resolución**: 32 bits (extraídos los 24 bits superiores).
- **Filtro DSP Embebido**: Filtro paso alto (HPF) a 80 Hz en software para eliminar componente DC y ruido de manipulación mecánica.

---

## ⚡ 4. Consideraciones de Alimentación y Aislamiento

> [!WARNING]
> Los 4 servomotores al moverse simultáneamente pueden generar picos de corriente de hasta **1.5 A - 2.0 A**.
> 
> - **Separación de Alimentación**: Conectar los servos a la línea directa de la batería LiPo de 3.7V - 4.2V (o un convertidor Buck de 5V independiente).
> - **Condensadores de Desacoplamiento**: Colocar un condensador electrolítico de **1000 µF / 10V** en la línea VCC de los servos para evitar caídas de tensión (brownouts) en la ESP32-S3.
