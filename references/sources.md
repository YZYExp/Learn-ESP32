# 参考资料索引

资料核对日期：2026-10-25。正文使用处保留来源；下列按首次出现顺序去重。stable/latest 为滚动链接，实作时应选择对应目标和版本。

## 从一块板看嵌入式世界

- [系列比较：乐鑫官方](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/hw-reference/chip-series-comparison.html)
- [开发框架入口](https://www.espressif.com/en/products/sdks/esp-idf)

## ESP32家族与板卡选择

- [官方模组料号解释](https://developer.espressif.com/blog/2025/03/espressif-part-numbers-explained/)
- [开发板指南与原理图入口](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/index.html)
- [Arduino 官方入口](https://docs.espressif.com/projects/arduino-esp32/en/latest/getting_started.html)
- [MicroPython ESP32 文档](https://docs.micropython.org/en/latest/esp32/quickref.html)

## 电路、供电与测量

- [ESP32-S3 数据手册入口](https://www.espressif.com/en/products/socs/esp32-s3)
- [S3 硬件设计指南](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/index.html)

## 从源码到第一次运行

- [官方安装说明](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html)
- [官方迁移说明](https://docs.espressif.com/projects/arduino-esp32/en/latest/migration_guides/2.x_to_3.0.html)
- [S3 开发板使用指南](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html)
- [IDF 入门](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/get-started/index.html)

## GPIO、按钮与状态机

- [Arduino GPIO 官方说明](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/gpio.html)

## 模拟量、ADC与PWM

- [S3 ADC 单次采样驱动](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/adc/adc_oneshot.html)
- [Arduino ADC](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/adc.html)
- [Arduino LEDC](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html)

## UART、I2C与SPI

- [Arduino-ESP32 UART 文档](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/serial.html)
- [Arduino-ESP32 I2C 文档](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/i2c.html)
- [官方 SPI 示例](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/spi.html)

## 传感器与数据可信度

- [Bosch 产品页](https://www.bosch-sensortec.com/en/products/environmental-sensors/humidity-sensors-bme280/)
- [数据手册](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf)
- [Sensor API](https://github.com/boschsensortec/BME280_SensorAPI)

## 屏幕、灯光与人机交互

- [`esp_lcd` 文档](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/lcd/index.html)
- [LVGL 的 ESP32 集成文档](https://lvgl.io/docs/open/integration/chip_vendors/espressif/add_lvgl_to_esp32_idf_project)
- [同一 SPI 总线上的 LCD 与触摸例程](https://github.com/espressif/esp-idf/blob/master/examples/peripherals/lcd/spi_lcd_touch/README.md)

## 电机、驱动与机械动作

- [TI 数据手册](https://www.ti.com/lit/ds/symlink/drv8833.pdf)

## Wi-Fi与网络基础

- [Arduino-ESP32 Wi-Fi API](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/wifi.html)
- [Wi-Fi 驱动说明](https://docs.espressif.com/projects/esp-idf/en/v5.5.4/esp32s3/api-guides/wifi.html)

## HTTP、MQTT与数据接口

- [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html)
- [`esp_http_client`](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/protocols/esp_http_client.html)
- [OASIS MQTT 3.1.1 标准](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)
- [ESP-MQTT 文档](https://docs.espressif.com/projects/esp-mqtt/en/latest/esp32/)
- [官方组件仓库](https://github.com/espressif/esp-mqtt)
- [ESP-TLS](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/protocols/esp_tls.html)

## 蓝牙与近距离连接

- [资料：ESP32-S3 BLE 概述](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-guides/ble/overview.html)
- [Bluetooth SIG 的 GATT 介绍](https://www.bluetooth.com/bluetooth-resources/intro-to-bluetooth-gap-gatt/)
- [资料：官方 BLE UART 服务示例](https://github.com/espressif/esp-idf/tree/master/examples/bluetooth/ble_uart_service)
- [乐鑫无线共存指南](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/coexist.html)

## Thread、Zigbee与Matter

- [资料：Connectivity Standards Alliance 的 Matter 说明](https://csa-iot.org/all-solutions/matter/)
- [Thread Group 的技术概览](https://www.threadgroup.org/What-is-Thread/Overview)
- [资料：ESP32-C6 数据手册](https://documentation.espressif.com/esp32-c6_datasheet_en.html)
- [ESP32-H2 产品说明](https://www.espressif.com/en/products/socs/esp32-h2)
- [ESP32-P4 产品说明](https://www.espressif.com/en/products/socs/esp32-p4)
- [资料：ESP Thread Border Router 硬件平台](https://docs.espressif.com/projects/esp-thread-br/en/latest/hardware_platforms.html)
- [资料：ESP-Matter 入门与支持路径](https://docs.espressif.com/projects/esp-matter/en/latest/esp32c6/introduction.html)

## FreeRTOS与并发

- [资料：ESP-IDF FreeRTOS 说明](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/freertos_idf.html)

## 存储、时间与离线运行

- [资料：Preferences API](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/preferences.html)
- [资料：NVS 的设计与限制](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/nvs_flash.html)
- [资料：ESP32-S3 系统时间](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/system_time.html)

## 电池、睡眠与功耗预算

- [资料：ESP32-S3 睡眠模式](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/sleep_modes.html)
- [资料：乐鑫系统低功耗说明](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/low-power-mode/low-power-mode-soc.html)

## 调试、测试与故障定位

- [资料：ESP32-S3 Fatal Errors](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/fatal-errors.html)
- [资料：ESP32-S3 JTAG 调试指南](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/jtag-debugging/index.html)
- [资料：ESP-IDF 堆内存调试](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/heap_debug.html)
- [资料：ESP32-S3 看门狗](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/wdts.html)
- [资料：Core Dump](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/core_dump.html)

## 安全、配网与OTA

- [资料：Espressif，Unified Provisioning](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/provisioning/provisioning.html)
- [资料：Espressif，OTA Process Overview](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/ota.html)
- [资料：Espressif，Secure Boot v2](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/security/secure-boot-v2.html)
- [资料：Espressif，Flash Encryption](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/security/flash-encryption.html)

## 从面包板到可靠硬件

- [资料：Espressif，ESP32-S3 Hardware Design Guidelines](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/)
- [资料：Espressif，PCB Layout Design，含模组布局要求](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html)

## 项目一：环境记录器

- [资料：Bosch Sensortec，BME280 产品页与数据手册](https://www.bosch-sensortec.com/en/products/environmental-sensors/humidity-sensors-bme280)
- [资料：Adafruit，BME280 Arduino Test](https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/arduino-test)

## 项目二：低压风扇控制器

- [资料：Noctua，Microcontroller guide](https://www.noctua.at/en/support/faqs/microcontroller-guide-pwm-setup-and-rpm-monitoring)
- [资料：AOS，AO3400A](https://www.aosmd.com/products/mosfets/low-voltage-mosfets-12v-30v/ao3400a)
- [资料：TI，TPL7407LA-Q1 数据手册，Application Information](https://www.ti.com/lit/gpn/TPL7407LA-Q1)

## 项目三：联网状态终端

- [资料：Adafruit，Monochrome OLED Arduino Library & Examples](https://learn.adafruit.com/monochrome-oled-breakouts/arduino-library-and-examples)
- [资料：ArduinoJson，v7 Deserialization tutorial](https://arduinojson.org/v7/tutorial/deserialization/)
- [资料：ArduinoJson，HTTPClient 集成说明](https://arduinojson.org/v6/how-to/use-arduinojson-with-httpclient/)

## 从ESP32走向完整系统

- [资料：Espressif，ESP-Hosted](https://github.com/espressif/esp-hosted)
- [资料：ESPHome，ESP32 Platform](https://esphome.io/components/esp32/)
- [资料：ESPHome，BME280 组件](https://esphome.io/components/sensor/bme280/)
- [资料：Espressif，ESP-BOX](https://github.com/espressif/esp-box)
- [资料：Espressif，ESP-DL Introduction](https://docs.espressif.com/projects/esp-dl/en/latest/introduction/readme.html)
- [资料：Espressif，ESP-SR S3 用户指南](https://docs.espressif.com/projects/esp-sr/en/latest/esp32s3/index.html)


## 新增设备照片与授权

设备图用于外观识别，接线仍以对应型号资料和章内连接表为准。图片仅缩放、白底处理并转为 JPEG，没有更改器件结构或原有标记。各照片及其技术处理版保留原授权，以下署名不表示原作者认可本书项目。

- **ESP32-S3-DevKitC-1 实物**：Espressif Systems；[来源页](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html)；[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)。
- **S3开发板元件位置**：Espressif Systems；[来源页](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html)；[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)。
- **S3引脚丝印**：Espressif Systems；[来源页](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html)；[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)。
- **ESP32-C6-DevKitC-1**：Espressif Systems；[来源页](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32c6/esp32-c6-devkitc-1/user_guide.html)；[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)。
- **ESP32-H2-DevKitM-1**：Espressif Systems；[来源页](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32h2/esp32-h2-devkitm-1/user_guide.html)；[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)。
- **ESP32-P4-Function-EV-Board**：Espressif Systems；[来源页](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html)；[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)。
- **BME280传感器模块正面**：Kattni Rembor / Adafruit；[来源页](https://learn.adafruit.com/assets/97111)；[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)。
- **BME280传感器模块背面**：Kattni Rembor / Adafruit；[来源页](https://learn.adafruit.com/assets/97114)；[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)。
- **BME280接口位置**：Kattni Rembor / Adafruit；[来源页](https://learn.adafruit.com/assets/97115)；[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)。
- **SSD1306单色OLED模块**：Kattni Rembor / Adafruit；[来源页](https://learn.adafruit.com/assets/93886)；[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)。
- **OLED实际点亮效果**：lady ada / Adafruit；[来源页](https://learn.adafruit.com/assets/654)；[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)。
- **MOSFET低边开关板**：Liz Clark / Adafruit；[来源页](https://learn.adafruit.com/assets/123234)；[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)。
