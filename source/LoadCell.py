import os
import pickle
import RPi.GPIO as GPIO #import I/O interface
from hx711 import HX711 #import HX711 class

class LoadCell():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  #set GPIO pind mode to BCM
        
        self.pd_sckPin=20
        self.dout_pin=21
        self.recorded_configFile_name = 'calibration.vlabs'

        ##HX711 object 
        self.cell = HX711(self.dout_pin,self.pd_sckPin)
        ##Status
        self.calibrated = 0

        self.checkCalibration()
        self.reading = 0
        self.initializing = 0
        self.force_reading = 0



    def checkCalibration(self):
        ##checking for previous calibration 
        if os.path.isfile('./' + self.recorded_configFile_name):
            with open(self.recorded_configFile_name,'rb') as File:
                self.cell = pickle.load(File)   #loading calibrated HX711 object
                print(self.cell)
 
    def userCalibrationPart1(self):
        self.cell = HX711(self.dout_pin,self.pd_sckPin)
        #send the user calibration message
        err = self.cell.zero()
        if err:
            raise ValueError('Tare is unsuccessful.')
        self.initializing = 1
        self.reading = self.cell.get_raw_data_mean()

        print(f'raw_data_mean: {self.reading}, predicted ratio = {self.reading/198}')

        print('getting initial data...')

        self.initializing = 0


    def userCalibrationPart2(self,knownGrams):
        self.initializing = 1
        self.reading = self.cell.get_data_mean()
        fileName = 'calibration.vlabs'
        print(f'get_data_mean: {self.reading}, predicted ratio = {self.reading/198}')

        if self.reading:
            known_weight_grams = knownGrams
            try:
                value = float(known_weight_grams)
                print(value, 'grams')
            except ValueError:
                print('Expected integer or float and I have got:',
                      known_weight_grams)

            ratio = self.reading / value  # calculate the ratio for channel A and gain 128
            print(ratio)
            self.cell.set_scale_ratio(ratio)  # set ratio for current channel
            print('Ratio is set.')
        else:
            raise ValueError(
                'Cannot calculate mean value. Try debug mode. Variable reading:',
                self.reading)
                    
        print('Saving the HX711 state to swap file on persistant memory')
        with open(fileName, 'wb') as File:
            pickle.dump(self.cell, File)
            File.flush()
            os.fsync(File.fileno())
            # you have to flush, fsynch and close the file all the time.
            # This will write the file to the drive. It is slow but safe.

        if os.path.isfile(self.recorded_configFile_name):
            with open(self.recorded_configFile_name,'rb') as File:
                self.cell = pickle.load(File)   #loading calibrated HX711 object
                self.calibrated = 1
        
        self.initializing = 0
    
    def readForce(self):
        try:
            force_reading_raw = self.cell.get_weight_mean(5)
            force_reading_kg = round(force_reading_raw,3)
        except:
            force_reading_kg = 0
            print('ERROR WHILE READING LOAD CELL')
        return force_reading_kg

    def zeroCell(self):
        self.cell.zero()
        self.tare = 1 

        print("Calibration is succesful")

LC = LoadCell()