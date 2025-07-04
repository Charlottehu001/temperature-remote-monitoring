# ESP32 MLX90640 温度报警系统
[中文版 README](README_CH.md) | [English README](README.md)
## 项目概述

本项目是一个基于ESP32-C6微控制器和MLX90640红外温度传感器的智能火灾检测系统。系统集成了TinyML机器学习算法、多种检测模式、实时数据可视化和MQTT远程监控功能，能够提供准确可靠的火灾预警。

### 主要特性

- **高精度温度检测**: 使用MLX90640红外传感器，32x24像素分辨率
-  **机器学习检测**: 集成TensorFlow Lite模型进行智能火灾识别
-  **多种检测模式**: 支持阈值检测、机器学习、时间积分和综合学习四种模式
-  **实时显示**: 1.3寸TFT彩屏显示热成像和温度数据
-  **多重报警**: LED指示灯、蜂鸣器声音报警
-  **MQTT通信**: 支持远程监控和配置管理
- **灵活配置**: 5个按键支持现场参数调节
-  **上位机软件**: Python PyQt5桌面应用程序用于数据监控

## 硬件配置

### 主控制器
- **MCU**: ESP32-C6 DevKitM-1
- **传感器**: MLX90640-D55 红外温度传感器阵列
- **显示屏**: 1.3寸 TFT ST7789 彩色显示屏
- **指示灯**: 4个LED指示灯
- **蜂鸣器**: 有源蜂鸣器
- **按键**: 5个功能按键

### 引脚连接

#### MLX90640传感器 (I2C接口)
| MLX90640 | ESP32-C6 |
|----------|----------|
| VCC 🔴   | 3V3      |
| GND ⚫   | GND      |
| SDA ⚪   | GPIO2    |
| SCL 🟢   | GPIO3    |

#### TFT显示屏 (SPI接口)
| TFT屏幕 | ESP32-C6 |
|---------|----------|
| VCC 🔴  | 3V3      |
| GND ⚫  | GND      |
| SCL 🟢  | GPIO21   |
| SDA ⚪  | GPIO19   |
| RES 🔁  | GPIO20   |
| DC 🟡   | GPIO22   |
| CS 🔷   | GPIO18   |

#### 其他外设
| 外设 | 引脚 |
|------|------|
| 蜂鸣器 | GPIO15 |
| LED1 | GPIO10 |
| LED2 | GPIO11 |
| LED3 | GPIO12 |
| LED4 | GPIO13 |
| KEY1 | GPIO9 |
| KEY2 | GPIO4 |
| KEY3 | GPIO5 |
| KEY4 | GPIO6 |
| KEY5 | GPIO7 |

## 软件架构

### 检测模式

1. **模式1 - 传统阈值检测**: 基于最高温度阈值判断
2. **模式2 - 机器学习检测**: 使用TensorFlow 
Lite模型进行智能识别
3. **模式3 - 时间积分检测**: 滑动窗口时间积分算法
4. **模式4 - 综合学习检测**: 机器学习结合时间积分
的混合模式

### FreeRTOS任务架构

- **显示任务**: 负责TFT屏幕显示和用户界面
- **检测处理任务**: 执行火灾检测算法和外设控制
- **按键处理任务**: 处理用户输入和参数调节
- **MQTT通信任务**: 处理远程通信和配置更新

### MQTT通信协议

- **数据上报**: `/ESP32/detection_data` - 温度数据和检测结果
- **配置接收**: `/ESP32/config` - 接收远程配置命令
- **配置响应**: `/ESP32/config_response` - 配置确认消息
- **配置更新**: `/ESP32/config_update` - 本地配置变更通知

## 项目结构

```
esp32_mlx90640_temp_alert/
├── hardware/                    # 硬件设计文件
│   ├── PCB.epro                # PCB设计文件
│   ├── Screen-structure.SLDDRW # 屏幕结构图
│   └── Screen-structure.SLDPRT # 屏幕结构3D模型
├── software/
│   ├── esp32/                  # ESP32固件代码
│   │   ├── project/            # 主项目代码
│   │   │   ├── project_patformio/  # PlatformIO版本
│   │   │   └── project_arduino/    # Arduino IDE版本
│   │   ├── component_test/     # 组件测试代码
│   │   └── tensorflow_lite_pio/ # TensorFlow Lite相关
│   │       ├── 01.data_collection/ # 数据收集
│   │       └── 04.run_model/      # 模型运行
│   └── mqtt_app/               # 上位机监控软件
│       ├── main.py            # 主程序
│       ├── ui/                # 用户界面
│       └── README.md          # 部署说明
├── README.md                   # 英文说明文档
├── README_CH.md               # 中文说明文档
└── .gitignore                 # Git忽略文件

```

## 安装和使用

### 环境要求

- **开发环境**: PlatformIO IDE 或 Arduino IDE
- **Python环境**: Python 3.x (用于上位机软件)
- **硬件**: ESP32-C6开发板、MLX90640传感器、TFT
显示屏等

### 固件编译和烧录

1. 克隆项目:
2. 使用PlatformIO编译 :
   - 打开 software/esp32/project/project_platformio/main/main.ino
   - 安装所需库文件
   - 选择开发板: ESP32C6 Dev Module
   - 编译并上传
3. 或使用Arduino IDE :
   - 打开 software/esp32/project/project_arduino/main/main.ino
   - 安装所需库文件
   - 选择开发板: ESP32C6 Dev Module
   - 编译并上传
### 依赖库
- Adafruit MLX90640 - MLX90640传感器驱动
- Adafruit ST7789 - TFT显示屏驱动
- Adafruit GFX Library - 图形库
- PubSubClient - MQTT客户端
- Chirale_TensorFLowLite - TensorFlow Lite支持
- ArduinoJson - JSON数据处理
### 上位机软件部署
1. 进入软件目录 :
   
   ```
   cd software/mqtt_app
   ```
2. 安装依赖 (使用uv包管理器):
   
   ```
   uv sync
   ```
3. 运行程序 :
   
   ```
   uv run python main.py
   ```
## 使用说明
### 按键功能
- KEY1 : 切换温度显示范围
- KEY2 : 进入/退出设置模式
- KEY3 : 在设置模式下选择参数项
- KEY4 : 增加参数值
- KEY5 : 减少参数值
### 设置参数

- Mode : 检测模式 (1-4)
- Th1 : 阈值1 - 传统检测温度阈值 (°C)
- Th2 : 阈值2 - 机器学习置信度阈值 (0-1)
- Th3 : 阈值3 - 时间积分温度阈值 (°C)
- Th4 : 阈值4 - 综合模式置信度阈值 (0-1)
- Th5 : 阈值5 - 综合模式火灾帧比例阈值 (%)
### 状态指示
- LED指示灯 : 火灾检测时全部点亮，正常时熄灭
- 蜂鸣器 : 火灾报警时鸣响，按键操作时短鸣
- TFT显示 : 实时热成像显示和温度数值
## 开发和调试
### 串口调试
- 波特率: 115200
- 实时输出温度数据和检测结果
- 系统状态和错误信息
### 数据收集
使用 software/esp32/tensorflow_lite_pio/01.data_collection/ 中的代码进行训练数据收集。

### 模型训练
收集的数据可用于训练自定义的火灾检测模型，然后转换为TensorFlow Lite格式部署到设备上。

## 许可证
本项目主要采用Apache License 2.0许可证。

- 所有原创代码和修改内容均采用Apache License 2.0许可证
- 第三方库和组件保持其原有许可证
- 部分代码参考了MIT许可证的开源项目
详细信息请参阅项目根目录下的LICENSE文件。

## 贡献
欢迎提交Issue和Pull Request来改进项目。

## 联系方式
如有问题或建议，请在GitHub仓库中创建Issue。

注意 : 本系统仅用于研究和学习目的，在实际应用中请根据具体环境进行充分测试和验证。
