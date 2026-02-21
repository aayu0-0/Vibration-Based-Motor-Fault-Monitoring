import serial
import csv
import time
import sys

PORT = 'COM5'
BAUD = 115200

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
except:
    print("Cannot open COM port")
    sys.exit()

time.sleep(2)

file = open("imu_data.csv", "w", newline='')
writer = csv.writer(file)

# Correct header (4 columns)
writer.writerow(["time", "ax_lin", "ay_lin", "az_lin"])

print("Logging started (CTRL+C to stop)\n")

sample_count = 0
start_time = time.time()

try:
    while True:

        line = ser.readline().decode('utf-8', errors='ignore').strip()

        if not line:
            continue

        print(line)

        parts = line.split(',')

        # FIXED: expecting 4 values
        if len(parts) == 4:
            writer.writerow(parts)
            file.flush()          # important
            sample_count += 1

except KeyboardInterrupt:
    pass

elapsed = time.time() - start_time
file.close()
ser.close()

print("\nSaved imu_data.csv")
print("Samples captured:", sample_count)
print("Average sampling rate: %.2f Hz" % (sample_count/elapsed))
