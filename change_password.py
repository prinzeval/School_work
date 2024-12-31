# change_password.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from auth_db_functions import change_password  # Import the change_password function

class ChangePasswordForm(QDialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Password")
        self.layout = QVBoxLayout(self)

        self.username = username
        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.layout.addWidget(QLabel("Current Password"))
        self.layout.addWidget(self.current_password_input)
        self.layout.addWidget(QLabel("New Password"))
        self.layout.addWidget(self.new_password_input)

        self.buttons_layout = QHBoxLayout()
        self.change_button = QPushButton("Change Password")
        self.change_button.clicked.connect(self.handle_change_password)
        self.buttons_layout.addWidget(self.change_button)

        self.layout.addLayout(self.buttons_layout)

    def handle_change_password(self):
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        change_password(self.username, current_password, new_password)
        self.accept()
