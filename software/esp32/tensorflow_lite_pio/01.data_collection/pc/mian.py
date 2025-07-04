import serial
import csv
import time

# ============ Parameter Configuration =============
PORT = 'COM55'           # Serial port (Windows example), Linux can use '/dev/ttyUSB0'
BAUD = 115200           # Baud rate
OUTPUT_CSV = 'mlx90640_data.csv'
MAX_SAMPLES = 1024       # Maximum number of frames to collect (set to None for unlimited)
SHOW_PROGRESS = True    # Whether to print real-time information
# ================================================

def main():
    ser = serial.Serial(PORT, BAUD, timeout=2)
    time.sleep(2)  # Wait for serial port to stabilize

    print(f"Connected to {PORT}, starting data collection...")
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        sample_count = 0
        header_written = False

        while True:
            try:
                line = ser.readline().decode('utf-8').strip()
                if not line:
                    continue

                row = line.split(',')

                # Write header (first row: label,p0,p1,...)
                if not header_written and row[0] == 'label':
                    writer.writerow(row)
                    header_written = True
                    continue

                # Skip data that hasn't started outputting yet
                if not header_written:
                    continue

                # Write data row
                writer.writerow(row)
                sample_count += 1

                if SHOW_PROGRESS:
                    print(f"Collecting frame {sample_count}")

                # Check if limit is reached
                if MAX_SAMPLES and sample_count >= MAX_SAMPLES:
                    print(f"Collected {sample_count} frames, saved to {OUTPUT_CSV}")
                    break

            except KeyboardInterrupt:
                print("\nManually interrupted, saving data")
                break
            except Exception as e:
                print(f"Exception: {e}")
                continue

    ser.close()
    print("Serial port closed, data collection completed.")

if __name__ == '__main__':
    main()
