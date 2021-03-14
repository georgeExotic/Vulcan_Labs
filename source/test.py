##code to figure out how to send negative commands to the SLEW register
##for a negative velocity --> "CCW"


from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils

def slewMotor(slew):
    print("input int = ",slew)

    complement = utils.get_2comp(slew,32)       
    word = utils.long_list_to_word([complement])

    # long = utils.word_list_to_long(complement)

    # complement2 = utils.get_list_2comp(long)

    # word2 = utils.long_list_to_word(complement2)
    
    # print(complement)
    print("2's complement = ", complement , "word", word , "\n")
    # print("2's complement = ", complement2, "word2 = ",word2, "\n")

slewMotor(-5000)
slewMotor(5000)

# [500,0] --> [500] word list to long
# [500] --> [500,0] long list to word

# get list 2 complement 

                        #val2write is the decimal value to be written to the register
            # self._motor.write_multiple_registers(startingAddressDEC,valueDEC) 
