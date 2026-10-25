#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BME280.h>
#include <math.h>

constexpr int FAN_PIN = 4;
Adafruit_BME280 sensor;
bool sensorReady = false;
uint8_t sensorAddress = 0x76;

bool sensorResponds() {
  Wire.beginTransmission(sensorAddress);
  Wire.write(0xD0);  // BME280 chip-ID register
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom(sensorAddress, (uint8_t)1) != 1) return false;
  return Wire.read() == 0x60;
}
bool fanOn = false;
uint32_t lastCheck = 0;

void setup() {
  digitalWrite(FAN_PIN, LOW);
  pinMode(FAN_PIN, OUTPUT);
  Serial.begin(115200);
  Wire.begin(8, 9);
  sensorReady = sensor.begin(0x76, &Wire);
  if (!sensorReady) {
    sensorAddress = 0x77;
    sensorReady = sensor.begin(sensorAddress, &Wire);
  }
}

void loop() {
  uint32_t now = millis();
  if ((uint32_t)(now - lastCheck) < 2000) return;
  lastCheck = now;
  float t = sensorReady && sensorResponds()
            ? sensor.readTemperature() : NAN;
  bool valid = isfinite(t) && t >= -40 && t <= 85;
  if (!valid) fanOn = true;
  else if (!fanOn && t >= 30.0f) fanOn = true;
  else if (fanOn && t <= 28.0f) fanOn = false;
  digitalWrite(FAN_PIN, fanOn ? HIGH : LOW);
  Serial.printf("temp=%.2f valid=%d fan=%d\n", t, valid, fanOn);
  delay(1);
}
