#This file is part of Oasis controller.

#Oasis controller is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#Oasis controller is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Oasis controller.  If not, see <https://www.gnu.org/licenses/>.




#The serialHP45 controls the serial connection with the HP45 controller
#Todo:
#-At the bottom of update, the lines that need to be sent to the printhead are handled
# there is a buffer holding this data, and when there is space, it is sent over.
# however, during the initial high transfer rate when going from 0 to 1000, it fills in an instant
# but later when the head is moving it slows to a crawl (10-20 lines per second)
# python has given the idea of being the problem, but the printhead is also a bit suspect. 
# for now, focus is set on making it work. 1000 lines is plenty for most shapes
# in the spirit of first make it work, the print function will cap at 900 or so, and split sweeps if the cap is reached
# also python sucks at high speed stuff, mark for future reference just how bad it is for me (I suspect 50% PEBKAC)

#-Send a list of settings to the printhead upon connection. DPI and density is not sent here right now when the head is not connected
# 

import serial
import threading
import time
import B64

class HP45(serial.Serial):
    def __init__(self):
        self.ser = serial.Serial() #make an instance of serial connection
        self.ser.baudrate = 115200 #set baudrate
        self.ser.timeout = 0 #set timeout to 0, non blocking mode
        
        #status flags
        self.connection_state = 0 #whether connected or not
        self.started_state = 0 
        self.ok_state = 1 #whether the response of serial has been OK or not
        self.error_state = 0 #error of system
        self.inkjet_version = 0.0 #version of grbl
        
        self.send_get_status = 0 #whether to fetch a value
        self.send_status_buffer = "" #buffer for status
        self.status_state = 0 #which status to fetch
        self.inkjet_x_pos = 0.0 #the position of the printhead
        self.inkjet_total_nozzles = 300 #the total amount of nozzles
        self.inkjet_working_nozzles = 0 #the total amount working of nozzles
        self.inkjet_temperature = 0.0 #the temperature of the printhead
        self.inkjet_writeleft = 0 #the amount of read lines left
        self.inkjet_dpi = 600 #the DPI of the printhead
        self.inkjet_density = 100 #the density of the printhead
        
        self.code_buffer = []
        self.code_buffer_left = 0
        
        self.window_output_buffer = "" #holds a buffer of what was sent out
        self.window_input_buffer = "" #holds a buffer of what was received
        
    def Connect(self, serial_port):
        """Attempt to connect to the HP45 controller"""
        self.com_port_raw = str(serial_port) #get value from set_com
        self.ser.port = self.com_port_raw #set com port
        
        if (self.connection_state == 0): #if not yet connected
            #print("attempting to open: " + self.com_port_raw)
            self.temp_com_success = 0
            try: #try to open a com port with it
                self.ser.open()
                self.temp_com_success = 1
            except:
                #print ("Unable to open connection")
                nothing = 0
            if (self.temp_com_success == 1):
                print(self.com_port_raw + " for HP45 opened")
                self.connection_state = 1
                self.started_state = 0 
                self.ok_state = 1 
                self.error_state = 0 
                self.homed_state = 0 
                self._stop_event = threading.Event()
                self.update_thread = threading.Thread(target=self.Update)
                self.update_thread.start()
                self.status_thread = threading.Thread(target=self.GetStatus)
                self.status_thread.start()
                return 1
            else:
                return 0
                
    def Disconnect(self):
        """close the connection to HP45"""
        if (self.connection_state == 1):
            self._stop_event.set()
            self.ser.close()
            print("Closing grbl connection")
            self.connection_state = 0
            return 0
            
    def Update(self):
        """Preforms all continous tasks required for HP45 connection"""
        time.sleep(0.05)
        read_buffer = "" #used to store Serial read data
        while not self._stop_event.is_set():
            #get code
            temp_success = 0 #success value
            try: #attempt to read serial
                if (self.ser.in_waiting > 0):
                    temp_read = self.ser.read(self.ser.in_waiting) #add serial to read buffer
                    temp_read = str(temp_read.decode('utf-8'))
                    temp_success = 1
            except:
                print("Read error") #some mistake, otherwise ignore quietly
                break
            if temp_success == 1: 
                read_buffer += temp_read
                #print(read_buffer)
                #add line to read buffer
                
            temp_decode = read_buffer.partition('\n') #check for EOL conditions
            if (temp_decode[1] == '\n'): #if '\n' 
                read_buffer = temp_decode[2] #write remainder to buffer
                read_line = str(temp_decode[0])
                #read_line = read_line.lower() #make all lower case for checking #(DONT!!!)
                read_line = read_line.rstrip() #remove carriage return
                #print("reading line: " + str(read_line)) 
                #check purpose of response
                if (read_line.startswith('OK')): #if ok was found,
                    self.ok_state = 1 #set ok state to 1
                    #print("OK found, setting ok state")
                if (read_line.startswith('GTP:')):
                    #print("getting temperature")
                    read_line = read_line.partition(':') #split at :
                    read_line = read_line[2] #get end
                    temp_return_string = B64.B64FromSingle(read_line)
                    self.inkjet_temperature = float(temp_return_string)
                    self.inkjet_temperature /= 10.0 #get whole degrees
                if (read_line.startswith('GEP:')):
                    #print("getting position")
                    read_line = read_line.partition(':') #split at :
                    read_line = read_line[2] #get end
                    #print("Decoding: " + read_line)
                    temp_return_string = B64.B64FromSingle(read_line)
                    #print("position found: " + str(temp_return_string))
                    self.inkjet_x_pos = float(temp_return_string)
                    self.inkjet_x_pos /= 1000.0 #get millimeters
                if (read_line.startswith('BWL:')):
                    #print("getting buffer write left")
                    read_line = read_line.partition(':') #split at :
                    read_line = read_line[2] #get end
                    temp_return_string = B64.B64FromSingle(read_line)
                    self.inkjet_writeleft = int(temp_return_string)
                    
                if (read_line.startswith('THD:')): 
                    #print("decoding test results")
                    read_line = read_line.partition(':') #split at :
                    read_line = read_line[2] #get end
                    #print("Decoding: " + read_line)
                    temp_return_string = B64.B64FromTestArray(read_line)
                    temp_total_nozzle = 0
                    temp_working_nozzles = 0
                    for n in temp_return_string:
                        #print(n)
                        temp_total_nozzle += 1
                        if (n == 1):
                            temp_working_nozzles += 1
                    self.inkjet_total_nozzles = temp_total_nozzle
                    self.inkjet_working_nozzles = temp_working_nozzles
        
            #is ok state is 1, and line buffered, send new line
            if (self.ok_state == 1):
                if (self.send_get_status == 1): 
                    #print("sending status")
                    self.ok_state = 0 #set ok state to 0
                    self.SerialWriteRaw(self.send_status_buffer + "\r",0) #send status request
                    self.send_get_status = 0 #set get status to 0
                    #print("Getting status")
                elif (self.BufferLeft() > 0): #if there are lines left to print
                    if (self.inkjet_writeleft > 50): #only send if space left in hp45 buffer
                        #print(self.BufferLeft())
                        self.ok_state = 0 #set ok state to 0
                        self.BufferNext() #print next line in buffer to serial            
                        self.inkjet_writeleft -= 1 #subtract 1 from line left (estimate)
    
    def SerialWriteRaw(self, input_string, temp_priority):
        """prints a line to the HP45 (no checks)
        priority is 0 for not send to output, and 1 for sent to output"""
        if (temp_priority == 1):
            self.window_output_buffer += input_string #add to the window buffer
        self.ser.write(input_string.encode('utf-8'))
        
    def SerialWriteBufferRaw(self, input_string):
        """Adds a line to the input buffer""" 
        if (self.connection_state == 1): #only work when connected
            self.code_buffer.append(str(input_string) + '\r') #add string to buffer
            self.code_buffer_left += 1 #add one to left value
    
    def BufferLeft(self):
        """returns how many lines are left in the buffer"""
        return self.code_buffer_left
    
    def BufferNext(self):
        """Writes the next line in the buffer to the serial"""
        if (self.BufferLeft() > 0): #if there are lines left in the buffer
            self.code_buffer_left -= 1 #subtract 1 from left value
            self.SerialWriteRaw(self.code_buffer[0],0) #print to HP45
            del self.code_buffer[0] #remove the written line
    
    def GetStatus(self):
        """periodically sends a get status command"""
        time.sleep(5) #initial wait to get system time to start
        while not self._stop_event.is_set():
            time.sleep(0.1) #wait for 0.2 seconds
            if (self.status_state == 0): #get temp
                self.send_status_buffer = "GTP" #get temperature
                #print("Ask for temp from HP45")
            if (self.status_state == 1): #get pos
                self.send_status_buffer = "GEP" #Get encoder position
                #print("Ask for pos from HP45")
            if (self.status_state == 2): #get write left
                self.send_status_buffer = "BWL" #Get write left
                #print("Ask for WL from HP45")
            self.send_get_status = 1
            self.status_state += 1
            if (self.status_state > 2): #reset state
                self.status_state = 0
    
    def GetWindowOutput(self):
        """returns the entire string of what was sent since the 
        last call of this function, then clears that buffer"""
        temp_return = self.window_output_buffer #write to return value
        self.window_output_buffer = "" #clear buffer
        return temp_return #return response
        
    def GetWindowInput(self):
        """returns the entire string of what was received since the 
        last call of this function, then clears that buffer"""
        temp_return = self.window_input_buffer #write to return value
        self.window_input_buffer = "" #clear buffer
        return temp_return #return response
        
    def Preheat(self, temp_pulses):
        """preheats the printhead for the given amount of pulses"""
        if (self.connection_state == 1): #check if connected before sending
            temp_send_pulses = "" 
            temp_send_pulses = B64.B64ToSingle(temp_pulses)
            self.SerialWriteBufferRaw("PHT " + temp_send_pulses) #send preheat command
            
    def Prime(self, temp_pulses):
        """preheats the printhead for the given amount of pulses"""
        if (self.connection_state == 1): #check if connected before sending
            temp_send_pulses = "" 
            temp_send_pulses = B64.B64ToSingle(temp_pulses)
            self.SerialWriteBufferRaw("PRM " + temp_send_pulses) #send preheat command
   
    def SetPosition(self, temp_position):
        """Takes the input position in microns and sends it to the printhead"""
        if (self.connection_state == 1): #check if connected before sending
            temp_send_pos = "" 
            temp_send_pos = B64.B64ToSingle(temp_position)
            self.SerialWriteBufferRaw("SEP " + temp_send_pos) #send preheat command

    def SetDPI(self, temp_dpi):
        """sends the DPI to the printhead"""
        if (self.connection_state == 1): #check if connected before sending
            temp_send_dpi = "" 
            temp_send_dpi = B64.B64ToSingle(temp_dpi)
            self.inkjet_dpi = int(temp_dpi) #write to variable
            self.SerialWriteBufferRaw("SDP " + str(temp_send_dpi)) #send dpi command
            
    def SetDensity(self, temp_density):
        """Sends the density in percent points to the printhead"""
        if (self.connection_state == 1): #check if connected before sending
            temp_send_density = "" 
            temp_send_density = B64.B64ToSingle(temp_density)
            self.inkjet_density = int(temp_density) #write to variable
            self.SerialWriteBufferRaw("SDN " + str(temp_send_density)) #send density command
            
    def ClearBuffer(self):
        """Completely clears the buffer"""
        if (self.connection_state == 1): #check if connected before sending
            self.SerialWriteBufferRaw("BCL") #send clear command
        
    def TestPrinthead(self):
        """Sends the test command to the printhead"""
        if (self.connection_state == 1): #check if connected before sending
            self.SerialWriteBufferRaw("THD")
    
    def SendInkjetLineRaw(self, temp_position, temp_inkjet_line):
        """Sends a line of inkjet information in raw format in the given coordinate"""
        #convert position to B64
        temp_pos_b64 = B64.B64ToSingle(temp_position)
        #print("Converting position: " + str(temp_position) + " to: " + str(temp_pos_b64))
        
        #convert inkjet line to B64
        temp_inkjet_b64 = B64.B64ToArray(temp_inkjet_line)
        #print("Converting position: " + str(temp_inkjet_line))
        #print(" to: " + str(temp_inkjet_b64))
        
        #convert turn this data into an inkjet command and add to buffer
        self.SerialWriteBufferRaw("SBR " + str(temp_pos_b64) + " " + str(temp_inkjet_b64))
        #print("SBR " + str(temp_pos_b64) + " " + str(temp_inkjet_b64) + "\r")
