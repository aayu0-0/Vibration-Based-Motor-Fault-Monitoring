import serial
import matplotlib.pyplot as plt
import time

ser = serial.Serial('COM5', 115200, timeout=1)
time.sleep(2)

x_data, y_data, z_data = [], [], []
time_data = []

plt.ion()
fig, ax = plt.subplots()

start_time = time.time()

while True:
    line = ser.readline().decode('utf-8').strip()

    if not line:
        continue

    try:
        a,x,y,z = map(float, line.split(','))

        current_time = time.time() - start_time

        x_data.append(x)
        y_data.append(y)
        z_data.append(z)
        time_data.append(current_time)

        if len(x_data) > 200:
            x_data.pop(0)
            y_data.pop(0)
            z_data.pop(0)
            time_data.pop(0)

        ax.clear()
        ax.plot(time_data, x_data, label="X")
        ax.plot(time_data, y_data, label="Y")
        ax.plot(time_data, z_data, label="Z")

        ax.legend()
        ax.set_title("Real-Time Linear Acceleration")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("m/s²")

        plt.pause(0.001)

    except:
        pass


