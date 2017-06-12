import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPlainTextEdit, \
QLabel, QFileDialog, QPushButton, QRadioButton, QButtonGroup, QTextEdit, QMessageBox, QListWidget, QListWidgetItem, \
QComboBox
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QTextLayout, QGuiApplication
from PyQt5.QtCore import Qt, pyqtSlot, QStringListModel, QCoreApplication, QObject, pyqtSignal
from time import sleep
from collections import defaultdict
import re
import win32.win32api as w32
import datetime
import ctypes
from register import Register
from commend import PopUpWindow
from preview import Previewer

ASADMIN = 'asadmin'

class Application(QMainWindow, QWidget):
    def __init__(self, parent=None):
        super(Application, self).__init__(parent)
        self.title = 'Zadanie projektowe nr 2'
        screen_width = w32.GetSystemMetrics(0)
        screen_height = w32.GetSystemMetrics(1)
        self.width = 1024
        self.height = 768
        self.left = (screen_width - self.width)/2
        self.top = -30+(screen_height-self.height)/2
        self.form_widget = None
        self.regA = Register("AX")
        self.regB = Register("BX")
        self.regC = Register("CX")
        self.regD = Register("DX")
        self.program_code = QPlainTextEdit(self)
        self.mode = -1
        self.help_bios = None
        self.step = False
        self.pattern1 = re.compile(r"\d{1,3}\s\D{3}\s\S{2},\S{2}")
        self.pattern2 = re.compile(r"\d{1,3}\s\D{3}\s\S{2},#\d{1,3}")
        self.pattern3 = re.compile(r"\d{1,3}\sINT\S{2}")
        self.pattern4 = re.compile(r"\d{1,3}\s\D{3,4}\s\S{2}")
        self.stack = []
        self.max_stack = 15
        self.stack_pointer = 0
        self.initWindow()

    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedSize(self.width, self.height)
        self.move(self.left, self.top)
        self.setFocusPolicy(Qt.StrongFocus)
        self.initWidgets()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Plik')
        editMenu = menubar.addMenu('&Edycja')
        helpMenu = menubar.addMenu('&Pomoc')
        load_a = fileMenu.addAction("Wczytaj kod programu z pliku")
        load_a.triggered.connect(self.load_action)
        save_a = fileMenu.addAction("Zapisz kod programu do pliku")
        save_a.triggered.connect(self.save_action)
        exit_a = fileMenu.addAction("Wyjdz")
        exit_a.triggered.connect(self.close)
        rest_a = editMenu.addAction("Przywróć ustawienia poczatkowe")
        rest_a.triggered.connect(self.restore_action)
        help_a = helpMenu.addAction("Funkcje BIOS")
        help_a.triggered.connect(self.help_action)
        self.statusBar().showMessage('Projekt wykonali: Natalia Sobolewska, Bartosz Żbikowski')
        self.show()

    def help_action(self):
        self.chooseBIOS = QListWidget()
        self.chooseBIOS.setWindowIcon(QIcon('icon.png'))
        self.chooseBIOS.setWindowTitle(" ")
        self.chooseBIOS.setFixedSize(200, 250)
        self.item1 = QListWidgetItem("INT1A, 02")  # read RTC time
        self.chooseBIOS.addItem(self.item1)
        self.item2 = QListWidgetItem("INT1A, 03")  # set RTC time
        self.chooseBIOS.addItem(self.item2)
        self.item3 = QListWidgetItem("INT1A, 04")  # read RTC date
        self.chooseBIOS.addItem(self.item3)
        self.item4 = QListWidgetItem("INT1A, 05")  # set RTC date
        self.chooseBIOS.addItem(self.item4)
        self.item5 = QListWidgetItem("INT10, 02")  # set cursor position
        self.chooseBIOS.addItem(self.item5)
        self.item6 = QListWidgetItem("INT21, 01")  # character input
        self.chooseBIOS.addItem(self.item6)
        self.item7 = QListWidgetItem("INT21, 02")  # character output
        self.chooseBIOS.addItem(self.item7)
        self.item8 = QListWidgetItem("INT21, 36")  # get free disk space
        self.chooseBIOS.addItem(self.item8)
        self.chooseBIOS.setCurrentItem(self.item1)
        self.chooseBIOS.itemSelectionChanged.connect(self.help_window_action)
        self.chooseBIOS.show()

    def help_window_action(self):
        text = self.chooseBIOS.currentItem().text()
        fun_dict = {"INT1A, 02" : 0, "INT1A, 03" : 1, "INT1A, 04" : 2, "INT1A, 05" : 3,"INT10, 02" : 4, \
        "INT21, 01" : 5, "INT21, 02" : 6, "INT21, 36" : 7}
        fun_dict = defaultdict(lambda: 10, fun_dict)
        if fun_dict[text] == 0:
            self.mode = 0
        elif fun_dict[text] == 1:
            self.mode = 1
        elif fun_dict[text] == 2:
            self.mode = 2
        elif fun_dict[text] == 3:
            self.mode = 3
        elif fun_dict[text] == 4:
            self.mode = 4
        elif fun_dict[text] == 5:
            self.mode = 5
        elif fun_dict[text] == 6:
            self.mode = 6
        elif fun_dict[text] == 7:
            self.mode = 7
        else:
            self.mode = -1
        if Previewer.instance == 0:
            self.help_bios = Previewer(self, self.mode)
            Previewer.instance += 1
        else:
            self.help_bios.zamknij()
            self.help_bios = Previewer(self, self.mode)
            Previewer.instance += 1
        print(Previewer.instance)


    def load_action(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        try:
            fileName, _ = QFileDialog.getOpenFileName(self,"Wybierz plik do odczytu", "", "Pliki tekstowe (*.txt)", options=options)
            file = open(fileName)
            text = file.read()
            self.program_code.setPlainText(text)
            file.close()
            print("Pomyslnie wczytano plik")
        except FileNotFoundError:
            print("Podany plik tekstowy nie istnieje")

    def save_action(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        try:
            fileName, _ = QFileDialog.getSaveFileName(self, "Wybierz plik do zapisu", "", "Pliki tekstowe (*.txt)", options=options)
            file = open(fileName, 'w')
            text = self.program_code.toPlainText()
            file.write(text)
            file.close()
            print("Pomyslnie zapisano plik")
        except FileNotFoundError:
            print("Podany plik tekstowy nie istnieje")

    def restore_action(self):
        self.wynik_AH.setText("00000000")
        self.wynik_AL.setText("00000000")
        self.regA.clearReg()
        self.wynik_BH.setText("00000000")
        self.wynik_BL.setText("00000000")
        self.regB.clearReg()
        self.wynik_CH.setText("00000000")
        self.wynik_CL.setText("00000000")
        self.regC.clearReg()
        self.wynik_DH.setText("00000000")
        self.wynik_DL.setText("00000000")
        self.regD.clearReg()
        self.program_counter.setText("000")
        self.max_stack = 15
        self.stack_pointer = 0
        self.stack = []
        self.clearStack()
        print("Przywrocono")

    def clearStack(self):
        self.stack_pointer_view.setText("15")
        for i in range(self.stack_view.count()):
            self.stack_view.removeItem(0)

    def initWidgets(self):
        self.label_code = QLabel(self)
        self.label_code.setText("Kod programu")
        self.label_code.move(175, 50)

        self.counter = 0
        self.program_code.setFont(QFont("Verdana", 20))
        self.program_code.move(30, 80)
        self.program_code.resize(350, 300)
        self.program_code.textChanged.connect(self.text_changed_action)

        self.program_counter = QLabel(self)
        self.program_counter.move(435, 450)
        self.program_counter.setFixedSize(90, 50)
        self.program_counter.setStyleSheet('background-color: black; color : white;')
        self.program_counter.setAlignment(Qt.AlignCenter)
        self.program_counter.setFont(QFont("Arial Black", 25))
        self.program_counter.setText("000")
        self.program_label = QLabel(self)
        self.program_label.move(435, 400)
        self.program_label.setFixedSize(90, 50)
        self.program_label.setAlignment(Qt.AlignCenter)
        self.program_label.setFont(QFont("Arial", 20))
        self.program_label.setText("PC")

        self.label_reg_AL = self.create_reg_label(880, 60, "AL")
        self.label_reg_AH = self.create_reg_label(680, 60, "AH")
        self.label_reg_BL = self.create_reg_label(880, 200, "BL")
        self.label_reg_BH = self.create_reg_label(680, 200, "BH")
        self.label_reg_CL = self.create_reg_label(880, 340, "CL")
        self.label_reg_CH = self.create_reg_label(680, 340, "CH")
        self.label_reg_DL = self.create_reg_label(880, 480, "DL")
        self.label_reg_DH = self.create_reg_label(680, 480, "DH")

        self.wynik_AH = self.create_reg_view(600, 100, self.regA, True)
        self.wynik_AL = self.create_reg_view(800, 100, self.regA, False)
        self.wynik_BH = self.create_reg_view(600, 240, self.regB, True)
        self.wynik_BL = self.create_reg_view(800, 240, self.regB, False)
        self.wynik_CH = self.create_reg_view(600, 380, self.regC, True)
        self.wynik_CL = self.create_reg_view(800, 380, self.regC, False)
        self.wynik_DH = self.create_reg_view(600, 520, self.regD, True)
        self.wynik_DL = self.create_reg_view(800, 520, self.regD, False)

        self.label_stack_point = QLabel(self)
        self.label_stack_point.move(475, 650)
        self.label_stack_point.setFixedSize(90, 50)
        self.label_stack_point.setAlignment(Qt.AlignCenter)
        self.label_stack_point.setFont(QFont("Arial", 20))
        self.label_stack_point.setText("SP")

        self.stack_pointer_view = QLabel(self)
        self.stack_pointer_view.move(475, 700)
        self.stack_pointer_view.setFixedSize(90, 50)
        self.stack_pointer_view.setStyleSheet('background-color: black; color : white;')
        self.stack_pointer_view.setAlignment(Qt.AlignCenter)
        self.stack_pointer_view.setFont(QFont("Arial Black", 25))
        self.stack_pointer_view.setText(str(self.max_stack))

        self.label_stack = self.create_reg_label(750, 660, "STACK")
        self.stack_view = QComboBox(self)
        self.stack_view.move(600, 700)
        self.stack_view.setFixedSize(380, 50)
        self.stack_view.setFont(QFont("Arial", 25))

        self.run_button = QPushButton("Uruchom", self)
        self.run_button.move(430, 80)
        self.run_button.clicked.connect(self.run_click)
        self.run_button.setDisabled(True)

        self.step_button = QPushButton("Krok", self)
        self.step_button.move(430, 160)
        self.step_button.clicked.connect(self.step_click)
        self.step_button.setDisabled(True)

        self.help_button = QPushButton("Kompiluj", self)
        self.help_button.move(430,240)
        self.help_button.clicked.connect(self.compile_action)

        self.edit_button = QPushButton("Komenda", self)
        self.edit_button.move(430, 320)
        self.edit_button.clicked.connect(self.edit_click)

    def changeCode(self, text):
        self.program_code.appendPlainText(text)

    def text_changed_action(self):
        self.run_button.setDisabled(True)
        self.step_button.setDisabled(True)

    def compile_action(self):
        text = self.program_code.toPlainText()
        text = text.split('\n')
        tested = True
        for i in range(len(text)):
            #sprawdz dla kazdego wiersza pattern
            result1 = self.pattern1.match(text[i])
            result2 = self.pattern2.match(text[i])
            result3 = self.pattern3.match(text[i])
            result4 = self.pattern4.match(text[i])
            if not result1 and not result2 and not result3 and not result4:
                print("Popraw blad w kodzie")
                tested = False
                break
        if tested:
            QMessageBox.warning(self, 'Uwaga',
                                "Kompilacja przebiegła poprawnie.", QMessageBox.Yes, QMessageBox.Yes)
            self.run_button.setDisabled(False)
            self.step_button.setDisabled(False)



    def create_reg_view(self, left, top, reg, ind):
        register = QLabel(self)
        if ind:
            register.setText(reg.high)
        else:
            register.setText(reg.low)
        register.setFixedSize(180, 50)
        register.move(left, top)
        register.setStyleSheet('background-color: lightgray')
        register.setAlignment(Qt.AlignCenter)
        register.setFont(QFont("Arial Black", 25))
        return register

    def create_reg_label(self, left, top, name):
        label_reg = QLabel(self)
        label_reg.setText(name)
        label_reg.move(left, top)
        label_reg.setFont(QFont("Arial", 20))
        return label_reg

    @pyqtSlot()
    def run_click(self):
        text = self.program_code.toPlainText()
        text = text.split('\n')
        for i in range(len(text)):
            commands = text[i].split(" ")
            index = commands[0] # numer instrukcji
            mode = commands[1] # rozkaz
            if "INT" in mode:
                option = 0
            elif mode == "PUSH" or mode == "POP":
                option = 1
                register = commands[2]
            else:
                option = 2
                register = commands[2].split(",") # dane
                if '#' in register[1]:
                     register[1] = register[1][1:]
                     address = True
            while len(index) < 3:
                index = '0' + index
            self.program_counter.setText(index)  # wysiwetl numer instrukcji
            ##################################
            if option == 2:
                op1, c1 = self.findReg(register[0])
                if not address:
                    op2, c2 = self.findReg(register[1])
            elif option == 1:
                op1 = self.findReg(register)
            ##################################
            if mode == 'MOV':
                if not address:
                    number = op2.getReg(c2)
                    op1.mov(number, c1)
                else:
                    number = bin(int(register[1]))[2:]
                    while len(number) < 8:
                        number = '0' + number
                    op1.mov(number, c1)
            if mode == 'ADD':
                if not address:
                    number = op2.getReg(c2)
                    number = int(number, 2)
                    op1.add(number, c1)
                else:
                    number = int(register[1])
                    op1.add(number, c1)
            if mode == 'SUB':
                if not address:
                    number = op2.getReg(c2)
                    number = int(number, 2)
                    op1.sub(number, c1)
                else:
                    number = int(register[1])
                    op1.sub(number, c1)
            if mode == "INT1A":
                if hex(int(self.regA.high, 2)) == "0x2":
                    czas = w32.GetSystemTime()
                    hour = self.convertToBCD(czas[4] + 2)
                    minute = self.convertToBCD(czas[5])
                    second = self.convertToBCD(czas[6])
                    self.regC.high = hour
                    self.regC.low = minute
                    self.regD.high = second
                if hex(int(self.regA.high, 2)) == "0x3":
                    hour = self.convertFromBCD(self.regC.high)-2
                    minute = self.convertFromBCD(self.regC.low)
                    second = self.convertFromBCD(self.regD.high)
                    year = datetime.datetime.now().year
                    month = datetime.datetime.now().month
                    day = datetime.datetime.now().day
                    dayOfWeek = datetime.date.today().weekday()
                    w32.SetSystemTime(year, month, dayOfWeek, day, hour, minute, second, 0)
                if hex(int(self.regA.high, 2)) == "0x4":
                    czas = w32.GetSystemTime()
                    century = self.convertToBCD(int(str(czas[0])[:2]))
                    year = self.convertToBCD(int(str(czas[0])[2:]))
                    month = self.convertToBCD(czas[1])
                    day = self.convertToBCD(czas[3])
                    self.regC.high = century
                    self.regC.low = year
                    self.regD.high = month
                    self.regD.low = day
                if hex(int(self.regA.high, 2)) == "0x5":
                    hour = datetime.datetime.now().time().hour - 2
                    minute = datetime.datetime.now().time().minute
                    second = datetime.datetime.now().time().second
                    year = self.convertFromBCD(self.regC.low)
                    century = 100 * self.convertFromBCD(self.regC.high)
                    month = self.convertFromBCD(self.regD.high)
                    day = self.convertFromBCD(self.regD.low)
                    dayOfWeek = datetime.date.weekday(datetime.date(century+year, month, day))
                    w32.SetSystemTime(century + year, month, dayOfWeek, day, hour, minute, second, 0)
                else:
                    print("Nie znaleziono komendy.")

            if mode == "INT10":
                if hex(int(self.regA.high, 2)) == "0x2":
                    x = int(self.regD.high, 2)
                    y = int(self.regD.low, 2)
                    w32.SetCursorPos((x, y))
                else:
                    print("Nie znaleziono komendy.")
            if mode == "INT21":
                if hex(int(self.regA.high, 2)) == "0x1":
                    line = sys.stdin.readline()
                    if len(line) > 1:
                        line = line[0]
                    print(line)
                    kod = bin(ord(line))[2:]
                    while len(kod) < 8:
                        kod = '0' + kod
                    self.regA.low = kod
                if hex(int(self.regA.high, 2)) == "0x2":
                    char = self.regD.low
                    self.regA.low = char
                    char = chr(int(char, 2))
                    sys.stdout.write(char)
                if hex(int(self.regA.high, 2)) == "0x36":
                    temp_dict = {1: 'A:', 2: 'B:', 3: 'C:', 4: 'D:', 5: 'E'}
                    temp_dict.setdefault(0, "")
                    ind = int(self.regD.low, 2)
                    test = w32.GetDiskFreeSpace(temp_dict[ind])
                    ra = test[0]
                    rb = test[1]
                    rc = test[2]
                    rd = test[3]
                    if rc >= 256*256:
                        rc = 256*256-1
                    if rd >= 256*256:
                        rd = 256*256-1
                    ra = bin(ra)[2:]
                    while len(ra) < 16:
                        ra = '0' + ra
                    rb = bin(rb)[2:]
                    while len(rb) < 16:
                        rb = '0' + rb
                    rc = bin(rc)[2:]
                    while len(rc) < 16:
                        rc = '0' + rc
                    rd = bin(rd)[2:]
                    while len(rd) < 16:
                        rd = '0' + rd
                    self.regA.high = ra[0:8]
                    self.regA.low = ra[8:16]
                    self.regB.high = rb[0:8]
                    self.regB.low = rb[8:16]
                    self.regC.high = rc[0:8]
                    self.regC.low = rc[8:16]
                    self.regD.high = rd[0:8]
                    self.regD.low = rd[8:16]
                else:
                    print("Nie znaleziono komendy. ")

            if mode == "PUSH":
                self.stack.insert(0, (op1.getFull(), op1))
                self.updateStack(True)
                self.stack_pointer += 1
            if mode == "POP":
                values = self.stack.pop(0)
                value = values[0]
                reg = values[1]
                reg.high = value[0:8]
                reg.low = value[8:16]
                self.stack_pointer -= 1
                self.updateStack()
            self.stack_pointer_view.setText(str(self.max_stack-self.stack_pointer))
            self.updateReg()
            sleep(1)

    def convertToBCD(self, number):
        text = ""
        for c in str(number):
            temp = bin(int(c))[2:]
            while len(temp) < 4:
                temp = '0' + temp
            text += temp
        while len(text) < 8:
            text = '0' + text
        return text

    def convertFromBCD(self, text):
        number = []
        final = 0
        for i in range(2):
            part = text[0:4]
            part = int(part, 2)
            number.append(part)
            text = text[4:]
        for i in range(len(number)):
            final += 10**i * number.pop(len(number)-1)
        return final

    def updateReg(self):
        self.wynik_AH.setText(self.regA.high)
        self.wynik_AL.setText(self.regA.low)
        self.wynik_BH.setText(self.regB.high)
        self.wynik_BL.setText(self.regB.low)
        self.wynik_CH.setText(self.regC.high)
        self.wynik_CL.setText(self.regC.low)
        self.wynik_DH.setText(self.regD.high)
        self.wynik_DL.setText(self.regD.low)
        QCoreApplication.processEvents()

    def updateStack(self, ind=False):
        if ind:
            self.stack_view.insertItem(0, self.stack[0][1].name + ": " + self.stack[0][0])
            self.stack_view.setCurrentIndex(0)
        else:
            self.stack_view.removeItem(0)
        QCoreApplication.processEvents()

    def findReg(self, text):
        if 'H' in text:
            if 'A' in text:
                return self.regA, True
            elif 'B' in text:
                return self.regB, True
            elif 'C' in text:
                return self.regC, True
            elif 'D' in text:
                return self.regD, True
        elif 'L' in text:
            if 'A' in text:
                return self.regA, False
            elif 'B' in text:
                return self.regB, False
            elif 'C' in text:
                return self.regC, False
            elif 'D' in text:
                return self.regD, False
        elif 'X' in text:
            if 'A' in text:
                return self.regA
            elif 'B' in text:
                return self.regB
            elif 'C' in text:
                return self.regC
            elif 'D' in text:
                return self.regD


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if self.step:
            if e.key() == Qt.Key_W:
                self.stop = False


    @pyqtSlot()
    def step_click(self):
        self.step = True
        self.program_code.setDisabled(True)
        QMessageBox.warning(self, 'Uwaga',
                            "Krokowe dzialanie programu. Nacisnij klaiwsz 'w' aby przejsc do nastepnego kroku.",
                                           QMessageBox.Yes , QMessageBox.Yes)
        text = self.program_code.toPlainText()
        text = text.split('\n')
        for i in range(len(text)):
            self.stop = True
            commands = text[i].split(" ")
            index = commands[0]  # numer instrukcji
            mode = commands[1]  # rozkaz
            if "INT" in mode:
                option = 0
            elif mode == "PUSH" or mode == "POP":
                option = 1
                register = commands[2]
            else:
                option = 2
                register = commands[2].split(",")  # dane
                if '#' in register[1]:
                    register[1] = register[1][1:]
                    address = True
            while len(index) < 3:
                index = '0' + index
            self.program_counter.setText(index)  # wysiwetl numer instrukcji
            ##################################
            if option == 2:
                op1, c1 = self.findReg(register[0])
                if not address:
                    op2, c2 = self.findReg(register[1])
            elif option == 1:
                op1 = self.findReg(register)
            ##################################
            if mode == 'MOV':
                if not address:
                    number = op2.getReg(c2)
                    op1.mov(number, c1)
                else:
                    number = bin(int(register[1]))[2:]
                    while len(number) < 8:
                        number = '0' + number
                    op1.mov(number, c1)
            if mode == 'ADD':
                if not address:
                    number = op2.getReg(c2)
                    number = int(number, 2)
                    op1.add(number, c1)
                else:
                    number = int(register[1])
                    op1.add(number, c1)
            if mode == 'SUB':
                if not address:
                    number = op2.getReg(c2)
                    number = int(number, 2)
                    op1.sub(number, c1)
                else:
                    number = int(register[1])
                    op1.sub(number, c1)
            if mode == "INT1A":
                if hex(int(self.regA.high, 2)) == "0x2":
                    czas = w32.GetSystemTime()
                    hour = self.convertToBCD(czas[4] + 2)
                    minute = self.convertToBCD(czas[5])
                    second = self.convertToBCD(czas[6])
                    self.regC.high = hour
                    self.regC.low = minute
                    self.regD.high = second
                if hex(int(self.regA.high, 2)) == "0x3":
                    hour = self.convertFromBCD(self.regC.high) - 2
                    minute = self.convertFromBCD(self.regC.low)
                    second = self.convertFromBCD(self.regD.high)
                    year = datetime.datetime.now().year
                    month = datetime.datetime.now().month
                    day = datetime.datetime.now().day
                    dayOfWeek = datetime.date.today().weekday()
                    w32.SetSystemTime(year, month, dayOfWeek, day, hour, minute, second, 0)
                if hex(int(self.regA.high, 2)) == "0x4":
                    czas = w32.GetSystemTime()
                    century = self.convertToBCD(int(str(czas[0])[:2]))
                    year = self.convertToBCD(int(str(czas[0])[2:]))
                    month = self.convertToBCD(czas[1])
                    day = self.convertToBCD(czas[3])
                    self.regC.high = century
                    self.regC.low = year
                    self.regD.high = month
                    self.regD.low = day
                if hex(int(self.regA.high, 2)) == "0x5":
                    hour = datetime.datetime.now().time().hour - 2
                    minute = datetime.datetime.now().time().minute
                    second = datetime.datetime.now().time().second
                    year = self.convertFromBCD(self.regC.low)
                    century = 100 * self.convertFromBCD(self.regC.high)
                    month = self.convertFromBCD(self.regD.high)
                    day = self.convertFromBCD(self.regD.low)
                    dayOfWeek = datetime.date.weekday(datetime.date(century + year, month, day))
                    w32.SetSystemTime(century + year, month, dayOfWeek, day, hour, minute, second, 0)
                else:
                    print("Nie znaleziono komendy.")
            if mode == "INT10":
                if hex(int(self.regA.high, 2)) == "0x2":
                    x = int(self.regD.high, 2)
                    y = int(self.regD.low, 2)
                    w32.SetCursorPos((x, y))
                else:
                    print("Nie znaleziono komendy.")
            if mode == "INT21":
                if hex(int(self.regA.high, 2)) == "0x1":
                    line = sys.stdin.readline()
                    if len(line) > 1:
                        line = line[0]
                    print(line)
                    kod = bin(ord(line))[2:]
                    while len(kod) < 8:
                        kod = '0' + kod
                    self.regA.low = kod
                if hex(int(self.regA.high, 2)) == "0x2":
                    char = self.regD.low
                    self.regA.low = char
                    char = chr(int(char, 2))
                    sys.stdout.write(char)
                if hex(int(self.regA.high, 2)) == "0x36":
                    temp_dict = {1: 'C:', 2: 'D:', 3: 'E:', 4: 'F:'}
                    temp_dict.setdefault(0, "")
                    ind = int(self.regD.low, 2)
                    test = w32.GetDiskFreeSpace(temp_dict[ind])
                    ra = test[0]
                    rb = test[1]
                    rc = test[2]
                    rd = test[3]
                    if rc >= 256 * 256:
                        rc = 256 * 256 - 1
                    if rd >= 256 * 256:
                        rd = 256 * 256 - 1
                    ra = bin(ra)[2:]
                    while len(ra) < 16:
                        ra = '0' + ra
                    rb = bin(rb)[2:]
                    while len(rb) < 16:
                        rb = '0' + rb
                    rc = bin(rc)[2:]
                    while len(rc) < 16:
                        rc = '0' + rc
                    rd = bin(rd)[2:]
                    while len(rd) < 16:
                        rd = '0' + rd
                    self.regA.high = ra[0:8]
                    self.regA.low = ra[8:16]
                    self.regB.high = rb[0:8]
                    self.regB.low = rb[8:16]
                    self.regC.high = rc[0:8]
                    self.regC.low = rc[8:16]
                    self.regD.high = rd[0:8]
                    self.regD.low = rd[8:16]
                else:
                    print("Nie znaleziono komendy. ")
            if mode == "PUSH":
                self.stack.insert(0, (op1.getFull(), op1))
                self.updateStack(True)
                self.stack_pointer += 1
            if mode == "POP":
                values = self.stack.pop(0)
                value = values[0]
                reg = values[1]
                reg.high = value[0:8]
                reg.low = value[8:16]
                self.stack_pointer -= 1
                self.updateStack()
            self.stack_pointer_view.setText(str(self.max_stack - self.stack_pointer))
            self.updateReg()
            while self.stop:
                QCoreApplication.processEvents()
                sleep(0.01)
        buttonReply = QMessageBox.warning(self, 'Uwaga', "Zakonczono krokowe dzialanie programu.",
                                           QMessageBox.Yes , QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            self.program_code.setDisabled(False)
        self.step = False

    @pyqtSlot()
    def edit_click(self):
        text = self.program_code.toPlainText()
        text = text.split('\n')
        if text[0] == '':
            self.counter = 0
        else:
            self.counter = len(text)*10
        self.okno = PopUpWindow(self.counter, self)
        self.okno.setGeometry(320, 500, 400, 200)
        self.okno.show()

def run_as_admin(argv=None, debug=False):
    shell32 = ctypes.windll.shell32
    if argv is None and shell32.IsUserAnAdmin():
        return True
    if argv is None:
        argv = sys.argv
    if hasattr(sys, '_MEIPASS'):
        arguments = argv[1:]
    else:
        arguments = argv
    argument_line = u' '.join(arguments)
    executable = sys.executable
    if debug:
        print('Command line: ', executable, argument_line)
    ret = shell32.ShellExecuteW(None, u"runas", executable, argument_line, None, 1)
    if int(ret) <= 32:
        return False
    return None

if __name__ == '__main__':
    app = QApplication([])
    run_as_admin()
    ex = Application()
    ex.show()
    sys.exit(app.exec_())
