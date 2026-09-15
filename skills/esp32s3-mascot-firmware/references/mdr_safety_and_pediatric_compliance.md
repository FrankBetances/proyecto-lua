# Normas de Seguridad Pediátrica y Cumplimiento Regulatorio (MDR / ISO 14971)

Este documento especifica los requisitos de seguridad mecánica, acústica y eléctrica integrados en el firmware de la mascota interactiva ESP32-S3 para cumplir con las directrices de dispositivos médicos y software pediátrico (**Reglamento UE 2017/745 MDR** e **ISO 14971**).

---

## 🔊 1. Seguridad Acústica (Protección Auditiva Infantil)

Dado que la mascota se utiliza en sesiones de terapia auditivo-verbal y audiometría en niños (incluyendo aquellos con implantes cocleares o audífonos):

1. **Límite de Presión Acústica Máxima (SPL)**: El firmware restringe por software la salida digital del DAC a un máximo equivalente de **75 dBA a 10 cm** de distancia de la boca/altavoz de la mascota.
2. **Limitador Digital Peak Guard**: Un algoritmo de compresión de rango dinámico (DRC) en el bus I2S previene picos inesperados o distorsiones de audio superiores a 0 dBFS.
3. **Silenciamiento Automático (Auto-Mute)**: Al encender el microcontrolador o si se detecta un reinicio inesperado por WDT, el pin `SD_MODE` se mantiene en `LOW` hasta que el motor de audio se haya inicializado completamente.

---

## ⚙️ 2. Seguridad Mecánica en Servomotores

Para evitar pellizcos, atrapamientos de dedos infantiles o sobrecalentamiento de motores SG90/MG90S:

1. **Detección de Bloqueo Mecánico (Stall Detection)**:
   - Si la posición angular del servo no logra avanzar hacia su objetivo durante más de 400 ms (estimado por seguimiento de corriente o timeout de movimiento), el firmware deshabilita inmediatamente la señal PWM del canal correspondiente.
2. **Curva de Aceleración Suave (Soft Start & S-Curve Kinematics)**:
   - Quedan prohibidos los cambios escalón instantáneos de ángulo (ej. pasar de 0° a 180° en 1 ms). Todo movimiento debe ser interpolado con una rampa sinusoidal de al menos 200 ms.
3. **Límite Mecánico Software (Safe Angle Boundaries)**:
   - Orejas: Rango limitado a `[15°, 165°]`.
   - Cabeza Pan: Rango limitado a `[30°, 150°]`.
   - Cabeza Tilt: Rango limitado a `[60°, 120°]`.

---

## 🔋 3. Seguridad Eléctrica y Gestión Térmica

1. **Monitorización Continuada de Batería**:
   - Lectura del ADC en `GPIO 1` cada 5 segundos.
   - Si la tensión desciende por debajo de **3.4 V** (batería en 10%), se emite una alerta BLE `BATTERY_LOW` y se deshabilitan las funciones mecánicas (servos) para preservar la capacidad de conexión BLE.
   - Si la tensión cae a **3.2 V**, el ESP32-S3 entra en modo `Deep Sleep` profundo de protección.
2. **Protección Térmica del SoC**:
   - Uso del sensor de temperatura interno del ESP32-S3 (`temp_sensor_read_celsius()`). Si la temperatura supera los **65 °C**, el firmware suspende la animación y apaga los LEDs WS2812B.

---

## 🛡️ 4. Protocolo Fail-Safe de Desconexión

En caso de que la aplicación móvil se cierre inesperadamente o el enlace BLE sufra interferencias:

```text
[ Pérdida BLE > 3.0 s ]
          │
          ▼
[ Transición Cinemática Suave (1.0 s) ] ──► Servos vuelven a posición neutra reposo
          │
          ▼
[ Iluminación Ocular ] ──────────────► LEDs reducen brillo a 20%, patrón azul suave
          │
          ▼
[ Estado del Dispositivo ] ──────────► Entra en modo de bajo consumo publicando Advertising
```
