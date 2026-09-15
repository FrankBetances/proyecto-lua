#include <Arduino.h>
#include "mascot_ble_server.hpp"
#include "mascot_kinematics.hpp"
#include "mascot_audio_i2s.hpp"
#include "mascot_touch.hpp"

// Colas de comunicación inter-tarea FreeRTOS
QueueHandle_t animationCmdQueue = nullptr;
QueueHandle_t telemetryQueue = nullptr;

// Instancias de Hardware
MascotBLEServer bleServer;
MascotKinematics kinematics;
MascotAudioI2S audioI2s;
MascotTouch touchSensors;

// Tarea 1 (Core 1): Animaciones, LEDs y Cinemática de Servos
void Task_Animation(void* pvParameters) {
    kinematics.init();
    const char* cmdState = nullptr;

    for (;;) {
        // Revisar si hay un comando animado entrante en la cola
        if (xQueueReceive(animationCmdQueue, &cmdState, 0) == pdTRUE) {
            Serial.printf("[TASK_ANIM] Estado cambiado a: %s\n", cmdState);
            if (strcmp(cmdState, "HAPPY") == 0) kinematics.setState(STATE_HAPPY);
            else if (strcmp(cmdState, "LISTENING") == 0) kinematics.setState(STATE_LISTENING);
            else if (strcmp(cmdState, "SLEEPING") == 0) kinematics.setState(STATE_SLEEPING);
            else kinematics.setState(STATE_IDLE);
        }

        kinematics.updateAnimationStep();
        vTaskDelay(pdMS_TO_TICKS(16)); // ~60 FPS update rate
    }
}

// Tarea 2 (Core 1): Lectura de Sensores Táctiles Capacitivos
void Task_TouchSensors(void* pvParameters) {
    touchSensors.init();

    for (;;) {
        int touchValue = touchSensors.readHead();
        // Umbral de capacitancia detectada por contacto
        if (touchValue < 30) {
            Serial.println("[TASK_TOUCH] Toque detectado en la cabeza.");
            bleServer.notifyTouch(0x01, 95); // Zona 1 (Cabeza), Batería 95%
            vTaskDelay(pdMS_TO_TICKS(500)); // Anti-debounce prolongado
        }
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

// Tarea 3 (Core 0): Audio I2S y procesamiento de micrófono
void Task_AudioI2S(void* pvParameters) {
    audioI2s.init();
    
    for (;;) {
        audioI2s.processAudioTask();
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

void setup() {
    Serial.begin(115200);
    while (!Serial && millis() < 2000);

    Serial.println("==========================================");
    Serial.println("  MASCOTA ROBÓTICA VALERIA+ / VIA+ (ESP32-S3)");
    Serial.println("==========================================");

    // Inicialización de colas FreeRTOS
    animationCmdQueue = xQueueCreate(10, sizeof(const char*));
    telemetryQueue    = xQueueCreate(10, sizeof(TelemetryPayload));

    // Inicializar Servidor BLE en Core 0
    bleServer.init("VALERIA-MASCOT-S3", animationCmdQueue);

    // Crear Tareas fijando afinidad de núcleos (Core 1 para Animación y Touch)
    xTaskCreatePinnedToCore(
        Task_Animation,
        "Task_Animation",
        4096,
        NULL,
        2,
        NULL,
        1 // Core 1
    );

    xTaskCreatePinnedToCore(
        Task_TouchSensors,
        "Task_TouchSensors",
        2048,
        NULL,
        3,
        NULL,
        1 // Core 1
    );

    xTaskCreatePinnedToCore(
        Task_AudioI2S,
        "Task_AudioI2S",
        4096,
        NULL,
        4,
        NULL,
        0 // Core 0
    );
}

void loop() {
    // El bucle principal loop() en Arduino corre en Core 1.
    // Mantenemos una tarea de supervisión ligera de Watchdog.
    vTaskDelay(pdMS_TO_TICKS(1000));
}
