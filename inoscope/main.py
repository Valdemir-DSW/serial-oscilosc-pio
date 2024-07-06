import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import numpy as np
import serial
import serial.tools.list_ports
from PyQt5.QtGui import QIcon
import os
class ConnectionDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Configure Connection')

        layout = QtWidgets.QVBoxLayout()

        # Serial port selection
        self.portLabel = QtWidgets.QLabel('Serial Port:')
        layout.addWidget(self.portLabel)
        self.freqA0 = 0
        self.freqA1 = 0        
        self.portComboBox = QtWidgets.QComboBox()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.portComboBox.addItem(port.device)
        layout.addWidget(self.portComboBox)

        # Baud rate selection
        self.baudLabel = QtWidgets.QLabel('Baud Rate:')
        layout.addWidget(self.baudLabel)

        self.baudComboBox = QtWidgets.QComboBox()
        baudRates = [9600, 19200, 38400, 57600, 115200]
        for rate in baudRates:
            self.baudComboBox.addItem(str(rate))
        layout.addWidget(self.baudComboBox)

        # OK and Cancel buttons
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def getSettings(self):
        return self.portComboBox.currentText(), int(self.baudComboBox.currentText())

class Oscilloscope(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Serial oscilloscope by Valdemir')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(os.path.abspath("icone.ico")))
        self.freqA0 = 0
        self.freqA1 = 0
        # Create central widget
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)
        
        # Create main layout
        mainLayout = QtWidgets.QHBoxLayout(centralWidget)

        # Create layout for buttons
        buttonLayout = QtWidgets.QVBoxLayout()

        self.connectButton = QtWidgets.QPushButton('Connect')
        self.connectButton.clicked.connect(self.showConnectionDialog)
        buttonLayout.addWidget(self.connectButton)

        self.startButton = QtWidgets.QPushButton('Start')
        self.startButton.clicked.connect(self.start)
        buttonLayout.addWidget(self.startButton)

        self.stopButton = QtWidgets.QPushButton('Stop')
        self.stopButton.clicked.connect(self.stop)
        buttonLayout.addWidget(self.stopButton)

        self.saveButton = QtWidgets.QPushButton('Save')
        self.saveButton.clicked.connect(self.saveData)
        buttonLayout.addWidget(self.saveButton)

        self.clearButton = QtWidgets.QPushButton('Clear')
        self.clearButton.clicked.connect(self.clearData)
        buttonLayout.addWidget(self.clearButton)

        self.autoScrollCheckBox = QtWidgets.QCheckBox('Auto Scroll')
        buttonLayout.addWidget(self.autoScrollCheckBox)

        self.scrollSpeedSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.scrollSpeedSlider.setRange(1, 100)
        self.scrollSpeedSlider.setValue(50)
        buttonLayout.addWidget(QtWidgets.QLabel('Scroll Speed'))
        buttonLayout.addWidget(self.scrollSpeedSlider)

        self.amplitudeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.amplitudeSlider.setRange(1, 100)
        self.amplitudeSlider.setValue(10)
        buttonLayout.addWidget(QtWidgets.QLabel('Amplitude'))
        buttonLayout.addWidget(self.amplitudeSlider)

        self.gridButton = QtWidgets.QPushButton('Toggle Grid')
        self.gridButton.clicked.connect(self.toggleGrid)
        buttonLayout.addWidget(self.gridButton)

        self.colorButton1 = QtWidgets.QPushButton('Set Color for Curve 1')
        self.colorButton1.clicked.connect(lambda: self.setColor(1))
        buttonLayout.addWidget(self.colorButton1)

        self.colorButton2 = QtWidgets.QPushButton('Set Color for Curve 2')
        self.colorButton2.clicked.connect(lambda: self.setColor(2))
        buttonLayout.addWidget(self.colorButton2)

        self.amplitudeMultiplierComboBox = QtWidgets.QComboBox()
        amplitudeMultipliers = {'x0.1': 0.1, 'x1': 1, 'x1.2': 1.2, 'x1.4': 1.4, 'x1.6': 1.6, 'x1.8': 1.8, 'x2': 2, 'x2.2': 2.2, 'x2.4': 2.4, 'x2.6': 2.6, 'x2.8': 2.8, 'x3': 3, 'x3.2': 3.2, 'x3.4': 3.4, 'x3.6': 3.6, 'x3.8': 3.8, 'x4': 4, 'x4.2': 4.2, 'x4.4': 4.4, 'x4.6': 4.6, 'x4.8': 4.8, 'x5': 5, 'x5.2': 5.2, 'x5.4': 5.4, 'x5.6': 5.6, 'x5.8': 5.8, 'x6': 6, 'x6.2': 6.2, 'x6.4': 6.4, 'x6.6': 6.6, 'x6.8': 6.8, 'x7': 7, 'x7.2': 7.2, 'x7.4': 7.4, 'x7.6': 7.6, 'x7.8': 7.8, 'x8': 8}

        for multiplier in amplitudeMultipliers.keys():
            self.amplitudeMultiplierComboBox.addItem(multiplier, userData=amplitudeMultipliers[multiplier])
        self.amplitudeMultiplierComboBox.setCurrentIndex(1)  # Set default to 'x1'
        self.amplitudeMultiplierComboBox.currentIndexChanged.connect(self.updateAmplitudeMultiplier)
        buttonLayout.addWidget(QtWidgets.QLabel('Amplitude calibre'))
        buttonLayout.addWidget(self.amplitudeMultiplierComboBox)

        buttonLayout.addStretch()

        # Create layout for graph and controls
        graphLayout = QtWidgets.QVBoxLayout()

        self.plotWidget = pg.PlotWidget()
        graphLayout.addWidget(self.plotWidget)

        self.voltimeterLabel = QtWidgets.QLabel('Voltage A0: 0 V')
        graphLayout.addWidget(self.voltimeterLabel)

        self.frequencimeterLabel = QtWidgets.QLabel('Frequency A0: 0 Hz')
        graphLayout.addWidget(self.frequencimeterLabel)

        self.timeScaleComboBox = QtWidgets.QComboBox()
        timeScales = ['1 ms', '10 ms', '100 ms', '1 s', '10 s']
        for scale in timeScales:
            self.timeScaleComboBox.addItem(scale, userData=float(scale.split()[0]))
        self.timeScaleComboBox.currentIndexChanged.connect(self.updateTimeScale)
        graphLayout.addWidget(self.timeScaleComboBox)

        self.scaleSpinBox = QtWidgets.QSpinBox()
        self.scaleSpinBox.setRange(1, 100)
        self.scaleSpinBox.setValue(10)
        self.scaleSpinBox.valueChanged.connect(self.updateInputScale)
        graphLayout.addWidget(self.scaleSpinBox)

        # Add layouts to main layout
        mainLayout.addLayout(graphLayout)
        mainLayout.addLayout(buttonLayout)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.resetFrequency)
        self.timer.start(1000)  # 1 second intervals

        self.data1 = []
        self.data2 = []
        self.curve1 = self.plotWidget.plot(pen='y')
        self.curve2 = self.plotWidget.plot(pen='b')

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timeScale = 1
        self.inputScale = 1
        self.amplitudeMultiplier = 1
        self.gridEnabled = False

    def showConnectionDialog(self):
        dialog = ConnectionDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            port, baud = dialog.getSettings()
            self.connect(port, baud)

    def connect(self, port, baud):
        try:
            self.serial = serial.Serial(port, baud, timeout=1)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def start(self):
        self.timer.start(50)

    def stop(self):
        self.timer.stop()

    def saveData(self):
        pass  # Implement save functionality

    def clearData(self):
        self.data1.clear()
        self.data2.clear()
        self.curve1.clear()
        self.curve2.clear()

    def updateTimeScale(self):
        self.timeScale = self.timeScaleComboBox.currentData()
        self.timer.setInterval(int(50 / self.timeScale))

    def updateInputScale(self):
        self.inputScale = self.scaleSpinBox.value()

    def updateAmplitudeMultiplier(self):
        self.amplitudeMultiplier = self.amplitudeMultiplierComboBox.currentData()
    
    
    def update(self):
        if hasattr(self, 'serial') and self.serial.in_waiting:
            try:
                line = self.serial.readline().decode('utf-8').strip()
                sensorValueA0, sensorValueA1 = map(int, line.split(','))

                # Apply input scale and multiplier
                sensorValueA0 = ((sensorValueA0 - 512) * (200 / 1024) * (self.inputScale / 1000)) * self.amplitudeMultiplier
                sensorValueA1 = ((sensorValueA1 - 512) * (200 / 1024) * (self.inputScale / 1000)) * self.amplitudeMultiplier

                self.data1.append(sensorValueA0)
                self.data2.append(sensorValueA1)

                if len(self.data1) > 1000:
                    self.data1.pop(0)
                    self.data2.pop(0)

                # Apply amplitude factor for graph display
                amplitudeFactor = self.amplitudeSlider.value() / 10
                displayData1 = [val * amplitudeFactor for val in self.data1]
                displayData2 = [val * amplitudeFactor for val in self.data2]

                self.curve1.setData(displayData1)
                self.curve2.setData(displayData2)

                # Update voltimeter labels
                self.voltimeterLabel.setText(f"Voltage A0: {sensorValueA0 * 1000} V")

                # Auto-scroll functionality
                if self.autoScrollCheckBox.isChecked():
                    scrollSpeed = self.scrollSpeedSlider.value()
                    self.plotWidget.setXRange(len(self.data1) - (100 + scrollSpeed), len(self.data1))

            except Exception as e:
                print(f"Error: {e}")

    def toggleGrid(self):
        self.gridEnabled = not self.gridEnabled
        self.plotWidget.showGrid(x=self.gridEnabled, y=self.gridEnabled)

    def setColor(self, curveNumber):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            if curveNumber == 1:
                self.curve1.setPen(color)
            elif curveNumber == 2:
                self.curve2.setPen(color)

    def calculateFrequency(self):
            # Calculate frequency for A0
            if len(self.data1) > 1:
                currentA0Value = self.data1[-1]
                previousA0Value = self.data1[-2]
                if (previousA0Value <= 0 and currentA0Value > 0) or (previousA0Value >= 0 and currentA0Value < 0):
                    self.freqA0 += 1

            # Calculate frequency for A1
            if len(self.data2) > 1:
                currentA1Value = self.data2[-1]
                previousA1Value = self.data2[-2]
                if (previousA1Value <= 0 and currentA1Value > 0) or (previousA1Value >= 0 and currentA1Value < 0):
                     self.freqA1 += 1

    def resetFrequency(self):
                self.calculateFrequency()
                vs =  self.freqA0
                print(vs)
                self.freqA0 = 0
                self.freqA1 = 0         
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    oscilloscope = Oscilloscope()
    oscilloscope.show()
    sys.exit(app.exec_())
