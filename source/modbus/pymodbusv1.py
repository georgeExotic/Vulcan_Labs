
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

ip_address = "192.168.33.1"

client = ModbusTcpClient(ip_address)
if client.connect():    # connection is OK
    # write float
    builder = BinaryPayloadBuilder(endian=Endian.Little)
    builder.add_32bit_float(77.77)
    payload = builder.build()
    result  = client.write_registers(1, payload, skip_encode=True)
    # read floats
    result  = client.read_holding_registers(0, 2)
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Little)
    print ("read_holding_registers: " + str(decoder.decode_32bit_float()))

    client.close()