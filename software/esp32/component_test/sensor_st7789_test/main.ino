/*********************************************************
  MLX90640-D55 + ESP32-C6 DevKitM-1 + 1.3 TFT ST7789
  Function: Serial real-time output & TFT display
  ▸ MLX90640 (I2C interface):
  │ VCC 🔴      │ → 3V3         
  │ GND ⚫      │ → GND         
  │ SDA ⚪      │ → GPIO11      
  │ SCL 🟢      │ → GPIO10   

  ▸ OLED Screen (SPI interface):
  │ VCC 🔴      │ → 3V3         
  │ GND ⚫      │ → GND         
  │ SCL 🟢      │ → GPIO21 (SPI CLK) (cannot be changed)
  │ SDA ⚪      │ → GPIO19 (SPI MOSI)(cannot be changed)
  │ RES 🔁      │ → GPIO4       
  │ DC  🟡      │ → GPIO5       
  │ CS  🔷      │ → (not connected)       
  │ BLK ⚫      │ → (not connected)  

*********************************************************/

#include <Adafruit_MLX90640.h>
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7789.h> // Hardware-specific library for ST7789
#include <SPI.h>
#include <Wire.h>

#define TFT_CS         13
#define TFT_RST        4
#define TFT_DC         5

Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);

constexpr uint8_t SDA_PIN   = 11;     // GPIO21 ← gray wire
constexpr uint8_t SCL_PIN   = 10;     // GPIO22 ← green wire
constexpr uint8_t MLX_ADDR  = 0x33;   // 7-bit address obtained from scan
constexpr uint32_t I2C_HZ   = 400000; // 100 kHz for initial testing
constexpr mlx90640_refreshrate_t FPS = MLX90640_16_HZ; // 2 fps



Adafruit_MLX90640 mlx;
float frame[32*24]; // Buffer to store entire temperature frame

// Minimum temperature range of sensor (will be displayed as blue on screen)
#define MINTEMP 20

// Maximum temperature range of sensor (will be displayed as red on screen)
#define MAXTEMP 36

//the colors we will be using
const uint16_t camColors[] = {0x480F,
0x400F,0x400F,0x400F,0x4010,0x3810,0x3810,0x3810,0x3810,0x3010,0x3010,
0x3010,0x2810,0x2810,0x2810,0x2810,0x2010,0x2010,0x2010,0x1810,0x1810,
0x1811,0x1811,0x1011,0x1011,0x1011,0x0811,0x0811,0x0811,0x0011,0x0011,
0x0011,0x0011,0x0011,0x0031,0x0031,0x0051,0x0072,0x0072,0x0092,0x00B2,
0x00B2,0x00D2,0x00F2,0x00F2,0x0112,0x0132,0x0152,0x0152,0x0172,0x0192,
0x0192,0x01B2,0x01D2,0x01F3,0x01F3,0x0213,0x0233,0x0253,0x0253,0x0273,
0x0293,0x02B3,0x02D3,0x02D3,0x02F3,0x0313,0x0333,0x0333,0x0353,0x0373,
0x0394,0x03B4,0x03D4,0x03D4,0x03F4,0x0414,0x0434,0x0454,0x0474,0x0474,
0x0494,0x04B4,0x04D4,0x04F4,0x0514,0x0534,0x0534,0x0554,0x0554,0x0574,
0x0574,0x0573,0x0573,0x0573,0x0572,0x0572,0x0572,0x0571,0x0591,0x0591,
0x0590,0x0590,0x058F,0x058F,0x058F,0x058E,0x05AE,0x05AE,0x05AD,0x05AD,
0x05AD,0x05AC,0x05AC,0x05AB,0x05CB,0x05CB,0x05CA,0x05CA,0x05CA,0x05C9,
0x05C9,0x05C8,0x05E8,0x05E8,0x05E7,0x05E7,0x05E6,0x05E6,0x05E6,0x05E5,
0x05E5,0x0604,0x0604,0x0604,0x0603,0x0603,0x0602,0x0602,0x0601,0x0621,
0x0621,0x0620,0x0620,0x0620,0x0620,0x0E20,0x0E20,0x0E40,0x1640,0x1640,
0x1E40,0x1E40,0x2640,0x2640,0x2E40,0x2E60,0x3660,0x3660,0x3E60,0x3E60,
0x3E60,0x4660,0x4660,0x4E60,0x4E80,0x5680,0x5680,0x5E80,0x5E80,0x6680,
0x6680,0x6E80,0x6EA0,0x76A0,0x76A0,0x7EA0,0x7EA0,0x86A0,0x86A0,0x8EA0,
0x8EC0,0x96C0,0x96C0,0x9EC0,0x9EC0,0xA6C0,0xAEC0,0xAEC0,0xB6E0,0xB6E0,
0xBEE0,0xBEE0,0xC6E0,0xC6E0,0xCEE0,0xCEE0,0xD6E0,0xD700,0xDF00,0xDEE0,
0xDEC0,0xDEA0,0xDE80,0xDE80,0xE660,0xE640,0xE620,0xE600,0xE5E0,0xE5C0,
0xE5A0,0xE580,0xE560,0xE540,0xE520,0xE500,0xE4E0,0xE4C0,0xE4A0,0xE480,
0xE460,0xEC40,0xEC20,0xEC00,0xEBE0,0xEBC0,0xEBA0,0xEB80,0xEB60,0xEB40,
0xEB20,0xEB00,0xEAE0,0xEAC0,0xEAA0,0xEA80,0xEA60,0xEA40,0xF220,0xF200,
0xF1E0,0xF1C0,0xF1A0,0xF180,0xF160,0xF140,0xF100,0xF0E0,0xF0C0,0xF0A0,
0xF080,0xF060,0xF040,0xF020,0xF800,};


void setup() {
  Serial.begin(115200);
  delay(50);

  // Sensor initialization 
  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(I2C_HZ);
  Serial.println(F("\nMLX90640-D55 init…"));
  if (!mlx.begin(MLX_ADDR, &Wire)) {
    Serial.println(F("ERROR: Sensor not found! (Check power / pins / address)"));
    while (true) delay(1000);
  }

  mlx.setMode(MLX90640_CHESS);          // Chess mode
  mlx.setResolution(MLX90640_ADC_18BIT); // 18 bit
  mlx.setRefreshRate(FPS);              // 2 fps
  Serial.println(F("Sensor initialization complete!"));

  // TFT initialization
  tft.init(240, 240,SPI_MODE3);           // Init ST7789 240x240
  tft.setSPISpeed(40000000);
  Serial.println(F("Initialized"));
  // Clear screen

  Serial.println(F("TFT screen initialization complete!"));

}

void loop() {
  uint32_t timestamp = millis(); // Get current timestamp
  /* Read one temperature frame */
  if (mlx.getFrame(frame) != 0) {
    Serial.println(F("Read failed, skipping this frame"));
    delay(10);
    return;
  }

  // // Calculate minimum / maximum / center pixel 
  float tMin = frame[0], tMax = frame[0];
  for (uint16_t i = 1; i < 768; ++i) {
    if (frame[i] < tMin) tMin = frame[i];
    if (frame[i] > tMax) tMax = frame[i];
  }
  float tCenter = frame[12 * 32 + 16];   // (x=16, y=12)

  // Serial output (minimum / maximum / center pixel)
  Serial.print(F("Min: "));
  Serial.print(tMin, 1);
  Serial.print(F(" °C | Max: "));
  Serial.print(tMax, 1);
  Serial.print(F(" °C | Center: "));
  Serial.println(tCenter, 1); 

  int displayPixelWidth = 8;  // Width of each pixel (adjust to appropriate value)
  int displayPixelHeight = 8; // Height of each pixel (adjust to appropriate value)

  // Traverse each pixel and draw corresponding color
  for (uint8_t h = 0; h < 24; h++) {
    for (uint8_t w = 0; w < 32; w++) {
      float t = frame[h * 32 + w]; // Get temperature value of each pixel

      t = min(t, (float)MAXTEMP); // Convert MAXTEMP to float type
      t = max(t, (float)MINTEMP); // Similarly, convert MINTEMP to float type

      uint8_t colorIndex = map(t, MINTEMP, MAXTEMP, 0, 255); // Map color index based on temperature
      colorIndex = constrain(colorIndex, 0, 255); // Ensure color index is within valid range

      // Draw each pixel (small rectangle) and map temperature-corresponding color
      tft.fillRect(w * displayPixelWidth, h * displayPixelHeight, 
                    displayPixelWidth, displayPixelHeight, 
                  camColors[colorIndex]);
    }
  }

  // Print frame time and FPS
  uint32_t frameTime = millis() - timestamp;
  Serial.print(frameTime);
  Serial.println(" milliseconds per frame");
  Serial.print(1000.0 / frameTime, 1);
  Serial.println(" FPS");
}

