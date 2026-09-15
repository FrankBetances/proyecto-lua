#ifndef MASCOT_TOUCH_HPP
#define MASCOT_TOUCH_HPP

#include <Arduino.h>

class MascotTouch {
public:
    void init() {
        pinMode(1, INPUT); // Cabeza
        pinMode(2, INPUT); // Oreja Izq
        pinMode(3, INPUT); // Oreja Der
        pinMode(4, INPUT); // Pecho
        Serial.println("[TOUCH] Sensores capacitivos inicializados.");
    }

    int readHead() { return touchRead(1); }
    int readLeftEar() { return touchRead(2); }
    int readRightEar() { return touchRead(3); }
    int readChest() { return touchRead(4); }
};

#endif // MASCOT_TOUCH_HPP
