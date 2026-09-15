// ============================================================================
// Lúa Expressive · Cinemática de Servos para ESP32-S3 (4 DoF)
//
// Implementa el motor de trayectorias suavizadas S-Curve y Bézier cúbico
// inspirado en Reachy Mini (Pollen Robotics / Hugging Face).
//
// Mapeo físico PWM (servos analógicos/digitales 50 Hz, 500-2400 µs):
//   - Pan  (Yaw)   : GPIO 19 -> 90° ± 45° (Rango [45°, 135°], Neutro: 90°)
//   - Tilt (Pitch) : GPIO 20 -> 90° [-20°, +30°] (Rango [70°, 120°], Neutro: 90°)
//   - Ear L (Oreja): GPIO 8  -> [30°, 90°] (0° a 60° de barrido, Neutro: 60°)
//   - Ear R (Oreja): GPIO 18 -> [30°, 90°] (0° a 60° de barrido, Neutro: 60°)
// ============================================================================
#ifndef MASCOT_KINEMATICS_HPP
#define MASCOT_KINEMATICS_HPP

#include <Arduino.h>
#include <ESP32Servo.h>
#include <FastLED.h>
#include <math.h>

#define PIN_SERVO_EAR_LEFT    8
#define PIN_SERVO_EAR_RIGHT   18
#define PIN_SERVO_HEAD_PAN    19
#define PIN_SERVO_HEAD_TILT   20

#define PIN_NEOPIXEL          38
#define NUM_LEDS_EYES         24 // 12 por ojo
#define NUM_LEDS_TOTAL        25 // 24 ojos + 1 corazón

enum MascotState {
    STATE_IDLE,
    STATE_LISTENING,
    STATE_HAPPY,
    STATE_TALKING,
    STATE_SLEEPING,
    STATE_CURIOSITY,
    STATE_PURRING,
    STATE_CELEBRATE
};

struct RobotPose {
    float pan;       // Grados físicos servo: [45, 135], neutro 90
    float tilt;      // Grados físicos servo: [70, 120], neutro 90
    float ear_left;  // Grados físicos servo: [30, 90], neutro 60
    float ear_right; // Grados físicos servo: [30, 90], neutro 60
};

class MascotKinematics {
private:
    Servo earLeft;
    Servo earRight;
    Servo headPan;
    Servo headTilt;

    CRGB leds[NUM_LEDS_TOTAL];
    MascotState currentState = STATE_IDLE;

    // Estado cinemático actual y de transición
    RobotPose currentPose = {90.0f, 90.0f, 60.0f, 60.0f};
    RobotPose startPose   = {90.0f, 90.0f, 60.0f, 60.0f};
    RobotPose targetPose  = {90.0f, 90.0f, 60.0f, 60.0f};

    uint32_t transitionStartMs = 0;
    uint32_t transitionDurationMs = 0;
    bool isTransitioning = false;
    bool servosRelaxed = false;

    // Protección pediátrica anti-bloqueo (> 500 ms)
    bool stallDetected = false;
    uint32_t stallStartMs = 0;
    bool powerCut = false;

    // Curva de Perlin SmootherStep C²: 6t⁵ - 15t⁴ + 10t³
    static float smootherStep(float t) {
        if (t <= 0.0f) return 0.0f;
        if (t >= 1.0f) return 1.0f;
        return t * t * t * (t * (t * 6.0f - 15.0f) + 10.0f);
    }

public:
    void init() {
        // Asignación de timers LEDC para ESP32Servo
        ESP32PWM::allocateTimer(0);
        ESP32PWM::allocateTimer(1);
        ESP32PWM::allocateTimer(2);
        ESP32PWM::allocateTimer(3);

        earLeft.setPeriodHertz(50);
        earRight.setPeriodHertz(50);
        headPan.setPeriodHertz(50);
        headTilt.setPeriodHertz(50);

        earLeft.attach(PIN_SERVO_EAR_LEFT, 500, 2400);
        earRight.attach(PIN_SERVO_EAR_RIGHT, 500, 2400);
        headPan.attach(PIN_SERVO_HEAD_PAN, 500, 2400);
        headTilt.attach(PIN_SERVO_HEAD_TILT, 500, 2400);

        FastLED.addLeds<WS2812B, PIN_NEOPIXEL, GRB>(leds, NUM_LEDS_TOTAL);
        FastLED.setBrightness(40); // Brillo seguro para visión infantil (< 50 nit)

        gotoPose({90.0f, 90.0f, 60.0f, 60.0f}, 0.8f);
        setEyeColor(CRGB::Blue);
    }

    /**
     * Movimiento suave hacia pose objetivo (inspirado en goto_target() de Reachy Mini).
     */
    void gotoPose(const RobotPose& target, float durationSec) {
        if (powerCut) return;

        startPose = currentPose;
        targetPose.pan       = constrain(target.pan,       45.0f, 135.0f);
        targetPose.tilt      = constrain(target.tilt,      70.0f, 120.0f);
        targetPose.ear_left  = constrain(target.ear_left,  30.0f,  90.0f);
        targetPose.ear_right = constrain(target.ear_right, 30.0f,  90.0f);

        transitionStartMs = millis();
        transitionDurationMs = durationSec > 0.05f ? static_cast<uint32_t>(durationSec * 1000.0f) : 10;
        isTransitioning = true;
        servosRelaxed = false;
    }

    void setTargetAngles(int leftEar, int rightEar, int pan, int tilt) {
        RobotPose p = {
            static_cast<float>(pan),
            static_cast<float>(tilt),
            static_cast<float>(leftEar),
            static_cast<float>(rightEar)
        };
        gotoPose(p, 0.4f);
    }

    void setEyeColor(CRGB color) {
        for (int i = 0; i < NUM_LEDS_EYES; i++) {
            leds[i] = color;
        }
        FastLED.show();
    }

    void setHeartPulse(CRGB color, uint8_t brightness) {
        leds[24] = color;
        leds[24].nscale8(brightness);
        FastLED.show();
    }

    void emergencyStop() {
        targetPose = {90.0f, 90.0f, 60.0f, 60.0f};
        currentPose = targetPose;
        isTransitioning = false;
        servosRelaxed = true;
    }

    void notifyStall(bool stalled) {
        if (stalled) {
            if (!stallDetected) {
                stallDetected = true;
                stallStartMs = millis();
            } else if (millis() - stallStartMs > 500) {
                // Corte de seguridad MDR pediátrica: deshabilitar PWM si hay atasco > 500 ms
                powerCut = true;
                emergencyStop();
            }
        } else {
            stallDetected = false;
            powerCut = false;
        }
    }

    void updateAnimationStep() {
        uint32_t now = millis();

        // 1. Actualización de trayectoria cinemática continua
        if (isTransitioning && !powerCut) {
            uint32_t elapsed = now - transitionStartMs;
            if (elapsed >= transitionDurationMs) {
                currentPose = targetPose;
                isTransitioning = false;
            } else {
                float t = static_cast<float>(elapsed) / static_cast<float>(transitionDurationMs);
                float factor = smootherStep(t);
                currentPose.pan       = startPose.pan       + factor * (targetPose.pan       - startPose.pan);
                currentPose.tilt      = startPose.tilt      + factor * (targetPose.tilt      - startPose.tilt);
                currentPose.ear_left  = startPose.ear_left  + factor * (targetPose.ear_left  - startPose.ear_left);
                currentPose.ear_right = startPose.ear_right + factor * (targetPose.ear_right - startPose.ear_right);
            }

            // Escritura PWM en los servos
            headPan.write(static_cast<int>(currentPose.pan + 0.5f));
            headTilt.write(static_cast<int>(currentPose.tilt + 0.5f));
            earLeft.write(static_cast<int>(currentPose.ear_left + 0.5f));
            earRight.write(static_cast<int>(currentPose.ear_right + 0.5f));
        }

        // 2. Renderizado de iluminación y respiración visual
        static uint8_t frame = 0;
        frame++;

        switch (currentState) {
            case STATE_IDLE:
                // Respiración suave en corazón y postura neutra
                setHeartPulse(CRGB::Blue, 50 + 40 * sin(frame * 0.05));
                break;

            case STATE_HAPPY:
                setEyeColor(CRGB::Green);
                setHeartPulse(CRGB::Yellow, 200);
                break;

            case STATE_LISTENING:
                setEyeColor(CRGB::Amber);
                break;

            case STATE_CURIOSITY:
                setEyeColor(CRGB::Cyan);
                setHeartPulse(CRGB::Cyan, 180);
                break;

            case STATE_PURRING:
                setEyeColor(CRGB::HotPink);
                setHeartPulse(CRGB::HotPink, 140 + 30 * sin(frame * 0.15));
                break;

            case STATE_SLEEPING:
                setEyeColor(CRGB::Black);
                setHeartPulse(CRGB::Purple, 20 + 15 * sin(frame * 0.02));
                break;

            case STATE_CELEBRATE:
                setEyeColor(CRGB::Gold);
                setHeartPulse(CRGB::White, 255);
                break;

            default:
                break;
        }
    }

    void setState(MascotState newState) {
        currentState = newState;
        switch (newState) {
            case STATE_IDLE:
                // Neutro centrado
                gotoPose({90.0f, 90.0f, 60.0f, 60.0f}, 0.8f);
                break;

            case STATE_LISTENING:
                // Cabeza atenta inclinada hacia arriba, ambas orejas erguidas
                gotoPose({90.0f, 95.0f, 90.0f, 90.0f}, 0.5f);
                break;

            case STATE_CURIOSITY:
                // Curiosidad: inclinación a un lado, oreja izquierda arriba, derecha baja
                gotoPose({110.0f, 105.0f, 85.0f, 45.0f}, 0.9f);
                break;

            case STATE_PURRING:
                // Respuesta táctil: cabeceo suave
                gotoPose({98.0f, 94.0f, 70.0f, 60.0f}, 0.7f);
                break;

            case STATE_HAPPY:
                // Asentimiento alegre
                gotoPose({90.0f, 98.0f, 75.0f, 75.0f}, 0.6f);
                break;

            case STATE_SLEEPING:
                // Standby: cabeza abajo, orejas plegadas
                gotoPose({90.0f, 70.0f, 35.0f, 35.0f}, 1.4f);
                break;

            case STATE_CELEBRATE:
                // Celebración rotunda
                gotoPose({115.0f, 102.0f, 88.0f, 88.0f}, 1.0f);
                break;

            default:
                break;
        }
    }
};

#endif // MASCOT_KINEMATICS_HPP
