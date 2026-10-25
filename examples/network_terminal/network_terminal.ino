// Design example: not compiled or tested on hardware.
// ESP32-S3-DevKitC-1; Arduino-ESP32 3.x.
// Dependencies: ArduinoJson 7, Adafruit SSD1306, Adafruit GFX.
// SSD1306 128x64 I2C OLED: SDA GPIO8, SCL GPIO9, 3.3 V logic.
// Plain HTTP is ONLY for the local non-secret lab in chapter 23.
// No API keys, authentication headers or personal data are sent.
#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <string.h>
#include <esp_timer.h>

const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* STATUS_URL = "http://192.168.1.50:8000/status.json";
constexpr uint32_t POLL_MS = 5000;
constexpr uint32_t STALE_MS = 15000;
constexpr size_t BODY_LIMIT = 512;

// HTTPClient removes HTTP/chunk framing before writing here.
// The real received body, including unknown-length responses, is bounded.
class BoundedBody : public Stream {
 public:
  using Print::write;
  size_t write(uint8_t value) override { return write(&value, 1); }
  size_t write(const uint8_t* input, size_t count) override {
    size_t room = BODY_LIMIT - used;
    size_t accepted = count < room ? count : room;
    memcpy(bytes + used, input, accepted);
    used += accepted;
    bytes[used] = '\0';
    if (accepted != count) overflow = true;
    return accepted;
  }
  int available() override { return 0; }
  int read() override { return -1; }
  int peek() override { return -1; }
  void flush() override {}
  char bytes[BODY_LIMIT + 1] = {};
  size_t used = 0;
  bool overflow = false;
};

Adafruit_SSD1306 screen(128, 64, &Wire, -1);
bool screenReady = false;
bool haveGoodData = false;
char state[16] = "";
uint32_t revision = 0;
int64_t lastGoodUs = 0;
uint32_t lastPollMs = 0;
uint32_t lastDrawMs = 0;
const char* lastResult = "WAITING";

void requestStatus() {
  WiFiClient client;
  HTTPClient http;
  http.setConnectTimeout(1500);
  http.setTimeout(1500);
  http.useHTTP10(true);
  if (!http.begin(client, STATUS_URL)) {
    lastResult = "BEGIN ERROR";
    return;
  }
  int response = http.GET();
  Serial.printf("http=%d\n", response);
  if (response != HTTP_CODE_OK) {
    lastResult = response < 0 ? "HTTP ERROR" : "HTTP STATUS";
    http.end();
    return;
  }
  int announcedSize = http.getSize();
  if (announcedSize > (int)BODY_LIMIT) {
    lastResult = "BODY TOO BIG";
    http.end();
    return;
  }
  BoundedBody body;
  int transferred = http.writeToStream(&body);
  http.end();
  if (body.overflow || transferred < 0 || body.used == 0) {
    lastResult = body.overflow ? "BODY TOO BIG" : "BODY ERROR";
    return;
  }
  if (announcedSize >= 0 && (size_t)announcedSize != body.used) {
    lastResult = "SHORT BODY";
    return;
  }
  JsonDocument doc;
  DeserializationError error = deserializeJson(
      doc, body.bytes, body.used, DeserializationOption::NestingLimit(4));
  if (error || !doc["state"].is<const char*>() ||
      !doc["revision"].is<uint32_t>()) {
    lastResult = "JSON ERROR";
    return;
  }
  const char* incoming = doc["state"].as<const char*>();
  if (strcmp(incoming, "ok") && strcmp(incoming, "degraded") &&
      strcmp(incoming, "maintenance")) {
    lastResult = "STATE ERROR";
    return;
  }
  strlcpy(state, incoming, sizeof(state));
  revision = doc["revision"].as<uint32_t>();
  lastGoodUs = esp_timer_get_time();
  haveGoodData = true;
  lastResult = "VALID";
  Serial.printf("accepted state=%s revision=%lu\n", state,
                (unsigned long)revision);
}

void drawStatus() {
  if (!screenReady) return;
  screen.clearDisplay();
  screen.setTextSize(1);
  screen.setTextColor(SSD1306_WHITE);
  screen.setCursor(0, 0);
  screen.println(WiFi.status() == WL_CONNECTED ? "Wi-Fi CONNECTED" : "Wi-Fi OFFLINE");
  if (!haveGoodData) {
    screen.println("NO DATA");
  } else {
    uint64_t age = (uint64_t)(esp_timer_get_time() - lastGoodUs) / 1000ULL;
    screen.println(state);
    screen.print("rev "); screen.println((unsigned long)revision);
    screen.print("age "); screen.print((unsigned long)(age / 1000));
    screen.println("s");
    if (age > STALE_MS) screen.println("STALE");
  }
  screen.println(lastResult);
  screen.display();
}

void setup() {
  Serial.begin(115200);
  Wire.begin(8, 9);
  // periphBegin=false preserves the explicit Wire pin selection above.
  screenReady = screen.begin(SSD1306_SWITCHCAPVCC, 0x3C, true, false);
  if (!screenReady) Serial.println("OLED init failed; serial diagnostics remain active");
  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  drawStatus();
}

void loop() {
  uint32_t now = millis();
  if ((uint32_t)(now - lastPollMs) >= POLL_MS) {
    lastPollMs = now;
    if (WiFi.status() == WL_CONNECTED) requestStatus();
    else lastResult = "NO WIFI";
    Serial.printf("result=%s\n", lastResult);
  }
  now = millis();
  if ((uint32_t)(now - lastDrawMs) >= 1000) {
    lastDrawMs = now;
    drawStatus();
  }
  delay(1);
}
