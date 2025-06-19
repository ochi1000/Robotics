from easygopigo3 import EasyGoPiGo3

import time

gpg = EasyGoPiGo3()
gpg.backward()
time.sleep(2)
gpg.stop()