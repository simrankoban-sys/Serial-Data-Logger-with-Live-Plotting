# Serial Data Logger with Live Matplotlib Plot

A Python tool that reads temperature and humidity data over serial (real or simulated), logs every reading to a CSV file, and displays a live, auto-scaling dual-axis plot.

## Features
- Real-time serial data acquisition and parsing
- Live Matplotlib animation (temperature + humidity, dual subplot)
- Rolling window display (configurable size) to keep the plot readable
- CSV logging with timestamps
- Includes a **virtual sensor simulator** for testing without real hardware (via a virtual COM port pair, e.g. com0com)
- Threaded architecture — sensor simulation, serial reading, and plotting run concurrently

## Tech Stack
- Python, PySerial, Matplotlib, threading, CSV

## File Structure
| File | Purpose |
|---|---|
| `config.py` | Central config — ports, baud rate, window size, log file, sample interval |
| `virtual_sensor.py` | Simulates temperature/humidity data and writes it to a virtual serial port |
| `data_logger.py` | Reads serial data, logs to CSV, and renders the live plot |

## Setup
1. Install dependencies: `pip install pyserial matplotlib`
2. (For simulation) Set up a virtual COM port pair, e.g. [com0com](https://sourceforge.net/projects/com0com/) on Windows, and set `VIRTUAL_WRITE_PORT` / `VIRTUAL_READ_PORT` in `config.py` accordingly.
3. Set `USE_VIRTUAL = True` in `config.py` to use the simulator, or `False` with a real sensor on the configured port.
4. Run:
```bash
   python data_logger.py
```

## Output
- Live dual-panel plot: temperature (°C) and humidity (%) vs. time
- `data_log.csv` — timestamped log of every reading

## Notes
- Designed to be easily adapted to a real sensor (e.g. DHT11/DHT22 on an Arduino) by pointing `VIRTUAL_READ_PORT` to the real hardware's COM port and setting `USE_VIRTUAL = False`.
