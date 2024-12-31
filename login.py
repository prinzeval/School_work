# login.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from auth_db_functions import verify_login  # Importing the verify_login function
from signup import SignUpForm  # Importing the SignUpForm
from change_password import ChangePasswordForm  # Importing the ChangePasswordForm

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
        self.change_password_button = QPushButton("Change Password")
        self.change_password_button.clicked.connect(self.show_change_password)
        self.change_password_button.setEnabled(False)  # Initially disabled
        self.buttons_layout.addWidget(self.login_button)
        self.buttons_layout.addWidget(self.signup_button)
        self.buttons_layout.addWidget(self.change_password_button)

        self.layout.addLayout(self.buttons_layout)

        self.logged_in_user = None
        print("LoginForm initialized")  # Debugging print statement

    # ... other methods ...



    # login.py
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = verify_login(username, password)
        if role:
            self.logged_in_user = username
            self.user_role = role  # Store the user role
            self.change_password_button.setEnabled(True)
            self.accept()
        else:
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setPlaceholderText("Invalid credentials")


    def show_signup(self):
        signup_form = SignUpForm(self)
        signup_form.exec()

    def show_change_password(self):
        if self.logged_in_user:
            print("Opening Change Password Form for:", self.logged_in_user)  # Debugging print statement
            change_password_form = ChangePasswordForm(self.logged_in_user, self)
            change_password_form.exec()
