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


##The interface holds the user interface for Oasis controller

#Todo list
#-Add status bar or status window to give updates that are now given
#in the comandline


import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit,
    QTextEdit, QGridLayout, QApplication, QPushButton, QDesktopWidget,
    QSlider, QComboBox)
from PyQt5.QtGui import QIcon, QPixmap, QFont



class Interface(QWidget):
    def __init__(self):
        super().__init__()
        #self.initUI()
        
    def initUI(self):	
        grid = QGridLayout()
        self.setLayout(grid)
        
        #set labels
        self.motion_title = QLabel('Motion Connection', self)
        self.inkjet_title = QLabel('Inkjet Connection', self) 
        self.image_title = QLabel('Image', self) 
        self.motion_function_title = QLabel('Motion Functions', self)   
        self.inkjet_function_title = QLabel('Inkjet Functions', self)
        
        self.motion_x_pos_title = QLabel('X Position', self)
        self.motion_y_pos_title = QLabel('Y Position', self)
        self.motion_f_pos_title = QLabel('F Position', self)
        self.motion_b_pos_title = QLabel('B Position', self)
        self.motion_state_title = QLabel('State', self)
        
        self.inkjet_pos_title = QLabel('Position', self)
        self.inkjet_temp_title = QLabel('Temperature', self)
        self.inkjet_writeleft_title = QLabel('Buffer Write left', self)
        self.threshold_slider_value = QLabel('Threshold: 128', self)
        self.layer_slider_value = QLabel('Layer: 0', self)
        self.dpi_title = QLabel('DPI', self)
        
        #Set buttons	
        self.motion_connect = QPushButton('Connect', self)
        self.motion_send_line = QPushButton('Send', self)
        self.inkjet_connect = QPushButton('Connect', self)
        self.inkjet_send_line = QPushButton('Send', self)
        self.motion_home = QPushButton('Home', self)
        self.motion_goto_home = QPushButton('Goto Home', self)
        self.motion_xp = QPushButton('X+', self)
        self.motion_xn = QPushButton('X-', self)
        self.motion_yp = QPushButton('Y+', self)
        self.motion_yn = QPushButton('Y-', self)
        self.motion_fu = QPushButton('Feed up', self)
        self.motion_fd = QPushButton('Feed down', self)
        self.motion_bu = QPushButton('Build up', self)
        self.motion_bd = QPushButton('Build down', self)
        self.motion_spreader = QPushButton('Spreader on', self)
        self.motion_new_layer = QPushButton('New layer', self)
        self.motion_prime_layer = QPushButton('Prime layer', self)
        self.inkjet_set_pos = QPushButton('Set Position', self)
        self.inkjet_preheat = QPushButton('Preheat', self)
        self.inkjet_prime = QPushButton('Prime', self)
        #self.inkjet_set_dpi = QPushButton('Set DPI', self)
        self.inkjet_set_density = QPushButton('Set Density', self)
        self.inkjet_test_button = QPushButton('Test', self)
        self.file_open_button = QPushButton('Open', self)
        self.file_convert_button = QPushButton('Convert', self)
        #self.save_png = QPushButton('Save PNG', self)
        self.file_print_button = QPushButton('Print', self)
        self.pause_button = QPushButton('Pause', self)
        self.abort_button = QPushButton('Abort', self)
        

        
        #set input lineedits
        self.motion_set_port = QLineEdit(self)
        self.motion_write_line = QLineEdit(self)
        self.motion_layer_thickness = QLineEdit(self)
        self.inkjet_set_port = QLineEdit(self)
        self.inkjet_write_line = QLineEdit(self)
        #self.inkjet_dpi = QLineEdit(self)
        self.inkjet_density = QLineEdit(self)
        #self.motion_speed = QLineEdit(self)
        
        #set output textedits
        self.motion_serial_output = QTextEdit(self)
        self.motion_serial_output.setReadOnly(True)
        self.motion_serial_output.setLineWrapMode(QTextEdit.NoWrap)
        self.motion_serial_input = QTextEdit(self)
        self.motion_serial_input.setReadOnly(True)
        self.motion_serial_input.setLineWrapMode(QTextEdit.NoWrap)
        
        self.inkjet_serial_output = QTextEdit(self)
        self.inkjet_serial_output.setReadOnly(True)
        self.inkjet_serial_output.setLineWrapMode(QTextEdit.NoWrap)
        self.inkjet_serial_input = QTextEdit(self)
        self.inkjet_serial_input.setReadOnly(True)
        self.inkjet_serial_input.setLineWrapMode(QTextEdit.NoWrap)
        
        #output lineedits
        self.motion_x_pos = QLineEdit(self)
        self.motion_x_pos.setReadOnly(True)
        self.motion_y_pos = QLineEdit(self)
        self.motion_y_pos.setReadOnly(True)
        self.motion_f_pos = QLineEdit(self)
        self.motion_f_pos.setReadOnly(True)
        self.motion_b_pos = QLineEdit(self)
        self.motion_b_pos.setReadOnly(True)
        self.motion_state = QLineEdit(self)
        self.motion_state.setReadOnly(True)
        
        self.inkjet_pos = QLineEdit(self)
        self.inkjet_pos.setReadOnly(True)
        self.inkjet_temperature = QLineEdit(self)
        self.inkjet_temperature.setReadOnly(True)
        self.inkjet_writeleft = QLineEdit(self)
        self.inkjet_writeleft.setReadOnly(True)
        self.inkjet_test_state = QLineEdit(self)
        self.inkjet_test_state.setReadOnly(True)
        
        #create image objects
        self.input_window = QLabel(self)
        self.output_window = QLabel(self) 
        
        #create sliders
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255) 
        self.threshold_slider.setValue(128)
        
        self.layer_slider = QSlider(Qt.Horizontal)
        self.layer_slider.setMinimum(0)
        self.layer_slider.setMaximum(0) 
        self.layer_slider.setValue(0)
        
        #create combobox dropdown
        self.dpi_combo = QComboBox()
        self.dpi_combo.addItems(["600","300","200","150"])
        
        
        #fix to grid  
        grid.addWidget(self.input_window,0,0,12,12) 
        grid.addWidget(self.output_window,0,12,12,12)
        
        grid.addWidget(self.motion_title,0,24,2,12) 
        grid.addWidget(self.motion_set_port,2,24,2,8) 
        grid.addWidget(self.motion_connect,2,32,2,4)
        grid.addWidget(self.motion_serial_output,4,24,4,12)
        grid.addWidget(self.motion_write_line,8,24,2,8) 
        grid.addWidget(self.motion_send_line,8,32,2,4)
        grid.addWidget(self.motion_serial_input,10,24,2,12)
        
        grid.addWidget(self.inkjet_title,12,24,2,12) 
        grid.addWidget(self.inkjet_set_port,14,24,2,8) 
        grid.addWidget(self.inkjet_connect,14,32,2,4)
        grid.addWidget(self.inkjet_serial_output,16,24,4,12)
        grid.addWidget(self.inkjet_write_line,20,24,2,8) 
        grid.addWidget(self.inkjet_send_line,20,32,2,4)
        grid.addWidget(self.inkjet_serial_input,22,24,4,12)
        
        grid.addWidget(self.motion_function_title,12,0,1,12)
        grid.addWidget(self.motion_home,14,0,1,2)
        grid.addWidget(self.motion_spreader,14,4,1,2)
        #grid.addWidget(self.motion_speed,14,4,1,2)
        grid.addWidget(self.motion_yp,14,2,1,2)
        grid.addWidget(self.motion_yn,16,2,1,2)
        grid.addWidget(self.motion_xp,15,4,1,2)
        grid.addWidget(self.motion_xn,15,0,1,2)
        grid.addWidget(self.motion_goto_home,15,2,1,2)
        grid.addWidget(self.motion_fu,17,0,1,2)
        grid.addWidget(self.motion_fd,18,0,1,2)
        grid.addWidget(self.motion_bu,17,4,1,2)
        grid.addWidget(self.motion_bd,18,4,1,2)
        grid.addWidget(self.motion_new_layer,19,4,1,2)
        grid.addWidget(self.motion_prime_layer,20,4,1,2)
        grid.addWidget(self.motion_layer_thickness,19,0,1,4)
        grid.addWidget(self.motion_x_pos_title,22,0,1,2)
        grid.addWidget(self.motion_y_pos_title,23,0,1,2)
        grid.addWidget(self.motion_f_pos_title,24,0,1,2)
        grid.addWidget(self.motion_b_pos_title,25,0,1,2)
        grid.addWidget(self.motion_state_title,26,0,1,2)
        grid.addWidget(self.motion_x_pos,22,2,1,4)
        grid.addWidget(self.motion_y_pos,23,2,1,4)
        grid.addWidget(self.motion_f_pos,24,2,1,4)
        grid.addWidget(self.motion_b_pos,25,2,1,4)
        grid.addWidget(self.motion_state,26,2,1,4)
        
        grid.addWidget(self.inkjet_function_title,19,12,1,12)
        grid.addWidget(self.inkjet_set_pos, 20,12,1,2)
        grid.addWidget(self.inkjet_preheat, 20,14,1,2)
        grid.addWidget(self.inkjet_prime, 20,16,1,2)
        #grid.addWidget(self.inkjet_dpi, 21,12,1,4)
        
        grid.addWidget(self.inkjet_density, 22,12,1,4)
        grid.addWidget(self.inkjet_test_button,23,12,1,2)
        grid.addWidget(self.inkjet_test_state,23,14,1,4)
        #grid.addWidget(self.inkjet_set_dpi, 21,16,1,2)
        
        grid.addWidget(self.inkjet_set_density, 22,16,1,2)
        grid.addWidget(self.inkjet_pos_title,24,12,1,2)
        grid.addWidget(self.inkjet_temp_title,25,12,1,2)
        grid.addWidget(self.inkjet_writeleft_title,26,12,1,2)
        grid.addWidget(self.inkjet_pos,24,14,1,4)
        grid.addWidget(self.inkjet_temperature,25,14,1,4)
        grid.addWidget(self.inkjet_writeleft,26,14,1,4)
        
        grid.addWidget(self.image_title,12,12,1,12)
        grid.addWidget(self.layer_slider,13,12,1,4)
        grid.addWidget(self.layer_slider_value,13,16,1,2)
        grid.addWidget(self.file_open_button,14,12,1,2)
        grid.addWidget(self.file_convert_button,14,14,1,2)
        #grid.addWidget(self.save_png,14,16,1,2)
        grid.addWidget(self.threshold_slider,15,12,1,4)
        grid.addWidget(self.threshold_slider_value,15,16,1,2)
        
        grid.addWidget(self.file_print_button,16,12,1,2)
        grid.addWidget(self.pause_button,16,14,1,2)
        grid.addWidget(self.abort_button,16,16,1,2)
        
        grid.addWidget(self.dpi_combo, 17,12,1,2)
        grid.addWidget(self.dpi_title, 17,14,1,2)
        
        
        #set tooltips
        self.motion_connect.setToolTip("The COM port the GRBL is on. 'COM#' for Windows, '/dev/ttyUSB#' for Linux") 
        self.inkjet_connect.setToolTip("The COM port the HP45 is on. 'COM#' for Windows, '/dev/ttyUSB#' for Linux") 
        self.motion_send_line.setToolTip("Send a raw command to the GRBL") 
        self.inkjet_send_line.setToolTip("Send a raw command to the HP45")
        self.motion_new_layer.setToolTip("Add a new layer by moving feed up, build down and transering the powder using the spreader [mm]")
        self.motion_prime_layer.setToolTip("Add a new layer of powder without moving build [mm]")
        self.inkjet_preheat.setToolTip("Send a burst of short pulses to the printhead, heating up the printhead without ejecting (much) ink")
        self.inkjet_prime.setToolTip("Send a burst of long pulses to the printhead, ejecting with each nozzle")
        
        
        #slider update
        self.threshold_slider.valueChanged.connect(self.UpdateThresholdSliderValue) 
        
        
        
        
        
        self.setFixedSize(1200, 800)
        self.center()
        self.setWindowTitle('Oasis Controller')
        self.setWindowIcon(QIcon('yteclogo.png')) 
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def UpdateThresholdSliderValue(self):
        """Updates the value next to the threshold slider"""
        temp_threshold = self.threshold_slider.value()
        self.threshold_slider_value.setText("Threshold: " + str(temp_threshold))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Interface()
    ex.initUI()
    sys.exit(app.exec_())
    

    
    
