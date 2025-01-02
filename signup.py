# signup.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox
from auth_db_functions import add_new_user  # Import the add_new_user function

class SignUpForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign Up")
        self.layout = QVBoxLayout(self)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_input = QComboBox()
        self.role_input.addItems(["Admin", "Technician"])  # Assuming these roles

        self.layout.addWidget(QLabel("Username"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QLabel("Password"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(QLabel("Role"))
        self.layout.addWidget(self.role_input)

        self.buttons_layout = QHBoxLayout()
        self.signup_button = QPushButton("Sign Up")
        self.signup_button.clicked.connect(self.handle_signup)
        self.buttons_layout.addWidget(self.signup_button)

        self.layout.addLayout(self.buttons_layout)

    def handle_signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText()
        add_new_user(username, password, role)
        self.accept()
















