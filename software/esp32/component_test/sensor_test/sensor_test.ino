/*********************************************************
  Sensor  MLX90640-D55
  MCU     ESP32-C6 DevKitM-1
  Function    Serial real-time output Min / Max / Center temperature

  Wiring (confirmed) ────────────────────────────
      MLX VCC (red)  → Breadboard red rail (+) → Jumper → ESP32 3V3
      MLX GND (black)  → Breadboard blue rail (–) → Jumper → ESP32 GND
      MLX SDA (gray)  → ESP32 GPIO21
      MLX SCL (green)  → ESP32 GPIO22
*********************************************************/
#include <Wire.h>
#include <Adafruit_MLX90640.h>

/*========== Parameters determined by wiring ==========*/
constexpr uint8_t SDA_PIN   = 11;     // GPIO21 ← gray wire
constexpr uint8_t SCL_PIN   = 10;     // GPIO22 ← green wire
constexpr uint8_t MLX_ADDR  = 0x33;   // 7-bit address obtained from scan
constexpr uint32_t I2C_HZ   = 100000; // 100 kHz for initial testing
constexpr mlx90640_refreshrate_t FPS = MLX90640_2_HZ; // 2 fps
/*======================================*/

Adafruit_MLX90640 mlx;
float frame[32 * 24];                 // 768 pixel buffer

void setup() {
  Serial.begin(115200);
  delay(50);

  /*--- I²C initialization ---*/
  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(I2C_HZ);

  /*--- Sensor initialization ---*/
  Serial.println(F("\nMLX90640-D55 init…"));
  if (!mlx.begin(MLX_ADDR, &Wire)) {
    Serial.println(F("ERROR: Sensor not found! (Check power / pins / address)"));
    while (true) delay(1000);
  }

  mlx.setMode(MLX90640_CHESS);          // Chess mode
  mlx.setResolution(MLX90640_ADC_18BIT); // 18 bit
  mlx.setRefreshRate(FPS);              // 2 fps

  Serial.println(F("Initialization complete, starting acquisition…"));
}

void loop() {
  /* Read one temperature frame */
  if (mlx.getFrame(frame) != 0) {
    Serial.println(F("Read failed, skipping this frame"));
    delay(10);
    return;
  }

  /* Calculate minimum / maximum / center pixel */
  float tMin = frame[0], tMax = frame[0];
  for (uint16_t i = 1; i < 768; ++i) {
    if (frame[i] < tMin) tMin = frame[i];
    if (frame[i] > tMax) tMax = frame[i];
  }
  float tCenter = frame[12 * 32 + 16];   // (x=16, y=12)

  /* Serial output */
  Serial.print(F("Min: "));
  Serial.print(tMin, 1);
  Serial.print(F(" °C | Max: "));
  Serial.print(tMax, 1);
  Serial.print(F(" °C | Center: "));
  Serial.println(tCenter, 1); 
}