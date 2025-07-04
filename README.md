
# ESP32 MLX90640 Temperature Alarm System
[Chinese README](README_CH.md) | [English README](README.md)

## Project Overview

This project is an intelligent fire detection system based on the ESP32-C6 microcontroller and the MLX90640 infrared temperature sensor. The system integrates TinyML machine learning algorithms, multiple detection modes, real-time data visualization, and MQTT remote monitoring functions to provide accurate and reliable fire warnings.

### Key Features

- **High-Precision Temperature Detection**: Uses MLX90640 IR sensor with 32x24 pixel resolution
- **Machine Learning Detection**: Integrated TensorFlow Lite model for intelligent fire recognition
- **Multiple Detection Modes**: Supports threshold detection, ML-based detection, time integration, and hybrid modes
- **Real-Time Display**: 1.3" TFT color screen for thermal imaging and temperature display
- **Multi-Level Alarms**: LED indicators and buzzer alerts
- **MQTT Communication**: Remote monitoring and configuration support
- **Flexible Configuration**: 5 physical buttons for local parameter adjustments
- **Host Software**: Python PyQt5 desktop application for data monitoring

## Hardware Configuration

### Main Controller

- **MCU**: ESP32-C6 DevKitM-1
- **Sensor**: MLX90640-D55 IR temperature sensor array
- **Display**: 1.3" TFT ST7789 color display
- **LEDs**: 4 indicator LEDs
- **Buzzer**: Active buzzer
- **Buttons**: 5 function buttons

### Pin Mapping

#### MLX90640 Sensor (I2C)

| MLX90640 | ESP32-C6 |
|----------|----------|
| VCC 🔴   | 3V3      |
| GND ⚫   | GND      |
| SDA ⚪   | GPIO2    |
| SCL 🟢   | GPIO3    |

#### TFT Display (SPI)

| TFT      | ESP32-C6 |
|----------|----------|
| VCC 🔴   | 3V3      |
| GND ⚫   | GND      |
| SCL 🟢   | GPIO21   |
| SDA ⚪   | GPIO19   |
| RES 🔁   | GPIO20   |
| DC 🟡    | GPIO22   |
| CS 🔷    | GPIO18   |

#### Other Peripherals

| Peripheral | Pin     |
|------------|---------|
| Buzzer     | GPIO15  |
| LED1       | GPIO10  |
| LED2       | GPIO11  |
| LED3       | GPIO12  |
| LED4       | GPIO13  |
| KEY1       | GPIO9   |
| KEY2       | GPIO4   |
| KEY3       | GPIO5   |
| KEY4       | GPIO6   |
| KEY5       | GPIO7   |

## Software Architecture

### Detection Modes

1. **Mode 1 - Traditional Threshold**: Based on max temperature threshold
2. **Mode 2 - ML Detection**: Fire recognition using TensorFlow Lite model
3. **Mode 3 - Time Integration**: Sliding window integration algorithm
4. **Mode 4 - Hybrid**: Combines ML and time integration for robust detection

### FreeRTOS Task Architecture

- **Display Task**: Handles TFT screen UI and image rendering
- **Detection Task**: Runs fire detection algorithms and peripheral control
- **Button Task**: Handles user input and parameter updates
- **MQTT Task**: Manages remote communication and config updates

### MQTT Communication Protocol

- **Data Reporting**: `/ESP32/detection_data` - Reports temperature and detection results
- **Config Receiving**: `/ESP32/config` - Receives config commands
- **Config Response**: `/ESP32/config_response` - Responds to config updates
- **Local Config Notification**: `/ESP32/config_update` - Reports local config changes

## Project Structure

```
esp32_mlx90640_temp_alert/
├── hardware/                    
│   ├── PCB.epro                
│   ├── Screen-structure.SLDDRW 
│   └── Screen-structure.SLDPRT 
├── software/
│   ├── esp32/                  
│   │   ├── project/            
│   │   │   ├── project_platformio/  
│   │   │   └── project_arduino/    
│   │   ├── component_test/     
│   │   └── tensorflow_lite_pio/ 
│   │       ├── 01.data_collection/
│   │       └── 04.run_model/      
│   └── mqtt_app/               
│       ├── main.py            
│       ├── ui/                
│       └── README.md          
├── README.md                   
├── README_CH.md               
└── .gitignore                 
```

## Installation and Usage

### Requirements

- **Development Environment**: PlatformIO IDE or Arduino IDE
- **Python Environment**: Python 3.x (for PC software)
- **Hardware**: ESP32-C6 board, MLX90640 sensor, TFT screen, etc.

### Firmware Build and Upload

1. Clone the repository
2. Use PlatformIO:
   - Open `software/esp32/project/project_platformio/main/main.ino`
   - Install required libraries
   - Select board: ESP32C6 Dev Module
   - Build and upload

3. Or use Arduino IDE:
   - Open `software/esp32/project/project_arduino/main/main.ino`
   - Install required libraries
   - Select board: ESP32C6 Dev Module
   - Build and upload

### Dependencies

- Adafruit MLX90640 - IR sensor driver
- Adafruit ST7789 - TFT display driver
- Adafruit GFX Library - Graphics library
- PubSubClient - MQTT client
- Chirale_TensorFLowLite - TensorFlow Lite support
- ArduinoJson - JSON parser

### PC Monitoring Software Setup

1. Navigate to the directory:

```
cd software/mqtt_app
```

2. Install dependencies (with uv package manager):

```
uv sync
```

3. Run the program:

```
uv run python main.py
```

## User Guide

### Button Functions

- KEY1: Toggle temperature range
- KEY2: Enter/exit settings
- KEY3: Select parameter in settings
- KEY4: Increase parameter value
- KEY5: Decrease parameter value

### Configurable Parameters

- Mode: Detection mode (1–4)
- Th1: Threshold 1 – traditional detection temperature (°C)
- Th2: Threshold 2 – ML confidence (0–1)
- Th3: Threshold 3 – time-integrated temperature (°C)
- Th4: Threshold 4 – hybrid mode confidence (0–1)
- Th5: Threshold 5 – fire frame ratio in hybrid mode (%)

### Status Indicators

- LEDs: All on when fire is detected; off in normal state
- Buzzer: Alarms on fire; short beep on key press
- TFT Display: Real-time thermal image and temperatures

## Development & Debugging

### Serial Debugging

- Baud rate: 115200
- Real-time output of temperatures and results
- System status and error logs

### Data Collection

Use code under `software/esp32/tensorflow_lite_pio/01.data_collection/` to collect training data.

### Model Training

The collected data can be used to train a custom fire detection model, convert it to TensorFlow Lite, and deploy it to the device.

## License

This project is licensed mainly under the Apache License 2.0.

- All original code and modifications: Apache License 2.0
- Third-party libraries retain their original licenses
- Some code references open-source MIT projects

See LICENSE file in the root directory for more details.

## Contributing

Feel free to submit Issues and Pull Requests to improve the project.

## Contact

If you have questions or suggestions, please open an Issue on GitHub.

> ⚠️ This system is for research and learning purposes only. Please fully test and validate it before using in real applications.
