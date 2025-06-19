from easygopigo3 import EasyGoPiGo3
import time

gpg = EasyGoPiGo3()

gpg.set_motor_power(gpg.MOTOR_LEFT, 50)
gpg.set_motor_power(gpg.MOTOR_RIGHT, 50)

time.sleep(2)

gpg.stop()