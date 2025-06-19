from easygopigo3 import EasyGoPiGo3
from evdev import InputDevice, categorize, ecodes,list_devices
import sys

#Find the PS4 controller and connect automatically
def find_ps4_controller():
    devices = [InputDevice(path) for path in list_devices()]
    for dev in devices:
        if "Wireless Controller" in dev.name or "Sony" in dev.name:
            print("Found Wireless Controller")
            return dev
    print("PS4 controller not found. Check connection")
    sys.exit(1)

gamepad = find_ps4_controller()

gpg = EasyGoPiGo3()

print("Ready! Use PS4-Controller to drive. \n LEFT stick to move, X button to STOP.")

NEUTRAL = 127
DEADZONE = 20

def within_deadzone(value):
    return abs(value - NEUTRAL) < DEADZONE

#Main loop
for event in gamepad.read_loop():

    if event.type == ecodes.EV_KEY:
        if event.code == 304: #X button
            if event.value == 1:
                print("STOP")
                gpg.stop()
    
    elif event.type == ecodes.EV_ABS: 
        if event.code == 1: #Left stick Y-axis
            y = event.value
            if within_deadzone(y):
                gpg.stop()
                #pass # Do nothing if near center
            elif y < NEUTRAL:
                print("Forward")
                gpg.forward()
            elif y > NEUTRAL:
                print("Backward")
                gpg.backward()

        elif event.code == 0: #Left Stick X-axis
            x = event.value
            if within_deadzone(x):
                pass # Do nothing if near center
            elif x < NEUTRAL:
                print("Left")
                gpg.left()
            elif x > NEUTRAL:
                print("Right")
                gpg.right()