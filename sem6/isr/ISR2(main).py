import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

import design

class ExampleApp(QtWidgets.QMainWindow, design.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.solution)
        self.msg = QMessageBox()

    def solution(self):
        det = self.x11.value() * self.x22.value() - self.x12.value()*self.x21.value()
        if(det != 0):
            firs_prt = self.b1.value() * self.x22.value() - self.x12.value()*self.b2.value()
            sec_prt = self.x11.value() * self.b2.value() - self.b1.value() * self.x21.value()
            self.answ1.setText(str(round(firs_prt/det, 3)))
            self.answ2.setText(str(round((sec_prt / det), 3)))
        else:
            QMessageBox.about(self, "Решение СЛАУ", "Система имеет либо бесконечное множество решений, либо не имеет их")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()



if __name__ == '__main__':
    main()
