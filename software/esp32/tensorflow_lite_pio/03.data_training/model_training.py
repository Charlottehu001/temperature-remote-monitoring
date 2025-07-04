import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

import matplotlib
matplotlib.rc("font",family='Arial')



# === 1. Read and preprocess data ===
df_1 = pd.read_csv('data/mlx90640_data_1.csv')
df_0 = pd.read_csv('data/mlx90640_data_0.csv')

data = pd.concat([df_1, df_0], ignore_index=True)
data = shuffle(data, random_state=42)

labels = data['label'].values.astype(np.int32)
features = data.drop(columns=['label']).values.astype(np.float32)

# Reshape data
features = features.reshape(-1, 24, 32, 1)  

X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, random_state=24
)

# === 2. Build model ===
model = tf.keras.Sequential([
    tf.keras.Input(shape=(24, 32, 1)),
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu'),  # Reduce channel count
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.SeparableConv2D(32, (3, 3), activation='relu'),  # Separable convolution
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])


model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# === 3. Train model and save training history ===
history = model.fit(X_train, y_train,
                    epochs=10,
                    batch_size=32,
                    validation_split=0.1)

# === 4. Visualize training process ===
plt.figure(figsize=(12, 4))

# Loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss Curve')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy Curve')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()

# === 5. Save model ===
model.save('thermal_classifier_model.keras')
print("✅ Model saved as thermal_classifier_model.keras")

# === 6. Evaluate model ===
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f'🧪 Test accuracy: {test_acc:.4f}')

# === 7. Load model and make predictions (multiple samples) ===
# Randomly select 8 samples from test set
random_indices = np.random.choice(len(X_test), 8, replace=False)
sample_images = X_test[random_indices]
true_labels = y_test[random_indices]

loaded_model = tf.keras.models.load_model('thermal_classifier_model.keras')
predictions = loaded_model.predict(sample_images, verbose=0)
pred_labels = (predictions > 0.5).astype(int).flatten()

# === 8. Display thermal images ===
plt.figure(figsize=(20, 10))

for i in range(8):
    plt.subplot(2, 4, i+1)
    im = plt.imshow(sample_images[i].reshape(24, 32), cmap='coolwarm', 
                   interpolation='nearest', vmin=0, vmax=200)
    plt.colorbar(label='Normalized Temperature')
    plt.title(f'Sample {i+1}\nActual: {true_labels[i]}, Predicted: {pred_labels[i]}\n(Probability: {predictions[i][0]:.2f})')

plt.tight_layout()
plt.show()

# Print prediction statistics
print("\n=== Prediction Statistics ===")
correct = np.sum(pred_labels == true_labels)
print(f"✅ Correct predictions: {correct}/8 ({correct/8*100:.1f}%)")
