import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QLineEdit, QMessageBox
from clinic.controller import Controller
from clinic.exception.invalid_login_exception import InvalidLoginException


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


    def loginHandler(self, username, password):
        self.user = username.text()
        self.passw = password.text()
        print(self.passw)
        print(self.user)
        
        try:
            logged_in = self.controller.login(self.user, self.passw)

            if logged_in:
                QMessageBox.information(None, "Succesfully logged in", f"welcome {self.user}")
                self.mainMenu()
            else:
                QMessageBox.warning(None, "Incorrect username/password" "Try a differnet username or password")
        except InvalidLoginException:
            QMessageBox.warning(None, "Incorrect username/password", "Try a differnet username or password")
            
    def mainMenu(self):
        self.setMinimumSize(900, 1200)
        self.setWindowTitle("Medical Thing")
        mainLayout = QGridLayout()
        center = QWidget()
        center.setLayout(mainLayout)
        self.setCentralWidget(center)




def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()
    

if __name__ == '__main__':
    main()
