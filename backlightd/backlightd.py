import os
import threading
import time
import serial
import json
from PIL import Image, ImageDraw, ImageGrab
import numpy as np
import pystray
from pystray import MenuItem as item

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.default.json")

# defaults
NUM_LEDS = 50
CHUNK_SIZE = 24
SERIAL_PORT = "COM3"
BAUD = 115200
COLOR_SMOOTHING = 0.8
SCREEN_UPDATE_INTERVAL = 0.1

# try to load config.json first, else config.default.json
for path in [CONFIG_PATH, DEFAULT_CONFIG_PATH]:
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                cfg = json.load(f)
                NUM_LEDS = cfg.get("num_leds", NUM_LEDS)
                CHUNK_SIZE = cfg.get("chunk_size", CHUNK_SIZE)
                SERIAL_PORT = cfg.get("serial_port", SERIAL_PORT)
                BAUD = cfg.get("baud", BAUD)
                COLOR_SMOOTHING = cfg.get("color_smoothing", COLOR_SMOOTHING)
                SCREEN_UPDATE_INTERVAL = cfg.get("screen_update_interval", SCREEN_UPDATE_INTERVAL)
            break
        except Exception as e:
            print(f"Failed to load {path}, using defaults: {e}")


target_r = target_g = target_b = 0.0
smooth_r = smooth_g = smooth_b = 0.0
last_screen_time = 0.0
running = True



def open_serial():
    try:
        return serial.Serial(SERIAL_PORT, BAUD, timeout=1)
    except Exception as e:
        print("Serial error:", e)
        return None

ser = open_serial()

def update_screen_average_color():
    img = ImageGrab.grab()
    img = img.resize((64, 64))
    arr = np.array(img)
    avg = arr.mean(axis=(0, 1))
    return avg[0], avg[1], avg[2]

def main():
    global last_screen_time, target_r, target_g, target_b, smooth_r, smooth_g, smooth_b
    global ser, running, led_process
    while running:
        now = time.perf_counter()
        
        # get screen color at intervals
        if now - last_screen_time > SCREEN_UPDATE_INTERVAL:
            try:
                target_r, target_g, target_b = update_screen_average_color()
                last_screen_time = now
            except Exception:
                pass

        # color smoothing
        smooth_r += (target_r - smooth_r) * (1-COLOR_SMOOTHING)
        smooth_g += (target_g - smooth_g) * (1-COLOR_SMOOTHING)
        smooth_b += (target_b - smooth_b) * (1-COLOR_SMOOTHING)

        # final color
        r = int(smooth_r)
        g = int(smooth_g)
        b = int(smooth_b)

        frame = bytes([r, g, b]) * NUM_LEDS

        # send serial
        if ser is None or not ser.is_open:
            ser = open_serial()

        if ser:
            for i in range(0, len(frame), CHUNK_SIZE):
                try:
                    ser.write(frame[i:i + CHUNK_SIZE])
                except Exception:
                    ser = None
                    break

        time.sleep(0.01)

led_process = None

def create_circle_icon(color, size=24):
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((2, 2, size-2, size-2), fill=color)
    return image

def get_status_color():
    global led_process
    if led_process:
        return (60, 179, 113) # green
    else:
        return (255, 0, 0) # red

def start_led(icon, menu_item):
    # run main loop in separate thread
    global led_process, running
    running = True
    led_process = threading.Thread(target=main, daemon=True)
    led_process.start()
    icon.icon = create_circle_icon(get_status_color())

def stop_led(icon, menu_item):
    global led_process, running
    if led_process and led_process.is_alive():
        running = False # signal thread to stop
        led_process.join(timeout=1)
    led_process = None
    icon.icon = create_circle_icon(get_status_color())

def restart_led(icon, menu_item):
    stop_led(icon, menu_item)
    start_led(icon, menu_item)

def exit_icon(icon, menu_item):
    stop_led(icon, menu_item)
    icon.stop()

menu = pystray.Menu(
    item("Start LED", start_led),
    item("Stop LED", stop_led),
    item("Exit", exit_icon)
)

icon = pystray.Icon(
    "backlightd",
    create_circle_icon(get_status_color()),
    "backlightd",
    menu
)

start_led(icon, None) # start LEDs on launch
icon.run()
