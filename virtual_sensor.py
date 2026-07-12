import serial
import time
import math
import random

from config import VIRTUAL_WRITE_PORT, BAUD_RATE, SAMPLE_INTERVAL


def simulate_temperature(t):
    base = 25.0
    wave = 5.0 * math.sin(t / 60.0)
    noise = random.uniform(-0.5, 0.5)
    return round(base + wave + noise, 1)


def simulate_humidity(t):
    base = 60.0
    wave = -8.0 * math.sin(t / 60.0)
    noise = random.uniform(-1.0, 1.0)
    return round(base + wave + noise, 1)


def run_sensor_loop():
    ser = serial.Serial(VIRTUAL_WRITE_PORT, BAUD_RATE, timeout=1)
    print("Sensor started. Writing to", VIRTUAL_WRITE_PORT)

    start_time = time.time()

    while True:
        t = time.time() - start_time
        temp = simulate_temperature(t)
        hum = simulate_humidity(t)

        message = f"T:{temp},H:{hum}\n"
        ser.write(message.encode("utf-8"))
        print("Sent:", message.strip())

        time.sleep(SAMPLE_INTERVAL)

    ser.close()


def start_virtual_sensor():
    run_sensor_loop()