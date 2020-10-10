from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils

class Motor:
    def __init__(self, localhost, port=502, **kwargs)
        self.ip_address = localhost 
        self.port = port
        self._Motor = ModbusClient(self.localhost,self.port, unit_id=1, auto_open=True)
        self.checkConnection()

    def _getversions(self):
        data = self._Motor.read_input_registers(17500, 6)
        self.os_version = ".".join(map(str, data.registers[0:3]))
        self.boot_version = ".".join(map(str, data.registers[3:6]))

    def checkConnection(self):
        if not _Motor.is_open():
            if not _Motor.open():
                print("unable to connect to motor")
        return None

    def readInputRegs(self, start_reg, byte_count):
        data = self._Motor.read_input_registers(start_reg, byte_count)
        return data

    def readCoils(self, start_reg, byte_count):
        pass

    def readHoldingRegs(self):
        pass

    def readMultipleReg(self):
        pass

###

    def writeSingleReg(self):
        pass

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

    def run(self):
        """
        run = 1
        3D print parts like Dr Hur said
        """

    def stopRun(self):
        """
        stop sending motion commands / cancel run 
        if run = 1 
            run , homing = 0 
            
            
        """
    
    def eStop(self):
        """
        if run = 1 
            write_single_register(0x001E,0) # write to enable register
            run = 0 
            homing = 0 ( so jogs are off - only option is re-homing)
        else :
            nothing 
        
        """