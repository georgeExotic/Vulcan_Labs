from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
# import paho.mqtt.client as paho
from ast import literal_eval #from hex to dec
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from hx711 import HX711 #import HX711 classq

import time
import math
import threading

class MQtt():
    #settup MQTT
    def __init__(self):
        self.baseTopic = "VulcanLabs/" #base topic
        self.mqtt = paho.Client()
        self.broker="broker.hivemq.com"
        self.port=1883
    def on_publish(self,client,userdata,result):
        pass

    def publish(self,value,topicName): # something.publish(value,"topicName")
        self.mqtt.on_publish = self.on_publish
        self.mqtt.connect(self.broker,self.port)
        self.value = value
        self.topic = topicName
        self.mqtt.publish((self.baseTopic + self.topic), str(self.value))

class limitSwitch:
    def __init__(self,limitPin):
        self.limitPin = limitPin
        GPIO.setmode(GPIO.BCM)  #set GPIO pind mode to BCM
        GPIO.setup(self.limitPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.updateSwitch()
    def updateSwitch(self):
        self.flag = GPIO.input(self.limitPin)

class loadCell:
    def __init__(self):
        self.pd_sck_pin = 20
        self.dout_pin = 21

class Motor:
    #Initialization of LMD57
    def __init__(self):

        #device information
        self.SERVER_HOST = "192.168.33.1"
        self.SERVER_PORT = 502
        self.deviceID = "LMDCE571C"
        self.softwareVersion = "2.4.0.6"
        self.manufactureName = "SCHNEIDER ELECTRIC MOTOR USA"
        #connection to modbus TCP steps
        self.connectionStatus = 0
        self._connectModbusClient()
        self._checkConnection()
        self.lock = threading.Lock()

        ###Velocities###
            #Jogging
        self.joggingInitialVelocity = 500
        self.joggingMaxVelocity = 1000
            #homing
        self.homingInitialVelocity = 10000
        self.homingMaxVelocity = 40000
            #running
        self.runningInitialVelocity = 1000
        self.runningMaxVelocity = 10000

        # self.runningInitialVelocity = 1000
        # self.runningMaxVelocity = 10000

        ###accelerations###
            #jogging
        self.joggingAcceleration = 50000
        self.joggingDeacceleration = 500000
            #homing
        self.homingAcceleration = 5000000
        self.homingDeacceleration = 5000000
            #running
        self.runningAcceleration = 200000
        self.runningDeacceleration = 200000


        ###hmt### motor behaivor
        self.Hmt = 2
        self.runCurrent = 100 #0x67
        self.makeUp = 2       #0xA0
        self.torqueSpeed = 10            #0xA3-0xA4
        self.torquePercentage = 100      #0xA6
        self.torqueDirection = 1         #0xA5 1CW 0CCW


        ###Performance settings###
        self.holdingCurrent = 100                        #0x29#0 - 100
        self.controlBound = 0                           #0x91#best torque performance
        self.microStep = 256.000                            #0x48



        ###hardware Settings
        self.strokeLength = 30 # mm
        self.pistonDiameter = 19.05 #mm
        self.pistonRadius = self.pistonDiameter/2
        self.leadTravel = 4.000 #mm per rev
        self.stepPerRevolution = 200.000 * self.microStep       #200*256 = 51200 steps per rev


        ###Flags
        self.topLimit = False # Top switch
        self.homeLimit = False # Home switch

        ###Hardware Flags
        self.moving = False

        ###Position
        self.absolutePosition = 0


        ##Parameters##
        self.running = False    #when in the run cycle 
        self.homed = False      #Had home and zero abosulute
        self.enable = 0             #Driver enable on/off



        self.initLayerHeight = 0    #initial Layer Height
        self.compactedLayerHeight = 0   #final Layer Height
        self.mass = 0       #keep track of mass of power
        self.modeSelected = 0   #motion mode 1 pressure mode 2
        self.layerDensity = 0   #keep track of density
        self.targetPressure = 0
        self.totalCycleStroke = 0   #to check that our total motion does not exceed our available stroke lenght
        self.numberOfLayers = 0     #user input number of layers
        self.layerNumber = 0    #keep track of layers
        self.massInput = False  #for guy to know when to ask for mass to the user
        self.massIn = False     # to know if user have input mass succesfully
        self.runCompleted = False #Set to true when run is complete, is reset in GUI
        self.cumulativeMass = 0 #addng mass each layer
        self.flushPosition = 0 #mm value at flush position after moving up 30 from bottom
        self.trigger = 0
        self.initialDensity = 0
        self.finalDensity = 0
        self.density = 0
        self.volume = 0
        self.height = 0


        ###init home limit switch###
        self.homeSwitch = limitSwitch(6)
        self.topSwitch = limitSwitch(5)


        self.setHmt()
        self.setPerformanceFeatures()
        self.setEnable(1)
        print("Congratulations Motor Initialization Complete!")

    ###function to connect to LMD57 using modbus TCP
    def _connectModbusClient(self):
        #define mosbus server and host
        self._motor = ModbusClient(host = self.SERVER_HOST, port = self.SERVER_PORT, unit_id=1, auto_open=True, debug = False)
        # self._motor.host(self.SERVER_HOST)
        # self._motor.port(self.SERVER_PORT)
        # self._motor.unit_id = 1
        # self._motor.auto_open = True
        # self._motor.debug = True
        self._motor.open()
        if self._motor.is_open():
            print("connected to " + self.SERVER_HOST + ":" + str(self.SERVER_PORT))
        else:
            print("unable to connect to "+self.SERVER_HOST+ ":" +str(self.SERVER_PORT))
        return

    ###function to check is modbus tcp connection is successful
    def _checkConnection(self):
        if not self._motor.is_open():
            if not self._motor.open():
                self.connectionStatus = 0
                self._connectModbusClient()
                return "unable to connect" #print("unable to connect to motor")
        self.connectionStatus = 1
        return self.connectionStatus

    def _hex2dec(self,hex):
        hex = str(hex)
        dec = int(literal_eval(hex))
        return dec

    def _mm2micron(self,mmValue):
        micronValue = mmValue * 1000
        return micronValue

    def _micron2mm(self,micronValue):
        mmValue = micronValue / 1000
        return mmValue

    def _mm2steps(self, displacment_mm):
        targetRevolutions = displacment_mm/self.leadTravel
        steps = int(targetRevolutions * self.stepPerRevolution)
        return steps

    def _steps2mm(self,steps):
        revs = float(steps/self.stepPerRevolution)
        displacement = float(revs * self.leadTravel)
        return displacement

    def _moving(self):
        if self._readHoldingRegs(0x4A):
            self.moving = True
        else:
            self.moving = False
        return self.moving

    ###checks the status of the switches and update flag
    def _checkLimits(self):
        self.topSwitch.updateSwitch()
        self.homeSwitch.updateSwitch()

        if self.topSwitch.flag:
            self.topLimit = True
        else:
            self.topLimit = False

        if self.homeSwitch.flag:
            self.homeLimit = True
        else:
            self.homeLimit= False
        return

    ###function to read from register of LMD57 modbus register map
    def _readHoldingRegs(self,startingAddressHex,regSize = 1):
        with self.lock:
            self._checkConnection()
            startingAddressDEC = self._hex2dec(startingAddressHex)
            reading = " "
            try:
                if regSize > 1 :
                    regSize = 2 #registers are 2 or 1 bytes
                    reg = self._motor.read_holding_registers(startingAddressDEC,regSize)
                    if reg is not None:
                        ans = utils.word_list_to_long(reg,False)
                        complement = utils.get_list_2comp(ans,32)
                        reading = complement[0]
                    else:
                        # print(f"Motor Reading {reg} as output 1")
                        reading = 0 # TEMP
                else:
                    regSize = 1
                    reg = self._motor.read_holding_registers(startingAddressDEC,regSize)
                    if reg is not None:
                        reading = reg[0]
                    else:
                        # print(f"Motor Reading {reg} as output 2")
                        pass
            except:
                self._connectModbusClient()
                print("ERROR - readHoldingRegs")
        return reading

    ###function to write to any register of LMD57 modbus register map
    def _writeHoldingRegs(self,startingAddressHEX,regSize,value):
        with self.lock:
            self._checkConnection()
            startingAddressDEC = self._hex2dec(startingAddressHEX)
            try:
                if regSize > 2:
                    complement = utils.get_2comp(value, 32)
                    word = utils.long_list_to_word([complement],False)
                    self._motor.write_multiple_registers(startingAddressDEC,word)
                else:
                    self._motor.write_multiple_registers(startingAddressDEC,[value])
            except:
                self._connectModbusClient()
                print("ERROR Modbus Reconnected.")
        return

    ###function to set the hMT technology from schneider motor
    def setHmt(self, hmt = 2):

        if hmt == 2:
            self._writeHoldingRegs(0x8E,1,self.Hmt)          #set hmt
            self._writeHoldingRegs(0x67,1,self.runCurrent)   #set run current
            self._writeHoldingRegs(0xA0,1,self.makeUp)       #set makup frequency

        elif hmt == 3:
            self._writeHoldingRegs(0x8E,1,self.Hmt)              #set hmt
            self._writeHoldingRegs(0xA3, 4,self.torqueSpeed)     #set torque speed
            self._writeHoldingRegs(0xA6, 1,self.torquePercentage)     #set torque percent
            self._writeHoldingRegs(0xA5, 1,self.torqueDirection)     #set torque direction
        self.Hmt = hmt
        return

    ###function to set enable on or off
    def setEnable(self,enable):
        self._writeHoldingRegs(0x1C, 1, enable)
        self.enable = enable
        return

    ###function to set performance settings###
    def setPerformanceFeatures(self):
        self._writeHoldingRegs(0x29,1,self.holdingCurrent)
        self._writeHoldingRegs(0x91,1,self.controlBound)
        self._writeHoldingRegs(0x48,1,self.microStep)
        return

    def setProfiles(self,motion = "homing"):
        if motion == "homing":
            self._writeHoldingRegs(0x89,4,self.homingInitialVelocity)
            self._writeHoldingRegs(0x8B,4,self.homingMaxVelocity)
            self._writeHoldingRegs(0x00,4,self.homingAcceleration)
            self._writeHoldingRegs(0x18,4,self.homingDeacceleration)
        elif motion == "jogging":
            self._writeHoldingRegs(0x89,4,self.joggingInitialVelocity)
            self._writeHoldingRegs(0x8B,4,self.joggingMaxVelocity)
            self._writeHoldingRegs(0x00,4,self.joggingAcceleration)
            self._writeHoldingRegs(0x18,4,self.joggingDeacceleration)
        elif motion == "running":
            self._writeHoldingRegs(0x89,4,self.runningInitialVelocity)
            self._writeHoldingRegs(0x8B,4,self.runningMaxVelocity)
            self._writeHoldingRegs(0x00,4,self.runningAcceleration)
            self._writeHoldingRegs(0x18,4,self.runningDeacceleration)

        print("motion profile set to = ",motion)
        return

    #function to slew axis in steps/seconds in speficied direction +/- (yes +/-!) 0 to +/- 5000000
    def slewMotor(self, slew):
        self._writeHoldingRegs(0x78,4,slew)
        return

    ###move platform +/- 
    def move(self,displacement,profile="running"):
        print('move function called')
        self.setProfiles(profile)
        steps2move = self._mm2steps(displacement)
        print("displacement", displacement, "steps2move = ",steps2move)
        self._writeHoldingRegs(0x46,4,steps2move)
        print('move function ended')
        return

    ##Stop using move relative
    def _stop(self):
        print("motor._stop running")
        self._writeHoldingRegs(0x46,4,1) # 1 step
        return

    ##home the platform 
    #check if machine is on the run cycle or on the homeFlag 
    #Zero out absolute position once hits homeLimit
    #stops with thread looking for homeLimit 
    def home(self):
        if self.running == False and self.homeLimit == False:
            self._writeHoldingRegs(0x57,4,0)
            print("motor.home running")
            self.setProfiles("homing")
            self.move(-40,"jogging")  
        return

    def flush(self):
        if self.running == False and self.topLimit == False:
            # self._writeHoldingRegs(0x57,4,0)
            print("motor.flush running")
            self.setProfiles("homing")
            self.move(40,"jogging")  
        return

    def updatePosition(self):
        try:
            pos = self._readHoldingRegs(0x57,4)
            position_reading = self._steps2mm(pos)
            self.absolutePosition = position_reading
        except:
            position_reading = 0

        return position_reading

    def run(self, LB, LA, LC):
        """
        home piston 
        (1) user notificaiton = let the uset know data collection is on / remove top cover
            user agrees to that
        wait 1 second
        move to the flush position 
            flush = True
            home = False
        set pos = 0
        wait 2 seconds 
        go down the "LAYER HEIGHT BEFORE COMPACTING" --- First motion (most important)
        (2 ) user notification = let the user know to add powder --- user inputs (mass of powder) --- 
            (2) user notificaiton to place the top thing 
        wiat 2 seconds 
        { REPEAT IF NEEDED:
        move up by DELTA "LAYER HEIGHT BEFORE COMPACTING" - "LAYER HIEGHT AFTER COMPACTING 
        if the motor stopped moving ----- move on the next layer 
            check steps moved --> calculate density per layer 
        if layer > 1 
            (4) user notification layer # is ready -- add more poder and record mass
        }                
        """
        ###First Layer

        # self.home()
        # self.home()
        # self.move(-3)
        # print("pop up (1)")
        # input("When top is removed press ENTER to proceed.")
        
        self.flush()
        # self.move(3)
        # set pos to 0
        input("ready to move down, press ENTER to proceed.")
        self.move(-LB)
        # print("pop up (2) - add powder/top thing")
        input("When powder is added and top is in place press ENTER to proceed.")
        # time.sleep(2)
        self.move(LB-LA)    #finished compression - calculate delta and density / store in database
        LC -= 1             #substracting a layer from LC (first layer)

        if LC > 0:
            for i in range(LC):
                input(f"Layer {i} is ready, press ENTER to proceed.")
                self.newLayer(LB,LA)
            print("Run Complete")


    def newLayer(self,LB,LA):
        input("#####NEW LAYER####")
        self.move(-LB)
        input("press enter when powder is added and top is in place")
        self.move(LB-LA)

    def motionRun(self):
        if self.massIn == True:
            self.cumulativeMass += self.mass
            if self.layerNumber < self.numberOfLayers:
                self._micron2mm()
                delta = self.initLayerHeightConverted - self.compactedLayerHeightConverted
                self.calculateDensity()
                self.initialDensity = self.density
                print("density: ",self.density)
                self.jogUp(delta,1)
                self.trigger = 1

    def calculateDensity(self):

        ###density = m / v
        # volume = pi * (pistonDiameter/2)^2 * h
        # h = finalabsolute - initial absolute
        #


        self.volume = 3.1415927 * (self.pistonRadius)**2 * (self.flushPosition - self.absolutePosition)
        self.density = self.cumulativeMass / self.volume



        """
        self.massInput = True
        if powder is in place
        delta = displacement2steps(self.initLayerHeight - self.compactedLayerHeight)
        self.writeHoldingRegs(0x46,4,delta)
        while _moving()
        """
        print("22222222222: ",self.mass)

    def eStop(self):
        """
        if run = 1
            write_single_register(0x001E,0) # write to enable register
            run = 0
            homing = 0 ( so jogs are off - only option is re-homing)
        else :
            nothing
        """
        print('MODBUS COMMAND: emergency stop')
        pass




if __name__ == "__main__":
    c = Motor()
    c.setProfiles("homing")
    c.move(10)

    # start_time = time.time()
    # seconds = 2
    # while True:
    #     current_time = time.time()
    #     elapsed_time = current_time - start_time
    #     c.slewMotor(80000)
    #     c._moving()
    #     print(c.moving)
    #     if elapsed_time > seconds:
    #         c.slewMotor(0)
    #         break


    # time.sleep(2)
    # c._moving()
    # print(c.moving,c.enable)

