from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
from DatabaseManager import DatabaseManager, DatabaseManager

ui, _ = loadUiType('school.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menuBar().setVisible(False)
        self.tbUsername.setFocus()
        self.btnLogin.clicked.connect(self.login)
        self.AddStd.triggered.connect(self.showAddNewTab)
        self.addAge.setValidator(QIntValidator())
        self.btnSaveStd.clicked.connect(self.OnSaveClick)



    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            if self.tbUsername.hasFocus():
                self.tbPassword.setFocus()
            elif self.tbPassword.hasFocus():
                self.login()
            elif self.addRegisNum.hasFocus():
                self.addName.setFocus()
            elif self.addName.hasFocus():
                self.addGender.setFocus()
            elif self.addGender.hasFocus():
                self.addDob.setFocus()
            elif self.addDob.hasFocus():
                self.addAge.setFocus()
            elif self.addAge.hasFocus():
                self.addAddress.setFocus()
            elif self.addAddress.hasFocus():
                self.addPhone.setFocus()
            elif self.addPhone.hasFocus():
                self.addEmail.setFocus()
            elif self.addEmail.hasFocus():
                self.addStandard.setFocus()
            elif self.addStandard.hasFocus():
                self.OnSaveClick()
        else:
            super().keyPressEvent(e)

    def login(self):
        un = self.tbUsername.text()
        pd = self.tbPassword.text()
        if un == "Mansi" and pd == "1234":
            self.menuBar().setVisible(True)
            self.tabWidget.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Error", "Invalid Username and Password")
            self.tbUsername.clear()
            self.tbPassword.clear()
            self.tbUsername.setFocus()

    #### Add new Student
    def showAddNewTab(self):
        self.tabWidget.setCurrentIndex(2)
        self.addRegisNum.setFocus()
        intValidator = QIntValidator()
        self.addAge.setValidator(intValidator)

    def OnSaveClick(self):
        regis_num = self.addRegisNum.text()
        name = self.addName.text()
        if regis_num == "" or name == "":
            QMessageBox.warning(self, "Error", "Please enter Registration Number and Name")
            return
        gender = self.addGender.currentText()
        dob = self.addDob.text()
        age = self.addAge.text()
        address = self.addAddress.toPlainText()
        phone = self.addPhone.text()
        email = self.addEmail.text()
        standard = self.addStandard.currentText()

        print(name, regis_num, gender, dob, age, address, phone, email, standard)
        try:
            db = DatabaseManager("localhost", "root", "*********", "school")
            db.add_student(regis_num, name, gender, dob, int(age), address, phone, email, standard)
            print("Added Successfully")
        except Exception as e:
            QMessageBox.warning(self, "Error", e)
        self.clearStd()
        self.addRegisNum.setFocus()

    def clearStd(self):
        self.addRegisNum.clear()
        self.addName.clear()
        self.addDob.clear()
        self.addAge.clear()
        self.addAddress.clear()
        self.addPhone.clear()
        self.addEmail.clear()

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
