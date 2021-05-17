'''
Black Betty load cell library 
hardware used : 
    hx711
    Load Cell = FC23 (0-50 lbf)
'''
import json
import time
import os
import pickle
import RPi.GPIO as GPIO #import I/O interfaceq
from hx711 import HX711 #import HX711 class

class LoadCell():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  #set GPIO pind mode to BCM
        
        self.pd_sckPin=20
        self.dout_pin=21
        self.gain = 128
        self.channel = 'A'
        self.recorded_configFile_name = 'calibration.vlabs'

        ##HX711 object 
        self.cell = HX711(self.dout_pin,self.pd_sckPin,self.gain,self.channel)
        ##Status
        self.calibrated = 0
        self.calibrationPart1 = 0 
        self.loadCalibrationFile()

        self.ratio = 0
        self.knownWeight = 0 #kg

    def _closeGPIOconnection(self):
        GPIO.cleanup()
        return

    def loadCalibrationFile(self):
        ##checking for previous calibration 
        if os.path.isfile('./' + self.recorded_configFile_name):
            with open(self.recorded_configFile_name,'rb') as File:
                self.cell = pickle.load(File)   #loading calibrated HX711 object
                self.calibrated = 1 #update status
        else: 
            self.calibrated = 0 
        return


    def calibrateLoadCell_part1(self):
        err = self.cell.zero() #set zero offset/ use to tare 
        if err:
            raise Exception('Something is very wrong JORGE')
        else:
            #measure with no load --> raw data mean
            firstReading = self.cell.get_raw_data_mean()
            if firstReading:
                # print("first reading = ",firstReading)
                pass
            else:
                raise Exception('Something is very wrong JORGE')
            self.calibrationPart1 = 1 


    #place calibration object before running this function
    #known weight must be in KG
    def calibrateLoadCell_part2(self,knownWeight):
        self.knownWeight = knownWeight
        if not self.calibrationPart1:
            raise Exception('calibration part 1 has issues')
        else:
            #measure with load --> data mean (raw data - offset)
            secondReading = self.cell.get_data_mean()
            if secondReading:
                self.knownWeight = float(self.knownWeight) #KG
                self.ratio = secondReading/self.knownWeight
                self.cell.set_scale_ratio(self.ratio)
                self.calibrated = 1
                print("Calibration Finished")
            else:
                raise Exception('Something is very wrong JORGE')
        return
    
    def readForce(self):

        if self.calibrated == 1:
            force_reading_raw = self.cell.get_weight_mean(5)
            force_reading_kg = round(force_reading_raw,3)
            # print(force_reading_kg)
        else:
            force_reading_kg = 0
            print('CALIBRATION FILE NOT FOUND')
        return force_reading_kg

    def zeroCell(self):
        
        self.cell.zero()
        self.tare = 1 

        print("Calibration is succesful")

    def saveCalibrationJSON(self,ratio):

        self.calibrationJson = {
                                "ratio":None,
                                "calibration date":None
                                } 

        self.ratio = ratio 
        self.calibrationJson["ratio"] = self.ratio

        with open("./jsonTest.json", "+w") as calibrationFile:
            json.dump(self.calibrationJson,calibrationFile, indent=4)

        return
    
    def saveCalibrationPICKLE(self):
        
        with open("./calibration.vlabs", 'wb') as savedCalibration:
            pickle.dump(self.cell, savedCalibration)
            savedCalibration.flush()
            os.fsync(savedCalibration.fileno())

if __name__ == "__main__":
    LC = LoadCell()
    # LC.calibrateLoadCell_part1()
    # weight=input("input known weight in KG")
    # LC.calibrateLoadCell_part2(weight)
    # LC.saveCalibrationPICKLE()
    LC.zeroCell()
    while True:
        LC.readForce()
        time.sleep(0.1)
        