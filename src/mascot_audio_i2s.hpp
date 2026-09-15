#ifndef MASCOT_AUDIO_I2S_HPP
#define MASCOT_AUDIO_I2S_HPP

#include <Arduino.h>

class MascotAudioI2S {
public:
    void init() {
        // Inicialización dummy I2S para MAX98357A (DAC) e INMP441 (Mic)
        // I2S config placeholder
        Serial.println("[AUDIO] I2S Inicializado (Micrófono y Speaker).");
    }

    void processAudioTask() {
        // Placeholder para lectura I2S y cálculo VAD/RMS
    }
};

#endif // MASCOT_AUDIO_I2S_HPP
