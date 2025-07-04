#include <Wire.h>
#include <Adafruit_MLX90640.h>
#include <Chirale_TensorFlowLite.h>
#include "model.h"
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"

constexpr uint8_t SDA_PIN = 2;
constexpr uint8_t SCL_PIN = 3;
#define MLX_ADDR 0x33

constexpr int kTensorArenaSize = 40000; // Increase appropriately based on model size
alignas(16) uint8_t tensor_arena[kTensorArenaSize];

Adafruit_MLX90640 mlx;
float frame[32 * 24];

// TFLite component pointers
const tflite::Model *model = nullptr;
tflite::MicroInterpreter *interpreter = nullptr;
TfLiteTensor *input = nullptr;
TfLiteTensor *output = nullptr;

void setup()
{
  Serial.begin(115200);
  delay(50);

  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(100000);

  Serial.println("Initializing thermal imaging sensor...");
  if (!mlx.begin(MLX_ADDR, &Wire))
  {
    Serial.println("Sensor not connected!");
    while (1)
      delay(1000);
  }
  mlx.setMode(MLX90640_CHESS);
  mlx.setResolution(MLX90640_ADC_18BIT);
  mlx.setRefreshRate(MLX90640_2_HZ);

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

  Serial.println("System initialization complete, starting inference...");
}

void loop()
{
  if (mlx.getFrame(frame) != 0)
  {
    Serial.println("Failed to read thermal image, skipping this frame");
    delay(100);
    return;
  }

  // Convert and fill input tensor (int8)
  for (int i = 0; i < 768; i++)
  {
    float val = frame[i];
    int8_t q = val / input->params.scale + input->params.zero_point;
    input->data.int8[i] = q;
  }

  // Execute inference
  if (interpreter->Invoke() != kTfLiteOk)
  {
    Serial.println("Inference failed!");
    return;
  }

  // Read output and decode
  int8_t result = output->data.int8[0];
  float score = (result - output->params.zero_point) * output->params.scale * 2;

  Serial.print("Score: ");
  Serial.print(score);

  Serial.print("Inference result: ");
  if (score >= 0.6)
  {
    Serial.println("🔥 Fire detected");
  }
  else
  {
    Serial.println("✅ No fire");
  }

  delay(500);
}
