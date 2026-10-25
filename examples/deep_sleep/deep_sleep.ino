// Static review only; not compiled or tested on hardware.
#include <Arduino.h>
#include "esp_sleep.h"

void setup() {
  Serial.begin(115200);
  delay(300);  // 仅给本次串口观察留时间，也会增加能耗
  Serial.println("awake: next wake in 30 seconds");
  Serial.flush();
  esp_sleep_enable_timer_wakeup(30ULL * 1000000ULL);
  esp_deep_sleep_start();
}
void loop() {}
