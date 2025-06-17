from easygopigo3 import EasyGoPiGo3
from evdev import InputDevice, categorize, ecodes, list_devices

import sys

# === 1) Find PS4 controller automatically ===

def find_ps4_controller():
    devices = [InputDevice(path) for path in list_devices()]
    for dev in devices:
        if "Wireless Controller" in dev.name or "Sony" in dev.name:
            print(f"Found PS4 controller at {dev.path} ({dev.name})")
            return dev
    print("PS4 controller not found. Is it paired & connected?")
    sys.exit(1)

gamepad = find_ps4_controller()

# === 2) Setup GoPiGo ===

gpg = EasyGoPiGo3()

print("\nReady! Use LEFT stick to drive, X button to STOP.\n")

# === 3) Define neutral range ===
NEUTRAL = 127
DEADZONE = 20

def within_deadzone(value):
    return abs(value - NEUTRAL) < DEADZONE

# === 4) Main loop ===

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.code == 304:  # X button
            if event.value == 1:
                print("STOP")
                gpg.stop()

    elif event.type == ecodes.EV_ABS:
        if event.code == 1:  # Left stick Y-axis
            y = event.value
            if within_deadzone(y):
                gpg.stop()
            elif y < NEUTRAL:
                print("FORWARD")
                gpg.forward()
            elif y > NEUTRAL:
                print("BACKWARD")
                gpg.backward()

        elif event.code == 0:  # Left stick X-axis
            x = event.value
            if within_deadzone(x):
                pass  # Do nothing if near center
            elif x < NEUTRAL:
                print("LEFT")
                gpg.left()
            elif x > NEUTRAL:
                print("RIGHT")
                gpg.right()
