from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils

class Motor:
    def __init__(self, localhost, port=502, **kwargs)
        self.ip_address = localhost 
        self.port = port
        self._Motor = ModbusClient(self.localhost,self.port, unit_id=1, auto_open=True)
        self.checkConnection()

    def checkConnection(self):
        if not _Motor.is_open():
            if not _Motor.open():
                print("unable to connect to motor")
        return None

    def _getversions(self):
        data = self._Motor.read_input_registers(17500, 6)
        self.os_version = ".".join(map(str, data.registers[0:3]))
        self.boot_version = ".".join(map(str, data.registers[3:6]))

    def readInputRegisters(self, start_reg, byte_count):
        data = self._Motor.read_input_registers(start_reg, byte_count)
        return data

    def readCoilRegisters(self, start_reg, byte_count):
        pass

    def 

