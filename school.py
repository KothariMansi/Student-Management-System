from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType

ui, _ = loadUiType('school.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menuBar().setVisible(False)
        self.btnLogin.clicked.connect(self.login)
        self.AddStd.triggered.connect(self.showAddNewTab)
        self.btnSaveStd.clicked.connect(self.OnSaveClick)


    def login(self):
        un = self.tbUsername.text()
        pd = self.tbPassword.text()
        if un == "Mansi" and pd == "1234":
            self.menuBar().setVisible(True)
            self.tabWidget.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Error", "Invalid Username or Password")

    #### Add new Student
    def showAddNewTab(self):
        self.tabWidget.setCurrentIndex(2)

    def OnSaveClick(self):
        name = self.addName.text()
        print(name)

    def clearStd(self):
        self.addName.clear()



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
