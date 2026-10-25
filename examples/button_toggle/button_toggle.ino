#include <Arduino.h>
constexpr uint8_t LED = 4;
constexpr uint8_t BUTTON = 5;
int candidate = HIGH;
int stable = HIGH;
uint32_t changedAt = 0;
bool on = false;
void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  pinMode(BUTTON, INPUT_PULLUP);
  candidate = stable = digitalRead(BUTTON);
  changedAt = millis();
}
void loop() {
  int raw = digitalRead(BUTTON);
  uint32_t now = millis();
  if (raw != candidate) { candidate = raw; changedAt = now; }
  if (candidate != stable && (uint32_t)(now - changedAt) >= 30) {
    stable = candidate;
    if (stable == LOW) {
      on = !on;
      digitalWrite(LED, on ? HIGH : LOW);
      Serial.println(on ? "on" : "off");
    }
  }
  delay(1);
}
