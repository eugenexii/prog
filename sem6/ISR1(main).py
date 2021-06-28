import sys
from PyQt5 import QtWidgets
import mydesign
import math

class ExampleApp(QtWidgets.QMainWindow, mydesign.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.SolveButton.clicked.connect(self.solution)
        self.CancelButton.clicked.connect(self.exit)


    def solution(self):
        a = self.a.value()
        b = self.b.value()
        c = self.c.value()
        print(-b)
        des = b ** 2 - 4*a*c
        print(des)
        print(math.sqrt(des))
        if(a != 0):
            if(des < 0):
                self.x1.setText(" D <0 => решений нет")
                self.x2.setText(" D <0 => решений нет")
            elif(des == 0):
                self.x1.setText(str(round((-b)/2*a),3))
                self.x2.setText(str(round((-b)/2*a), 3))
            else:
                self.x1.setText(str(round((-b - math.sqrt(des)) / (2 * a), 3)))
                self.x2.setText(str(round((-b + math.sqrt(des)) / (2 * a), 3)))
        else:
            self.x1.setText(" Это не кв.урав")
            self.x2.setText(" Это не кв.урав")

    def exit(self):
        exit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()



if __name__ == '__main__':
    main()
