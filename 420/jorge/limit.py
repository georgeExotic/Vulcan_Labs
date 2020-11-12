import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
# GPIO.setwarnings(False) # Ignore warning for now

class limitSwitch():
    def __init__(self,limitPin):
        self.limitPin = limitPin
        GPIO.setmode(GPIO.BCM)  #set GPIO pind mode to BCM
        GPIO.setup(self.limitPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.home = False
        #pin 29 GPIO 5
        #pin 31 GPIO 6
    def updateSwitch(self):
        # GPIO.input(self.limitPin) == GPIO.HIGH:
        result = GPIO.input(self.limitPin)
        print(result)
        # print(f'raw_data_mean: {self.reading}, predicted ratio = {self.reading/198}')

if __name__ == "__main__":
    while 1:
        home = limitSwitch(5)
        home.updateSwitch()
        time.sleep(0.2)
    