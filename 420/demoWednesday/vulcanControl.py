from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
from ast import literal_eval #from hex to dec
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

import time
import math

class limitSwitch:
    def __init__(self,limitPin):
        self.limitPin = limitPin
        GPIO.setmode(GPIO.BCM)  #set GPIO pind mode to BCM
        GPIO.setup(self.limitPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.updateSwitch()
    def updateSwitch(self):
        self.flag = GPIO.input(self.limitPin)

class Motor:
    def __init__(self):
        #Initialization of LMD57 
        #device information
        self.SERVER_HOST = "192.168.33.1"
        self.SERVER_PORT = 502
        self.deviceID = "LMDCE571C"
        self.softwareVersion = "2.4.0.6"
        self.manufactureName = "SCHNEIDER ELECTRIC MOTOR USA"
        self.connectionStatus = 0
        #connection to modbus TCP steps
        self._connectModbusClient()
        self._checkConnection()

        ###Velocities### 
            #Jogging
        self.joggingInitialVelocity = 1000
        self.joggingMaxVelocity = 50000
            #homing
        self.homingInitialVelocity = 1000
        self.homingMaxVelocity = 20000
            #runing
        self.runningInitialVelocity = 1000
        self.runningMaxVelocity = 20000

        ###accelerations###
            #jogging
        self.joggingAcceleration = 300000 
        self.joggingDeacceleration = 300000    
            #homing
        self.homingAcceleration = 300000
        self.homingDeacceleration = 300000
            #runing 
        self.runningAcceleration = 300000
        self.runningDeacceleration = 300000


        ###hmt### motor behaivor
        self.Hmt = 2                                    #default 2 = variable current mode --> current will vary as needed to postion the load with the maximun current set by the run current command 
        self.setHmt()
        

        ###Performance settings###
        #holding current
        self.holdingCurrent = 100                        #0x29#0 - 100
        #control Bound
        self.controlBound = 0                           #0x91#best torque performance
        #microsteeping
        self.microStep = 256                            #0x48

        self.setPerformanceFeatures()
        self.setEnable(1)

        ###hardware Settings
        self.pistonDiameter = 19.05 #mm
        self.leadTravel = 4 #mm per rev
        self.stepPerRevolution = 200 * self.microStep       #200*256 = 51200 steps per rev        
        
        ###homing###


        ###Flags
        self.home = False # at bottom
        self.top = False #is at the top
        self.homed = False  # has been homed Default False
        self.homing = False 
        self.flagCheck = False #will be updated to true if any flag is triggered
       
        ###Homing
        self.absolutePosition = 0 
        self.maxPosition = 300 # mm
        
        ###init home limit switch###
        self.homeSwitch = limitSwitch(6)
        self.topSwitch = limitSwitch(5)

        ###user input params for motion profile###
        self.initLayerHeight = 0
        self.compactionDepth = 0
        self.targetPressure = 0
        self.numberOfLayers = 0
        self.mass = 0
        self.modeSelected = 0
    
        print("Congratulations Motor Initialization Complete!")

    ###function to connect to LMD57 using modbus TCP 
    def _connectModbusClient(self):
        #define mosbus server and host
        self._motor = ModbusClient()
        self._motor.host(self.SERVER_HOST)
        self._motor.port(self.SERVER_PORT)
        #open TCP server
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
                return "unable to connect" #print("unable to connect to motor")
        return "connected!"


    ###function to read if the shaft is moving /// update self.moving
    def _moving(self):
        x = self.readHoldingRegs(0x4A,1)
        if x[0] == 0 :
            self.moving = False
        elif x[0] == 1:
            self.moving = True
        return

    ###function to convert any hex number into decimal 
    def _hex2dec(self,hex):
        hex = str(hex)
        dec = literal_eval(hex)
        return dec

    ###function will be called as much as posible to check the status of both flags and check that they have not been trigger during motion
    def _updateFlagCheck(self):
        self.topSwitch.updateSwitch()
        self.homeSwitch.updateSwitch()
        # print("updating checkflag")
        if self.home == True and self.homed == True:
            self.flagCheck = False
            self.home = False
            time.sleep(0.5)
            print("jorge")
        elif self.home == False and self.homed == True:
            if self.topSwitch.flag == 1 or self.homeSwitch.flag == 1:
                print("here")
                self.flagCheck = True
            else:
                self.flagCheck = False
        return

    ###function to read from register of LMD57 modbus register map
    def readHoldingRegs(self,startingAddressHex,regSize = 1):                             #startingAddressHex [address of register in HEX] regSize [size of regiter]
        startingAddressDEC = self._hex2dec(startingAddressHex)                             #hex --> dec
        if regSize > 2:                                                                   #for registers with 4 byte (32bit) data
            reg2read = 2                                                                  #2 registers to read because is a 4 byte, each register is 2 byte
            reg = self._motor.read_holding_registers(int(startingAddressDEC),reg2read)    #read 2 modbus registers //// reg is a list [lsb,msb]
            ans = utils.word_list_to_long(reg,False)                                    #from list[lsb,msb] to a value /// done with big endian        
        else:                                                                             # for 2 bytes or 1 byte register 
            reg2read = 1                                                                  #1 register to read
            ans = self._motor.read_holding_registers(int(startingAddressDEC),reg2read)    #read 1 register from the address (remenber 1 address = 2 bytes(16bits))
        return ans

    ###function to write to any register of LMD57 modbus register map
    def writeHoldingRegs(self,startingAddressHEX,regSize,valueDEC):                         #startingAddressHex [address of register in HEX] regSize [size of regiter] ValueDEC [value in decimal to write]
        startingAddressDEC = self._hex2dec(startingAddressHEX)                               #hex --> dec
        if regSize > 2:                                                                     #for registers with 4 byte (32bit) data
            valueDEC = utils.long_list_to_word([valueDEC],False)                            #val2write is the decimal value to be written to the register
            self._motor.write_multiple_registers(startingAddressDEC,valueDEC)               #write to starting register the value as a list of word [valueDEC]
                                                                                            #into to write function takes list of vals
        else:                                                                               #if 2 or 1 bytes then just send that value as a list  
             self._motor.write_multiple_registers(startingAddressDEC,[valueDEC])            #writting [value DEC] to the starting address
        return


    #function to slew axis in steps/seconds in speficied direction +/- (yes +/-!) 0 to +/- 5000000
    def slewMotor(self, slew = 50000, slewDir = "cw"):
        #in the future translata that to mm/sec or something
        #inclomplete waiting for ccw motion 
        if slewDir == "cw":
            print("turning cw by = ", slew, "step/sec")
            self.writeHoldingRegs(0x78,4,slew)  
        #need to finish#
        elif slewDir == "ccw":
            print("ccw")
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
            
            print("Variable current mode is activated ... hmt mode = ",self.readHoldingRegs(0x8E,1))
            print("Run current = ", self.readHoldingRegs(0x67,1))
            print("make Up frequency mode = ", self.readHoldingRegs(0xA0,1))
                     
        ###Hmt 3### Torque mode
        elif self.Hmt == 3:
            self.writeHoldingRegs(0x8E,1,self.Hmt)       #set hmt 

            self.writeHoldingRegs(0xA3, 4,self.torqueSpeed)     #set torque speed
            self.writeHoldingRegs(0xA6, 1,self.torquePercentage)     #set torque percent
            self.writeHoldingRegs(0xA5, 1,self.torqueDirection)     #set torque direction 

            print("Torque mode is activated ... hmt mode = ", self.readHoldingRegs(0x8E,1))
            print("torque speed is = ", self.readHoldingRegs(0xA3,4))
            print("torque percentage is = ", self.readHoldingRegs(0xA6,1))
            print("torque direction is = ", self.readHoldingRegs(0xA5,1))

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

        print("holding current = ",self.readHoldingRegs(0x29,1))
        print("control bound = ",self.readHoldingRegs(0x91,1))
        print("microstep = ",self.readHoldingRegs(0x48,1))
        return

    ###function to convert linar displacement in mm to amount of steps
    def displacement2steps(self, displacment_mm):
        targetRevolutions = displacment_mm/self.leadTravel
        steps = int(targetRevolutions * self.stepPerRevolution)
        return steps

        
    def jogUp(self,displacementChoice):

        #verify that we are not on the limit already!
        self.topSwitch.updateSwitch()
        ok = False  
        if self.topSwitch.flag == 1:
            ok = False
        elif self.topSwitch.flag == 0:
            ok = True

        #displacement choice from GUI
        if displacementChoice == 0:
            displacement = 1
        elif displacementChoice == 1:
            displacement = 5
        else:
            displacement = 10
        print(self.homed)
        print(ok)
        if self.homed == True and ok == True:
            steps2Jog = self.displacement2steps(displacement)
            # self.setProfiles("jogging")
            self.writeHoldingRegs(0x46,4,steps2Jog)
            self._moving()
            self._updateFlagCheck()
            print(self.flagCheck)
            print(self.moving)
            while self.flagCheck == False and self.moving == True:
                self._updateFlagCheck()
                self._moving()
                # print("Jogging UP!!") 
            if self.flagCheck == True:
                self.writeHoldingRegs(0x1C,1,0)
                print("driver off beacuse of trip of trigger")
        # time.sleep(0.2)
        self.writeHoldingRegs(0x1C,1,1)
        print("driver enable again")
        
        return

    def jogDown(self,displacementChoice):

        if displacementChoice == 0:
            displacement = 1
        elif displacementChoice == 1:
            displacement = 5
        else:
            displacement = 10

        steps2Jog = self.displacement2steps(displacement)

        self.setProfiles("jogging")

        absolutePosition = self.readHoldingRegs(0x57,4) #read absolute postion 

        if absolutePosition[0] == 0:
            self.writeHoldingRegs(0x57,4,steps2Jog)
            self.writeHoldingRegs(0x43,4,0)

        elif (steps2Jog - absolutePosition[0]) < 0 :        
            add = steps2Jog + absolutePosition[0]
            self.writeHoldingRegs(0x57,4,add)
            self.writeHoldingRegs(0x43,4,absolutePosition[0])
    

        print("Jogging DOWN!!")
        return

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

    def Home(self):
        self.homeSwitch.updateSwitch()      #update flag
        ok = False

        if self.homeSwitch.flag == 1:
            ok = False
        elif self.homeSwitch.flag == 0:
            ok = True
        
        if self.homed == False and ok == True:
            # print("homing starting in 3 seconds")   
            # self.countdown()
            self.setProfiles("homing")
            steps2Jog = self.displacement2steps(40)
            self.writeHoldingRegs(0x57,4,steps2Jog) #overwriting the absolute position
            self.writeHoldingRegs(0x43,4,0)
            self.homing = True      # true during homing 
            while self.homed == False:       #if not homed 
                self.homeSwitch.updateSwitch()
                # time.sleep(0.05)
                if self.homeSwitch.flag == 1:
                    # pos = self.readHoldingRegs(0x57, 4)
                    # self.writeHoldingRegs(0x43,4,pos[0])
                    self.writeHoldingRegs(0x1C,1,0)
                    self.absolutePosition = 0
                    self.writeHoldingRegs(0x57,4,0)
                    self.home = True
                    self.homed = True
                    self.homing = False      # true during homing
                    print("Homing Completed")
                    break
            self.writeHoldingRegs(0x1C,1,1)
        elif self.homed == True or ok == False:
            print("already homed")
            self.homed = True
            pass

        return

    def cleanUp(self):
        self.topSwitch.updateSwitch()
        ok = False  #to check if it is already in the switch

        if self.topSwitch.flag == 1:
            ok = False
        elif self.topSwitch.flag == 0:
            ok = True
        
        if self.homed == True and ok == True:
            self.setProfiles("homing")
            current = self.readHoldingRegs(0x57,4)
            steps2Jog = self.displacement2steps(40)
            steps2Jog = steps2Jog + current[0]
            self.writeHoldingRegs(0x43,4,steps2Jog) #overwriting the absolute position
            # self.writeHoldingRegs(0x43,4,)
            while self.top == False:
                self.topSwitch.updateSwitch()
                if self.topSwitch.flag == 1:
                    self.writeHoldingRegs(0x1C,1,0)
                    self.top = True #at the max (top)
                    self.home = False # not at the button anymore
                    print("ready for clean up")
                    break
            self.writeHoldingRegs(0x1C,1,1)
        elif ok == False:
            print("already at the top")
            pass
        elif ok == True and self.homed == False:
            print("havent home yet")
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
        
        """
        things that need to be done before running
        -home = true
        -choosen a motion profile
        -input the necessary input data
        -
        """
        print("running")
        pass

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
    c.Home()
    time.sleep(3)
    # c.jogDown(2)
    c.jogUp(1)
    time.sleep(2)
    c.jogUp(2)
    time.sleep(5)
    c.jogUp(2)
    # c.cleanUp()
    # time.sleep(2)
    # c.writeHoldingRegs(0x1C,1,0)
    # time.sleep(2)
    # print(c.readHoldingRegs)
    # print(c.readHoldingRegs(0x57,4))
    # time.sleep(3)
    # print(c.readHoldingRegs(0x57,4))
