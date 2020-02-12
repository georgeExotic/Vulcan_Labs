#Oasis controller is the software used to control the HP45 and GRBL driver in Oasis
#Copyright (C) 2018  Yvo de Haas

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
#TESTE

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox, QComboBox
from PyQt5.QtGui import QPixmap, QColor, QImage
from SerialGRBL import GRBL
from SerialHP45 import HP45
from Interface import Interface
import os
from ImageConverter import ImageConverter
import B64
from numpy import * 
import threading
import time

#a small note on threading. It is used so some of the functions update automatically (serial GRBL and inkjet)
#however, it is a bit of a lie. If python is busy in one thread, it will quietly ignore the others
#sleep commands will give enough room that python works on other threads.
#this is the reason why sending inkjet while moving is difficult. Will fix later, with another attempt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()        
        self.ui = Interface()
        self.ui.initUI()
        self.ui.show()
        
        self.grbl = GRBL()
        self.inkjet = HP45()
        self.imageconverter = ImageConverter()
        
        self.printing_state = 0 #whether the printer is printing
        self.printing_abort_flag = 0
        self.printing_pause_flag = 0
        
        #grbl connect button
        self.grbl_connection_state = 0 #connected state of grbl
        self.ui.motion_connect.clicked.connect(self.GrblConnect)
        self.ui.motion_set_port.returnPressed.connect(self.GrblConnect)
        
        #grbl send command button
        self.ui.motion_send_line.clicked.connect(self.GrblSendCommand)
        self.ui.motion_write_line.returnPressed.connect(self.GrblSendCommand)
        
        #grbl home button
        self.ui.motion_home.clicked.connect(self.grbl.Home)
        
        #grbl jog buttons
        self.ui.motion_xp.clicked.connect(lambda: self.grbl.Jog('X', '10', '6000'))
        self.ui.motion_xn.clicked.connect(lambda: self.grbl.Jog('X', '-10', '6000'))
        self.ui.motion_yp.clicked.connect(lambda: self.grbl.Jog('Y', '10', '6000'))
        self.ui.motion_yn.clicked.connect(lambda: self.grbl.Jog('Y', '-10', '6000'))
        self.ui.motion_goto_home.clicked.connect(lambda: self.grbl.SerialGotoXY(5, 245, '12000')) #I am lazy, this should be automatically generated
        self.ui.motion_fu.clicked.connect(lambda: self.grbl.Jog('A', '-1', '150'))
        self.ui.motion_fd.clicked.connect(lambda: self.grbl.Jog('A', '1', '150'))
        self.ui.motion_bu.clicked.connect(lambda: self.grbl.Jog('Z', '-1', '150'))
        self.ui.motion_bd.clicked.connect(lambda: self.grbl.Jog('Z', '1', '150'))
        self.ui.motion_spreader.clicked.connect(self.GRBLSpreader)
        self.ui.motion_new_layer.clicked.connect(self.GRBLNewLayer)
        self.ui.motion_prime_layer.clicked.connect(self.GRBLPrimeLayer)
        
        #inkjet connect button
        self.inkjet_connection_state = 0 #connected state of inkjet
        self.ui.inkjet_connect.clicked.connect(self.InkjetConnect)
        self.ui.inkjet_set_port.returnPressed.connect(self.InkjetConnect)
        
        #inkjet send command button
        self.ui.inkjet_send_line.clicked.connect(self.InkjetSendCommand)
        self.ui.inkjet_write_line.returnPressed.connect(self.InkjetSendCommand)
        
        #inkjet function buttons
        self.ui.inkjet_preheat.clicked.connect(lambda: self.inkjet.Preheat(5000))
        self.ui.inkjet_prime.clicked.connect(lambda: self.inkjet.Prime(100))
        self.ui.inkjet_set_pos.clicked.connect(self.InkjetSetPosition)
        #self.ui.inkjet_set_dpi.clicked.connect(self.InkjetSetDPI)
        self.ui.dpi_combo.currentIndexChanged.connect(self.InkjetSetDPI)
        #self.ui.inkjet_dpi.returnPressed.connect(self.InkjetSetDPI)
        self.ui.inkjet_set_density.clicked.connect(self.InkjetSetDensity)
        self.ui.inkjet_density.returnPressed.connect(self.InkjetSetDensity)
        self.ui.inkjet_test_button.clicked.connect(self.inkjet.TestPrinthead)
        
        #file buttons
        self.file_loaded = 0
        self.ui.file_open_button.clicked.connect(self.OpenFile)
        self.ui.file_convert_button.clicked.connect(self.RenderOutput)
        self.ui.file_print_button.clicked.connect(self.RunPrintArray)
        self.ui.pause_button.clicked.connect(self.PausePrint)
        self.ui.abort_button.clicked.connect(self.AbortPrint)
        #self.ui.file_print_button.clicked.connect(self.RenderRGB)
        self.ui.layer_slider.valueChanged.connect(self.UpdateLayer) 
        
        #self.ui.save_png.clicked.connect(self.SavePng)
        
        
    
    def GrblConnect(self):
        """Gets the GRBL serial port and attempt to connect to it"""
        
        if (self.grbl_connection_state == 0): #get connection state, if 0 (not connected)
            #print("Attempting connection with GRBL")
            temp_port = str(self.ui.motion_set_port.text()) #get text
            temp_succes = self.grbl.Connect(temp_port) #attempt to connect
            if (temp_succes == 1): #on success, 
                self.ui.motion_connect.setText("Disconnect")#rewrite button text
                self.grbl_connection_state = 1 #set  state
                self.ui.motion_set_port.clear()
                #start a thread that will update the serial in and output for GRBL
                self._grbl_stop_event = threading.Event()
                self.grbl_update_thread = threading.Thread(target=self.GrblUpdate)
                self.grbl_update_thread.start()
                
            else:
                print("Connection with GRBL failed")
        else: #on state 1
            #print("disconnecting from GRBL")
            self.grbl.Disconnect() #disconnect
            self.grbl_connection_state = 0 #set state to disconnected
            self.ui.motion_connect.setText("Connect") #rewrite button
            self._grbl_stop_event.set() #close the grbl serial thread
            
    def GrblUpdate(self):
        """updates serial in and output for the GRBL window"""
        time.sleep(1)
        while not self._grbl_stop_event.is_set():
            grbl_serial_in = str(self.grbl.GetWindowInput())
            grbl_serial_out = str(self.grbl.GetWindowOutput())
            
            self.ui.motion_serial_output.moveCursor(QtGui.QTextCursor.End)
            self.ui.motion_serial_output.insertPlainText(grbl_serial_out)
            self.ui.motion_serial_output.moveCursor(QtGui.QTextCursor.End)
            
            self.ui.motion_serial_input.moveCursor(QtGui.QTextCursor.End)
            self.ui.motion_serial_input.insertPlainText(grbl_serial_in)
            self.ui.motion_serial_input.moveCursor(QtGui.QTextCursor.End)
            
            #update state and coordinates
            self.ui.motion_state.setText(self.grbl.motion_state)
            self.ui.motion_x_pos.setText(str(self.grbl.motion_x_pos))
            self.ui.motion_y_pos.setText(str(self.grbl.motion_y_pos))
            self.ui.motion_b_pos.setText(str(self.grbl.motion_z_pos))
            self.ui.motion_f_pos.setText(str(self.grbl.motion_a_pos))
            
            time.sleep(0.2)
            
    def GrblSendCommand(self):
        """Gets the command from the textedit and prints it to Grbl"""
        if (self.grbl_connection_state == 1):
            temp_command = str(self.ui.motion_write_line.text())#get line
            temp_command += "\r" #add end of line
            self.grbl.SerialWriteBufferRaw(temp_command) #write to grbl
            self.ui.motion_write_line.clear() #clear line

    def InkjetConnect(self):
        """Gets the inkjet serial port and attempt to connect to it"""
        if (self.inkjet_connection_state == 0): #get connection state, if 0 (not connected)
            #print("Attempting connection with HP45")
            temp_port = str(self.ui.inkjet_set_port.text()) #get text
            temp_succes = self.inkjet.Connect(temp_port) #attempt to connect
            if (temp_succes == 1): #on success, 
                self.ui.inkjet_connect.setText("Disconnect") #rewrite button text
                self.inkjet_connection_state = 1 #set  state
                self.ui.inkjet_set_port.clear()
                #start a thread that will update the serial in and output for HP45
                self._inkjet_stop_event = threading.Event()
                self.inkjet_update_thread = threading.Thread(target=self.InkjetUpdate)
                self.inkjet_update_thread.start()
                
            else:
                print("Connection with HP failed")
        else: #on state 1
            #print("disconnecting from HP45")
            self.inkjet.Disconnect() #disconnect
            self.inkjet_connection_state = 0 #set state to disconnected
            self.ui.inkjet_connect.setText("Connect") #rewrite button
            self._inkjet_stop_event.set() #close the HP45 serial thread
            
    def InkjetUpdate(self):
        """updates serial in and output for the inkjet window"""
        time.sleep(1)
        while not self._inkjet_stop_event.is_set():
            inkjet_serial_in = str(self.inkjet.GetWindowInput())
            inkjet_serial_out = str(self.inkjet.GetWindowOutput())
            
            self.ui.inkjet_serial_output.moveCursor(QtGui.QTextCursor.End)
            self.ui.inkjet_serial_output.insertPlainText(inkjet_serial_out)
            self.ui.inkjet_serial_output.moveCursor(QtGui.QTextCursor.End)
            
            self.ui.inkjet_serial_input.moveCursor(QtGui.QTextCursor.End)
            self.ui.inkjet_serial_input.insertPlainText(inkjet_serial_in)
            self.ui.inkjet_serial_input.moveCursor(QtGui.QTextCursor.End)
            
            #update state and coordinates
            self.ui.inkjet_temperature.setText(str(self.inkjet.inkjet_temperature))
            self.ui.inkjet_pos.setText(str(self.inkjet.inkjet_x_pos))
            self.ui.inkjet_writeleft.setText(str(self.inkjet.inkjet_writeleft))
            
            #update inkjet test state
            self.ui.inkjet_test_state.setText(str(self.inkjet.inkjet_working_nozzles) + "/" + str(self.inkjet.inkjet_total_nozzles))
            
            time.sleep(0.2)
    
    def InkjetSendCommand(self):
        """Gets the command from the textedit and prints it to Inkjet"""
        if (self.inkjet_connection_state == 1):
            temp_command = str(self.ui.inkjet_write_line.text())#get line
            temp_command += "\r" #add end of line
            self.inkjet.SerialWriteBufferRaw(temp_command) #write to inkjet
            self.ui.inkjet_write_line.clear() #clear line

    def InkjetSetPosition(self):
        """Gets the position from GRBL, converts it and sends it to HP45"""
        if (self.inkjet_connection_state == 1):
            time.sleep(0.3) #wait for a while to get the newest pos
            temp_pos = self.grbl.motion_y_pos #set pos to variable
            temp_pos *= 1000.0
            temp_pos = int(temp_pos) #cast to interger
            self.inkjet.SetPosition(temp_pos) #set position
    
    def InkjetSetDPI(self):
        """Writes the DPI to the printhead and decode function"""
        #temp_dpi = str(self.ui.inkjet_dpi.text()) #get text#get dpi
        temp_dpi = str(self.ui.dpi_combo.currentText()) #get text#get dpi
        temp_dpi_val = 0
        temp_success = 0
        try:
            temp_dpi_val = int(temp_dpi)
            temp_success = 1
        except:
            #print ("Unable to convert to dpi")
            nothing = 0

        if (temp_success == 1): #if conversion was successful
            if (self.printing_state == 0): #only set DPI when not printing
                print("DPI to set: " + str(temp_dpi_val))
                if (self.inkjet_connection_state == 1): #only write to printhead when connected
                    self.inkjet.SetDPI(temp_dpi_val) #write to inkjet
                self.imageconverter.SetDPI(temp_dpi_val) #write to image converter
                if (self.file_loaded != 0): #if any file is loaded
                    print("resising image")
                    self.OpenFile(self.input_file_name[0])
                
    def InkjetSetDensity(self):
        """Writes the Density to the printhead"""
        if (self.inkjet_connection_state == 1):
            temp_density = str(self.ui.inkjet_density.text()) #get text #get density
            temp_density_val = 0
            temp_success = 0
            try:
                temp_density_val = int(temp_density)
                temp_success = 1
            except:
                #print ("Unable to convert to dpi")
                nothing = 0

            if (temp_success == 1): #if conversion was successful
                #print("Density to set: " + str(temp_density_val))
                self.inkjet.SetDensity(temp_density_val) #write to inkjet
                
    def GRBLSpreader(self):
        """Toggles the spreader on or off and sets the button"""
        temp_return = self.grbl.SpreaderToggle()
        if (temp_return == 1):
            self.ui.motion_spreader.setText("Spreader off")
        else:
            self.ui.motion_spreader.setText("Spreader on")
    
    def GRBLNewLayer(self):
        """add a new layer"""
        if (self.grbl_connection_state == 1):
            #print("new layer")
            temp_layer_thickness = str(self.ui.motion_layer_thickness.text())
            temp_layer_thickness_val = 0
            temp_success = 0
            try:
                temp_layer_thickness_val = float(temp_layer_thickness)
                temp_success = 1
            except:
                #print ("Unable to convert to layer thickness")
                nothing = 0
            if (temp_success == 1):
                #print("adding new layer: " + str(temp_layer_thickness_val))
                self.grbl.NewLayer(temp_layer_thickness_val)
                
    def GRBLPrimeLayer(self):
        """add a new layer"""
        if (self.grbl_connection_state == 1):
            #print("new layer")
            temp_layer_thickness = str(self.ui.motion_layer_thickness.text())
            temp_layer_thickness_val = 0
            temp_success = 0
            try:
                temp_layer_thickness_val = float(temp_layer_thickness)
                temp_success = 1
            except:
                #print ("Unable to convert to layer thickness")
                nothing = 0
            if (temp_success == 1):
                #print("adding new layer: " + str(temp_layer_thickness_val))
                self.grbl.NewLayer(temp_layer_thickness_val, 1)
        
    
    def OpenFile(self, temp_input_file = ""):
        """Opens a file dialog, takes the filepath, and passes it to the image converter"""
        if (temp_input_file):
            temp_response = self.imageconverter.OpenFile(temp_input_file)
        else:
            self.input_file_name = QFileDialog.getOpenFileName(self, 'Open file', 
            '',"Image files (*.jpg *.png *.svg)")
            temp_response = self.imageconverter.OpenFile(self.input_file_name[0])
            
        if (temp_response == 1):
            self.RenderInput()
            self.file_loaded = 1
        if (temp_response == 2):
            self.file_loaded = 2
            self.ui.layer_slider.setMaximum(self.imageconverter.svg_layers-1)
            self.RenderOutput()
            
            
    def UpdateLayer(self):
        if (self.imageconverter.file_type == 2 and self.printing_state == 0): #if file is svg
            temp_layer = self.ui.layer_slider.value()
            self.ui.layer_slider_value.setText("Layer: " + str(temp_layer))
            self.imageconverter.SVGLayerToArray(temp_layer)
            self.RenderOutput()
            
    def PausePrint(self):
        if (self.file_loaded == 2 ): #only update pause if print is running
            if(self.printing_pause_flag == 0):
                self.printing_pause_flag = 1
                self.ui.pause_button.setText("Resume")
            else:
                self.printing_pause_flag = 0
                self.ui.pause_button.setText("Pause")
                
    def AbortPrint(self):
        if (self.file_loaded == 2): #only update pause if print is running
            #MessageBox.about(self, "Title", "Message")
            temp_response = QMessageBox.question(self, 'Abort print', "Do you really want to abort the print?",QMessageBox.Yes | QMessageBox.No)
            if (temp_response == QMessageBox.Yes):
                self.printing_abort_flag = 1
            
    
    def RenderInput(self):
        """Gets an image from the image converter class and renders it to input"""
        self.input_image_display = self.imageconverter.input_image
        if (self.input_image_display.width() > 300 and self.input_image_display.height() > 300):
            self.input_image_display = self.input_image_display.scaled(300,300, QtCore.Qt.KeepAspectRatio)
        self.ui.input_window.setPixmap(self.input_image_display)
        #self.ui.input_window.setPixmap(self.imageconverter.input_image)
        
    def RenderOutput(self):
        """Gets an image from the image converter class and renders it to output"""
        if (self.file_loaded == 1):
            temp_threshold = self.ui.threshold_slider.value()
            self.imageconverter.Threshold(temp_threshold)
            self.imageconverter.ArrayToImage()
            self.output_image_display = self.imageconverter.output_image
            if (self.output_image_display.width() > 300 and self.output_image_display.height() > 300):
                self.output_image_display = self.output_image_display.scaled(300,300, QtCore.Qt.KeepAspectRatio)
            self.ui.output_window.setPixmap(self.output_image_display)
            
        if (self.file_loaded == 2):
            self.imageconverter.ArrayToImage()
            self.output_image_display = self.imageconverter.output_image
            if (self.output_image_display.width() > 300 and self.output_image_display.height() > 300):
                self.output_image_display = self.output_image_display.scaled(300,300, QtCore.Qt.KeepAspectRatio)
            self.ui.output_window.setPixmap(self.output_image_display)
            
    def RenderAlpha(self):
        """Renders alpha mask (used for troubleshooting)"""
        self.imageconverter.AlphaMaskToImage()
        self.output_image_display = self.imageconverter.output_image
        if (self.output_image_display.width() > 300 and self.output_image_display.height() > 300):
            self.output_image_display = self.output_image_display.scaled(300,300, QtCore.Qt.KeepAspectRatio)
        self.ui.output_window.setPixmap(self.output_image_display)
        
    def RenderRGB(self):
        """Renders only RGB, ignoring alpha (used for troubleshooting)"""
        self.imageconverter.RGBToImage()
        self.output_image_display = self.imageconverter.output_image
        if (self.output_image_display.width() > 300 and self.output_image_display.height() > 300):
            self.output_image_display = self.output_image_display.scaled(300,300, QtCore.Qt.KeepAspectRatio)
        self.ui.output_window.setPixmap(self.output_image_display)
    
    def RunPrintArray(self):
        """Starts a thread for the print array function"""
        if (self.file_loaded == 1):
            self._printing_stop_event = threading.Event()
            self.printing_thread = threading.Thread(target=self.PrintArray)
            self.printing_thread.start()
        if (self.file_loaded == 2):
            self._printing_stop_event = threading.Event()
            self.printing_thread = threading.Thread(target=self.PrintSVG)
            self.printing_thread.start()
        
    def PrintSVG(self):
        """Prints the currently loaded SVG file if present.
        This will not check powder levels, ink levels and if file is much more than theoretically possible
        """
        #Todo: 
        #-Add printhead purge to the start of the print so the first sweep will work properly
        #-Re-add send code while printing. The problem with speed was traced to threading not working
        # while another thread is busy. Now there are sleep command in the While(True) blocks,
        # Giving the other threads time to do stuff.
        
        print("Starting print from SVG")
        
        #start printing if file is svg, inkjet and motion are started
        if (self.file_loaded == 2 and self.inkjet_connection_state == 1 and self.grbl_connection_state == 1):
            self.printing_state = 2 #set printing state
            self.inkjet.ClearBuffer() #clear inkjet buffer on HP45
            self.grbl.Home() #home printer
            
            #make variables
            self.build_center_x = 163.0 #where the center of the build platform is
            self.build_center_y = 111.0 #where the center of the build platform is
            self.print_speed = 3000.0 #how fast to print
            self.travel_speed = 15000.0 #how fast to travel
            self.acceleration_distance = 20.0 #how much to accelerate before printing
            self.printing_dpi = int(self.imageconverter.dpi) #the set DPI
            self.printing_sweep_size = int(self.printing_dpi / 2) #the sweep size
            self.pixel_to_pos_multiplier = 25.4 / self.printing_dpi #the value from pixel to mm 
            self.image_size_x = self.imageconverter.image_array_height #the max size of image, in X-direction
            self.image_size_y = self.imageconverter.image_array_width #the max size of image, in Y-direction
            self.layers = self.imageconverter.svg_layers #how many layers there are
            self.current_layer = 0 #the currently printed layer
            self.current_layer_height = self.imageconverter.svg_layer_height[0]
            print("Starting print at height: " + str(self.current_layer_height))
            
            #set flags
            self.printing_abort_flag = 0
            self.printing_pause_flag = 0
            
            #set inkjet settings
            self.inkjet.SetDPI(self.printing_dpi)
            
            #set motion settings
            
            #check file
            #offsets given above are assumed to be the center of bed
            #calculate offsets for centering file
            #width is Y, height is X
            #self.svg_offset_x = self.imageconverter.svg_height / 2
            #self.svg_offset_y = self.imageconverter.svg_width / 2
            #I flipped these because of a boo-boo somewhere. 
            self.svg_offset_y = self.imageconverter.svg_height / 2
            self.svg_offset_x = self.imageconverter.svg_width / 2
            
            #Wait till homing is done
            if (self.grbl_connection_state == 1): #conditional for testing, only wait for home if there is home to wait on
                while (self.grbl.motion_state != 'idle'):
                    time.sleep(0.1)
                    pass
                    
            time.sleep(0.25) #extra delay so the system can stabilize
            self.InkjetSetPosition() #set position
            time.sleep(0.25) #extra delay so position can be set
            
            #add priming purge here, with motions to start the printhead
            
            #start printing
            while(True):
                
                #load proper layer
                self.imageconverter.SVGLayerToArray(self.current_layer)
                self.ui.layer_slider.setValue(self.current_layer) #set layer slider value
                self.ui.layer_slider_value.setText("Layer: " + str(self.current_layer))
                self.RenderOutput() #render image
                print("Printing layer: " + str(self.current_layer))
                
                #hold firmware while a new layer is being deposited
                while(self.grbl.nl_state == 0): #hold firmware till layer is done
                    time.sleep(0.1)
                    pass
                    
                #check abort state
                if (self.printing_abort_flag == 1):
                    break
                
                #calculate start and end in gantry direction
                #look for X-min and X-max in image 
                self.sweep_x_min = 0
                self.sweep_x_max = 0
                temp_break_loop = 0
                #loop through image
                for h in range(0,self.image_size_x):
                    for w in range(0,self.image_size_y):
                        if (self.imageconverter.image_array[h][w] != 0):
                            self.sweep_x_min = h
                            temp_break_loop = 1
                            print("X-min on row: " + str(h))
                            break
                    if (temp_break_loop == 1):
                        break
                temp_break_loop = 0
                for h in reversed(range(0,self.image_size_x)):
                    for w in range(0,self.image_size_y):
                        if (self.imageconverter.image_array[h][w] != 0):
                            self.sweep_x_max = h
                            temp_break_loop = 1
                            print("X-max on row: " + str(h))
                            break
                    if (temp_break_loop == 1):
                        break
                        
                #calculate how many sweeps are required
                self.sweep_x_size = self.sweep_x_max - self.sweep_x_min
                print("Sweep size in pixels: " + str(self.sweep_x_size))
                if (self.sweep_x_size % int(self.printing_sweep_size) == 0):
                    temp_round = 1
                else:
                    temp_round = 0
                self.sweeps = int(self.sweep_x_size / self.printing_sweep_size)
                if (temp_round == 0):
                    self.sweeps += 1
                print("Sweeps in layer: " + str(self.sweeps))
                
                #calculate starting position and pixel
                #printer prints from x max to x min because of new layer reasons
                self.sweep_x_pix = self.sweep_x_max - self.printing_sweep_size
                
                #load sweep by sweep
                for L in range(self.sweeps):
                    print("printing sweep" + str(L))
                    
                    #set X position
                    self.sweep_x_pos = (self.sweep_x_pix * self.pixel_to_pos_multiplier) + self.build_center_x - self.svg_offset_x                     
                    
                    #calculate start and end in sweep direction
                    temp_break_loop = 0
                    for w in range(self.image_size_y):
                        for h in range(int(self.sweep_x_pix), int(self.sweep_x_pix + self.printing_sweep_size)): 
                            if (h > 0): #if h is within bounds
                                if (self.imageconverter.image_array[h][w] != 0):
                                    self.sweep_y_min = w
                                    temp_break_loop = 1
                                    break
                        if (temp_break_loop == 1):
                            break
                    #get Y max
                    temp_break_loop = 0
                    for w in reversed(range(self.image_size_y)):
                        for h in range(int(self.sweep_x_pix), int(self.sweep_x_pix + self.printing_sweep_size)):
                            if (h > 0): #if h is within bounds
                                if (self.imageconverter.image_array[h][w] != 0):
                                    self.sweep_y_max = w
                                    temp_break_loop = 1
                                    break
                        if (temp_break_loop == 1):
                            break                    
                    
                    #calculate position
                    self.sweep_y_start_pix = self.sweep_y_min
                    self.sweep_y_end_pix = self.sweep_y_max
                    self.sweep_y_start_pos = (self.sweep_y_start_pix * self.pixel_to_pos_multiplier) + self.build_center_y - self.svg_offset_y - self.acceleration_distance
                    self.sweep_y_end_pos = (self.sweep_y_end_pix * self.pixel_to_pos_multiplier) + self.build_center_y - self.svg_offset_y + self.acceleration_distance
                    print("Sweep from: " + str(self.sweep_y_start_pos) + ", to: " + str(self.sweep_y_end_pos))
                            
                    #fill inkjet buffer ------------------------------------------
                    print("Filling local buffer with inkjet")
                    temp_line_history = ""
                    temp_line_string = ""
                    temp_line_array = zeros(self.printing_sweep_size)
                    temp_line_history = B64.B64ToArray(temp_line_array) #make first history 0
                    temp_line_string = temp_line_history #make string also 0
                    
                    #add all of starter cap at the front
                    temp_pos = ((self.sweep_y_start_pix - 1) * self.pixel_to_pos_multiplier) + self.build_center_y - self.svg_offset_y
                    temp_pos *= 1000 #printhead pos is in microns
                    temp_b64_pos = B64.B64ToSingle(temp_pos) #make position value
                    self.inkjet.SerialWriteBufferRaw("SBR " + str(temp_b64_pos) + " " + str(temp_line_string))
                    print("SBR " + str(temp_b64_pos) + " " + str(temp_line_string) + ", real pos: " + str(temp_pos)) 
                        
                    for w in range(self.sweep_y_start_pix,self.sweep_y_end_pix):
                        #print("Parsing line: " + str(w))
                        temp_line_changed = 0 #reset changed
                        temp_counter = 0 
                        for h in range(int(self.sweep_x_pix), int(self.sweep_x_pix + self.printing_sweep_size)):
                            #loop through all pixels to make a new burst
                            #while counting down h will become negative, breaking the array
                            #if h lower than 0, value defaults to 0
                            if (h >= 0): 
                                temp_line_array[temp_counter] = self.imageconverter.image_array[h][w] #write array value to temp
                            else:
                                temp_line_array[temp_counter] = 0
                            temp_counter += 1
                        temp_line_string = B64.B64ToArray(temp_line_array) #convert to string
                        if (temp_line_string != temp_line_history):
                            #print("line changed on pos: " + str(w))
                            temp_line_history = temp_line_string
                            #add line to buffer
                            temp_pos = (w * self.pixel_to_pos_multiplier) + self.build_center_y - self.svg_offset_y
                            temp_pos *= 1000 #printhead pos is in microns
                            temp_b64_pos = B64.B64ToSingle(temp_pos) #make position value
                            self.inkjet.SerialWriteBufferRaw("SBR " + str(temp_b64_pos) + " " + str(temp_line_string))
                            print("SBR " + str(temp_b64_pos) + " " + str(temp_line_string) + ", real pos: " + str(temp_pos)) 
                    
                    #add all off cap at the end of the image
                    temp_line_array = zeros(self.printing_sweep_size)
                    temp_line_string = B64.B64ToArray(temp_line_array)
                    temp_pos = ((self.sweep_y_end_pix + 1) * self.pixel_to_pos_multiplier) + self.build_center_y - self.svg_offset_y
                    temp_pos *= 1000 #printhead pos is in microns
                    temp_b64_pos = B64.B64ToSingle(temp_pos) #make position value
                    self.inkjet.SerialWriteBufferRaw("SBR " + str(temp_b64_pos) + " " + str(temp_line_string))
                    print("SBR " + str(temp_b64_pos) + " " + str(temp_line_string) + ", real pos: " + str(temp_pos)) 
                        
                    print("Making printing buffer done: ")
                    #end of fill inkjet buffer -----------------------------------
                    #move to start of sweep position
                    self.grbl.SerialGotoXY(self.sweep_x_pos, self.sweep_y_start_pos, self.travel_speed)
                    self.grbl.StatusIndexSet() #set current status index 
                    while (True): #wait till the printhead is at start position
                        time.sleep(0.1)
                        if (self.grbl.StatusIndexChanged() == 1 and self.grbl.motion_state == 'idle'):
                            #print("break conditions for print while loop")
                            break #break if exit conditions met
                    
                    #wait till inkjet is loaded and motion is done
                    while(self.inkjet.BufferLeft() >0):
                        time.sleep(0.1)
                        pass
                    
                    #set current position to inkjet
                    time.sleep(0.2)
                    self.InkjetSetPosition()
                    time.sleep(0.2)
                    
                    #fill motion buffer with end of sweep
                    self.grbl.SerialGotoXY(self.sweep_x_pos, self.sweep_y_end_pos, self.print_speed)
                    self.grbl.StatusIndexSet() #set current status index 
                    while (True): #wait till the printhead is at home
                        time.sleep(0.1)
                        if (self.grbl.StatusIndexChanged() == 1 and self.grbl.motion_state == 'idle'):
                            #print("break conditions for print while loop")
                            break #break if exit conditions met
                    
                    #check pause state
                    #if pause state, go to home pos and wait till restart
                    if (self.printing_pause_flag == 1):
                        #goto home and wait to reach position
                        self.grbl.SerialGotoHome(self.travel_speed)
                        self.grbl.StatusIndexSet() #set current status index 
                        while (True): #wait till the printhead is at home
                            if (self.grbl.StatusIndexChanged() == 1 and self.grbl.motion_state == 'idle' and self.printing_pause_flag == 0):
                                #print("break conditions for print while loop")
                                break #break if exit conditions met
                    
                    #check abort state
                    if (self.printing_abort_flag == 1):
                        break
                    
                    #set next sweep
                    self.sweep_x_pix = self.sweep_x_pix - self.printing_sweep_size
                    
                    #return to load sweep
                
                #return to load layer
                self.current_layer += 1
                if (self.current_layer >= self.layers):
                    print("Last layer printed")
                    break
                    
                #check exit conditions
                if (self.printing_abort_flag == 1):
                    print("Print aborted")
                    break
                    
                #Add next layer
                temp_layer_thickness = self.imageconverter.svg_layer_height[self.current_layer] - self.current_layer_height
                print("Adding new layer, thickness: " + str(temp_layer_thickness))
                self.current_layer_height = self.imageconverter.svg_layer_height[self.current_layer]
                self.grbl.NewLayer(temp_layer_thickness)
                
                
            #if all layers printed or stop button pressed, exit
            if (self.grbl_connection_state == 1): #conditional for testing, only wait for goto home if there is motion to wait on
                self.grbl.SerialGotoHome(self.travel_speed)
                self.grbl.StatusIndexSet() #set current status index 
                while (True): #wait till the printhead is at home
                    if (self.grbl.StatusIndexChanged() == 1 and self.grbl.motion_state == 'idle'):
                        #print("break conditions for print while loop")
                        break #break if exit conditions met
                    
            self.printing_state = 0 #set printing to stopped
        
        
    
    def PrintArray(self):
        """Prints the current converted image array, only works if both inkjet and motion are connected"""
        #y is sweep direction, x is gantry direction
        #Width is Y direction, height is X direction
        
        #check if printhead and motion are connected
        if (self.grbl_connection_state == 0): #do not continue if motion is not connected
            return
        #inkjet is ignored for now
            
        
        #make universal variables
        self.inkjet_line_buffer = [] #buffer storing the print lines
        self.inkjet_lines_left = 0 #the number of lines in buffer
        self.inkjet_line_history = "" #the last burst line sent to buffer
        self.travel_speed = 12000.0
        self.print_speed = 3000.0
        
        self.inkjet.ClearBuffer() #clear inkjet buffer on HP45
        
        self.grbl.Home() #home gantry
        
        
        #look for X-min and X-max in image 
        self.sweep_x_min = 0
        self.sweep_x_max = 0
        temp_break_loop = 0
        #loop through image
        for h in range(0,self.imageconverter.image_array_height):
            for w in range(0,self.imageconverter.image_array_width):
                if (self.imageconverter.image_array[h][w] != 0):
                    self.sweep_x_min = h
                    temp_break_loop = 1
                    print("X-min on row: " + str(h))
                    break
            if (temp_break_loop == 1):
                break
        temp_break_loop = 0
        for h in reversed(range(0,self.imageconverter.image_array_height)):
            for w in range(0,self.imageconverter.image_array_width):
                if (self.imageconverter.image_array[h][w] != 0):
                    self.sweep_x_max = h
                    temp_break_loop = 1
                    print("X-max on row: " + str(h))
                    break
            if (temp_break_loop == 1):
                break
                
        #set X start pixel, X pixel step (using current DPI)
        self.sweep_size = int(self.imageconverter.GetDPI() / 2) #get sweep size (is halve of DPI)
        print("Sweep size: " + str(self.sweep_size))
        #determine pixel to position multiplier (in millimeters)
        self.pixel_to_pos_multiplier = 25.4 / self.imageconverter.GetDPI() 
        #determine x and y start position (in millimeters)
        self.y_start_pos = 100.0
        self.x_start_pos = 150.0
        self.y_acceleration_distance = 25.0
        
        self.sweep_x_min_pos = self.sweep_x_min
        ###loop through all sweeps
        temp_sweep_stop = 0
        while (temp_sweep_stop == 0):
            #determine if there still is a sweep left
            #determine X-start and X end of sweep
            if (self.sweep_x_min_pos + self.sweep_size <= self.sweep_x_max):
                self.sweep_x_max_pos = self.sweep_x_min_pos + self.sweep_size
            else:
                self.sweep_x_max_pos = self.sweep_x_max #set max of image as max pos
                temp_sweep_stop = 1 #mark last loop
            print("Sweep from: " + str(self.sweep_x_min_pos) + ", to: " + str(self.sweep_x_max_pos))
            
            
            #Look for Y min and Y max in sweep
            self.sweep_y_min = 0
            self.sweep_y_max = 0
            #get Y min
            temp_break_loop = 0
            for w in range(self.imageconverter.image_array_width):
                for h in range(self.sweep_x_min_pos, self.sweep_x_max_pos):
                    if (self.imageconverter.image_array[h][w] != 0):
                        self.sweep_y_min = w
                        temp_break_loop = 1
                        break
                if (temp_break_loop == 1):
                    break
            #get Y max
            temp_break_loop = 0
            for w in reversed(range(self.imageconverter.image_array_width)):
                for h in range(self.sweep_x_min_pos, self.sweep_x_max_pos):
                    if (self.imageconverter.image_array[h][w] != 0):
                        self.sweep_y_max = w
                        temp_break_loop = 1
                        break
                if (temp_break_loop == 1):
                    break
            print("sweep Y min: " + str(self.sweep_y_min) +", Y max: " + str(self.sweep_y_max))
            
            #determine printing direction (if necessary)
            self.printing_direction = 1 #only 1 for now
            
            #Set Y at starting and end position
            if (self.printing_direction == 1):
                self.y_printing_start_pos = self.sweep_y_min * self.pixel_to_pos_multiplier
                self.y_printing_start_pos += self.y_start_pos - self.y_acceleration_distance
                self.y_printing_end_pos = self.sweep_y_max * self.pixel_to_pos_multiplier
                self.y_printing_end_pos += self.y_start_pos + self.y_acceleration_distance
                print("Sweep ranges from: " + str(self.y_printing_start_pos) + "mm, to: " + str(self.y_printing_end_pos) + "mm")
            
            #set X position
            self.x_printing_pos = self.sweep_x_min_pos * self.pixel_to_pos_multiplier
            self.x_printing_pos += self.x_start_pos
            
            #fill local print buffer with lines
            print("Filling local buffer with inkjet")
            temp_line_history = ""
            temp_line_string = ""
            temp_line_array = zeros(self.sweep_size)
            temp_line_history = B64.B64ToArray(temp_line_array) #make first history 0
            temp_line_string = temp_line_history #make string also 0
            
            #add all of starter cap at the front
            if (self.printing_direction == 1):
                temp_pos = ((self.sweep_y_min - 1) * self.pixel_to_pos_multiplier) + self.y_start_pos
                temp_pos *= 1000 #printhead pos is in microns
                temp_b64_pos = B64.B64ToSingle(temp_pos) #make position value
                self.inkjet_line_buffer.append("SBR " + str(temp_b64_pos) + " " + str(temp_line_string))
                self.inkjet_lines_left += 1
                
            for w in range(self.sweep_y_min,self.sweep_y_max):
                #print("Parsing line: " + str(w))
                temp_line_changed = 0 #reset changed
                temp_counter = 0
                for h in range(self.sweep_x_min_pos, self.sweep_x_max_pos):
                    #loop through all pixels to make a new burst
                    temp_line_array[temp_counter] = self.imageconverter.image_array[h][w] #write array value to temp
                    
                    temp_counter += 1
                temp_line_string = B64.B64ToArray(temp_line_array) #convert to string
                if (temp_line_string != temp_line_history):
                    #print("line changed on pos: " + str(w))
                    temp_line_history = temp_line_string
                    #add line to buffer
                    temp_pos = (w * self.pixel_to_pos_multiplier) + self.y_start_pos
                    temp_pos *= 1000 #printhead pos is in microns
                    temp_b64_pos = B64.B64ToSingle(temp_pos) #make position value
                    self.inkjet_line_buffer.append("SBR " + str(temp_b64_pos) + " " + str(temp_line_string))
                    self.inkjet_lines_left += 1
            
            #add all off cap at the end of the image
            temp_line_array = zeros(self.sweep_size)
            temp_line_string = B64.B64ToArray(temp_line_array)
            if (self.printing_direction == 1):
                temp_pos = ((self.sweep_y_max + 1) * self.pixel_to_pos_multiplier) + self.y_start_pos
                temp_pos *= 1000 #printhead pos is in microns
                temp_b64_pos = B64.B64ToSingle(temp_pos) #make position value
                self.inkjet_line_buffer.append("SBR " + str(temp_b64_pos) + " " + str(temp_line_string))
                self.inkjet_lines_left += 1
                
            print("Making printing buffer done: ")
            #print(self.inkjet_line_buffer)
            
            #wait till the head is idle
            while (self.grbl.motion_state != 'idle'):
                nothing = 0
            print("break from idle, moving to filling buffers")
            
            
            
            #match inkjet and printer pos
            self.InkjetSetPosition()
            
            #Fill inkjet buffer with with sweep lines
            print("Filling inkjet buffer")
            #start filling the inkjet buffer on the HP45 lines
            temp_lines_sent = 0
            while(True):
                if (self.inkjet_lines_left > 0):
                    self.inkjet.SerialWriteBufferRaw(self.inkjet_line_buffer[0])
                    #time.sleep(0.001) #this is a good replacement for print, but takes forever
                    print(str(self.inkjet_line_buffer[0])) #some sort of delay is required, else the function gets filled up too quickly. Will move to different buffer later
                    del self.inkjet_line_buffer[0] #remove sent line
                    self.inkjet_lines_left -= 1
                    temp_lines_sent += 1
                else:
                    break
            
            
            #send motion lines
            print("Filling motion buffer")
            self.grbl.SerialGotoXY(self.x_printing_pos, self.y_printing_start_pos, self.travel_speed)
            self.grbl.SerialGotoXY(self.x_printing_pos, self.y_printing_end_pos, self.print_speed) 
            self.grbl.StatusIndexSet() #set current status index 
            
            
            while (True):
                if (self.grbl.StatusIndexChanged() == 1 and self.grbl.motion_state == 'idle'):
                    print("break conditions for print while loop")
                    break #break if exit conditions met
            
            self.sweep_x_min_pos += self.sweep_size
        ###end of loop through sweep
        #repeat loop until all sweeps are finished
        print("Printing done")
        #home gantry
        #self.grbl.Home() #home gantry
        
    def SavePng(self):
        """Saves current SVG to array of bitmap images, enables camera"""
        if (self.file_loaded == 2): #if a file is present
            if not os.path.exists('demo'):
                os.makedirs('demo')#make demo folder
            
            #run through all layers of the file
            for L in range(self.imageconverter.svg_layers):
                #save each of the files to the demo folder
                print("Layer" + str(L))
                self.imageconverter.SVGLayerToArray(L)
                self.RenderOutput() #render image
                self.imageconverter.output_image.save("demo\Layer" + str(L) + ".png", "PNG") 
                
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainWindow()
    sys.exit(app.exec_())


