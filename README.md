# 从 ESP32 看懂嵌入式世界

电路、程序、连接与可验证的小项目

24 章中文图解读本，以 ESP32-S3 为主要实验平台，从电路与代码扩展到传感器、连接、并发、存储、功耗、安全和完整项目。

## 阅读

[在线阅读](https://yzyexp.github.io/Learn-ESP32/) · [下载整本 EPUB](editions/ESP32-Atlas.epub) · [GitHub 仓库](https://github.com/YZYExp/Learn-ESP32)

- [导读与实验边界](appendices/reading-guide.md)
- [术语与实验记录](appendices/glossary.md)
- [参考资料索引](references/sources.md)

- [01 从一块板看嵌入式世界](chapters/01.md)
- [02 ESP32家族与板卡选择](chapters/02.md)
- [03 电路、供电与测量](chapters/03.md)
- [04 从源码到第一次运行](chapters/04.md)
- [05 GPIO、按钮与状态机](chapters/05.md)
- [06 模拟量、ADC与PWM](chapters/06.md)
- [07 UART、I2C与SPI](chapters/07.md)
- [08 传感器与数据可信度](chapters/08.md)
- [09 屏幕、灯光与人机交互](chapters/09.md)
- [10 电机、驱动与机械动作](chapters/10.md)
- [11 Wi-Fi与网络基础](chapters/11.md)
- [12 HTTP、MQTT与数据接口](chapters/12.md)
- [13 蓝牙与近距离连接](chapters/13.md)
- [14 Thread、Zigbee与Matter](chapters/14.md)
- [15 FreeRTOS与并发](chapters/15.md)
- [16 存储、时间与离线运行](chapters/16.md)
- [17 电池、睡眠与功耗预算](chapters/17.md)
- [18 调试、测试与故障定位](chapters/18.md)
- [19 安全、配网与OTA](chapters/19.md)
- [20 从面包板到可靠硬件](chapters/20.md)
- [21 项目一：环境记录器](chapters/21.md)
- [22 项目二：低压风扇控制器](chapters/22.md)
- [23 项目三：联网状态终端](chapters/23.md)
- [24 从ESP32走向完整系统](chapters/24.md)

## 示例程序

基础：serial_hello、button_toggle、i2c_scanner、deep_sleep。完整项目：environment_logger、fan_controller、network_terminal。均位于 `examples/`，每个 `.ino` 与目录同名。

选择实际 ESP32-S3 板卡，安装 Arduino-ESP32 3.x；项目传感器使用 Adafruit BME280 及依赖，联网屏幕使用 ArduinoJson 7、Adafruit SSD1306、Adafruit GFX。将联网终端的 SSID、密码和局域网 URL 改成实验值，不将真实凭据提交进版本管理。

示例仅做静态审查，未执行工具链编译或实板烧录。每章给出逐级验收与故障实验；不要以本书代码替代关键安全控制器。

## 构建

依赖：Python 3、Pandoc（支持 `--split-level` 的版本）。

```bash
python3 scripts/build.py
```

产物为 `build/ESP32-Atlas.epub`、合并 Markdown 和检查报告。EPUB 内含全部章内图片；不依赖外网加载插图。构建不生成网站，不需要 TeX 或浏览器。

原始精确图解保存在 `assets/images/*.svg`，正文引用 PNG 便于阅读器兼容。重新绘图另需 Inkscape：

```bash
python3 scripts/draw.py
```

该绘图命令会覆盖图解；普通构建无需执行。`book.json` 是章节标题、顺序和稳定路径的唯一清单，为后续主页发布保留结构；网页直接消费同一份主稿。

## 交付与版本

完整工程包保留 Git 历史、分章 Markdown、SVG/PNG 图解、七组示例、来源与构建脚本；仓库另提供已构建的 EPUB。首次提交仅含零字节 README，后续按结构、正文与成品验证叠加提交。远端为 `https://github.com/YZYExp/Learn-ESP32.git`，默认分支 `main`。仓库提供分章阅读与 `editions/ESP32-Atlas.epub` 阅读版；网站由独立 GitHub Actions 流程部署到 GitHub Pages。

## 网站与发布 CI

```bash
python -m pip install -r site/requirements.txt
python scripts/build_site.py --base-path /Learn-ESP32/
```

产物为 `build/site/`。网页仅依赖 Python 和 Markdown，校验全部内部链接与锚点，直接复制已交付的 EPUB；不安装或运行 Pandoc、Inkscape、Arduino 工具链。PR 只构建检查，main 推送构建并部署。首次发布需在仓库 Settings → Pages 中选择 GitHub Actions。EPUB 重新导出仍单独运行 `scripts/build.py`，不会阻塞网页更新。
