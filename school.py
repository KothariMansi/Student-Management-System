import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

from DatabaseManager import DatabaseManager
from SearchDialog import SearchDialog

ui, _ = loadUiType('school.ui')

class MainApp(QMainWindow, ui):

    db = DatabaseManager("localhost", "root", "mansi_116", "school")
    def __init__(self):
        QMainWindow.__init__(self)
        self.searchDialog = None
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menuBar().setVisible(False)
        self.tbUsername.setFocus()
        self.btnLogin.clicked.connect(self.login)
        self.AddStd.triggered.connect(self.showAddNewTab)
        self.addAge.setValidator(QIntValidator())
        self.btnSaveStd.clicked.connect(self.OnSaveClick)
        self.DeleteEditStd.triggered.connect(self.showDeleteEditTab)
        self.editRegis_num.setReadOnly(True)
        self.id = 0
        self.deleteStd.clicked.connect(self.OnDeleteClick)
        self.editStd.clicked.connect(self.OnEditClick)

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
            elif self.editRegis_num.hasFocus():
                # show QDialog search
                try:
                    self.searchDialog = SearchDialog(callback=self.handle_selected_value_of_edit)
                    self.searchDialog.show()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            elif self.editName.hasFocus():
                self.editGender.setFocus()
            elif self.editGender.hasFocus():
                self.editDob.setFocus()
            elif self.editDob.hasFocus():
                self.editAge.setFocus()
            elif self.editAge.hasFocus():
                self.editAddress.setFocus()
            elif self.editAddress.hasFocus():
                self.editPhone.setFocus()
            elif self.editPhone.hasFocus():
                self.editEmail.setFocus()
            elif self.editEmail.hasFocus():
                self.editStandard.setFocus()
        #     elif self.editStandard.hasFocus():
        #         self.editStd.setFocusPolicy(Qt.StrongFocus)
        #         self.editStd.setFocus()
        #         self.editStd.setFoucs()
        #     elif self.editStd.hasFocus():
        #         self.OnEditClick()
        #     elif self.deleteStd.hasFocus():
        #         self.OnDeleteClick()
        # elif e.key() == Qt.Key_Left and self.editStd.hasFocus():
        #     self.deleteStd.setFocusPolicy(Qt.StrongFocus)
        #     self.deleteStd.setFocus()
        # elif e.key() == Qt.Key_Right and self.deleteStd.hasFocus():
        #     self.editStd.setFocusPolicy(Qt.StrongFocus)
        #     self.editStd.setFocus()
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
            self.db.add_student(regis_num, name, gender, dob, int(age), address, phone, email, standard)
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

    ##### Edit New Std
    def showDeleteEditTab(self):
        self.tabWidget.setCurrentIndex(3)
        self.editRegis_num.setFocus()

    def handle_selected_value_of_edit(self, value):
        self.id = value
        print(self.id)
        ### Query to get the data and fill in the text field TODO
        data = self.db.fetch_query("select * from student where id = %s", (self.id, ))
        print(data)
        if data:
            data = data[0]
            self.editRegis_num.setText(data[1])
            self.editName.setText(data[2])
            self.editGender.setCurrentText(data[3])
            self.editDob.setText(data[4])
            self.editAge.setText(str(data[5]))
            self.editAddress.setPlainText(data[6])
            self.editPhone.setText(data[7])
            self.editEmail.setText(data[8])
            self.editStandard.setCurrentText(data[9])
        self.editName.setFocus()

    def OnEditClick(self):
        #Query to update Data
        try:
            self.db.execute_query(
                "Update student set full_name=%s, gender=%s, date_of_birth=%s, age=%s, address=%s, phone=%s, email=%s, standard=%s where id=%s",
                (self.editName.text(), self.editGender.currentText(), self.editDob.text(), int(self.editAge.text()), self.editAddress.toPlainText(),
                 self.editPhone.text(), self.editEmail.text(), self.editStandard.currentText(), self.id)
            )
            print("Updated Successfully")
            self.editScreenClear()
        except Exception as e:
            print("Error in updating:", e)

    def OnDeleteClick(self):
        #Query to delete Data
        try:
            self.db.execute_query("delete from student where id = %s", (self.id,))
            print("Deleted Successfully")
            self.editScreenClear()
        except Exception as e:
            print(e)

    def editScreenClear(self):
        self.editRegis_num.clear()
        self.editName.clear()
        self.editDob.clear()
        self.editGender.setCurrentIndex(0)
        self.editAge.clear()
        self.editAddress.clear()
        self.editPhone.clear()
        self.editEmail.clear()
        self.editStandard.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
