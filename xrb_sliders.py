from PyQt5 import QtCore
#from PyQt4 import QtCore
from PyQt5.QtWidgets import (
#from PyQt4.QtGui import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
	QGridLayout, QCheckBox, QComboBox, QScrollArea, QStatusBar,
    QGroupBox, QSpinBox, QDoubleSpinBox, QSlider, QDial, QBoxLayout,
    QHBoxLayout, QLineEdit
    )

import sys


class SlidersGroup(QGroupBox):

    valueChanged = QtCore.pyqtSignal(int)

    def __init__(self, orientation, name, title, parent=None):
        super(SlidersGroup, self).__init__(title, parent)

        self.name = name
        self.value = 0.0
        
        valueLabel = QLabel("Current value:")
        #self.valueSpinBox = QDoubleSpinBox ()
        self.valueSpinBox = QSpinBox()
        self.valueSpinBox.setSingleStep(1)
        self.valueSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        
        self.slider = QSlider(orientation)
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)

        self.dial = QDial()
        self.dial.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.slider.valueChanged.connect(self.setValue)
        self.dial.valueChanged.connect(self.setValue)
        
        direction = QBoxLayout.TopToBottom

        slidersLayout = QBoxLayout(direction)
        slidersLayout.addWidget(valueLabel)
        slidersLayout.addWidget(self.valueSpinBox)
        slidersLayout.addWidget(self.slider)
        #slidersLayout.addWidget(self.dial)
        self.setLayout(slidersLayout)    

    def setValue(self, value):
        self.valueSpinBox.setValue(value)
        self.slider.setValue(value)
        self.dial.setValue(value)
        self.value = value

    def setMinimum(self, value):    
        self.slider.setMinimum(value)
        self.dial.setMinimum(value)    

    def setMaximum(self, value):    
        self.valueSpinBox.setRange(0, value)
        self.slider.setMaximum(value)
        self.dial.setMaximum(value)    


class Window(QWidget):
    def __init__(self, dr):
        super(Window, self).__init__()
        
        self.dr = dr
        self.value = 0.0    # peak value from antenna
        self.hold = True    # pause graph
        xrb_together = True # NRB, ARB move together
        
        self.setWindowTitle('xRB Simulation')
        self.setGeometry(20,50,330,250)

        self.vbox_top = QVBoxLayout()
        
        # 1
        self.w15Hz = SlidersGroup(QtCore.Qt.Horizontal, "15Hz", "15Hz Offset")
        self.w15Hz.valueSpinBox.valueChanged.connect(self.updateValue_15Hz)
        self.w15Hz.setMinimum(0)
        self.w15Hz.setMaximum(360)
        self.vbox_top.addWidget(self.w15Hz)        
        
        # 2
        self.w135Hz = SlidersGroup(QtCore.Qt.Horizontal, "135Hz", "135Hz Offset")
        self.w135Hz.valueSpinBox.valueChanged.connect(self.updateValue_135Hz)
        self.w135Hz.setMinimum(0)
        self.w135Hz.setMaximum(40)
        self.vbox_top.addWidget(self.w135Hz)

        # 3
        self.nrb = SlidersGroup(QtCore.Qt.Horizontal, "NRB", "NRB Offset")
        self.nrb.valueSpinBox.valueChanged.connect(self.updateValue_nrb)
        self.nrb.setMinimum(0)
        self.nrb.setMaximum(360)
        self.vbox_top.addWidget(self.nrb)

        # 4
        self.arb = SlidersGroup(QtCore.Qt.Horizontal, "ARB", "ARB Offset")
        self.arb.valueSpinBox.valueChanged.connect(self.updateValue_arb)
        self.arb.setMinimum(0)
        self.arb.setMaximum(40)
        self.vbox_top.addWidget(self.arb)
        
        #5
        self.cb_xrb = QCheckBox("NRB,ARB move together", self)
        self.cb_xrb.setCheckState(2)
        self.vbox_top.addWidget(self.cb_xrb)
        
        #6
        self.hb1 = QHBoxLayout()
        self.nrbLabel = QLabel("NRB:")
        self.z15Label = QLabel("15Hz Zero-cross")
        self.b15Label = QLabel("15Hz Bearing")
        self.hb1.addWidget(self.nrbLabel)
        self.hb1.addWidget(self.z15Label)
        self.hb1.addWidget(self.b15Label)
        self.vbox_top.addLayout(self.hb1)

        self.hb2 = QHBoxLayout()
        self.text_nrb = QLineEdit()
        self.text_z15 = QLineEdit()
        self.text_b15 = QLineEdit()
        self.hb2.addWidget(self.text_nrb)
        self.hb2.addWidget(self.text_z15)
        self.hb2.addWidget(self.text_b15)
        self.vbox_top.addLayout(self.hb2)

        self.hb3 = QHBoxLayout()       
        self.arbLabel = QLabel("ARB:")
        self.z135Label = QLabel("135Hz Zero-cross:")
        self.b135Label = QLabel("135Hz Bearing:")
        self.hb3.addWidget(self.arbLabel)
        self.hb3.addWidget(self.z135Label)
        self.hb3.addWidget(self.b135Label)
        self.vbox_top.addLayout(self.hb3)

        self.hb4 = QHBoxLayout()       
        self.text_arb = QLineEdit()
        self.text_z135 = QLineEdit()
        self.text_b135 = QLineEdit()
        self.hb4.addWidget(self.text_arb)
        self.hb4.addWidget(self.text_z135)
        self.hb4.addWidget(self.text_b135)
        self.vbox_top.addLayout(self.hb4)

        self.hb5 = QHBoxLayout()       
        self.cntLabel = QLabel("ARB Count:")
        self.bearLabel = QLabel("Bearing_org:")
        self.bearingLabel = QLabel("Bearing:")
        self.hb5.addWidget(self.cntLabel)
        self.hb5.addWidget(self.bearLabel)
        self.hb5.addWidget(self.bearingLabel)
        self.vbox_top.addLayout(self.hb5)
        
        self.hb6 = QHBoxLayout()       
        self.text_cnt = QLineEdit()
        self.text_bear = QLineEdit()
        self.text_bearing = QLineEdit()
        self.updateBearing()
        self.hb6.addWidget(self.text_cnt)
        self.hb6.addWidget(self.text_bear)
        self.hb6.addWidget(self.text_bearing)
        self.vbox_top.addLayout(self.hb6)

        # Push Button
        self.hb7 = QHBoxLayout()       
        self.btn_test=QPushButton('Test', self)
        self.hb7.addWidget(self.btn_test)
        self.btn_save=QPushButton('Save', self)
        self.hb7.addWidget(self.btn_save)
        self.vbox_top.addLayout(self.hb7)

        #result
        # self.resultLabel = QLabel("Test Result:")
        # self.vbox_top.addWidget(self.resultLabel)
        # self.text_result = QLineEdit()
        # self.vbox_top.addWidget(self.text_result)
        
        #Add layout
        self.setLayout(self.vbox_top)
        
        # Initial data
        self.w15Hz.setValue(10)
        self.w135Hz.setValue(0)
        self.nrb.setValue(213)
        self.arb.setValue(213%40)

        self.dr.SetGUI(self)    
    
    def updateBearing(self):
        result = self.dr.calBearing()
        self.text_nrb.setText(str(result[0]))
        self.text_z15.setText(str(result[1]))
        self.text_b15.setText(str(result[2]))
        self.text_arb.setText(str(result[3]))
        self.text_z135.setText(str(result[4]))
        self.text_b135.setText(str(result[5]))
        self.text_cnt.setText(str(result[6]))
        self.text_bear.setText(str(result[7]))
        self.text_bearing.setText(str(result[8]))
    
    def updateValue_15Hz(self, value):
        self.w15Hz.setValue(value)
        self.dr.update("15Hz", value)
        self.updateBearing()
    
    def updateValue_135Hz(self, value):
        self.w135Hz.setValue(value)
        self.dr.update("135Hz", value)
        self.updateBearing()

    def updateValue_nrb(self, value):
        self.nrb.setValue(value)
        self.dr.update("NRB", value)
        if self.cb_xrb.isChecked():
            self.arb.setValue(value%40)
            self.dr.update("ARB", value%40)            
        self.updateBearing()

    def updateValue_arb(self, value):
        if self.cb_xrb.isChecked():
            pass
        else:
            self.arb.setValue(value)
            self.dr.update("ARB", value)
        self.updateBearing()
        
    def saveGraph(self):
        self.dr.gui_save()

    def closeEvent(self, event):
        print("Closing GUI")
        sys.exit()

    def HoldGraph(self):
        self.hold ^= True
        if self.hold == True:
            self.Pause.setText('Pause')            
        else:
            self.Pause.setText('Run')
        self.dr.gui_set_hold(not self.hold)
                        
        
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())