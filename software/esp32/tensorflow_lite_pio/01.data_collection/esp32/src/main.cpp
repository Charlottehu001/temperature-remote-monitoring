/*********************************************************
  MLX90640-D55 Data Collection Test Program (CSV Output with Labels)
*********************************************************/
#include <Wire.h>
#include <Adafruit_MLX90640.h>

/*========== Parameter Configuration ==========*/
#define LABEL 1 // Data label: 0 = no flame, 1 = flame detected

constexpr uint8_t SDA_PIN = 2;
constexpr uint8_t SCL_PIN = 3;
constexpr uint8_t MLX_ADDR = 0x33;
constexpr uint32_t I2C_HZ = 100000;
constexpr mlx90640_refreshrate_t FPS = MLX90640_2_HZ;
/*==========================================*/

Adafruit_MLX90640 mlx;
float frame[32 * 24];
bool headerPrinted = false;

void setup()
{
  Serial.begin(115200);
  delay(50);

  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(I2C_HZ);

  Serial.println(F("\nMLX90640-D55 initializing..."));
  if (!mlx.begin(MLX_ADDR, &Wire))
  {
    Serial.println(F("ERROR: Sensor not found!"));
    while (true)
      delay(1000);
  }

  mlx.setMode(MLX90640_CHESS);
  mlx.setResolution(MLX90640_ADC_18BIT);
  mlx.setRefreshRate(FPS);

  Serial.println(F("Initialization complete, starting data collection..."));
}

void loop()
{
  if (mlx.getFrame(frame) != 0)
  {
    Serial.println(F("Read failed, skipping this frame"));
    delay(10);
    return;
  }

  // Print CSV header (only once)
  if (!headerPrinted)
  {
    Serial.print("label");
    for (int i = 0; i < 768; i++)
    {
      Serial.print(",p");
      Serial.print(i);
    }
    Serial.println();
    headerPrinted = true;
  }

  // Print one frame of data (first column is label)
  Serial.print(LABEL);
  for (int i = 0; i < 768; i++)
  {
    Serial.print(",");
    Serial.print(frame[i], 2); // Keep 2 decimal places
  }
  Serial.println();

  delay(500); // Control sampling frequency (one frame per second)
}
