from easygopigo3 import GoPiGo3
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
MAX_INPUT = 255
MAX_POWER =  100 # Max motor power
DEADZONE = 15

def within_deadzone(value):
    return abs(value - NEUTRAL) < DEADZONE

def scale(value):
    """SCALE STICK VALUE [-128, +128] TO [-1, +1]"""
    return (value - NEUTRAL) / 128.0

def drive(left_power, right_power):
    #Clamp and convert to 0-100
    lp = max(min(left_power, 1), -1) * MAX_POWER
    rp = max(min(right_power, 1), -1) * MAX_POWER
    
    #Forward/backward logic
    if lp > 0:
        gpg.set_motor_power(gpg.MOTOR_LEFT, abs(lp))
        gpg.motor_fwd(gpg.MOTOR_LEFT)
    else:
        gpg.set_motor_power(gpg.MOTOR_LEFT, abs(lp))
        gpg.motor_bwd(gpg.MOTOR_LEFT)
    
    if rp > 0:
        gpg.set_motor_power(gpg.MOTOR_RIGHT, abs(rp))
        gpg.motor_fwd(gpg.MOTOR_RIGHT)
    else:
        gpg.set_motor_power(gpg.MOTOR_RIGHT, abs(rp))
        gpg.motor_bwd(gpg.MOTOR_RIGHT)
        

#Main loop
current_x = 0.0
current_y = 0.0

for event in gamepad.read_loop():

    if event.type == ecodes.EV_KEY:
        if event.code == 304 and event.value == 1: #X button
            print("STOP")
            gpg.stop()
    
    elif event.type == ecodes.EV_ABS: 
        if event.code == 1: #Left stick Y-axis
            if within_deadzone(event.value):
                current_y = 0.0 #pass # Do nothing if near center
            else:
                current_y = -scale(event.value) #Y is inverted

        elif event.code == 0: #Left Stick X-axis
            if within_deadzone(event.value):
                current_x = 0.0 #pass # Do nothing if near center
            else:
                current_x = scale(event.value)
                
        # Compute Tank Drive
        left = current_y + current_x
        right = current_y - current_x
        
        #Normalize to max 1.0
        max_mag = max(abs(left), abs(right), 1.0)
        left /= max_mag
        right /=max_mag
        
        drive(left, right)
