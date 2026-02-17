# backlightd

A PC-controlled ambient backlighting system using Arduino and WS2811 LEDs. It captures your screen’s average color and drives an LED strip to match it for immersive lighting.

## Hardware
- Arduino Uno
- LED Strip
    - Type: WS2811
    - \# of LEDs: 50
    - Data pin in Arduino pin 5
    - Power pin in Arduino 5V
    - Ground pin in Arduino GND

## Dependencies
### Arduino Dependencies

This project uses the [FastLED](https://github.com/FastLED/FastLED) library.

To install FastLED:

1. Open the Arduino IDE.
2. Go to **Sketch → Include Library → Manage Libraries...**
3. Search for **FastLED** and click **Install**.

### Python Dependencies

You must have Python installed.

Install the required Python packages: 
```bash
pip install -r requirements.txt
```


## Installation
1. Install all dependencies above.
2. Open `firmware/backlightd_arduino.ino` in Arduino IDE.
3. Upload code to your Arduino.
4. Note COM port of your Arduino in the IDE.
5. Create `backlightd/config.json` by copying `backlightd/config.default.json`
6. In `backlightd/config.json` set `serial_port` to COM port of Arduino
6. Run `scripts/install_startup.bat`.
7. Restart your computer.
8. **backlightd** will now be running in the system tray.


## Config
Config for the Python script is located in `backlightd/config.json`.
(If this does not exist, create it by copying `backlightd/config.default.json`)

Changing COM port

Changing number of LEDs:
- Change in `firmware/backlightd_arduino.ino` and reupload to Arduino.
- Change in `backlightd/config.json`


After changing any config, restart to apply changes.