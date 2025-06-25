from gopigo3 import GoPiGo3
from evdev import InputDevice, categorize, ecodes,list_devices
import sys

# Find the PS4 controller and connect automatically
def find_ps4_controller():
    # List all input devices and search for the PS4 controller by name
    devices = [InputDevice(path) for path in list_devices()]
    for dev in devices:
        if "Wireless Controller" in dev.name or "Sony" in dev.name:
            print("Found Wireless Controller")
            return dev
    # Exit if controller is not found
    print("PS4 controller not found. Check connection")
    sys.exit(1)
 
gamepad = find_ps4_controller()  # Initialize the gamepad device

gpg = GoPiGo3()  # Initialize the GoPiGo3 robot

print("Ready! Use PS4-Controller to drive. \n LEFT stick to move, X button to STOP.")

NEUTRAL = 127  # Neutral value for joystick
MAX_POWER =  100 # Max motor power
DEADZONE = 15    # Deadzone for joystick to avoid drift

def within_deadzone(value):
    # Check if joystick value is within the deadzone
    return abs(value - NEUTRAL) < DEADZONE

def scale(value):
    """SCALE STICK VALUE [-128, +128] TO [-1, +1]"""
    # Convert joystick value to range [-1, 1]
    return (value - NEUTRAL) / 128.0

def drive(left_power, right_power):
    # Clamp and convert to 0-100
    lp = max(min(left_power, 1), -1) * MAX_POWER
    rp = max(min(right_power, 1), -1) * MAX_POWER
    
    # Apply sign for direction and set motor power
    gpg.set_motor_power(gpg.MOTOR_LEFT, lp)
    gpg.set_motor_power(gpg.MOTOR_RIGHT, rp)
    
    
# Main loop to process controller events
current_x = 0.0  # Current X-axis value from joystick
current_y = 0.0  # Current Y-axis value from joystick

for event in gamepad.read_loop():
    # Handle button press events
    if event.type == ecodes.EV_KEY:
        if event.code == 304 and event.value == 1: # X button
            print("STOP")
            gpg.set_motor_power(gpg.MOTOR_LEFT, 0)
            gpg.set_motor_power(gpg.MOTOR_RIGHT, 0)
    
    # Handle joystick movement events
    elif event.type == ecodes.EV_ABS: 
        if event.code == 1: # Left stick Y-axis
            if within_deadzone(event.value):
                current_y = 0.0 # Do nothing if near center
            else:
                current_y = scale(event.value) # Y is inverted

        elif event.code == 0: # Left Stick X-axis
            if within_deadzone(event.value):
                current_x = 0.0 # Do nothing if near center
            else:
                current_x = scale(event.value)
                
        # Compute Tank Drive values based on joystick input
        left = current_y + current_x
        right = current_y - current_x
        
        # Normalize to max 1.0 to prevent exceeding motor limits
        max_mag = max(abs(left), abs(right), 1.0)
        left /= max_mag
        right /=max_mag
        
        drive(left, right)  # Drive the robot with computed values

