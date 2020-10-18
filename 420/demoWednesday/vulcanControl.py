from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
from ast import literal_eval #from hex to dec

import time
import math

class Motor:
    def __init__(self):
        self.SERVER_HOST = "192.168.33.1"
        self.SERVER_PORT = 502
        self.deviceID = "LMDCE571C"
        self.softwareVersion = "2.4.0.6"
        self.manufactureName = "SCHNEIDER ELECTRIC MOTOR USA"
        self._connectModbusClient()
        self._checkConnection()
        

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


    def _checkConnection(self):
        if not self._motor.is_open():
            if not self._motor.open():
                return "unable to connect" #print("unable to connect to motor")
        return "connected!"

    #function to read from register of LMD57 modbus register map
    def readHoldingRegs(self,startingAddressHex,regSize = 1):                             #startingAddressHex [address of register in HEX] regSize [size of regiter]
        startingAddressDEC = self.hex2dec(startingAddressHex)                             #hex --> dec
        reg = 0
        if regSize > 2:                                                                   #for registers with 4 byte (32bit) data
            reg2read = 2                                                                  #2 registers to read because is a 4 byte, each register is 2 byte
            reg = self._motor.read_holding_registers(int(startingAddressDEC),reg2read)    #read 2 modbus registers //// reg is a list [lsb,msb]
            ans = utils.word_list_to_long(reg,False)                                      #from list[lsb,msb] to a value /// done with big endian        
        else:                                                                             # for 2 bytes or 1 byte register 
            reg2read = 1                                                                  #1 register to read
            reg = self._motor.read_holding_registers(int(startingAddressDEC),reg2read)    #read 1 register from the address (remenber 1 address = 2 bytes(16bits))
            ans = utils.word_list_to_long(reg,False)                                      #from list[lsb] to a value /// done with big endian 
        return ans[0]

    #function to write to any register of LMD57 modbus register map
    def writeHoldingRegs(self,startingAddressHEX,regSize,valueDEC):                         #startingAddressHex [address of register in HEX] regSize [size of regiter] ValueDEC [value in decimal to write]
        startingAddressDEC = self.hex2dec(startingAddressHEX)                               #hex --> dec
        reg = 0 
        if regSize > 2:                                                                     #for registers with 4 byte (32bit) data
            reg = utils.long_list_to_word([valueDEC],False)                                 #val2write is the decimal value to be written to the register
            self._motor.write_multiple_registers(startingAddressDEC,reg)                    #
            
        else: 
             self._motor.write_multiple_registers(startingAddressDEC,[valueDEC])
        
        print(f"write done")
        return

    
    def hex2dec(self,hex):
        hex = str(hex)
        dec = literal_eval(hex)
        return dec


    def writeSingleReg(self):
        pass

    def displacement2steps(self, displacment_mm):
        """ 1 mm travel  =  12857 steps """
        displacement_steps = displacment_mm*12857
        # return [sign*d_lsb, sign*d_msb]
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
        d = curr_pos - d
        self.writeHoldingRegs(0x46,4,d)
        print(f'displacement in steps: {d}')
        # print(self._motor.write_multiple_registers(70, d))
        print(f'MODBUS COMMAND: jogging down {displacement}')
        pass

    def run(self):
        """
        run = 1
        3D print parts like Dr Hur said
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

# time.sleep(100000)
if __name__ == "__main__":
    c = Motor()
    c.writeHoldingRegs(0x46,4,512000)
    x = c.readHoldingRegs(0x00,4)
    print(x)
