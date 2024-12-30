# login.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from auth_db_functions import verify_login  # Importing the verify_login function
from signup import SignUpForm  # Importing the SignUpForm

class LoginForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.layout = QVBoxLayout(self)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.layout.addWidget(QLabel("Username"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QLabel("Password"))
        self.layout.addWidget(self.password_input)

        self.buttons_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        self.signup_button = QPushButton("Sign Up")
        self.signup_button.clicked.connect(self.show_signup)
        self.buttons_layout.addWidget(self.login_button)
        self.buttons_layout.addWidget(self.signup_button)

        self.layout.addLayout(self.buttons_layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = verify_login(username, password)
        if role:
            self.accept()
        else:
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setPlaceholderText("Invalid credentials")

    def show_signup(self):
        signup_form = SignUpForm(self)
        signup_form.exec()
