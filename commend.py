import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPlainTextEdit, \
QLabel, QFileDialog, QPushButton, QRadioButton, QButtonGroup, QTextEdit, QMessageBox, QListWidget, QListWidgetItem
from win32api import GetSystemMetrics
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QTextLayout, QGuiApplication
from PyQt5.QtCore import Qt, pyqtSlot, QStringListModel, QCoreApplication
from time import sleep

class PopUpWindow(QWidget):
    counter = 0
    def __init__(self, count, parent=None):
        QWidget.__init__(self)
        self.parent = parent
        PopUpWindow.counter = count
        self.menu()

    def menu(self):
        self.setFixedSize(400, 200)
        self.setWindowTitle("Dodawanie komend")
        self.setWindowIcon(QIcon('icon.png'))
        self.modeGroup = QButtonGroup()
        self.mButton = QRadioButton("MOV", self)
        self.mButton.move(20,10)
        self.aButton = QRadioButton("ADD", self)
        self.aButton.move(20, 30)
        self.sButton = QRadioButton("SUB", self)
        self.sButton.move(20, 50)
        self.int1Button = QRadioButton("INT10", self)
        self.int1Button.move(20, 70)
        self.int1Button.toggled.connect(self.int_action)
        self.int2Button = QRadioButton("INT1A", self)
        self.int2Button.move(20, 90)
        self.int2Button.toggled.connect(self.int_action)
        self.int3Button = QRadioButton("INT21", self)
        self.int3Button.move(20, 110)
        self.int3Button.toggled.connect(self.int_action)
        self.pushButton = QRadioButton("PUSH", self)
        self.pushButton.move(20, 130)
        self.pushButton.toggled.connect(self.pup_action)
        self.popButton = QRadioButton("POP", self)
        self.popButton.move(20, 150)
        self.popButton.toggled.connect(self.pup_action)
        self.modeGroup.addButton(self.mButton)
        self.modeGroup.addButton(self.aButton)
        self.modeGroup.addButton(self.sButton)
        self.modeGroup.addButton(self.int1Button)
        self.modeGroup.addButton(self.int2Button)
        self.modeGroup.addButton(self.int3Button)
        self.modeGroup.addButton(self.pushButton)
        self.modeGroup.addButton(self.popButton)
        self.reg1Group = QButtonGroup()
        self.AH1Button = QRadioButton("AH", self)
        self.AH1Button.move(120, 10)
        self.AL1Button = QRadioButton("AL", self)
        self.AL1Button.move(120, 30)
        self.BH1Button = QRadioButton("BH", self)
        self.BH1Button.move(120, 50)
        self.BL1Button = QRadioButton("BL", self)
        self.BL1Button.move(120, 70)
        self.CH1Button = QRadioButton("CH", self)
        self.CH1Button.move(120, 90)
        self.CL1Button = QRadioButton("CL", self)
        self.CL1Button.move(120, 110)
        self.DH1Button = QRadioButton("DH", self)
        self.DH1Button.move(120, 130)
        self.DL1Button = QRadioButton("DL", self)
        self.DL1Button.move(120, 150)
        self.pupGroup = QButtonGroup()
        self.AXButton = QRadioButton("AX", self)
        self.AXButton.move(20, 180)
        self.AXButton.setVisible(False)
        self.BXButton = QRadioButton("BX", self)
        self.BXButton.move(80, 180)
        self.BXButton.setVisible(False)
        self.CXButton = QRadioButton("CX", self)
        self.CXButton.move(140, 180)
        self.CXButton.setVisible(False)
        self.DXButton = QRadioButton("DX", self)
        self.DXButton.move(200, 180)
        self.DXButton.setVisible(False)
        self.pupGroup.addButton(self.AXButton)
        self.pupGroup.addButton(self.BXButton)
        self.pupGroup.addButton(self.CXButton)
        self.pupGroup.addButton(self.DXButton)

        self.reg1Group.addButton(self.AH1Button)
        self.reg1Group.addButton(self.AL1Button)
        self.reg1Group.addButton(self.BH1Button)
        self.reg1Group.addButton(self.BL1Button)
        self.reg1Group.addButton(self.CH1Button)
        self.reg1Group.addButton(self.CL1Button)
        self.reg1Group.addButton(self.DH1Button)
        self.reg1Group.addButton(self.DL1Button)
        self.reg2Group = QButtonGroup()
        self.AH2Button = QRadioButton("AH", self)
        self.AH2Button.move(240, 10)
        self.AL2Button = QRadioButton("AL", self)
        self.AL2Button.move(240, 30)
        self.BH2Button = QRadioButton("BH", self)
        self.BH2Button.move(240, 50)
        self.BL2Button = QRadioButton("BL", self)
        self.BL2Button.move(240, 70)
        self.CH2Button = QRadioButton("CH", self)
        self.CH2Button.move(240, 90)
        self.CL2Button = QRadioButton("CL", self)
        self.CL2Button.move(240, 110)
        self.DH2Button = QRadioButton("DH", self)
        self.DH2Button.move(240, 130)
        self.DL2Button = QRadioButton("DL", self)
        self.DL2Button.move(240, 150)
        self.ImButton = QRadioButton("Zmienna", self)
        self.ImButton.move(240, 170)
        self.ImButton.toggled.connect(self.check)
        self.reg2Group.addButton(self.AH2Button)
        self.reg2Group.addButton(self.AL2Button)
        self.reg2Group.addButton(self.BH2Button)
        self.reg2Group.addButton(self.BL2Button)
        self.reg2Group.addButton(self.CH2Button)
        self.reg2Group.addButton(self.CL2Button)
        self.reg2Group.addButton(self.DH2Button)
        self.reg2Group.addButton(self.DL2Button)
        self.reg2Group.addButton(self.ImButton)
        self.label_panel = QLabel(self)
        self.label_panel.move(300,20)
        self.label_panel.setAlignment(Qt.AlignCenter)
        self.label_panel.setText("Wartosc zmiennej")
        self.label_panel.setVisible(False)
        self.panel = QTextEdit(self)
        self.panel.move(300, 40)
        self.panel.setFixedSize(80,25)
        self.panel.setVisible(False)
        self.acceptButton = QPushButton("Wyslij", self)
        self.acceptButton.move(300,100)
        self.acceptButton.clicked.connect(self.add)

    def pup_action(self, enabled):
        if enabled:
            self.AXButton.setVisible(True)
            self.BXButton.setVisible(True)
            self.CXButton.setVisible(True)
            self.DXButton.setVisible(True)
            self.AH1Button.setDisabled(True)
            self.AH2Button.setDisabled(True)
            self.AL1Button.setDisabled(True)
            self.AL2Button.setDisabled(True)
            self.BH1Button.setDisabled(True)
            self.BH2Button.setDisabled(True)
            self.BL1Button.setDisabled(True)
            self.BL2Button.setDisabled(True)
            self.CH1Button.setDisabled(True)
            self.CH2Button.setDisabled(True)
            self.CL1Button.setDisabled(True)
            self.CL2Button.setDisabled(True)
            self.DH1Button.setDisabled(True)
            self.DH2Button.setDisabled(True)
            self.DL1Button.setDisabled(True)
            self.DL2Button.setDisabled(True)
            self.ImButton.setDisabled(True)
        else:
            self.AXButton.setVisible(False)
            self.BXButton.setVisible(False)
            self.CXButton.setVisible(False)
            self.DXButton.setVisible(False)
            self.AH1Button.setDisabled(False)
            self.AH2Button.setDisabled(False)
            self.AL1Button.setDisabled(False)
            self.AL2Button.setDisabled(False)
            self.BH1Button.setDisabled(False)
            self.BH2Button.setDisabled(False)
            self.BL1Button.setDisabled(False)
            self.BL2Button.setDisabled(False)
            self.CH1Button.setDisabled(False)
            self.CH2Button.setDisabled(False)
            self.CL1Button.setDisabled(False)
            self.CL2Button.setDisabled(False)
            self.DH1Button.setDisabled(False)
            self.DH2Button.setDisabled(False)
            self.DL1Button.setDisabled(False)
            self.DL2Button.setDisabled(False)
            self.ImButton.setDisabled(False)

    def int_action(self, enabled):
        if enabled:
            self.AH1Button.setDisabled(True)
            self.AH2Button.setDisabled(True)
            self.AL1Button.setDisabled(True)
            self.AL2Button.setDisabled(True)
            self.BH1Button.setDisabled(True)
            self.BH2Button.setDisabled(True)
            self.BL1Button.setDisabled(True)
            self.BL2Button.setDisabled(True)
            self.CH1Button.setDisabled(True)
            self.CH2Button.setDisabled(True)
            self.CL1Button.setDisabled(True)
            self.CL2Button.setDisabled(True)
            self.DH1Button.setDisabled(True)
            self.DH2Button.setDisabled(True)
            self.DL1Button.setDisabled(True)
            self.DL2Button.setDisabled(True)
            self.ImButton.setDisabled(True)
        else:
            self.AH1Button.setDisabled(False)
            self.AH2Button.setDisabled(False)
            self.AL1Button.setDisabled(False)
            self.AL2Button.setDisabled(False)
            self.BH1Button.setDisabled(False)
            self.BH2Button.setDisabled(False)
            self.BL1Button.setDisabled(False)
            self.BL2Button.setDisabled(False)
            self.CH1Button.setDisabled(False)
            self.CH2Button.setDisabled(False)
            self.CL1Button.setDisabled(False)
            self.CL2Button.setDisabled(False)
            self.DH1Button.setDisabled(False)
            self.DH2Button.setDisabled(False)
            self.DL1Button.setDisabled(False)
            self.DL2Button.setDisabled(False)
            self.ImButton.setDisabled(False)

    def check(self, enabled):
        if enabled:
            self.panel.setVisible(True)
            self.label_panel.setVisible(True)
        else:
            self.panel.setVisible(False)
            self.label_panel.setVisible(False)

    @pyqtSlot()
    def add(self):
        if not self.modeGroup.checkedId() == -5 and not self.modeGroup.checkedId() == -6 \
                and not self.modeGroup.checkedId() == -7 and not self.modeGroup.checkedId() == -8 and not self.modeGroup.checkedId() == -9:
            special = 0
            if self.modeGroup.checkedId() == -1 or self.reg1Group.checkedId() == -1 or self.reg2Group.checkedId() == -1:
                print("Nie wybrano wszystkich opcji")
                return
        else:
            if self.modeGroup.checkedId() == -8 or self.modeGroup.checkedId() == -9:
                special = 1
                if self.pupGroup.checkedId() == -1:
                    print("Nie wybrano wszystkich opcji")
                    return
            else:
                special = 2
        mode = self.getMode(self.modeGroup.checkedId())
        if special==0:
            reg1 = self.getReg(self.reg1Group.checkedId())
            if(self.reg2Group.checkedId() == -10):
                reg2 = "#" + self.panel.toPlainText()
            else:
                reg2 = self.getReg(self.reg2Group.checkedId())
            napis = str(PopUpWindow.counter) + " " + mode + " " + reg1 + "," + reg2
        elif special==1:
            reg = self.getStack(self.pupGroup.checkedId())
            napis = str(PopUpWindow.counter) + " " + mode + " " + reg
        else:
            napis = str(PopUpWindow.counter) + " " + mode
        self.parent.changeCode(napis)
        PopUpWindow.counter += 10


    def getMode(self, index):
        return {
        -9: 'POP',
        -8: 'PUSH',
        -7: 'INT21',
        -6: 'INT1A',
        -5: 'INT10',
        -4: 'SUB',
        -3: 'ADD',
        -2: 'MOV',
    }[index]

    def getReg(self, index):
        return {
            -2: 'AH',
            -3: 'AL',
            -4: 'BH',
            -5: 'BL',
            -6: 'CH',
            -7: 'CL',
            -8: 'DH',
            -9: 'DL',
        }[index]

    def getStack(self, index):
        return {
            -2: 'AX',
            -3: 'BX',
            -4: 'CX',
            -5: 'DX',
        }[index]