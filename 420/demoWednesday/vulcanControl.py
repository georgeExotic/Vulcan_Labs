from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
from ast import literal_eval #from hex to dec
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

import time
import math

class Motor:
    def __init__(self):
        #Initialization of LMD57 
        #device information
        self.SERVER_HOST = "192.168.33.1"
        self.SERVER_PORT = 502
        self.deviceID = "LMDCE571C"
        self.softwareVersion = "2.4.0.6"
        self.manufactureName = "SCHNEIDER ELECTRIC MOTOR USA"
        #connection to modbus TCP steps
        self._connectModbusClient()
        self._checkConnection()
        #Init variables
        self.moving = False
        # self.initialVelocity = 1000 #steps/second
        # self.finalVelocity = 750000 #steps/second
        self.hmt = 2 #default 2 = variable current mode --> current will vary as needed to postion the load with the maximun current set by the run current command 
        self.sethmt(2)
        
        # #testing torque
        # self.writeHoldingRegs(0x8E,1,self.hmt) 
        # #control Bound 
        # # self.writeHoldingRegs(0x91,1,1)
        # #torque direction
        # self.writeHoldingRegs(0xA5,1,1)
        # #torque percentage
        # self.writeHoldingRegs(0xA6,1,100)
        # #torque speed
        # self.writeHoldingRegs(0xA3,2,255)

        # print(f'hmt: {self.readHoldingRegs(0x8E,1)}')
        # print(f'control bounds: {self.readHoldingRegs(0x91,1)}')
        # print(f'torque dir: {self.readHoldingRegs(0xA5,1)}')
        # print(f'set torque: {self.readHoldingRegs(0xA6,1)}')
        # print(f'torque speed: {self.readHoldingRegs(0xA3,2)}')

        ## Testing Variable Current Mode ##
        #set Running Current
        # self.writeHoldingRegs(0x67,1,100)
        #Enable variable current 
        self.writeHoldingRegs(0x8E,1,self.hmt)
        #control Bound 
        self.writeHoldingRegs(0x91,1,0)
        #make up
        self.writeHoldingRegs(0xA0,1,2)
        #rotate CW
        print(f'hmt: {self.readHoldingRegs(0x8E,1)}')
        print(f'running current: {self.readHoldingRegs(0x67,1)}')

        ##setUp Registers/update variables
        # acce
        # self.writeHoldingRegs(0x00,4,500000)
        self.acceleration = self.readHoldingRegs(0x00,4)
        #deaccel
        # self.writeHoldingRegs(0x18,4,500000)
        self.deacceleration = self.readHoldingRegs(0x18,4)
        #enable
        # self.writeHoldingRegs(0x1C,1,1)
        self.enable = self.readHoldingRegs(0x1C,1)
        #MicroStep Resolution
        self.writeHoldingRegs(0x48,1,256)
        #update self.moving
        self._moving()
        #holding current 
        # self.writeHoldingRegs(0x29,1,25)
        #Initial velocity
        # self.writeHoldingRegs(0x89,4,self.initialVelocity)
        #MAX velcity
        # self.writeHoldingRegs(0x8B,4,self.finalVelocity)

        
        print("Congratulations Initialization Complete!")

    #function to connect to LMD57 using modbus TCP 
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

    #function to check is modbus tcp connection is successful 
    def _checkConnection(self):
        if not self._motor.is_open():
            if not self._motor.open():
                return "unable to connect" #print("unable to connect to motor")
        return "connected!"


    #function to read if the shaft is moving /// update self.moving
    def _moving(self):
        x = self.readHoldingRegs(0x4A,1)
        if x[0] == 0 :
            self.moving = False
        elif x[0] == 1:
            self.moving = True
        return

    #function to convert any hex number into decimal 
    def _hex2dec(self,hex):
        hex = str(hex)
        dec = literal_eval(hex)
        return dec


    #function to read from register of LMD57 modbus register map
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

    #function to write to any register of LMD57 modbus register map
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
    def slewMotor(self,slewDir = "cw", slew = 50000):
        #in the future translata that to mm/sec or something
        #inclomplete waiting for ccw motion 
        if slewDir == "cw":
            print("turning cw by = ", slew, "step/sec")
            self.writeHoldingRegs(0x78,4,slew)  
        elif slewDir == "ccw":
            print("ccw")

        return
    
    
    #function to set the hMT technology from schneider motor
    """
    0 --> hMTechnology circuity disabled.
    1 --> Fixed current mode. Current is
            set by the run and hold current
            commands, Speed is set by the
            system speed command.
    2 --> Variable current mode. Current will
            vary as needed to position the load
            with the maximum current set by
            the run current command. 
            self.runCurrent
    3 --> Torque mode, torque and speed
            will vary as needed to move/
            position the load with the maximum
            torque % and speed as specified
            by the torque and torque-speed
            commands.
            self.torquePercentage
            self.torqueSpeed
            self.torqueDirection


    """
    def sethmt(self, hmt = 2, runCurrentpercentage = 100, torquePercentage = 50, torqueSpeed = 10, direction = "cw"):
        #will not use 0 or 1 
        self.runCurrent = runCurrentpercentage 
        self.torquePercentage = torquePercentage #1 byte / percentage 0 - 100% 
        self.torquespeed = torqueSpeed #0 - 255
        print(self.torquespeed)
        if direction == "cw":
            self.torqueDirection = 1
        else:
            self.torqueDirection = 0

        torqueDirectionAddress = 0xA5 # 1byte / 0(ccw) - 1(cw) 
        torqueSpeedAddress = 0xA3 
        torquePercentageAddress = 0xA6 
        
        
        if hmt == 2:
            self.writeHoldingRegs(0x8E,1,hmt)
            self.writeHoldingRegs(0x67,1,self.runCurrent)
            print("Variable current mode is activated ... hmt mode = ",self.readHoldingRegs(0x8E,1))
        elif hmt == 3:
            self.writeHoldingRegs(0x8E,1,hmt)
            self.writeHoldingRegs(torquePercentageAddress,1,self.torquePercentage)
            self.writeHoldingRegs(0xA3,4,100)
            self.writeHoldingRegs(torqueDirectionAddress,1,self.torqueDirection)
            print("Torque mode is activated ... hmt mode = ",self.readHoldingRegs(0x8E,1))
            print("torque percentage is = ",self.readHoldingRegs(0xA6,1))
            print("torque speed is = ",self.readHoldingRegs(0xA3,2))
            print("torque direction is = ",self.readHoldingRegs(0xA5,1))

        return



    def displacement2steps(self, displacment_mm):
        """ 1 mm travel  =  12857 steps """
        displacement_steps = displacment_mm*12857
        # return [sign*d_lsb, sign*d_msb]
        print(f'before d in mm: {displacment_mm}, d in steps: {displacement_steps}')
        return displacement_steps

    def Home(self):
        """
        Homming routine:
            check if home 
                if not
                    if not enabled
                        set enable
                    begin moving downwards towards limit switch 
                    hit limit switch
                    stop moving
                    home = true 
                    absolute position = 0
                    
        """
        print("MODBUS COMMAND: homing")
        pass
        
    def jogUp(self,displacement):
        """
        jogUp Routine:
            check if home 
            if home & (absolute + displacement < stroke lenght )
                completeJog = 0
                call function to convert displacement into step count
                write to MA/MR the amounts of steps 
                check motion flag MP
                absolute position += displacement
                completeJog = 1
            else
                cant jogUP
                                
            if not home
                cant jogUP
        """
        if displacement == 0:
            displacement = 1
        elif displacement == 1:
            displacement = 5
        else:
            displacement = 10

        d = self.displacement2steps(displacement)
        self.writeHoldingRegs(0x46,4,d)
        # self._motor.write_multiple_registers(70, d)

        print(f'MODBUS COMMAND: jogging up {displacement} mm')
        return

    def jogDown(self,displacement):
        """
        does not matter if home or not
        if not home 
            do not do shit
        if home (absolute + displacement < stroke lenght )
            completeJog = 0
            call function to convert displacement into step count
            step count * -1
            write to MA/MR the amounts of steps 
            check motion flag MP
            absolute position -= displacement
            completeJog = 1
        
        """
        if displacement == 0:
            displacement = 1
        elif displacement == 1:
            displacement = 5
        else:
            displacement = 10

        d = self.displacement2steps(displacement)
        curr_pos = self.readHoldingRegs(0x57,4)
        print(curr_pos)
        # print(f'd before subtracting pos: {d}')
        # print(f'current pos: {curr_pos}')
        d = curr_pos[0] - d
        # print(f'd after subtracting pos: {d}')
        self.writeHoldingRegs(0x43,4,d)
        # print(f'displacement in steps: {d}')
        # print(self._motor.write_multiple_registers(70, d))
        print(f'MODBUS COMMAND: jogging down {displacement}')
        pass

    def Move(self, direction, displacement):
        d = self.displacement2steps(displacement)
        if direction == 'cw':
            self.writeHoldingRegs(0x46,4,d)
        else:
            p = self.readHoldingRegs(0x57,4)
            d = p[0] - d
            self.writeHoldingRegs(0x43,4,d)
        return

    def run(self):
        """
        run = 1
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


class limitSwitch():
    def __init__(self,limitPin):
        self.limitPin = limitPin
        GPIO.setmode(GPIO.BCM)  #set GPIO pind mode to BCM
        GPIO.setup(self.limitPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.home = False
        #pin 29 GPIO 5 
    def updateSwitch(self):
        # GPIO.input(self.limitPin) == GPIO.HIGH:
        result = GPIO.input(self.limitPin)
        print(result)

if __name__ == "__main__":
    c = Motor()
    home = limitSwitch()
    c.writeHoldingRegs(0x46,4,51200)

