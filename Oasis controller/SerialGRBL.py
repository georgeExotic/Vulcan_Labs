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



#The Serial GRBL class handles all levels of comunications to the GRBL 
#controller
#Todo: 
#-error lock, stop sending code if errors occur
#-add get and set grbl $ settings
#-check settings to list of required settings
#-auto set settings if different
#-add endstops to pistons, not to home, but to check end (0) reached
#-Change new layer so the last motion is always up, to increase repeatability

import serial
import threading
import time
#import CameraCapture

class GRBL(serial.Serial):
    def __init__(self):
        self.ser = serial.Serial() #make an instance of serial connection
        self.ser.baudrate = 115200 #set baudrate
        self.ser.timeout = 0 #set timeout to 0, non blocking mode
        
        #status flags
        self.connection_state = 0 #whether connected or not
        self.started_state = 0 
        self.ok_state = 1 #whether the response of serial has been OK or not
        self.error_state = 0 #error of system
        self.motion_state = "" #what the GRBL is doing 
        self.motion_state_index = 0 #the number of the last read command (used for inital conditions)
        self.motion_state_index_set = 0 #the set number of the index
        self.motion_state_changed = 1 #whether the index has changed since a set
        self.motion_state_index_limit = 100 #the max index number
        self.homed_state = 0 #if printer is homed
        
        self.send_get_status = 0 #whether to send ?
        self.motion_x_pos = 0.0
        self.motion_y_pos = 0.0
        self.motion_z_pos = 0.0
        self.motion_a_pos = 0.0
        
        self.printer_size_x = 480.0 #x total size
        self.printer_size_y = 250.0 #y total size
        self.printer_size_f = 100.0 #feed hopper total size
        self.printer_size_b = 100.0 #build hopper total size
        
        self.spreader_state = 0
        
        self.nl_back_pos_x = 100.0 #where x starts feeding
        self.nl_back_pos_y = 240.0 #where y starts and ends while feeding
        self.nl_front_pos_x = 475.0 #where x ends
        self.nl_travel_speed = 12000.0 #how fast new layer travels
        self.nl_feed_speed = 6000.0 #how fast new layer feeds (default 3000)
        self.nl_piston_speed = 150.0 #how fast the pistons move
        self.nl_piston_clearance = 0.25 #how much the pistons lower after a new layer to clear the spreader
        self.nl_piston_hysteresis = 1.00 #how much the piston needs to move down before it can move up
        self.nl_piston_feed_overfill = 1.1 #the fraction which feed supplies more than built takes
        self.nl_end_tolerance = 10.0 #how close to the end pos the gantry needs to be to consider new layer done
        self.nl_state = 1  #state of new layer, 1 is done, 0 is in progress
        
        self.printer_homing_dir_x = -1 #homing direction
        self.printer_homing_dir_y = 1 #homing direction
        self.printer_homing_pulloff = 5 #how much the printer steps back after a home
        
        self.window_output_buffer = "" #holds a buffer of what was sent out
        self.window_input_buffer = "" #holds a buffer of what was received
        
        self.grbl_version = 0.0 #version of grbl
        
        self.gcode_buffer = []
        self.gcode_buffer_left = 0
        
        #self.temp_cam = CameraCapture.CameraCapture()
        
    
    def Connect(self, serial_port):
        """Attempt to connect to the GRBL controller"""
        self.com_port_raw = str(serial_port) #get value from set_com
        self.ser.port = self.com_port_raw #set com port .
        
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
                print(self.com_port_raw + " for grbl opened")
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
        """close the connection to GRBL"""
        if (self.connection_state == 1):
            self._stop_event.set()
            self.ser.close()
            print("Closing grbl connection")
            self.connection_state = 0
            return 0
        
    def Update(self):
        """Preforms all continous tasts required for GRBL connection"""
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
                read_line = read_line.lower() #make all lower case for checking 
                read_line = read_line.rstrip() #remove carriage return
                #print("reading line: " + str(read_line)) 
                #check purpose of response
                if (read_line.startswith('ok')): #if ok was found,
                    self.ok_state = 1 #set ok state to 1
                    if (self.homed_state == 2):
                        self.homed_state = 1 #first OK after homing is homing done, set to 1
                        #print("Is homed")
                    #print("OK found, setting ok state")
                if (read_line.startswith('error')): #if error was found,
                    self.window_input_buffer += str(read_line) #add to the window buffer
                    self.error_state = 1
                    print("error found, getting error type")
                if (read_line.startswith('[')): #if message was found,
                    self.window_input_buffer += str(read_line) #add to the window buffer
                    print("message found, getting message")
                    #self.Home()
                if (read_line.startswith('<')): #if status was found,
                    #print("status found, getting status")
                    read_line = read_line.partition(',')#partition till |, compare options
                    temp_line = read_line[0].lstrip('<') #get value
                    read_line = read_line[2] #set remainder
                    self.motion_state = str(temp_line) #set status
                    self.motion_state_index += 1 #add one to index
                    if (self.motion_state_index > self.motion_state_index_limit): 
                        self.motion_state_index = 0 #reset index after reaching max
                    read_line = read_line.partition(':')
                    temp_line = read_line[0]
                    read_line = read_line[2]
                    if (temp_line == "wpos"):
                        read_line = read_line.partition(',')
                        temp_line = read_line[0] #get x
                        self.motion_x_pos = float(temp_line)
                        read_line = read_line[2]
                        
                        read_line = read_line.partition(',')
                        temp_line = read_line[0] #get y
                        self.motion_y_pos = float(temp_line)
                        read_line = read_line[2]
                        
                        read_line = read_line.partition(',')
                        temp_line = read_line[0] #get z
                        self.motion_z_pos = float(temp_line)
                        read_line = read_line[2]
                        
                        read_line = read_line.partition(',')
                        temp_line = read_line[0] #get a
                        self.motion_a_pos = float(temp_line)
                        read_line = read_line[2]
                    
                    #print("Status: " + self.motion_state)
                if (read_line.startswith('grbl')): #if grbl was found,
                    self.started_state = 1
                    print("grbl found, getting version")
                    read_line = read_line.partition(' ') #strip grbl from file
                    read_line = read_line[2].partition('f ') #strip instructions past version number
                    if (read_line[1] == 'k '):
                        self.window_input_buffer += str(read_line) #add to the window buffer
                        self.grbl_version = float(read_line[0])
                        print("GRBL Version: " + str(self.grbl_version))
                        
                        
                
            #is ok state is 1, and line buffered, send new line
            if (self.ok_state == 1 and self.started_state == 1):
                if (self.send_get_status == 1): 
                    self.ok_state = 0 #set ok state to 0
                    self.SerialWriteRaw("?\r",0) #send ?
                    self.send_get_status = 0 #set get status to 0
                    #print("Getting status")
                elif (self.BufferLeft() > 0): #if there are lines left to print
                    self.ok_state = 0 #set ok state to 0
                    self.BufferNext() #print next line in buffer to serial
                    
            #check if new layer is done
            if (self.nl_state == 0): #if new layer is in progress
                if (self.motion_state == 'idle'): #if printer is not moving
                    #if position is withing the bounds of the target
                    if (self.motion_x_pos > self.nl_front_pos_x - self.nl_end_tolerance and self.motion_x_pos < self.nl_front_pos_x + self.nl_end_tolerance):
                        self.nl_state = 1 #set new layer to 1 (done)
                        print("new layer done")
                
        
    def SerialWriteRaw(self, input_string, temp_priority):
        """prints a line to the GRBL (no checks)
        priority is 0 for not send to output, and 1 for sent to output"""
        if (temp_priority == 1):
            self.window_output_buffer += input_string #add to the window buffer
        self.ser.write(input_string.encode('utf-8'))
        
    def SerialWriteBufferRaw(self, input_string):
        """Adds a line to the input buffer""" 
        if (self.connection_state == 1): #only work when connected
            self.gcode_buffer.append(str(input_string) + '\r') #add string to buffer
            self.gcode_buffer_left += 1 #add one to left value
    
    def SerialGotoXY(self, temp_x, temp_y, temp_f=''):
        """move to the given X/Y position at feedrate in mm/min"""
        temp_string = "G1 X"
        temp_string += str(temp_x)
        temp_string += " Y"
        temp_string += str(temp_y)
        if (temp_f):
            temp_string += " F"
            temp_string += str(temp_f)
        self.SerialWriteBufferRaw(temp_string)
        
    def SerialGotoHome(self, temp_f):
        """move the printer to the home position, does NOT home the printer"""

        #get X
        if (self.printer_homing_dir_x  == -1):
            temp_x = 0 + self.printer_homing_pulloff
        else:
            temp_x = self.printer_size_x - self.printer_homing_pulloff
        #get Y
        if (self.printer_homing_dir_y  == -1):
            temp_y = 0 + self.printer_homing_pulloff
        else:
            temp_y = self.printer_size_y - self.printer_homing_pulloff
            
        self.SerialGotoXY(temp_x, temp_y, temp_f)
        
    def Jog(self, temp_axis, temp_distance, temp_feed):
        """Jogs the given axis for the given distance at the given feed,
        Has no protections built in"""
        if (self.homed_state == 1): #only jog if homed
            self.SerialWriteBufferRaw("G91") #set printer to relative (G91)
            #move axis relatively
            temp_string = "G1 "
            temp_string += str(temp_axis)
            temp_string += str(temp_distance)
            temp_string += " F"
            temp_string += str(temp_feed)
            self.SerialWriteBufferRaw(temp_string)
            self.SerialWriteBufferRaw("G90")#set printer to absolute (G90)
        else:
            print("Home printer before jogging")
        
    def SpreaderToggle(self):
        """Toggles the spreader on or off and returns on or off (1 or 0)"""
        if (self.spreader_state == 0):
            self.spreader_state = 1
            self.SerialWriteBufferRaw("M4") #set spreader to on
        else:
            self.spreader_state = 0
            self.SerialWriteBufferRaw("M5") #set spreader to off
        return self.spreader_state
        
    def SpreaderSet(self, temp_spreader_state):
        """Turns spreader on or off"""
        if (temp_spreader_state == 1):
            self.spreader_state = 1
            self.SerialWriteBufferRaw("M4") #set spreader to on
        else:
            self.spreader_state = 0
            self.SerialWriteBufferRaw("M5") #set spreader to off
        
    def NewLayer(self, temp_thickness, temp_override_build = 0):
        """Adds goes through all the motions to add a new layer and add these to the buffer
        This function will leave the motion in a RUN state, but will then hand control back
        before idle.
        All piston movements are done by relative motion, not absolute"""
        if(self.homed_state == 1):
            #calculate piston movements
            if (temp_override_build == 0):
                print("Normal new layer")
                temp_b_feed_distance = temp_thickness - self.nl_piston_clearance - self.nl_piston_hysteresis
            else:
                print("Only feed")
                temp_b_feed_distance =  (self.nl_piston_clearance * -1) - self.nl_piston_hysteresis
            temp_f_feed_distance = (temp_thickness * self.nl_piston_feed_overfill * -1) - self.nl_piston_clearance - self.nl_piston_hysteresis
            temp_hysteresis_clearance =  self.nl_piston_clearance - self.nl_piston_hysteresis
            
            #b hysteresis = 1
            #thickness = 0.25
            #clearance = 0.5
            #b moves down 1, moves up 0.25-0.5-1 = -1.25 (nett -0.25)
            #b moves down 1, moves down 0.5-1 = -0.5 (nett 0.5)
            
            self.SerialGotoXY(self.nl_back_pos_x, self.nl_back_pos_y, self.nl_travel_speed) #move gantry to back position
            
            #try to take picture
            #self.StatusIndexSet()
            #while (self.StatusIndexChanged() == 0):
            #    time.sleep(0.005)
            #print("Halt exited, state: " + self.motion_state)
            #try:
                #time.sleep(0.5)
                #self.temp_cam.CaptureImage(self.motion_z_pos)
                #time.sleep(0.5)
            #except:
            #    pass
            
            self.SerialWriteBufferRaw("G91") #set motion to relative
            self.SerialWriteBufferRaw("G1 Z" + str(self.nl_piston_hysteresis) + " F" + str(self.nl_piston_speed))#move hysteresis down
            self.SerialWriteBufferRaw("G1 Z" + str(temp_b_feed_distance) + " F" + str(self.nl_piston_speed)) #Lower build piston to build position
            self.SerialWriteBufferRaw("G1 A" + str(self.nl_piston_hysteresis) + " F" + str(self.nl_piston_speed)) #move hysteresis down
            self.SerialWriteBufferRaw("G1 A" + str(temp_f_feed_distance) + " F" + str(self.nl_piston_speed)) #raise feed piston to feed position
            
            
            self.SerialWriteBufferRaw("G90") #set motion to absolute
            self.SpreaderSet(1) #start spreader
            self.SerialGotoXY(self.nl_front_pos_x, self.nl_back_pos_y, self.nl_feed_speed) #move gantry to overshoot
            self.SpreaderSet(0) #stop spreader
            self.SerialWriteBufferRaw("G91") #set motion to relative
            self.SerialWriteBufferRaw("G1 Z" + str(self.nl_piston_hysteresis) + " F" + str(self.nl_piston_speed)) #move hysteresis down
            self.SerialWriteBufferRaw("G1 Z" + str(temp_hysteresis_clearance) + " F" + str(self.nl_piston_speed)) #move build pistons down clearance amount
            self.SerialWriteBufferRaw("G1 A" + str(self.nl_piston_hysteresis) + " F" + str(self.nl_piston_speed)) #move hysteresis down
            self.SerialWriteBufferRaw("G1 A" + str(temp_hysteresis_clearance) + " F" + str(self.nl_piston_speed)) #move feed pistons down clearance amount
            self.SerialWriteBufferRaw("G90") #set motion to absolute
            
            
            #wait till state is not idle anymore
            self.StatusIndexSet()
            while (self.StatusIndexChanged() == 0):
                time.sleep(0.005)
            #print("Halt exited, state: " + self.motion_state)
            
            self.nl_state = 0 #set new layer state to in progress
        
        
    def BufferLeft(self):
        """returns how many lines are left in the buffer"""
        return self.gcode_buffer_left
    
    def BufferNext(self):
        """Writes the next line in the buffer to the serial"""
        if (self.BufferLeft() > 0): #if there are lines left in the buffer
            self.gcode_buffer_left -= 1 #subtract 1 from left value
            self.SerialWriteRaw(self.gcode_buffer[0],1) #print to GRBL
            del self.gcode_buffer[0] #remove the written line
    
    def Home(self):
        """Homes the printer and sets the coordinates
        Because homing only sends the ok after the home, it suffices
        to simply send the move to home ('$H') and then 
        G92 X# Y#. The ok buffer will take care of the rest"""
        self.SerialWriteBufferRaw('$h') #buffer home command
        #calculate x and y home based on home dir and length
        if (self.printer_homing_dir_x == -1):
            temp_x = self.printer_homing_pulloff
        else:
            temp_x = self.printer_size_x -self.printer_homing_pulloff
        
        if (self.printer_homing_dir_y == -1):
            temp_y = self.printer_homing_pulloff
        else:
            temp_y = self.printer_size_y -self.printer_homing_pulloff
        
        self.SerialWriteBufferRaw('G92 X' + str(temp_x) + ' Y' + str(temp_y))#buffer G92 command
        self.homed_state = 2 #set homed state to 2 (homing in progress)
        self.motion_state = "home" #set status
    
    def GetStatus(self):
        """periodically sends a ? to get status"""
        time.sleep(5) #initial wait to get system time to start
        while not self._stop_event.is_set():
            time.sleep(0.1) #wait for 0.1 seconds
            self.send_get_status = 1
            
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
        
    def StatusIndexSet(self):
        """Sets the current status index value, so later function will know if it changed"""
        self.motion_state_changed = 0
        self.motion_state_index = 0
        self.motion_state_index_set = self.motion_state_index
        
    def StatusIndexChanged(self):
        """Look if the current index has changed (new update of status),
        return 1 if new index, 0 if not"""
        if (self.motion_state_changed == 0):
            if (self.motion_state_index_set + 3 > self.motion_state_index):
                #state is set to 0 on set, wait till value is more than N off
                return 0 #return 0 if the values are the same
            else:
                self.motion_state_changed = 1 #set value to changed, so this will not be called again
                #print("Status changed: " + str(self.motion_state_index_set) + ", " + str(self.motion_state_index))
                return 1 #return 1 if the values are the not same
        else:
            return 1 #return 1 if value was already marked as changed

if __name__ == '__main__':
    printer = GRBL()
    temp_com = input("give com port input: ")
    printer.Connect(str(temp_com))
    while 1:
        #temp_out = input("Send command: ")
        #temp_out = str(temp_out)
        #printer.SerialWriteBufferRaw(temp_out)
        temp_x = input("X: ")
        temp_y = input("Y: ")
        printer.SerialGotoXY(temp_x, temp_y, 12000)
        


#messages expected:
#Grbl 1.1f ['$' for help] #initial welcome
#[MSG:'$H'|'$X' to unlock] #unlock message
#ok
#error:#
#<Idle|WPos:0.000,250.000,0.000|Bf:15,127|FS:0,0>
