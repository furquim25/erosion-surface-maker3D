import sys, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from natsort import natsorted, ns
from stl import mesh #pip install numpy-stl
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel, QMessageBox

import backend

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('mainUi.ui',self) #UI file
        self.setFixedSize(420, 560)
        self.setWindowTitle("Erosion Surface Maker 3D") #Title window
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'nidflogo.png')) #Logo window
        self.home()

    def home(self):
        self.pushButton_importData.clicked.connect(self.select_folder)
        self.pushButton_run.clicked.connect(self.run_button)
        self.checkBox_custom_axis.stateChanged.connect(self.show_custom_axis)

    def select_folder(self):
        dialog=QFileDialog(self)
        global folder_path
        folder_path = dialog.getExistingDirectory(self, 'Select Folder')
        if (folder_path != ''):
            self.label_importData.setText("Folder selected:")
            self.label_importData2.setText(folder_path)
            self.label_importData2.setToolTip(folder_path)

            self.label_yInterval.setEnabled(True)
            self.doubleSpinBox.setEnabled(True)
            self.label_resInterval.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.pushButton_run.setEnabled(True)
            self.progressBar.setEnabled(True)
            self.checkBox_leveling.setEnabled(True)

            self.checkBox_custom_axis.setEnabled(True)
            self.label_size.setEnabled(True)
            self.doubleSpinBox_size.setEnabled(True)

    def show_custom_axis(self):
        show_custom = self.checkBox_custom_axis.isChecked()
        self.label_x_axis.setEnabled(show_custom)
        self.label_y_axis.setEnabled(show_custom)
        self.label_z_axis.setEnabled(show_custom)
        self.doubleSpinBox_x_min.setEnabled(show_custom)
        self.doubleSpinBox_y_min.setEnabled(show_custom)
        self.doubleSpinBox_z_min.setEnabled(show_custom)
        self.doubleSpinBox_x_max.setEnabled(show_custom)
        self.doubleSpinBox_y_max.setEnabled(show_custom)
        self.doubleSpinBox_z_max.setEnabled(show_custom)

    def run_button(self):
        input1 = folder_path #Folder Path
        input2 = self.doubleSpinBox.value() #y Interval
        input3 = self.horizontalSlider.value() #Resolution Interval
        input4 = self.checkBox.isChecked() #STL generator
        input5 = self.checkBox_leveling.isChecked() #Leveling
        input6 = '' #STL file saving path

        if input4 == True:
            input6 = QFileDialog.getSaveFileName(self, 'Save STL file', os.getenv('HOME'), 'STL(*.stl)')[0]
            if input6 == '':
                return

        input7 = self.checkBox_custom_axis.isChecked()
        if input7 == True:
            input7 = [
                    [self.doubleSpinBox_x_min.value(),self.doubleSpinBox_x_max.value()],
                    [self.doubleSpinBox_y_min.value(),self.doubleSpinBox_y_max.value()],
                    [self.doubleSpinBox_z_min.value(),self.doubleSpinBox_z_max.value()]] # Custom axis intervals = [[xmin,xmax],[ymin,ymax],[zmin,zmax]]
        input8 = self.doubleSpinBox_size.value() # Size of output image window
        print (f"input1={input1}\ninput2={input2}\ninput3={input3}\ninput4={input4}\ninput5={input5}\ninput6={input6}\ninput7={input7}\ninput8={input8}")

        backend.main(input1,input2,input3,input4,input5,input6,input7,input8)
        self.label_loading.setText(backend.get_load_message())
        backend.plot_3D_graphic()

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec()