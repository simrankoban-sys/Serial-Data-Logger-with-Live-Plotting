import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import datetime
import threading

from config import VIRTUAL_READ_PORT, BAUD_RATE, LOG_FILE, WINDOW_SIZE, USE_VIRTUAL


timestamps = []
temperatures = []
humidities = []


def parse_line(line):
    parts = line.split(",")
    temp = float(parts[0].split(":")[1])
    hum = float(parts[1].split(":")[1])
    return temp, hum


def read_serial(port_name):
    ser = serial.Serial(port_name, BAUD_RATE, timeout=2)
    print("Connected to", port_name)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Temperature_C", "Humidity_Pct"])

        while True:
            raw = ser.readline()
            if not raw:
                continue

            line = raw.decode("utf-8").strip()
            temp, hum = parse_line(line)

            ts = datetime.datetime.now().strftime("%H:%M:%S")

            timestamps.append(ts)
            temperatures.append(temp)
            humidities.append(hum)

            if len(timestamps) > WINDOW_SIZE:
                timestamps.pop(0)
                temperatures.pop(0)
                humidities.pop(0)

            writer.writerow([ts, temp, hum])
            f.flush()

            print(f"[{ts}]  Temp: {temp}°C   Humidity: {hum}%")


fig, (ax_temp, ax_hum) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle("Serial Data Logger")

line_temp, = ax_temp.plot([], [], color="red",  label="Temperature °C")
line_hum,  = ax_hum.plot([],  [], color="blue", label="Humidity %")

ax_temp.set_ylabel("Temperature (°C)")
ax_hum.set_ylabel("Humidity (%)")
ax_hum.set_xlabel("Time")

ax_temp.legend()
ax_hum.legend()


def animate(frame):
    if len(timestamps) < 2:
        return

    x = range(len(timestamps))

    line_temp.set_data(x, temperatures)
    line_hum.set_data(x, humidities)

    ax_temp.set_xlim(0, len(timestamps))
    ax_hum.set_xlim(0, len(timestamps))

    ax_temp.set_ylim(min(temperatures) - 2, max(temperatures) + 2)
    ax_hum.set_ylim(min(humidities) - 5, max(humidities) + 5)

    step = max(1, len(timestamps) // 8)
    ax_hum.set_xticks(range(0, len(timestamps), step))
    ax_hum.set_xticklabels([timestamps[i] for i in range(0, len(timestamps), step)], rotation=30, fontsize=7)
    ax_temp.set_xticks([])

from virtual_sensor import start_virtual_sensor
threading.Thread(target=start_virtual_sensor, daemon=True).start()

threading.Thread(target=read_serial, args=(VIRTUAL_READ_PORT,), daemon=True).start()

ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
plt.show()
