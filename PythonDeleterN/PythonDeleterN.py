import sys
import pymorphy2
import re
import pyperclip
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QTextEdit, QLabel)
from PyQt5.QtGui import QFont


class Example(QWidget):

    def __init__(self):
        super().__init__()

        # Button's
        self.btn1 = QPushButton('Refact', self)
        self.btn2 = QPushButton('Clear Fields', self)
        self.btn3 = QPushButton('Refact Paste', self)

        # Label's
        self.label1 = QLabel("Input Text", self)
        self.label2 = QLabel("Refactor text", self)

        # Text Field's
        self.edit1 = QTextEdit("", self)
        self.edit2 = QTextEdit("", self)

        # Pymorph analyzer
        self.morph = pymorphy2.MorphAnalyzer()

        self.initUI()


    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.btn1.setToolTip('This is a <b>Refact</b> button to convert text')
        self.btn1.clicked.connect(self.Refactor)
        self.btn1.resize(195, 100)
        self.btn1.move(10, 470)

        self.btn3.setToolTip('This is a <b>Paste Refactor</b> button to convert text')
        self.btn3.clicked.connect(self.Refactor_Paste)
        self.btn3.resize(195, 100)
        self.btn3.move(210, 470)
        
        self.btn2.setToolTip('This is a <b>Clear Fields</b> button to clear text fields')
        self.btn2.clicked.connect(self.Clear_fields)
        self.btn2.resize(400, 100)
        self.btn2.move(451, 470)

        font_btn = self.btn1.font()
        font_btn.setBold(True)
        font_btn.setPointSize(14)

        # Set font size
        self.btn1.setFont(font_btn)
        self.btn2.setFont(font_btn)
        self.btn3.setFont(font_btn)

        
        self.label1.move(10,10)
        self.label2.move(451, 10)

        # Get font and preference 
        font = self.label1.font()
        font.setPointSize(12)
        font.setBold(True)
       
        # Set font for labels
        self.label1.setFont(font)
        self.label1.setFixedSize
        self.label2.setFont(font)
        self.label2.setFixedSize
        
        # Set Font edits
        self.edit1.resize(400, 400)
        self.edit1.selectAll()
        self.edit1.setFontPointSize(10)
        self.edit1.move(10, 40)

        self.edit2.resize(400, 400)
        self.edit2.selectAll()
        self.edit2.setFontPointSize(10)
        self.edit2.move(451, 40)

        self.setGeometry(50, 50, 860, 580)
        self.setWindowTitle('Refactor code')
        self.show()

    def Clear_fields(self):
        self.edit1.setText("")
        self.edit2.setText("")

    def Refactor_Paste(self):
        self.edit1.setText(pyperclip.paste())
        self.Refactor()

    def Refactor(self):

        inp = self.edit1.toPlainText()
        
        position = 0

        # Analyze \r\n
        print(inp)
        while inp.find('\r\n', position) != -1:
            position = inp.find('\r\n', position)
            if position + 1 >= len(inp):
                break
            if inp[position - 1] == '-':
                inp_ex = inp[:position - 1] + inp[position + 1:]
            elif inp[position + 1] == '[':
                position += 1
                continue
            else:
                inp_ex = inp[:position] + ' ' + inp[position + 1:]
            inp = inp_ex

        # Analyze \n

        while inp.find('\n', position) != -1:
            position = inp.find('\n', position)
            if position + 1 >= len(inp):
                break
            if inp[position - 1] == '-':
                inp_ex = inp[:position - 1] + inp[position + 1:]
            elif inp[position + 1] == '[':
                position += 1
                continue
            else:
                inp_ex = inp[:position] + ' ' + inp[position + 1:]
            inp = inp_ex

        # Analyze pymorphy
        position = 0
        list_stop = [' ', '.', ',', '!', "?"]
        while position != len(inp):
            if (inp[position] == '-'):
                position_begin_word = position
                position_end_word = position
                while inp[position_begin_word] not in list_stop:
                    position_begin_word -= 1
                while inp[position_end_word] not in list_stop:
                    position_end_word += 1
                word1 = inp[position_begin_word:]
                word1 = word1[:position - position_begin_word]
                word2 = inp[position + 1:]
                word2 = word2[:position_end_word - position - 1]
                if not self.morph.word_is_known(word1) or not self.morph.word_is_known(word2):
                    temp = inp[position + 1:]
                    inp = inp[:position]
                    inp += temp
                    position -= 1
            position += 1

        # Analyze double space
        res = inp.replace("  ", " ")

        pyperclip.copy(res)
        self.edit2.setText(res)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())