#include "main.h"
#include <ArduinoJson.h>

#define MLX_ADDR 0x33
#define I2C_HZ 400000

Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);
constexpr mlx90640_refreshrate_t FPS = MLX90640_16_HZ;
Adafruit_MLX90640 mlx;

// Temperature range definition
typedef struct
{
  int minTemp;
  int maxTemp;
} TempRange;

// Temperature range groups (determines display effect)
TempRange tempRanges[] = {
    {20, 36},
    {25, 40},
    {15, 30}};
volatile int currentRangeIndex = 0; // Currently selected temperature range group

// Inference library configuration
constexpr int kTensorArenaSize = 35000; // Increase appropriately according to model
alignas(16) uint8_t tensor_arena[kTensorArenaSize];

// TFLite component pointers
const tflite::Model *model = nullptr;
tflite::MicroInterpreter *interpreter = nullptr;
TfLiteTensor *input = nullptr;
TfLiteTensor *output = nullptr;

// Configuration update flag
volatile bool configUpdatePending = false;

typedef struct
{
  bool setting;         // Whether in setting mode
  int selectedItem;     // Currently selected setting item
  int measurement_mode; // Measurement mode: 1: Threshold method, 2: Machine learning method, 3: Time integration method, 4: Comprehensive learning method
  float threshold_1;
  float threshold_2;
  float threshold_3;
  float threshold_4;
  float threshold_5;
} SystemSettings;

// Specific settings
SystemSettings sysConfig = {
    .setting = false,
    .selectedItem = 0,
    .measurement_mode = 1,
    .threshold_1 = 45,
    .threshold_2 = 0.7,
    .threshold_3 = 45,
    .threshold_4 = 0.7,
    .threshold_5 = 70};

// Key structure
typedef struct
{
  uint8_t pin;
  bool pressed;
  void (*onPressed)(); // Callback function when pressed
} Key;

void onKey1Pressed()
{
  Serial.println("KEY1 pressed!");
  currentRangeIndex++;
  if (currentRangeIndex >= (sizeof(tempRanges) / sizeof(tempRanges[0])))
    currentRangeIndex = 0;
  Serial.print("Switch to temperature range group: ");
  Serial.println(currentRangeIndex);
}

void onKey2Pressed()
{
  Serial.println("KEY2 pressed! (can add functionality)");
  // Switch setting mode
  if (sysConfig.setting)
  {
    sysConfig.setting = false;
    Serial.println("Exited setting mode");
  }
  else
  {
    sysConfig.setting = true;
    Serial.println("Entered setting mode");
  }
}

void onKey3Pressed()
{
  Serial.println("KEY3 pressed! (adjustment mode)");
  sysConfig.selectedItem++;
  if (sysConfig.selectedItem > 5)
  {
    sysConfig.selectedItem = 0;
  }
}

void onKey4Pressed()
{
  switch (sysConfig.selectedItem)
  {
  case 0:
    sysConfig.measurement_mode++;
    if (sysConfig.measurement_mode > 4)
    {
      sysConfig.measurement_mode = 1;
    }
    break;
  case 1:
    sysConfig.threshold_1 = sysConfig.threshold_1 + 10;
    if (sysConfig.threshold_1 > 150)
    {
      sysConfig.threshold_1 = 0;
    }
    break;
  case 2:
    sysConfig.threshold_2 = sysConfig.threshold_2 + 0.1;
    if (sysConfig.threshold_2 > 1)
    {
      sysConfig.threshold_2 = 0;
    }
    break;
  case 3:
    sysConfig.threshold_3 = sysConfig.threshold_3 + 10;
    if (sysConfig.threshold_3 > 100)
    {
      sysConfig.threshold_3 = 0;
    }
    break;
  case 4:
    sysConfig.threshold_4 = sysConfig.threshold_4 + 0.1;
    if (sysConfig.threshold_4 > 1)
    {
      sysConfig.threshold_4 = 0;
    }
    break;
  case 5:
    sysConfig.threshold_5 = sysConfig.threshold_5 + 10;
    if (sysConfig.threshold_5 > 100)
    {
      sysConfig.threshold_5 = 0;
    }
    break;
  default:
    break;
  }
  
  // Mark that configuration update needs to be sent (delayed to task execution)
  configUpdatePending = true;
}

void onKey5Pressed()
{
  switch (sysConfig.selectedItem)
  {
  case 0:
    sysConfig.measurement_mode--;
    if (sysConfig.measurement_mode < 1)
    {
      sysConfig.measurement_mode = 4;
    }
    break;
  case 1:
    sysConfig.threshold_1 -= 10;
    if (sysConfig.threshold_1 < 0)
    {
      sysConfig.threshold_1 = 150;
    }
    break;
  case 2:
    sysConfig.threshold_2 -= 0.1;
    if (sysConfig.threshold_2 < 0)
    {
      sysConfig.threshold_2 = 1.0;
    }
    break;
  case 3:
    sysConfig.threshold_3 -= 10;
    if (sysConfig.threshold_3 < 0)
    {
      sysConfig.threshold_3 = 100;
    }
    break;
  case 4:
    sysConfig.threshold_4 -= 0.1;
    if (sysConfig.threshold_4 < 0)
    {
      sysConfig.threshold_4 =  1.0;
    }
    break;
  case 5:
    sysConfig.threshold_5 -= 10;
    if (sysConfig.threshold_5 < 0)
    {
      sysConfig.threshold_5 = 100;
    }
    break;
  default:
    break;
  }
  
  // Mark that configuration update needs to be sent (delayed to task execution)
  configUpdatePending = true;
}

// Instantiate keys
Key keys[] = {
    {KEY1_PIN, false, onKey1Pressed},
    {KEY2_PIN, false, onKey2Pressed},
    {KEY3_PIN, false, onKey3Pressed},
    {KEY4_PIN, false, onKey4Pressed},
    {KEY5_PIN, false, onKey5Pressed}};
const uint8_t keyCount = sizeof(keys) / sizeof(keys[0]);

// Frame data structure
typedef struct
{
  float frame[32 * 24];
  float tMin;
  float tMax;
  float tCenter;
} FrameData;

// Queue handles
QueueHandle_t displayQueue;
QueueHandle_t disposalQueue;



// MQTT message processing callback function
void onMQTTMessage(char* topic, byte* payload, unsigned int length)
{
  // Convert payload to string
  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';
  
  Serial.print("Received MQTT message [Topic: ");
  Serial.print(topic);
  Serial.print("] Content: ");
  Serial.println(message);
  
  // Parse JSON message
  DynamicJsonDocument doc(1024);
  DeserializationError error = deserializeJson(doc, message);
  
  if (error) {
    Serial.print("JSON parsing failed: ");
    Serial.println(error.c_str());
    return;
  }
  
  // Update system configuration
  if (doc.containsKey("measurement_mode")) {
    int mode = doc["measurement_mode"];
    if (mode >= 1 && mode <= 4) {
      sysConfig.measurement_mode = mode;
      Serial.print("Update measurement mode: ");
      Serial.println(mode);
    }
  }
  
  if (doc.containsKey("threshold_1")) {
    float th1 = doc["threshold_1"];
    if (th1 >= 0 && th1 <= 150) {
      sysConfig.threshold_1 = th1;
      Serial.print("Update threshold 1: ");
      Serial.println(th1);
    }
  }
  
  if (doc.containsKey("threshold_2")) {
    float th2 = doc["threshold_2"];
    if (th2 >= 0 && th2 <= 1.0) {
      sysConfig.threshold_2 = th2;
      Serial.print("Update threshold 2: ");
      Serial.println(th2);
    }
  }
  
  if (doc.containsKey("threshold_3")) {
    float th3 = doc["threshold_3"];
    if (th3 >= 0 && th3 <= 100) {
      sysConfig.threshold_3 = th3;
      Serial.print("Update threshold 3: ");
      Serial.println(th3);
    }
  }
  
  if (doc.containsKey("threshold_4")) {
    float th4 = doc["threshold_4"];
    if (th4 >= 0 && th4 <= 1.0) {
      sysConfig.threshold_4 = th4;
      Serial.print("Update threshold 4: ");
      Serial.println(th4);
    }
  }
  
  if (doc.containsKey("threshold_5")) {
    float th5 = doc["threshold_5"];
    if (th5 >= 0 && th5 <= 100) {
      sysConfig.threshold_5 = th5;
      Serial.print("Update threshold 5: ");
      Serial.println(th5);
    }
  }
  
  // Send confirmation message
  char confirmMsg[256];
  snprintf(confirmMsg, sizeof(confirmMsg), 
           "{\"status\":\"ok\",\"mode\":%d,\"th1\":%.1f,\"th2\":%.2f,\"th3\":%.1f,\"th4\":%.2f,\"th5\":%.1f}",
           sysConfig.measurement_mode, sysConfig.threshold_1, sysConfig.threshold_2, 
           sysConfig.threshold_3, sysConfig.threshold_4, sysConfig.threshold_5);
  sendMQTTMessage("/ESP32/config_response", confirmMsg);
}

// -------------------- Task Definitions -------------------------

// Model inference initialization
void TFLite_init()
{
  Serial.println("Initializing TFLite Micro...");
  model = tflite::GetModel(g_model);
  if (model->version() != TFLITE_SCHEMA_VERSION)
  {
    Serial.println("Model version incompatible with library!");
    while (1)
      ;
  }

  static tflite::AllOpsResolver resolver;
  static tflite::MicroInterpreter static_interpreter(model, resolver, tensor_arena, kTensorArenaSize);
  interpreter = &static_interpreter;

  if (interpreter->AllocateTensors() != kTfLiteOk)
  {
    Serial.println("Tensor memory allocation failed!");
    while (1)
      ;
  }

  input = interpreter->input(0);
  output = interpreter->output(0);
}

// Display task
void Task_Display(void *pvParameters)
{
  (void)pvParameters;
  FrameData frameData;
  int displayPixelWidth = 8;
  int displayPixelHeight = 8;

  static bool settingLastState = false; // Whether it was in setting state last time

  while (1)
  {
    bool settingNow = sysConfig.setting;

    if (settingNow)
    {
      // If entering setting mode for the first time, clear screen + display title
      if (!settingLastState)
      {
        tft.fillScreen(ST77XX_BLACK);
        tft.setTextSize(2);
        tft.setTextColor(ST77XX_WHITE);
        tft.setCursor(10, 10);
        tft.print("== SETTINGS ==");
      }

      // Highlight color definition
      uint16_t highlightColor = ST77XX_YELLOW;
      uint16_t normalColor = ST77XX_WHITE;

      // Menu items
      String items[] = {
          "Mode: " + String(sysConfig.measurement_mode),
          "Th1: " + String(sysConfig.threshold_1, 1),
          "Th2: " + String(sysConfig.threshold_2, 1),
          "Th3: " + String(sysConfig.threshold_3, 1),
          "Th4: " + String(sysConfig.threshold_4, 1),
          "Th5: " + String(sysConfig.threshold_5, 1)};

      for (int i = 0; i < 6; i++)
      {
        int y = 40 + i * 30;
        // Only update changed content (can be further optimized)
        tft.fillRect(5, y - 2, 230, 24, ST77XX_BLACK);
        tft.setTextColor(i == sysConfig.selectedItem ? highlightColor : normalColor);
        tft.setCursor(10, y);
        tft.print(items[i]);
      }

      delay(1); // Reduce refresh tearing
    }
    else if (xQueueReceive(displayQueue, &frameData, portMAX_DELAY) == pdPASS)
    {
      float tMinSet = tempRanges[currentRangeIndex].minTemp;
      float tMaxSet = tempRanges[currentRangeIndex].maxTemp;

      for (uint8_t h = 0; h < 24; h++)
      {
        for (uint8_t w = 0; w < 32; w++)
        {
          float t = frameData.frame[h * 32 + w];
          t = min(t, tMaxSet);
          t = max(t, tMinSet);
          uint8_t colorIndex = map(t, tMinSet, tMaxSet, 0, 255);
          colorIndex = constrain(colorIndex, 0, 255);
          tft.fillRect(w * displayPixelWidth, h * displayPixelHeight,
                       displayPixelWidth, displayPixelHeight, camColors[colorIndex]);
        }
      }

      // Display temperature values
      if (!settingNow)
      {
        tft.fillRect(0, 192, 240, 48, ST77XX_BLACK);

        tft.setCursor(10, 200);
        tft.setTextColor(ST77XX_WHITE);
        tft.setTextSize(2);
        tft.print("Max:");
        tft.print(frameData.tMax, 1);

        tft.setCursor(120, 200);
        tft.print("Min:");
        tft.print(frameData.tMin, 1);

        tft.setCursor(10, 220);
        tft.print("Center: ");
        tft.print(frameData.tCenter, 1);
      }
    }

    // Update status flag
    settingLastState = settingNow;
  }
}

// Detection processing task
void Task_Disposal(void *pvParameters)
{
  (void)pvParameters;
  FrameData frameData;

  while (1)
  {
    if (xQueueReceive(disposalQueue, &frameData, portMAX_DELAY) == pdPASS)
    {
      bool fireDetected = false; // Whether fire is detected

      switch (sysConfig.measurement_mode)
      {
      case 1: // Mode 1: Traditional threshold detection
        if (frameData.tMax >= sysConfig.threshold_1)
        {
          fireDetected = true;
        }
        break;

      case 2: // Mode 2: ML inference detection
      {
        // Fill input tensor (int8)
        for (int i = 0; i < 768; i++)
        {
          float val = frameData.frame[i];
          int8_t q = (int8_t)(roundf(val / input->params.scale) + input->params.zero_point);
          input->data.int8[i] = q;
        }

        if (interpreter->Invoke() != kTfLiteOk)
        {
          Serial.println("Inference failed!");
          break;
        }

        int8_t result = output->data.int8[0];
        float score = (result - output->params.zero_point) * output->params.scale * 2;

        Serial.print("Score: ");
        Serial.println(score);

        if (score >= sysConfig.threshold_2)
        {
          fireDetected = true;
        }
        break;
      }

      case 3: // Mode 3: Sliding window integration detection
      {
        // Static variables to maintain sliding window
        static const int N = 10; // Window size
        static const int M = 6;  // Trigger condition (fire frame count)
        static bool ringBuffer[N] = {0};
        static int index = 0;
        static int fireCount = 0;

        // Determine if current frame is a "fire frame"
        bool currentIsFire = frameData.tMax >= sysConfig.threshold_3;

        // Update sliding window
        if (ringBuffer[index])
          fireCount--;                     // Subtract old value
        ringBuffer[index] = currentIsFire; // Write new value
        if (currentIsFire)
          fireCount++; // Add new value

        index = (index + 1) % N; // Circular update index

        // Check if fire alarm condition is met
        if (fireCount >= M)
        {
          fireDetected = true;
        }

        break;
      }

      case 4: // Mode 4: Machine learning with sliding window time integration
      {
        // First perform ML inference
        for (int i = 0; i < 768; i++)
        {
          float val = frameData.frame[i];
          int8_t q = (int8_t)(roundf(val / input->params.scale) + input->params.zero_point);
          input->data.int8[i] = q;
        }

        if (interpreter->Invoke() != kTfLiteOk)
        {
          Serial.println("Inference failed!");
          break;
        }

        int8_t result = output->data.int8[0];
        float score = (result - output->params.zero_point) * output->params.scale * 2;

        Serial.print("Score: ");
        Serial.println(score);

        // Static variables to maintain sliding window
        static const int N = 10; // Window size
        static bool ringBuffer[N] = {0};
        static int index = 0;
        static int fireCount = 0;

        // Determine if current frame is a "fire frame" (based on ML score)
        bool currentIsFire = score >= sysConfig.threshold_4;

        // Update sliding window
        if (ringBuffer[index])
          fireCount--;                     // Subtract old value
        ringBuffer[index] = currentIsFire; // Write new value
        if (currentIsFire)
          fireCount++; // Add new value

        index = (index + 1) % N; // Circular update index

        // Calculate fire frame ratio and compare with threshold
        float fireRatio = (float)fireCount / N * 100.0; // Calculate fire frame ratio (percentage)
        if (fireRatio >= sysConfig.threshold_5)
        {
          fireDetected = true;
        }
        break;
      }

      default:
        Serial.println("Unknown measurement mode");
        break;
      }

      // Send detection result data (send regardless of whether fire is detected)
      char dataMsg[256];
      snprintf(dataMsg, sizeof(dataMsg),
               "{\"tMin\":%.1f,\"tMax\":%.1f,\"tCenter\":%.1f,\"fireDetected\":%d}",
               frameData.tMin, frameData.tMax, frameData.tCenter, fireDetected ? 1 : 0);
      sendMQTTMessage("/ESP32/detection_data", dataMsg);

      // Control peripherals based on fireDetected
      if (fireDetected)
      {
        Serial.println("🔥 Fire detected");
        buzzer_on();
        led_on(0);
        led_on(1);
        led_on(2);
      }
      else
      {
        Serial.println("✅ No fire");
        buzzer_off();
        led_off(0);
        led_off(1);
        led_off(2);
      }
    }
  }
}

// Key scanning task
void Task_KeyProcess(void *pvParameters)
{
  (void)pvParameters;
  for (uint8_t i = 0; i < keyCount; ++i)
    pinMode(keys[i].pin, INPUT_PULLUP);

  while (1)
  {
    for (uint8_t i = 0; i < keyCount; ++i)
    {
      static bool lastState[10] = {true}; // Support up to 10 buttons
      bool currentState = digitalRead(keys[i].pin);

      // Detected button press (falling edge)
      if (lastState[i] && !currentState)
      {
        buzzer_beep(1);
        keys[i].pressed = true;
        if (keys[i].onPressed)
          keys[i].onPressed();
      }

      lastState[i] = currentState;
    }
    vTaskDelay(pdMS_TO_TICKS(10)); // Scan interval
  }
}

// MQTT message receiving task
void Task_MQTTReceive(void *pvParameters)
{
  (void)pvParameters;
  
  while (1)
  {
    mqttLoop(); // Process MQTT messages
    
    // Check if configuration update needs to be sent
    if (configUpdatePending)
    {
      configUpdatePending = false;
      
      // Send configuration update to MQTT
      char configMsg[256];
      snprintf(configMsg, sizeof(configMsg), 
               "{\"measurement_mode\":%d,\"threshold_1\":%.1f,\"threshold_2\":%.2f,\"threshold_3\":%.1f,\"threshold_4\":%.2f,\"threshold_5\":%.1f}",
               sysConfig.measurement_mode, sysConfig.threshold_1, sysConfig.threshold_2, 
               sysConfig.threshold_3, sysConfig.threshold_4, sysConfig.threshold_5);
      sendMQTTMessage("/ESP32/config_update", configMsg);
      Serial.println("Configuration uploaded via MQTT");
    }
    
    vTaskDelay(pdMS_TO_TICKS(50)); // 50ms interval
  }
}

// -------------------- System Initialization -------------------------

// Generic screen initialization progress display function
void displayInitProgress(const char* message, bool success = true)
{
  static int lineCount = 0;
  static bool screenCleared = false;
  
  // Clear screen and display title on first call
  if (!screenCleared) {
    tft.fillScreen(ST77XX_BLACK);
    tft.setTextSize(2);
    tft.setTextColor(ST77XX_WHITE);
    tft.setCursor(10, 10);
    tft.print("System Init...");
    tft.drawLine(10, 35, 230, 35, ST77XX_WHITE);
    lineCount = 0;
    screenCleared = true;
  }
  
  // Calculate display position
  int y = 50 + lineCount * 20;
  
  // If exceeding screen range, scroll display
  if (y > 220) {
    // Scroll up
    tft.fillRect(10, 50, 220, 170, ST77XX_BLACK);
    lineCount = 0;
    y = 50;
  }
  
  // Set text attributes
  tft.setTextSize(1);
  tft.setTextColor(success ? ST77XX_GREEN : ST77XX_RED);
  tft.setCursor(10, y);
  
  // Display message
  tft.print(success ? "[OK] " : "[ERR] ");
  tft.print(message);
  
  lineCount++;
  
  // Brief delay to let user see progress
  delay(10);
}

void setup()
{
  // Initialize serial port
  Serial.begin(115200);
  delay(50);

  // Initialize TFT
  tft.init(240, 240, SPI_MODE3);
  tft.setSPISpeed(40000000);
  tft.setRotation(2);
  Serial.println(F("Display initialization complete!"));
  displayInitProgress("TFT Display");

  // Initialize buzzer
  displayInitProgress("Buzzer");
  buzzer_init(BUZZER_PIN);
  buzzer_on();
  delay(100);
  buzzer_off();

  // Initialize LED
  displayInitProgress("LED Control");
  led_control_init(LED1_PIN, LED2_PIN, LED3_PIN, LED4_PIN);

  // WiFi connection
  displayInitProgress("WiFi Connection");
  connectWiFi();
  led_on(3);

  // MQTT connection
  displayInitProgress("MQTT Setup");
  connectMQTT();
  
  // Set MQTT message receive callback function
  setMQTTCallback(onMQTTMessage);
  
  // Subscribe to configuration topic
  subscribeMQTTTopic("/ESP32/config");

  // Initialize I2C
  displayInitProgress("I2C Bus");
  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(I2C_HZ);

  // Initialize infrared sensor
  displayInitProgress("MLX90640 Sensor");
  Serial.println(F("\nMLX90640-D55 init..."));
  if (!mlx.begin(MLX_ADDR, &Wire))
  {
    Serial.println(F("ERROR: Sensor not found! (Check power/pins/address)"));
    displayInitProgress("MLX90640 Sensor", false);
    while (true)
      delay(1000);
  }
  mlx.setMode(MLX90640_CHESS);
  mlx.setResolution(MLX90640_ADC_18BIT);
  mlx.setRefreshRate(FPS);
  Serial.println(F("Sensor initialization complete!"));


  // Initialize TFLite
  displayInitProgress("TensorFlow Lite");
  TFLite_init();

  // Create queues
  displayInitProgress("FreeRTOS Queues");
  displayQueue = xQueueCreate(5, sizeof(FrameData));
  disposalQueue = xQueueCreate(5, sizeof(FrameData));

  if (displayQueue == NULL || disposalQueue == NULL)
  {
    Serial.println(F("Failed to create queues!"));
    displayInitProgress("FreeRTOS Queues", false);
    while (1)
      ;
  }

  // Create tasks
  displayInitProgress("FreeRTOS Tasks");
  xTaskCreatePinnedToCore(Task_Display, "Display", 8192, NULL, 2, NULL, 0);
  xTaskCreatePinnedToCore(Task_Disposal, "Serial", 8192, NULL, 1, NULL, 0);
  xTaskCreatePinnedToCore(Task_KeyProcess, "KeyProcess", 4096, NULL, 1, NULL, 0);
  xTaskCreatePinnedToCore(Task_MQTTReceive, "MQTTReceive", 4096, NULL, 1, NULL, 1);
  
  // Initialization complete
  delay(1000);
  displayInitProgress("System Ready!");
  delay(2000); // Display for 2 seconds then enter normal operation mode
}

// -------------------- Main Loop -------------------------
void loop()
{
  static uint32_t lastTime = 0;
  uint32_t timestamp = millis();

  FrameData frameData;

  // Collect data
  if (mlx.getFrame(frameData.frame) != 0)
  {
    Serial.println(F("Read failed, skip this frame"));
    delay(10);
    return;
  }

  // Data preprocessing (calculate mean, center point)
  frameData.tMin = frameData.frame[0];
  frameData.tMax = frameData.frame[0];
  for (uint16_t i = 1; i < 768; ++i)
  {
    if (frameData.frame[i] < frameData.tMin)
      frameData.tMin = frameData.frame[i];
    if (frameData.frame[i] > frameData.tMax)
      frameData.tMax = frameData.frame[i];
  }
  frameData.tCenter = frameData.frame[12 * 32 + 16];

  // Send data frame to queues
  xQueueSend(displayQueue, &frameData, portMAX_DELAY);
  xQueueSend(disposalQueue, &frameData, portMAX_DELAY);

  uint32_t now = millis();
  uint32_t frameTime = now - lastTime;
  lastTime = now;

  Serial.print(F("Frame collection time: "));
  Serial.print(frameTime);
  Serial.println(F(" ms"));
}
