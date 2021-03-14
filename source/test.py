##code to figure out how to send negative commands to the SLEW register
##for a negative velocity --> "CCW"


from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils

def slewMotor(slew):
    print("input int = ",slew)

    word = utils.long_list_to_word([slew],False)
    
    complement = utils.get_list_2comp([slew])       

    print("word = ", word, "2's complement = ", complement, "\n")

slewMotor(500000)
slewMotor(41249)
reg = 50
print(reg)
reg = list((reg))
print(reg)

# [500,0] --> [500] word list to long
# [500] --> [500,0] long list to word

# get list 2 complement 

                        #val2write is the decimal value to be written to the register
            # self._motor.write_multiple_registers(startingAddressDEC,valueDEC) 