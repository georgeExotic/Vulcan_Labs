from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
# import paho.mqtt.client as paho
from ast import literal_eval #from hex to dec
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

import time
import math

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

        ###Velocities###
            #Jogging
        self.joggingInitialVelocity = 1000
        self.joggingMaxVelocity = 100000
            #homing
        self.homingInitialVelocity = 1000
        self.homingMaxVelocity = 60000
            #running
        self.runningInitialVelocity = 1000
        self.runningMaxVelocity = 20000

        ###accelerations###
            #jogging
        self.joggingAcceleration = 500000
        self.joggingDeacceleration = 500000
            #homing
        self.homingAcceleration = 300000
        self.homingDeacceleration = 300000
            #running
        self.runningAcceleration = 300000
        self.runningDeacceleration = 300000


        ###hmt### motor behaivor
        self.Hmt = 2                                    


        ###Performance settings###
        self.holdingCurrent = 100                        #0x29#0 - 100
        self.controlBound = 0                           #0x91#best torque performance
        self.microStep = 256                            #0x48



        ###hardware Settings
        self.strokeLength = 30 # mm
        self.pistonDiameter = 19.05 #mm
        self.pistonRadius = self.pistonDiameter/2
        self.leadTravel = 4 #mm per rev
        self.stepPerRevolution = 200 * self.microStep       #200*256 = 51200 steps per rev


        ###Flags
        self.topLimit = False # Top switch
        self.homeLimit = False # Home switch



        self.homed = False  # has been homed Default False
        self.moving = False #shaft moving
        self.homeFlag = False
        self.topFlag = False

        ###Homing
        self.absolutePosition = 0


        ##Parameters##

        self.initLayerHeight = 0    #initial Layer Height
        self.compactedLayerHeight = 0   #final Layer Height
        self.mass = 0       #keep track of mass of power
        self.modeSelected = 0   #motion mode 1 pressure mode 2
        self.layerDensity = 0   #keep track of density
        self.targetPressure = 0
        self.totalCycleStroke = 0   #to check that our total motion does not exceed our available stroke lenght
        self.numberOfLayers = 0     #user input number of layers
        self.layerNumber = 0    #keep track of layers
        self.running = False    #
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
        self._motor = ModbusClient()
        self._motor.host(self.SERVER_HOST)
        self._motor.port(self.SERVER_PORT)
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
                return "unable to connect" #print("unable to connect to motor")
        self.connectionStatus = 1
        return "connected!"

    ###function to convert any hex number into decimal
    def _hex2dec(self,hex):
        hex = str(hex)
        dec = int(literal_eval(hex))
        return dec

    ##converting the user input to micron o leaving in mm depending on drop down choice [0] = mm [1] = mm/1000
    def _micron2mm(self):
        if self.initLayerHeight[1] == 0:
            self.initLayerHeightConverted = self.initLayerHeight[0]
        elif self.initLayerHeight[1] == 1:
            self.initLayerHeightConverted = self.initLayerHeight[0]/1000

        if self.compactedLayerHeight[1] == 0:
            self.compactedLayerHeightConverted = self.compactedLayerHeight[0]
        elif self.initLayerHeight[1] == 1:
            self.compactedLayerHeightConverted = self.compactedLayerHeight[0]/1000

    ###function to read if the shaft is moving 
    def _moving(self):
        temp = self.readHoldingRegs(0x4A,2)
        if temp[0] == 0 :
            self.moving = False
        elif temp[0] == 1:
            self.moving = True
        return


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
    def readHoldingRegs(self,startingAddressHex,regSize = 1):                             
        startingAddressDEC = self._hex2dec(startingAddressHex)                            
        reading = " "
        if regSize > 1 : 
            regSize = 2 #registers are 2 or 1 bytes
            reg = self._motor.read_holding_registers(startingAddressDEC,regSize)
            if reg is not None:
                ans = utils.word_list_to_long(reg,False)
                complement = utils.get_list_2comp(ans,32)
                reading = complement[0]
            else: 
                print("Motor Reading NONE as output")
                pass                
        else:                                                                            
            regSize = 1                                                                  
            reg = self._motor.read_holding_registers(startingAddressDEC,regSize)
            if reg is not None:
                reading = reg[0]
            else:
                print("Motor Reading NONE as output")
        return reading

    ###function to write to any register of LMD57 modbus register map
    def writeHoldingRegs(self,startingAddressHEX,regSize,value):                         
        startingAddressDEC = self._hex2dec(startingAddressHEX)                           
        if regSize > 2:                                                                  
            complement = utils.get_2comp(value, 32)
            word = utils.long_list_to_word([complement],False)
            self._motor.write_multiple_registers(startingAddressDEC,word)                                                                                      
        else:                                                                           
             self._motor.write_multiple_registers(startingAddressDEC,[value])   
        return


    #function to slew axis in steps/seconds in speficied direction +/- (yes +/-!) 0 to +/- 5000000
    def slewMotor(self, slew):
        self.writeHoldingRegs(0x78,4,slew)
        return

    ###function to set the hMT technology from schneider motor
    def setHmt(self, hmt = 2, direction = "cw"):

        self.Hmt = hmt
        #will not use 0 or 1
        #hmt 2
        self.runCurrent = 100           #0x67
        self.makeUp = 2                 #0xA0

        #hmt 3
        self.torqueSpeed = 10            #0xA3-0xA4
        self.torquePercentage = 100      #0xA6
        self.torqueDirection = 1         #0xA5 1CW 0CCW

        #set up shaft rotation direction ## need to change it to up and down
        if direction == "cw":
            self.torqueDirection = 1
        else:
            self.torqueDirection = 0

        ###Hmt 2### variable current mode
        if self.Hmt == 2:
            self.writeHoldingRegs(0x8E,1,self.Hmt)      #set hmt

            self.writeHoldingRegs(0x67,1,self.runCurrent)   #set run current
            self.writeHoldingRegs(0xA0,1,self.makeUp)       #set makup frequency

            # print("Variable current mode is activated ... hmt mode = ",self.readHoldingRegs(0x8E,1))
            # print("Run current = ", self.readHoldingRegs(0x67,1))
            # print("make Up frequency mode = ", self.readHoldingRegs(0xA0,1))

        ###Hmt 3### Torque mode
        elif self.Hmt == 3:
            self.writeHoldingRegs(0x8E,1,self.Hmt)       #set hmt

            self.writeHoldingRegs(0xA3, 4,self.torqueSpeed)     #set torque speed
            self.writeHoldingRegs(0xA6, 1,self.torquePercentage)     #set torque percent
            self.writeHoldingRegs(0xA5, 1,self.torqueDirection)     #set torque direction

            # print("Torque mode is activated ... hmt mode = ", self.readHoldingRegs(0x8E,1))
            # print("torque speed is = ", self.readHoldingRegs(0xA3,4))
            # print("torque percentage is = ", self.readHoldingRegs(0xA6,1))
            # print("torque direction is = ", self.readHoldingRegs(0xA5,1))

        return

    ###function to set enable on or off
    def setEnable(self,enable=1):
        self.writeHoldingRegs(0x1C, 1, enable)
        self.enable = self.readHoldingRegs(0x1C,1)
        return

    ###function to set performance settings###
    def setPerformanceFeatures(self):
        self.writeHoldingRegs(0x29,1,self.holdingCurrent)
        self.writeHoldingRegs(0x91,1,self.controlBound)
        self.writeHoldingRegs(0x48,1,self.microStep)

        # print("holding current = ",self.readHoldingRegs(0x29,1))
        # print("control bound = ",self.readHoldingRegs(0x91,1))
        # print("microstep = ",self.readHoldingRegs(0x48,1))
        return

    ###function to convert linar displacement in mm to amount of steps
    def displacement2steps(self, displacment_mm):
        targetRevolutions = displacment_mm/self.leadTravel
        steps = int(targetRevolutions * self.stepPerRevolution)
        return steps

    ###convert step to linear motion
    def steps2displacement(self,steps):
        revs = steps/self.stepPerRevolution
        displacement = revs * self.leadTravel
        return displacement





    ###This function takes STEPS,  writes to register on motor to make it move
    def jogUp(self,steps2Jog):
        self.writeHoldingRegs(0x46,4,steps2Jog)
        return

    ##takes user jog input and command motion for jog up button // only mm!!!! // anydistance == 0 for only button and == 1 when user input is ready
    def buttonUp(self,userChoice_mm,anyDistance = 0):
        if anyDistance == 0 :
            if userChoice_mm == 0:
                distance2move = 1
            elif userChoice_mm == 1:
                distance2move = 5
            elif userChoice_mm == 2:
                distance2move = 10
        elif anyDistance == 1:
            distance2move = userChoice_mm

        if self.homed == True:
            steps2jog = self.displacement2steps(distance2move)
            self.setProfiles("jogging")
            self.home = False
            print(f'topflag: {self.topFlag}')
            if self.topFlag == False:
                self.jogUp(steps2jog)
        elif self.homed == False:
            print("please home")





    ##function to jogUp
    def jogUpOld(self,displacementChoice, anyRun = 0):

        if self.running == False or self.running == True:
            if anyRun == 0:
            #displacement choice from GUI
                if displacementChoice == 0:
                    displacement = 1
                elif displacementChoice == 1:
                    displacement = 5
                elif displacementChoice == 2:
                    displacement = 10 # 30.16 for flush from home
                elif displacementChoice > 2:
                    displacement = displacementChoice
            elif anyRun == 1:
                displacement = displacementChoice



            self.homed = True
            if self.homed == True:
                initialStepPosition = self.readHoldingRegs(0x57,4)
                print("initstepPosition:",initialStepPosition)

                steps2Jog = self.displacement2steps(displacement)
                self.setProfiles("jogging")
                # self._checkLimits()

                if self.topFlag == False:
                    self.writeHoldingRegs(0x46,4,steps2Jog) #already started moving
                    self._moving()
                    self.home = False
                    while self.topFlag == False and self.moving == True:
                        # self._checkLimits()
                        self._moving()
                    if self.topFlag == True:
                        # self.writeHoldingRegs(0x1C,1,0)
                        self.setEnable(0)
                        self.home = False

                finalStepPosition = self.readHoldingRegs(0x57,4)
                # print("finalstepPosition:",finalStepPosition)
                DeltaStepsPosition = finalStepPosition[0] - initialStepPosition[0]
                # print(DeltaStepsPosition)
                self.absolutePosition = self.absolutePosition + self.steps2displacement(DeltaStepsPosition)
                # print(self.absolutePosition)

            elif self.homed == False:
                print("please home")

            self.home = False
            self.setEnable(1)
            print("driver enable again")
            return
        else:
            print("cannot perform function while running")

    def jogDown(self,displacementChoice,anyRun = 0):
        print(self.running)

        if self.running == False or self.running == True:
            self.setProfiles("jogging")
            initialStepPosition = self.readHoldingRegs(0x57,4)
            homeCheck = 0

            if anyRun == 0:
                if displacementChoice == 0:
                    displacement = 1
                elif displacementChoice == 1:
                    displacement = 5
                elif displacementChoice == 2:
                    displacement = 10
                elif displacementChoice > 2:
                    displacement = displacementChoice
            if anyRun == 1:
                displacement = displacementChoice

            steps2Jog = self.displacement2steps(displacement)

            # self._checkLimits()

            if self.homeFlag == True:

                self.absolutePosition = 0

            else:

                currentStepPos = initialStepPosition[0] + steps2Jog
                self.writeHoldingRegs(0x57,4,currentStepPos) #overwriting motor absolute
                self.writeHoldingRegs(0x43,4,(currentStepPos-steps2Jog)) #making it move

                self._moving()

                while self.homeFlag == False and self.moving == True:
                    # self._checkLimits()
                    self._moving()
                    self.home = False

                    if self.homeFlag == True:
                        homeCheck = 1   #to check if we need to substract or not
                        self.setEnable(0)
                        self.setEnable(1)
                        self.absolutePosition = 0
                        self.writeHoldingRegs(0x57,4,self.absolutePosition)
                        self.home = True

                #if we havent home then substract to have an accurate absolute postion
                if homeCheck == 0:

                    finalStepPosition = initialStepPosition[0] - steps2Jog
                    delta = finalStepPosition - initialStepPosition[0]
                    self.absolutePosition = self.absolutePosition + self.steps2displacement(delta)

                else:

                    self.absolutePosition = 0

                homeCheck = 0

            print("Jogging DOWN!!")
            return
        else:
            print("cannot perform function while running")


    def Home(self):
        if self.running == False or self.running == True:
            self.homeSwitch.updateSwitch()
            ok = False
            print('homeswitch: ',self.homeSwitch.flag)
            if self.homeSwitch.flag == 1:
                ok = False
            elif self.homeSwitch.flag == 0:
                ok = True
            print(f'homeFlag={self.homeSwitch.flag},ok={ok},self.home={self.home}')

            if self.home == False and ok == True:
                print("homing starting in 3 seconds")
                # self.countdown()
                self.setProfiles("homing")
                steps2Jog = self.displacement2steps(40)
                self.writeHoldingRegs(0x57,4,steps2Jog) #overwriting the absolute position
                self.writeHoldingRegs(0x43,4,0)
                self.homing = True      # true during homing
                while self.home == False:
                    self.homeSwitch.updateSwitch()
                    if self.homeSwitch.flag == 1:
                        # self.writeHoldingRegs(0x1C,1,0)
                        self.setEnable(0)
                        self.absolutePosition = 0
                        self.home = True
                        self.homed = True
                        self.homing = False      # true during homing
                        print("Homing Completed")
                        break
                # self.writeHoldingRegs(0x1C,1,1)
                self.setEnable(1)
                self.writeHoldingRegs(0x57,4,0)
                time.sleep(0.2)
            elif self.home == True or ok == False:
                self.absolutePosition = 0
                self.writeHoldingRegs(0x57,4,0)
                self.home = True
                self.homed = True
                print("already homed")
                print("setting absolute position to 0")
                pass
            return
        else:
            print("cannot perform function while running")

    def tempHome(self):
        if self.home == True or self.running == True or self.homeFlag == True:
            print("already homed")
        else:
            self.setProfiles("homing")
            steps2Jog = self.displacement2steps(40)
            self.writeHoldingRegs(0x57,4,steps2Jog)
            self.writeHoldingRegs(0x43,4,0)


    def updatePosition(self):
        try:
            pos = self.readHoldingRegs(0x57,4)
            position_reading = self.steps2displacement(pos[0])
        except:
            print("ERROR while reading position")
            position_reading = 0

        return position_reading

    def setProfiles(self,motion = "homing"):
        if motion == "homing":
            self.writeHoldingRegs(0x89,4,self.homingInitialVelocity)
            self.writeHoldingRegs(0x8B,4,self.homingMaxVelocity)
            self.writeHoldingRegs(0x00,4,self.homingAcceleration)
            self.writeHoldingRegs(0x18,4,self.homingDeacceleration)
        elif motion == "jogging":
            self.writeHoldingRegs(0x89,4,self.joggingInitialVelocity)
            self.writeHoldingRegs(0x8B,4,self.joggingMaxVelocity)
            self.writeHoldingRegs(0x00,4,self.joggingAcceleration)
            self.writeHoldingRegs(0x18,4,self.joggingDeacceleration)
        elif motion == "running":
            self.writeHoldingRegs(0x89,4,self.runningInitialVelocity)
            self.writeHoldingRegs(0x8B,4,self.runningMaxVelocity)
            self.writeHoldingRegs(0x00,4,self.runningAcceleration)
            self.writeHoldingRegs(0x18,4,self.runningDeacceleration)

        print("motion profile set to = ",motion)
        return

    def cleanUp(self):
        self.jogUp(35)
        self.top = True
        return

    def countdown(self):
        print("3...")
        time.sleep(1)
        print("2..")
        time.sleep(1)
        print("1..")
        time.sleep(1)
        return

    def run(self):

        self.cumulativeMass = 0
        self.density = 0
        self.volume = 0
        self._micron2mm()
        self.totalCycleStroke = self.initLayerHeightConverted * self.numberOfLayers

        if self.totalCycleStroke <= self.strokeLength:

            print("its gonna home, are you ready for it Miao?")
            self.Home()

            if self.home == True:
                self.jogUp(30.16,1) # jog to flush poition
                self.flushPosition = self.absolutePosition
                self.jogDownLayerHeight()
                self.running = True

            if self.modeSelected == 0:
                print("no mode selected")
            elif self.modeSelected == 1:
                print("Motion Limiting")
                self.newLayerMotionRun()
            elif self.modeSelected == 2:
                print("Pressure Limiting")
                self.newLayerMotionRun()
                print("havent done this one! Come later")

        elif self.totalCycleStroke > self.totalCycleStroke:
            print("you cant do that, you dont enough stroke")

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

    def motionRun2(self):
        print("done")
        self.calculateDensity()
        self.finalDensity = self.density
        print("density: ",self.density)
        self.massIn = False
        self.layerNumber += 1
        print("layer num: ",self.layerNumber)
        self.jogDownLayerHeight()
        print("abs: ",self.absolutePosition)
        if self.layerNumber == self.numberOfLayers:
            self.layerNumber = 0
            self.runCompleted = True
            print("hello")
            pass
        # elif self.layerNumber == self.numberOfLayers:
        #     self.runCompleted = True
        else:
            self.newLayerMotionRun()
            print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
            # self.runCompleted = True
            print("run complete")

    def newLayerMotionRun(self):
        self.massInput = True

    def pressureRun(self):
        if self.massIn == True:
            self.cumulativeMass += self.mass
            if self.layerNumber < self.numberOfLayers:
                self._micron2mm()
                self.calculateDensity()
                self.initialDensity = self.density
                print("density: ",self.density)
                self.jogUp(30,1) #########
                print("done")
                self.calculateDensity()
                self.finalDensity = self.density
                print("density: ",self.density)
                self.massIn = False
                self.layerNumber += 1
                print("layer num: ",self.layerNumber)
                self.jogDownLayerHeight()
                print("abs: ",self.absolutePosition)
                if self.layerNumber == self.numberOfLayers:
                    self.layerNumber = 0
                    self.runCompleted = True
                else:
                    self.newLayerMotionRun()
            else:
                print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
                # self.runCompleted = True
                print("run complete")

        """ if check layer count """
        # self.newLayerMotionRun()

    def jogDownLayerHeight(self):
        self.jogDown(self.initLayerHeightConverted,1) #jog down for a layer height

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


    def stopRun(self):

        """
        stop sending motion commands / cancel run
        if run = 1
            run , homing = 0
        """
        self._motor.write_multiple_registers(70,[0,0])
        print("stopped")
        pass

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
    
    
    
    # start_time = time.time()
    # seconds = 1
    # while True:
    #     current_time = time.time()
    #     elapsed_time = current_time - start_time
    #     print(c.readHoldingRegs(0x57,2))
    #     if elapsed_time > seconds:
    #         c.slewMotor(0)
    #         break
   
