#ifndef MASCOT_KINEMATICS_HPP
#define MASCOT_KINEMATICS_HPP

#include <Arduino.h>
#include <ESP32Servo.h>
#include <FastLED.h>

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
    STATE_SLEEPING
};

class MascotKinematics {
private:
    Servo earLeft;
    Servo earRight;
    Servo headPan;
    Servo headTilt;

    CRGB leds[NUM_LEDS_TOTAL];
    MascotState currentState = STATE_IDLE;

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
        FastLED.setBrightness(40); // Brillo seguro para visión infantil

        setTargetAngles(90, 90, 90, 90);
        setEyeColor(CRGB::Blue);
    }

    void setTargetAngles(int leftEar, int rightEar, int pan, int tilt) {
        // Enforzar rangos de seguridad pediátrica
        leftEar  = constrain(leftEar, 15, 165);
        rightEar = constrain(rightEar, 15, 165);
        pan      = constrain(pan, 30, 150);
        tilt     = constrain(tilt, 60, 120);

        earLeft.write(leftEar);
        earRight.write(rightEar);
        headPan.write(pan);
        headTilt.write(tilt);
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

    void updateAnimationStep() {
        static uint8_t frame = 0;
        frame++;

        switch (currentState) {
            case STATE_IDLE:
                // Respiración suave en corazón y postura neutra
                setHeartPulse(CRGB::Blue, 50 + 40 * sin(frame * 0.05));
                break;

            case STATE_HAPPY:
                // Movimiento batiendo orejas alternadamente
                earLeft.write(60 + 40 * sin(frame * 0.2));
                earRight.write(60 - 40 * sin(frame * 0.2));
                setEyeColor(CRGB::Green);
                setHeartPulse(CRGB::Yellow, 200);
                break;

            case STATE_LISTENING:
                // Orejas atentas inclinadas hacia adelante
                setTargetAngles(120, 120, 90, 105);
                setEyeColor(CRGB::Amber);
                break;

            case STATE_SLEEPING:
                setTargetAngles(30, 30, 90, 60);
                setEyeColor(CRGB::Black);
                setHeartPulse(CRGB::Purple, 20 + 15 * sin(frame * 0.02));
                break;

            default:
                break;
        }
    }

    void setState(MascotState newState) {
        currentState = newState;
    }
};

#endif // MASCOT_KINEMATICS_HPP
