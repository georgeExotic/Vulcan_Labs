import json
import os

import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711

class 

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y)

# a Python object (dict):
x1 = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y1 = json.dumps(x1)

# the result is a JSON string:
print(y1)