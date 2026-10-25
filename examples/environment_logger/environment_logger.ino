#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BME280.h>
#include <math.h>

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
uint32_t lastSample = 0;
uint32_t sequenceNumber = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  Wire.begin(8, 9);
  sensorReady = sensor.begin(0x76, &Wire);
  if (!sensorReady) {
    sensorAddress = 0x77;
    sensorReady = sensor.begin(sensorAddress, &Wire);
  }
  Serial.println("seq,uptime_ms,valid,temp_c,rh_pct,pressure_hpa");
}

void loop() {
  uint32_t now = millis();
  if ((uint32_t)(now - lastSample) < 2000) return;
  lastSample = now;
  float t = NAN, h = NAN, p = NAN;
  if (sensorReady && sensorResponds()) {
    t = sensor.readTemperature();
    h = sensor.readHumidity();
    p = sensor.readPressure() / 100.0f;
  }
  bool valid = isfinite(t) && isfinite(h) && isfinite(p)
               && t >= -40 && t <= 85
               && h >= 0 && h <= 100 && p >= 300 && p <= 1100;
  Serial.printf("%lu,%lu,%d,", (unsigned long)sequenceNumber++,
                (unsigned long)now, valid ? 1 : 0);
  if (valid) Serial.printf("%.2f,%.2f,%.2f\n", t, h, p);
  else Serial.println(",,");
  delay(1);
}
