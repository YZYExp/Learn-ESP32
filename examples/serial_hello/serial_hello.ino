#include <Arduino.h>
uint32_t count = 0;
uint32_t last = 0;
void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("boot: hello esp32");
}
void loop() {
  uint32_t now = millis();
  if ((uint32_t)(now - last) >= 1000) {
    last = now;
    Serial.printf("tick %lu\n", (unsigned long)count++);
  }
  delay(1);
}
