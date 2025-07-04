
#ifndef MAIN_H
#define MAIN_H

/*********************************************************
	MLX90640-D55 + ESP32-C6 DevKitM-1 + 1.3 TFT ST7789
	Function: Real-time serial output & TFT display
	▸ MLX90640 (I2C interface):
	│ VCC 🔴      │ → 3V3
	│ GND ⚫      │ → GND
	│ SDA ⚪      │ → GPIO11   (c3: 8)
	│ SCL 🟢      │ → GPIO10   (c3: 7)

	▸ OLED Screen (SPI interface):
	│ VCC 🔴      │ → 3V3
	│ GND ⚫      │ → GND
	│ SCL 🟢      │ → GPIO21 (SPI CLK) (c3: 4)(cannot be changed)
	│ SDA ⚪      │ → GPIO19 (SPI MOSI)(c3: 6)(cannot be changed)
	│ RES 🔁      │ → GPIO4 (c3: 12)
	│ DC  🟡      │ → GPIO5 (c3: 18)
	│ CS  🔷      │ → (not connected)
	│ BLK ⚫      │ → (not connected)

*********************************************************/
#include <Adafruit_MLX90640.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <SPI.h>
#include <Wire.h>
#include <Arduino.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "cam_colors.h"
#include "wifi_mqtt.h"
#include "led.h"
#include "buzzer.h"
#include <Chirale_TensorFlowLite.h>
#include "model.h"
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"

// TFT pin definitions
#define TFT_CS  18
#define TFT_RST 20
#define TFT_DC  22
#define TFT_SDA 19  // (cannot be changed)
#define TFT_SCL 21	// (cannot be changed)

// MLX90640 configuration
#define SDA_PIN 2
#define SCL_PIN 3

// Buzzer pin
#define BUZZER_PIN 15

// LED pin definitions
#define LED1_PIN 10
#define LED2_PIN 11
#define LED3_PIN 12
#define LED4_PIN 13

// Button pins
#define KEY1_PIN 9
#define KEY2_PIN 4
#define KEY3_PIN 5
#define KEY4_PIN 6
#define KEY5_PIN 7



#endif