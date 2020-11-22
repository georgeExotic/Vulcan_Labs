from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils


import time

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

    def readInputRegs(self, start_reg, byte_count):
        data = self._motor.read_input_registers(start_reg, byte_count)
        return data

    def readCoils(self, start_reg, byte_count):
        pass

    def readHoldingRegs(self,byteCount = 2):
        if byteCount > 2:   #4 byte number = 2 registers
            

        pass

###

    def writeSingleReg(self):
        pass

    def displacement2steps(self, displacment_mm):
        """ 1mm = 12800steps """
        displacement_steps = displacment_mm*12857
        d_msb = 0
        if displacement_steps > 65536:
            d_lsb = 65536
            d_msb = displacement_steps - d_lsb
        else:
            d_lsb = displacement_steps
        return d_lsb,

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

        print(f'displacement: {displacement}')

        d = self.displacement2steps(displacement)
        print(f'displacement in steps: {d}')

        self._motor.write_multiple_registers(70, [d,0])
        print(f'MODBUS COMMAND: jogging up {displacement}')
        pass

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
    while 1:
        print("ok")