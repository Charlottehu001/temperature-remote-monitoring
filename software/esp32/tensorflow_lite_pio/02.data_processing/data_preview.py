import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os

# Load data files
BASE_DIR = os.path.dirname(__file__)
data_fire = pd.read_csv(os.path.join(BASE_DIR, 'data', 'mlx90640_data_1.csv'))
data_no_fire = pd.read_csv(os.path.join(BASE_DIR, 'data', 'mlx90640_data_0.csv'))

# Extract features (temperature data) and labels, ensure conversion to float
features_fire = data_fire.iloc[:, 1:].astype(float).values  # Temperature values for fire source data
features_no_fire = data_no_fire.iloc[:, 1:].astype(float).values  # Temperature values for no fire source data

# Calculate basic statistical information
print("Fire source data statistics:")
print(f"Sample count: {len(features_fire)}")
print(f"Average temperature: {np.mean(features_fire):.2f}°C")
print(f"Maximum temperature: {np.max(features_fire):.2f}°C")
print(f"Minimum temperature: {np.min(features_fire):.2f}°C")
print(f"Temperature standard deviation: {np.std(features_fire):.2f}°C")
print("\nNo fire source data statistics:")
print(f"Sample count: {len(features_no_fire)}")
print(f"Average temperature: {np.mean(features_no_fire):.2f}°C")
print(f"Maximum temperature: {np.max(features_no_fire):.2f}°C")
print(f"Minimum temperature: {np.min(features_no_fire):.2f}°C")
print(f"Temperature standard deviation: {np.std(features_no_fire):.2f}°C")

# Set matplotlib font for proper display
plt.rcParams['font.sans-serif'] = ['Arial']  # For proper label display
plt.rcParams['axes.unicode_minus'] = False  # For proper minus sign display

# Create a function to plot thermal images
def plot_thermal_image(data, title, subplot_pos):
    plt.subplot(subplot_pos)
    im = plt.imshow(data.reshape(24, 32), cmap='coolwarm', interpolation='nearest', vmin=0, vmax=120)
    plt.title(title)
    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax, label='Temperature (°C)')

# Create a large figure to contain random sample subplots
plt.figure(figsize=(20, 10))

# Randomly select 4 sample indices
random_indices = np.random.choice(len(features_fire), 4, replace=False)

# Thermal image comparison (random samples)
for i, idx in enumerate(random_indices):
    # Fire source sample
    plt.subplot(2, 4, i+1)
    im = plt.imshow(features_fire[idx].reshape(24, 32), cmap='coolwarm', interpolation='nearest', vmin=0, vmax=120)
    plt.title(f'Fire Source Sample {idx+1}')
    plt.colorbar(label='Temperature (°C)')
    
    # No fire source sample
    plt.subplot(2, 4, i+5)
    im = plt.imshow(features_no_fire[idx].reshape(24, 32), cmap='coolwarm', interpolation='nearest', vmin=0, vmax=120)
    plt.title(f'No Fire Source Sample {idx+1}')
    plt.colorbar(label='Temperature (°C)')

plt.tight_layout()
plt.show()

# Display average thermal images in a new figure
plt.figure(figsize=(15, 5))
# Fire source average thermal image
plot_thermal_image(np.mean(features_fire, axis=0), 'Fire Source Average Thermal Image', 121)
# No fire source average thermal image
plot_thermal_image(np.mean(features_no_fire, axis=0), 'No Fire Source Average Thermal Image', 122)
plt.tight_layout()
plt.show()

