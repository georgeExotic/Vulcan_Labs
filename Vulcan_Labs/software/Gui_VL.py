import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit,
    QTextEdit, QGridLayout, QApplication, QPushButton, QDesktopWidget,
    QSlider, QComboBox, QButtonGroup, QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap, QFont

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        #self.initUI()
       
    def initUI(self):	
        grid = QGridLayout()
        self.setLayout(grid)

        #set labels
        ##self.endLabel = QLabel('E',self)
        self.function_label = QLabel('Additonal Functions',self)
        self.function_label.setFixedWidth(400)
        self.function_label.setFont(QFont('Arial', 14))
        self.main_label = QLabel('Main Operation',self)
        self.main_label.setFixedWidth(400)
        self.main_label.setFixedHeight(100)
        self.main_label.setFont(QFont('Arial', 14))
        self.feedback_label = QLabel('             Feedback',self)
        self.feedback_label.setFixedWidth(400)
        self.feedback_label.setFont(QFont('Arial', 14))
        self.sysStatus_label = QLabel('            System Status: ',self)
        self.sysStatus_label.setFont(QFont('Arial', 10))
        self.desiredParam_label = QLabel('Desired End Parameter: ',self)
        self.desiredParam_label.setFont(QFont('Arial', 10))
        self.currentValue_label = QLabel('             Current Value: ',self)
        self.currentValue_label.setFont(QFont('Arial', 10))
        self.forceSensorValue_label = QLabel('  Force Sensor Reading: ',self)
        self.forceSensorValue_label.setFont(QFont('Arial', 10))

        self.cycle_slider_value = QLabel('Number of Cycles: 3 cycles',self)
        self.cycle_slider_value.setFont(QFont('Arial',10))
        self.pressure_slider_value = QLabel('    Desired Pressure: 100 kPa', self)
        self.pressure_slider_value.setFont(QFont('Arial',10))
        self.depth_slider_value = QLabel('    Desired Compaction Depth: 10 mm',self)
        self.depth_slider_value.setFont(QFont('Arial',10))
        self.layer_slider_value = QLabel('    Desired Layer Count: 2 layers',self)
        self.layer_slider_value.setFont(QFont('Arial',10))

        #self.pressure_slider_value = QLabel('Pressure: 50 kPa', self)
        # self.motion_title = QLabel('Motion Connection', self) 
        # self.motion_function_title = QLabel('Motion Functions', self)   
        
        # self.motion_x_pos_title = QLabel('X Position', self)
        # self.motion_y_pos_title = QLabel('Y Position', self)
        # self.motion_state_title = QLabel('State', self)
        
        # self.pressure_slider_value = QLabel('Pressure: 50 kPa', self)
        
        # -- Set buttons
        # self.compact_compact = QPushButton('Compact', self)
        # self.compact_estop = QPushButton('Emergency Stop', self)
        # self.compact_clean = QPushButton('Clean', self)
        # self.compact_resume = QPushButton('Resume', self)
        # self.compact_pause = QPushButton('Pause', self)

        # self.motion_connect = QPushButton('Connect', self)
        # self.motion_send_line = QPushButton('Send', self)

        self.motion_home = QPushButton('Home', self)
        self.motion_home.setFixedWidth(100)
        self.motion_goto_home = QPushButton('Goto Home', self)
        self.motion_goto_home.setFixedWidth(100)
        self.motion_xp = QPushButton('X+', self)
        self.motion_xp.setFixedWidth(100)
        self.motion_xn = QPushButton('X-', self)
        self.motion_xn.setFixedWidth(100)
        self.motion_yp = QPushButton('Z+', self)
        self.motion_yp.setFixedWidth(100)
        self.motion_yn = QPushButton('Z-', self)
        self.motion_yn.setFixedWidth(100)

        self.run = QPushButton('Run',self)
        self.run.setFixedWidth(100)
        self.stop = QPushButton('Stop',self)
        self.stop.setFixedWidth(100)
        self.pause = QPushButton('Pause',self)
        self.pause.setFixedWidth(100)
        self.resume = QPushButton('Resume',self)
        self.resume.setFixedWidth(100)
        self.reset = QPushButton('Reset', self)
        self.reset.setFixedWidth(100)

        #set checkboxes
        self.bg = QButtonGroup()
        self.serviceMode = QCheckBox("Service Mode")
        self.serviceMode.setFont(QFont('Arial', 10))
        self.bg.addButton(self.serviceMode,1)
        self.mimicPrint = QCheckBox("Print Demo")
        self.mimicPrint.setFont(QFont('Arial', 10))
        self.bg.addButton(self.mimicPrint,2)
        self.pressureSelect = QCheckBox("")
        self.pressureSelect.setFont(QFont('Arial', 10))
        self.bg.addButton(self.pressureSelect,3)
        self.depthSelect = QCheckBox("")
        self.depthSelect.setFont(QFont('Arial', 10))
        self.bg.addButton(self.depthSelect,4)
        self.layerSelect = QCheckBox("")
        self.layerSelect.setFont(QFont('Arial', 10))
        self.bg.addButton(self.layerSelect,5)
    
        #set input lineedits
        self.pressure_set = QLineEdit(self)
        self.pressure_set.setFixedWidth(30)
        self.depth_set = QLineEdit(self)
        self.depth_set.setFixedWidth(30)
        self.layer_set = QLineEdit(self)
        self.layer_set.setFixedWidth(30)
        # self.motion_set_port = QLineEdit(self)
        # self.motion_write_line = QLineEdit(self)
        # self.motion_layer_thickness = QLineEdit(self)
        
        #set output textedits
        # self.feedback_output_read = QTextEdit(self)
        # self.feedback_output_read.setReadOnly(True)
        # self.feedback_output_read.setLineWrapMode(QTextEdit.NoWrap)

        # self.compaction_serial_output = QTextEdit(self)
        # self.compaction_serial_output.setReadOnly(True)
        # self.compaction_serial_output.setLineWrapMode(QTextEdit.NoWrap)

        # self.motion_serial_output = QTextEdit(self)
        # self.motion_serial_output.setReadOnly(True)
        # self.motion_serial_output.setLineWrapMode(QTextEdit.NoWrap)
        # self.motion_serial_input = QTextEdit(self)
        # self.motion_serial_input.setReadOnly(True)
        # self.motion_serial_input.setLineWrapMode(QTextEdit.NoWrap)
        
        #output lineedits
        # self.motion_x_pos = QLineEdit(self)
        # self.motion_x_pos.setReadOnly(True)
        # self.motion_y_pos = QLineEdit(self)
        # self.motion_y_pos.setReadOnly(True)
        # self.motion_f_pos = QLineEdit(self)
        # self.motion_f_pos.setReadOnly(True)
        # self.motion_b_pos = QLineEdit(self)
        # self.motion_b_pos.setReadOnly(True)
        # self.motion_state = QLineEdit(self)
        # self.motion_state.setReadOnly(True)
        
        #create image objects
        # self.input_window = QLabel(self)
        # self.output_window = QLabel(self) 
        
        #create sliders
        self.pressure_slider = QSlider(Qt.Horizontal)
        self.pressure_slider.setMinimum(0)
        self.pressure_slider.setMaximum(100)
        self.pressure_slider.setValue(50)
        self.pressure_slider.setFixedWidth(190)

        self.depth_slider = QSlider(Qt.Horizontal)
        self.depth_slider.setMinimum(0)
        self.depth_slider.setMaximum(100)
        self.depth_slider.setValue(50)
        self.depth_slider.setFixedWidth(190)

        self.layer_slider = QSlider(Qt.Horizontal)
        self.layer_slider.setMinimum(0)
        self.layer_slider.setMaximum(100)
        self.layer_slider.setValue(50)
        self.layer_slider.setFixedWidth(190)

        self.cycle_slider = QSlider(Qt.Horizontal)
        self.cycle_slider.setMinimum(1)
        self.cycle_slider.setMaximum(50)
        self.cycle_slider.setValue(3)
        self.cycle_slider.setFixedWidth(190)
        
        #fix to grid  

        # -- Col1

####   ADDED LOGO HERE

        logo = QLabel(self)
        pixmap = QPixmap('VulcanLabsLogo.png')
        # pixmap = pixmap.scaled(200*1.6, 200*1.6, Qt.KeepAspectRatio)
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        logo.setPixmap(pixmap)
        grid.addWidget(logo,1,2,1,4)

################################################################################

        grid.addWidget(self.function_label,2,2,1,4)
        grid.addWidget(self.serviceMode,4,1,1,2)
        grid.addWidget(self.mimicPrint,6,1,1,2)
        grid.addWidget(self.cycle_slider,5,1,1,2)
        grid.addWidget(self.cycle_slider_value,7,1,1,3)

        grid.addWidget(self.motion_goto_home,8,1,1,1)
        grid.addWidget(self.motion_home,9,2,1,1)
        grid.addWidget(self.motion_xn,9,1,1,1)
        grid.addWidget(self.motion_xp,9,3,1,1)
        grid.addWidget(self.motion_yn,10,2,1,1)
        grid.addWidget(self.motion_yp,8,2,1,1)

        # -- Col2
        grid.addWidget(self.main_label,1,6,1,4)
        grid.addWidget(self.pressureSelect,2,5,1,2)
        grid.addWidget(self.pressure_slider_value,2,5,1,3)
        grid.addWidget(self.depthSelect,4,5,1,2)
        grid.addWidget(self.depth_slider_value,4,5,1,3)
        grid.addWidget(self.layerSelect,6,5,1,2)
        grid.addWidget(self.layer_slider_value,6,5,1,3)

        grid.addWidget(self.pressure_slider,3,5,1,3)
        grid.addWidget(self.depth_slider,5,5,1,3)
        grid.addWidget(self.layer_slider,7,5,1,3)

        grid.addWidget(self.pressure_set,3,7,1,1)
        grid.addWidget(self.depth_set,5,7,1,1)
        grid.addWidget(self.layer_set,7,7,1,1)

        grid.addWidget(self.run,9,6,1,1)
        grid.addWidget(self.stop,10,5,1,1)
        grid.addWidget(self.pause,10,6,1,1)
        grid.addWidget(self.resume,10,7,1,1)
        grid.addWidget(self.reset,11,6,1,1)

        #grid.addWidget(label,5,5,5,5)

        ###grid.addWidget(self.endLabel,800,1200,1,1)

        # -- Col3
        grid.addWidget(self.feedback_label,1,9,1,4)
        grid.addWidget(self.sysStatus_label,3,9,1,1)
        grid.addWidget(self.desiredParam_label,5,9,1,1)
        grid.addWidget(self.currentValue_label,7,9,1,1)
        grid.addWidget(self.forceSensorValue_label,9,9,1,1)

        
        #grid.addWidget(self.feedback_output_read,2,10,2,1)
        #grid.addWidget(self.feedback_output_read,2,9,1,1)

        # grid.addWidget(self.compact_compact,4,0,4,2)
        # grid.addWidget(self.compact_pause,6,0,4,2)
        # grid.addWidget(self.compact_resume,6,2,4,2)
        # grid.addWidget(self.compact_clean,0,0,4,2)
        # grid.addWidget(self.compact_estop,2,12,4,6)
        # grid.addWidget(self.pressure_slider,2,0,4,6)
        # grid.addWidget(self.pressure_slider_value,2,6,4,2)
        # grid.addWidget(self.compaction_serial_output,10,0,1,4)

        # grid.addWidget(self.input_window,0,4,12,12) 
        # grid.addWidget(self.output_window,0,12,12,12)
        
        # grid.addWidget(self.motion_title,0,24,2,12) 
        # grid.addWidget(self.motion_set_port,2,24,2,8) 
        # grid.addWidget(self.motion_connect,2,32,2,4)
        # grid.addWidget(self.motion_serial_output,4,24,4,12)
        # grid.addWidget(self.motion_write_line,8,24,2,8) 
        # grid.addWidget(self.motion_send_line,8,32,2,4)
        # grid.addWidget(self.motion_serial_input,10,24,2,12)
        
        # grid.addWidget(self.motion_function_title,12,0,1,12)
        # grid.addWidget(self.motion_home,14,0,1,2)
        # grid.addWidget(self.motion_yp,14,2,1,2)
        # grid.addWidget(self.motion_yn,16,2,1,2)
        # grid.addWidget(self.motion_xp,15,4,1,2)
        # grid.addWidget(self.motion_xn,15,0,1,2)
        # grid.addWidget(self.motion_goto_home,15,2,1,2)
        # grid.addWidget(self.motion_layer_thickness,19,0,1,4)
        # grid.addWidget(self.motion_x_pos_title,22,0,1,2)
        # grid.addWidget(self.motion_y_pos_title,23,0,1,2)
        # grid.addWidget(self.motion_state_title,26,0,1,2)
        # grid.addWidget(self.motion_x_pos,22,2,1,4)
        # grid.addWidget(self.motion_y_pos,23,2,1,4)
        # grid.addWidget(self.motion_f_pos,24,2,1,4)
        # grid.addWidget(self.motion_b_pos,25,2,1,4)
        # grid.addWidget(self.motion_state,26,2,1,4)
        
        #set tooltips
        # self.motion_connect.setToolTip("The COM port the GRBL is on. 'COM#' for Windows, '/dev/ttyUSB#' for Linux") 
        # self.motion_send_line.setToolTip("Send a raw command to the GRBL") 
        
        #slider update
        self.pressure_slider.valueChanged.connect(self.UpdatePressureSliderValue)
        self.cycle_slider.valueChanged.connect(self.UpdateCycleSliderValue) 
        self.depth_slider.valueChanged.connect(self.UpdateDepthSliderValue) 
        self.layer_slider.valueChanged.connect(self.UpdateLayerSliderValue)  

        self.setFixedSize(1200, 800)
        self.center()
        self.setWindowTitle('Oasis Controller')
        #self.setWindowIcon(QIcon('3DPrinterLogo.png')) 
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def UpdatePressureSliderValue(self):
        """Updates the value next to the threshold slider"""
        pressure_threshold = self.pressure_slider.value()
        self.pressure_slider_value.setText("    Desired Pressure: " + str(pressure_threshold) + " kPa")

    def UpdateCycleSliderValue(self):
        """Updates the value next to the threshold slider"""
        cycle_threshold = self.cycle_slider.value()
        self.cycle_slider_value.setText("Number of Cycles: " + str(cycle_threshold) + " cycles")

    def UpdateDepthSliderValue(self):
        """Updates the value next to the threshold slider"""
        depth_threshold = self.depth_slider.value()
        self.depth_slider_value.setText("    Desired Compaction Depth: " + str(depth_threshold) + " mm")

    def UpdateLayerSliderValue(self):
        """Updates the value next to the threshold slider"""
        layer_threshold = self.layer_slider.value()
        self.layer_slider_value.setText("    Desired Layer Count: " + str(layer_threshold) + " layers")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setStyle('Mac')
    ex = Interface()
    ex.initUI()
    sys.exit(app.exec_())