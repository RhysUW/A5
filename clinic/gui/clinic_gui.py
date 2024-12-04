import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
                             QApplication, QMainWindow, QLabel, QPushButton, 
                             QGridLayout, QWidget, QLineEdit, QMessageBox, QVBoxLayout,
                             QScrollArea, QTableView, QAbstractItemView, QHBoxLayout,
                             QHeaderView, QRadioButton, QPlainTextEdit, QSpacerItem, QSizePolicy
                             )
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from clinic.controller import Controller
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException


class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # Continue here with your code!
        self.controller = Controller()
        self.setWindowTitle("Login")
        self.setMinimumSize(400, 600)
        self.loginScreen() 
        self.user = ""
        self.passw = ""
        self.oldPhn = ""
        self.note = None
        
    #initializes the login screen and allows user to login
    def loginScreen(self):
        layout = QGridLayout()
        username = QLabel("Username: ")
        userInput = QLineEdit(self)
        password = QLabel("Password: ")
        passInput = QLineEdit(self)
        loginButton = QPushButton("Login")
        username.setMinimumHeight(300)

        layout.addWidget(username, 1, 0)
        layout.addWidget(userInput, 1, 1)
        layout.addWidget(password, 2, 0)
        layout.addWidget(passInput, 2, 1)
        layout.addWidget(loginButton, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.setVerticalSpacing(50)

        center = QWidget()
        center.setLayout(layout)
        self.setCentralWidget(center)

        loginButton.clicked.connect(lambda: self.loginHandler(userInput, passInput))

    #handles what happens when login button is clicked
    def loginHandler(self, username, password):
        self.user = username.text()
        self.passw = password.text()
        
        try:
            logged_in = self.controller.login(self.user, self.passw)

            if logged_in:
                QMessageBox.information(None, "Succesfully logged in", f"welcome {self.user}")
                self.mainMenu()
            else:
                QMessageBox.warning(None, "Incorrect username/password" "Try a differnet username or password")
        except InvalidLoginException:
            QMessageBox.warning(None, "Incorrect username/password", "Try a differnet username or password")

    #initializes the main screen 
    def mainMenu(self):
        self.setMinimumSize(900, 1200)
        self.setWindowTitle("Medical Thing")
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(10, 25, 10, 10)
        inputLayout = QGridLayout()
        inputLayout.setHorizontalSpacing(30)  # Space between columns
        inputLayout.setVerticalSpacing(15)    # Space between rows

        #need these input fields phn, name, birth_date, phone, email, address
        phnText = QLabel("Personal Health Number: ")
        phnInput = QLineEdit()
        nameText = QLabel("Name: ")
        nameInput = QLineEdit()
        birthDateText = QLabel("Date of Birth: ")
        BirthDateInput = QLineEdit()
        phoneText = QLabel("Phone Number: ")
        phoneInput = QLineEdit()
        emailText = QLabel("Email: ")
        emailInput = QLineEdit()
        addressText = QLabel("Address: ")
        addressInput = QLineEdit()

        inputLayout.addWidget(phnText, 0, 0)
        inputLayout.addWidget(phnInput, 0, 1)
        inputLayout.addWidget(nameText, 1, 0)
        inputLayout.addWidget(nameInput, 1, 1)
        inputLayout.addWidget(birthDateText, 2, 0)
        inputLayout.addWidget(BirthDateInput, 2, 1)
        inputLayout.addWidget(phoneText, 3, 0)
        inputLayout.addWidget(phoneInput, 3, 1)
        inputLayout.addWidget(emailText, 4, 0)
        inputLayout.addWidget(emailInput,4 , 1)
        inputLayout.addWidget(addressText, 5, 0)
        inputLayout.addWidget(addressInput, 5, 1)

        #all the buttons below the input fields
        buttonLayout = QGridLayout()
        buttonLayout.setContentsMargins(0, 10, 0, 10)
        buttonLayout.setVerticalSpacing(10)
        searchButton = QPushButton("Search")
        createButton = QPushButton("Create New Patient")
        listButton = QPushButton("List All Patients")
        updateButton = QPushButton("Update Paitent info")
        deleteButton = QPushButton("Delete Patient")
        currentButton = QPushButton("Set Current Patient")
        unsetButton = QPushButton("Unset Current Patient")
        buttonLayout.addWidget(searchButton, 0, 0)
        buttonLayout.addWidget(createButton, 0, 1)
        buttonLayout.addWidget(listButton, 0, 2)
        buttonLayout.addWidget(updateButton, 1, 0)
        buttonLayout.addWidget(deleteButton, 1, 1)
        buttonLayout.addWidget(currentButton, 1, 2)
        buttonLayout.addWidget(unsetButton, 1, 3)
        searchButton.clicked.connect(lambda: self.searchPatient(nameInput, phnInput, patientTable))
        createButton.clicked.connect(lambda: self.createPatient(phnInput, nameInput, BirthDateInput, phoneInput, emailInput, addressInput))
        listButton.clicked.connect(lambda: self.listPatients(patientTable))
        updateButton.clicked.connect(lambda: self.updatePatient(phnInput, nameInput, BirthDateInput, phoneInput, emailInput, addressInput))
        deleteButton.clicked.connect(lambda: self.deletePatient(phnInput))
        currentButton.clicked.connect(lambda: self.setCurrent(phnInput))
        unsetButton.clicked.connect(self.unsetCurrent)

        #table that displays patient information
        patientTable = QTableView()
        patientTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        patientTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(patientTable)

        #Area to make and display notes
        noteDisplay = QPlainTextEdit()

        #buttons for creating and altering notes
        noteButtons = QGridLayout()
        newNoteButton = QPushButton("Create new Note")
        retNotesButton = QPushButton("Retrieve existing Notes")
        updateNoteButton = QPushButton("Update Existing Note")
        delNoteButton = QPushButton("Delete Note")
        recordButton = QPushButton("List patient record")
        noteButtons.addWidget(newNoteButton, 0, 0)
        noteButtons.addWidget(retNotesButton, 0, 1)
        noteButtons.addWidget(updateNoteButton, 0, 2)
        noteButtons.addWidget(delNoteButton, 0, 3)
        noteButtons.addWidget(recordButton, 0, 4)
        newNoteButton.clicked.connect(lambda: self.newNote(noteDisplay))
        retNotesButton.clicked.connect(lambda: self.retNote(noteDisplay))
        updateNoteButton.clicked.connect(lambda: self.updateNote(noteDisplay))
        delNoteButton.clicked.connect(lambda: self.delNote(noteDisplay))
        recordButton.clicked.connect(lambda: self.listRecord(noteDisplay))

        #layout for the logout button
        logoutLayout = QGridLayout()
        logoutButton = QPushButton("Logout")
        logoutLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 0) 
        logoutLayout.addWidget(logoutButton, 0, 1)
        logoutButton.clicked.connect(self.logout)

        #adding layouts and widgets to the main layout
        mainLayout.addLayout(inputLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(scrollArea, stretch=3)
        mainLayout.addLayout(noteButtons)
        mainLayout.addWidget(noteDisplay, stretch=2)
        mainLayout.addLayout(logoutLayout)
        mainLayout.addStretch()
        
        center = QWidget()
        center.setLayout(mainLayout)
        self.setCentralWidget(center)

    #method handles the search patient function and the retrieve patients function
    def searchPatient(self, name, phn, patientTable):
        print(name.text())
        print(phn.text())
        #if searched is pressed and neither field is filled
        if(name.text() == "" and phn.text() == ""):
            QMessageBox.warning(None, "Invalid Information", "Enter a valid personal health number or name")
            return
        #if search is pressed and a phn is entered search patient by phn
        elif(name.text() == "" and phn.text()):
            try:
                patient = self.controller.search_patient(phn.text())
                if patient:
                    #remove this when done
                    model = QStandardItemModel()
                    setCurrentPatient = QRadioButton()
                    model.setHorizontalHeaderLabels(["Name", "PHN", "Date of Birth", "Phone", "Email", "Address", "Set Current Patient"])
                    model.appendRow([QStandardItem(patient.getName()), 
                                     QStandardItem(patient.getPhn()), 
                                     QStandardItem(patient.getBirthDay()),
                                     QStandardItem(patient.getPhone()),
                                     QStandardItem(patient.getEmail()),
                                     QStandardItem(patient.getAddress())])                  
                    patientTable.setModel(model)
                    patientTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                else:
                    QMessageBox.warning(None, "Not found", "no patient found with that phn please try again")
            except Exception as e:
                QMessageBox.warning(None, "Error", "an error occured")
        elif(name.text() and phn.text() == ""):
            try:
                model = QStandardItemModel()
                patients = self.controller.retrieve_patients(name.text())
                model.setHorizontalHeaderLabels(["Name", "PHN", "Date of Birth", "Phone", "Email", "Address", "Set Current Patient"])
                #loops through all the patients printing their data to the table
                for patient in patients:
                    model.appendRow([QStandardItem(patient.getName()), 
                                     QStandardItem(patient.getPhn()), 
                                     QStandardItem(patient.getBirthDay()),
                                     QStandardItem(patient.getPhone()),
                                     QStandardItem(patient.getEmail()),
                                     QStandardItem(patient.getAddress())])                  
                    patientTable.setModel(model)
                    patientTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            except Exception as e:
                QMessageBox.warning(None, "Error", "an error occured")

        #either wrong phn or wrong name
        else:
            QMessageBox.warning(None, "Invalid Information", "Enter a valid personal health number or name")
            return

    #handles what happens when the createPatient button is pressed    
    def createPatient(self, phnInput, nameInput, BirthDateInput, phoneInput, emailInput, addressInput):
        if(phnInput.text() == "" or nameInput.text() == "" or BirthDateInput.text() == "" 
           or phoneInput.text() == "" or emailInput.text() == "" or addressInput.text() == ""):
            QMessageBox.warning(None, "Missing Information", "please enter data into all fields")
        else: 
            try:
                self.controller.create_patient(phnInput.text(), nameInput.text(), BirthDateInput.text(), phoneInput.text(), emailInput.text(), addressInput.text())
                QMessageBox.information(None, "Succsess", "Patient created succesfully")
            except IllegalOperationException as e:
                QMessageBox.warning(None, "Illegal Operation", "Patient with that PHN already exists")
        phnInput.clear()
        nameInput.clear()
        BirthDateInput.clear()
        phoneInput.clear()
        emailInput.clear()
        addressInput.clear()

    #handles what happens when the list patient button is pressed
    def listPatients(self, patientTable):
        patients = self.controller.list_patients()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Name", "PHN", "Date of Birth", "Phone", "Email", "Address", "Set Current Patient"])
            #loops through all the patients printing their data to the table
        for patient in patients:
            model.appendRow([QStandardItem(patient.getName()), 
                            QStandardItem(patient.getPhn()), 
                            QStandardItem(patient.getBirthDay()),
                            QStandardItem(patient.getPhone()),
                            QStandardItem(patient.getEmail()),
                            QStandardItem(patient.getAddress())])                  
            patientTable.setModel(model)
            patientTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    
    def deletePatient(self, phn):
        try:
            patient = self.controller.search_patient(phn.text())
        except IllegalOperationException as e:
            QMessageBox.warning(None, "Error", "Patient with that phn does not exist try again")
        try:
            self.controller.delete_patient(phn.text())
            QMessageBox.information(None, "Success", "Patient Succesfully deleted")
        except IllegalOperationException as e:
            QMessageBox.warning(None, "Error", "Cannot delete current patient please unset before deleting")
    #press the button once to get the old PHN, then press again with new data in fields to update the patient
    def updatePatient(self, phn, name, birthDay, phone, email, address):
        try:  
            if(phn.text() != "" and name.text() != "" and birthDay.text() != ""
                  and phone.text() != "" and email.text() != "" and address.text() != ""):
                self.controller.update_patient(self.oldPhn, phn.text(), name.text(), birthDay.text(), phone.text(), email.text(), address.text())
                QMessageBox.information(None, "Success", "Patient information succesfully updated")
            elif(phn.text() != ""):
                self.oldPhn = phn.text()
                phn.clear()
                QMessageBox.information(None, "Information", "please enter new information")
            else:
                 QMessageBox.warning(None, "Error", "Please enter patient you wish to update's PHN")

        except IllegalOperationException as e:
            QMessageBox.warning(None, "Error", "Please try again")

    def setCurrent(self, phn):
        try:
            if self.controller.current_patient:
                QMessageBox.warning(None, "Illegal Operation", "Please unset current patient before setting a new one")
            self.controller.set_current_patient(phn.text())
            QMessageBox.information(None, "Patient set", "Current patient set")
        except IllegalOperationException as e:
            QMessageBox.warning(None, "No User Found", "No patients match the PHN please try again")

    def unsetCurrent(self):
        self.controller.unset_current_patient()

    def newNote(self, textField):
        try:
            self.controller.create_note(textField.toPlainText())
            QMessageBox.information(None, "Added to Record", "Note succesfully added to patient record")
            textField.clear()
        except NoCurrentPatientException:
            QMessageBox.warning(None, "Error", "Select a current patient")

    def retNote(self, input):
        try:
            if(input.toPlainText() == ""):
                QMessageBox.warning(None, "Warning", "Please enter search criteria in the box below")
            else:
                list = self.controller.retrieve_notes(input.toPlainText())
                for note in list:
                    input.appendPlainText(note.__str__())
        except NoCurrentPatientException:
            QMessageBox.warning(None, "Error", "Must set current patient")
    
    def updateNote(self, input):
        try:
            if(self.note is None):
                QMessageBox.information(None, "Note selected", "Please enter new information and press again")
                change = self.controller.search_note(int(input.toPlainText()))
                self.note = change
            elif(self.note is not None):
                self.controller.update_note(self.note.getCode(), input.toPlainText())
                self.note = None
                QMessageBox.information(None, "Success", "Note updated succesfully")
            else:
                QMessageBox.warning(None, "Error", "please enter a valid note code")
                

        except NoCurrentPatientException:
            QMessageBox.warning(None, "Warning", "Please set a current patient")

    def delNote(self, input):
        try:
            note = self.controller.delete_note(int(input.toPlainText()))
            if(note):
                QMessageBox.information(None, "Success", "Note deleted successfully")
            else:
                QMessageBox.warning(None, "Error", "No note with that code exists")
        except NoCurrentPatientException:
            QMessageBox.warning(None, "Error", "Please set a current patient")

    def listRecord(self, display):
        try:
            list = self.controller.list_notes()
            for note in list:
                display.appendPlainText(note.__str__())
        except NoCurrentPatientException:
            QMessageBox.warning(None, "Error", "Please set a current patient")

    def logout(self):
        self.controller.logout()
        self.loginScreen()


def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()
    

if __name__ == '__main__':
    main()
