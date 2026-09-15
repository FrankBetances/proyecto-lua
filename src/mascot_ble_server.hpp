#ifndef MASCOT_BLE_SERVER_HPP
#define MASCOT_BLE_SERVER_HPP

#include <Arduino.h>
#include <NimBLEDevice.h>
#include <ArduinoJson.h>

// Definición de UUIDs GATT para Valeria+ y VIA+
#define SERVICE_UUID           "0000fa10-0000-1000-8000-00805f9b34fb"
#define CHAR_COMMAND_UUID       "0000fa11-0000-1000-8000-00805f9b34fb"
#define CHAR_TELEMETRY_UUID     "0000fa12-0000-1000-8000-00805f9b34fb"
#define CHAR_ACOUSTIC_UUID      "0000fa13-0000-1000-8000-00805f9b34fb"

// Estructura de evento táctil y estado
struct TelemetryPayload {
    uint8_t eventCode;
    uint8_t touchZone;
    uint8_t batteryPct;
    uint8_t batteryStatus;
    uint8_t headPanAngle;
    uint8_t checksum;
};

class MascotBLECallbacks : public NimBLEServerCallbacks, public NimBLECharacteristicCallbacks {
public:
    static bool deviceConnected;
    static String lastCommand;
    static QueueHandle_t cmdQueue;

    void onConnect(NimBLEServer* pServer) override {
        deviceConnected = true;
        Serial.println("[BLE] App Valeria+/VIA+ conectada.");
    }

    void onDisconnect(NimBLEServer* pServer) override {
        deviceConnected = false;
        Serial.println("[BLE] App desconectada. Iniciando advertising...");
        NimBLEDevice::startAdvertising();
    }

    void onWrite(NimBLECharacteristic* pCharacteristic) override {
        std::string rxValue = pCharacteristic->getValue();
        if (rxValue.length() > 0) {
            String jsonStr = String(rxValue.c_str());
            Serial.printf("[BLE] Comando recibido: %s\n", jsonStr.c_str());
            
            // Decodificación simplificada con ArduinoJson
            StaticJsonDocument<256> doc;
            DeserializationError err = deserializeJson(doc, jsonStr);
            if (!err && cmdQueue != nullptr) {
                const char* state = doc["state"] | "IDLE";
                xQueueSend(cmdQueue, &state, portMAX_DELAY);
            }
        }
    }
};

bool MascotBLECallbacks::deviceConnected = false;
String MascotBLECallbacks::lastCommand = "";
QueueHandle_t MascotBLECallbacks::cmdQueue = nullptr;

class MascotBLEServer {
private:
    NimBLEServer* pServer = nullptr;
    NimBLEService* pService = nullptr;
    NimBLECharacteristic* pCmdChar = nullptr;
    NimBLECharacteristic* pTelemChar = nullptr;
    NimBLECharacteristic* pAudioChar = nullptr;

public:
    void init(const char* deviceName, QueueHandle_t animationQueue) {
        MascotBLECallbacks::cmdQueue = animationQueue;
        NimBLEDevice::init(deviceName);
        NimBLEDevice::setPower(ESP_PWR_LVL_P9); // Potencia máxima de transmisión BLE

        pServer = NimBLEDevice::createServer();
        pServer->setCallbacks(new MascotBLECallbacks());

        pService = pServer->createService(SERVICE_UUID);

        // Característica de Comandos (WRITE)
        pCmdChar = pService->createCharacteristic(
            CHAR_COMMAND_UUID,
            NIMBLE_PROPERTY::WRITE | NIMBLE_PROPERTY::WRITE_NR
        );
        pCmdChar->setCallbacks(new MascotBLECallbacks());

        // Característica de Telemetría (NOTIFY)
        pTelemChar = pService->createCharacteristic(
            CHAR_TELEMETRY_UUID,
            NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
        );

        // Característica de Sonometría / VAD (NOTIFY)
        pAudioChar = pService->createCharacteristic(
            CHAR_ACOUSTIC_UUID,
            NIMBLE_PROPERTY::NOTIFY
        );

        pService->start();

        NimBLEAdvertising* pAdvertising = NimBLEDevice::getAdvertising();
        pAdvertising->addServiceUUID(SERVICE_UUID);
        pAdvertising->setScanResponse(true);
        pAdvertising->start();
        Serial.printf("[BLE] Servidor '%s' iniciado y anunciando.\n", deviceName);
    }

    void notifyTouch(uint8_t touchZone, uint8_t batteryLevel) {
        if (!MascotBLECallbacks::deviceConnected || pTelemChar == nullptr) return;

        TelemetryPayload payload;
        payload.eventCode = 0x01; // Evento Toque
        payload.touchZone = touchZone;
        payload.batteryPct = batteryLevel;
        payload.batteryStatus = 0x00;
        payload.headPanAngle = 90;
        payload.checksum = payload.eventCode ^ payload.touchZone ^ payload.batteryPct;

        pTelemChar->setValue((uint8_t*)&payload, sizeof(TelemetryPayload));
        pTelemChar->notify();
    }
};

#endif // MASCOT_BLE_SERVER_HPP
