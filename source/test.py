import json
import os

import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711

if os.path.isfile("./calibration.vlabs"):
	print("exist")
else:
	print("not")

