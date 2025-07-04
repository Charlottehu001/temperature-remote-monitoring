import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import numpy as np

# Function: Convert some hex value into an array for C programming
def hex_to_c_array(hex_data, var_name):
    c_str = ''
    # Create header guard
    c_str += '#ifndef ' + var_name.upper() + '_H\n'
    c_str += '#define ' + var_name.upper() + '_H\n\n'
    # Add array length at top of file
    c_str += '\nunsigned int ' + var_name + '_len = ' + str(len(hex_data)) + ';\n'
    # Declare C variable
    c_str += 'unsigned char ' + var_name + '[] = {'
    hex_array = []
    for i, val in enumerate(hex_data):
        # Construct string from hex
        hex_str = format(val, '#04x')
        # Add formatting so each line stays within 80 characters
        if (i + 1) < len(hex_data):
            hex_str += ','
        if (i + 1) % 12 == 0:
            hex_str += '\n '
        hex_array.append(hex_str)
    # Add closing brace
    c_str += '\n ' + format(' '.join(hex_array)) + '\n};\n\n'
    # Close out header guard
    c_str += '#endif //' + var_name.upper() + '_H'
    return c_str



# Define representative dataset generator (very important!)
def representative_dataset():
    for _ in range(100):
        # Simulate raw temperature values (assuming thermal camera data is 0~200)
        data = np.random.uniform(0, 200, size=(1, 24, 32, 1)).astype(np.float32)
        yield [data]


# Load saved Keras model
model = tf.keras.models.load_model('thermal_classifier_model.keras')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8
tflite_model = converter.convert()


# Save TensorFlow Lite model
with open('thermal_classifier_model.tflite', 'wb') as f:
    f.write(tflite_model)
print("📦 Saved as thermal_classifier_model.tflite")


with open('model' + '.h', 'w') as file:
    file.write(hex_to_c_array(tflite_model, 'g_model'))

# Get model input/output information
interpreter = tf.lite.Interpreter(model_path='thermal_classifier_model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Input data type:", input_details[0]['dtype'])
print("Input quantization info:", input_details[0]['quantization'])
print("Output data type:", output_details[0]['dtype'])
print("Output quantization info:", output_details[0]['quantization'])
