#include <Arduino.h>
#include <Wire.h>

void setup() {
  Serial.begin(115200);
  if (!Wire.begin(8, 9, 100000)) {
    Serial.println("I2C initialization failed");
    return;
  }
  for (uint8_t address = 0x08; address <= 0x77; ++address) {
    Wire.beginTransmission(address);
    uint8_t result = Wire.endTransmission();
    if (result == 0) {
      Serial.printf("ACK at 0x%02X\n", address);
    }
  }
}

void loop() {
  delay(1000);
}
