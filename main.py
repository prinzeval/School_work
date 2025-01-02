import sys
from PyQt6.QtWidgets import QApplication
from login import LoginForm  # Import the LoginForm
from pages.pages import AutoShopManagementApp  # Update the import path to match the directory structure

def main():
    app = QApplication(sys.argv)

    # Apply global style
    app.setStyleSheet("""
        QMainWindow {
            background-color: #E1F4F3;
            border: 3px solid #2E8B57;
        }
        QLabel {
            font-size: 18px;
            color: #2E8B57;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
        }
        QLineEdit {
            font-size: 16px;
            padding: 10px;
            border: 2px solid #2E8B57;
            border-radius: 5px;
            background-color: #E1F4F3;
        }
        QTabWidget {
            font-size: 16px;
            background-color: #E1F4F3;
            border: 2px solid #2E8B57;
            font-weight: bold;
        }
        QTabBar::tab {
            background-color: #3CB371;
            color: white;
            padding: 10px;
        }
        QTabBar::tab:selected {
            background-color: #2E8B57;
        }
        QTableWidget {
            font-size: 16px;
            background-color: #F8F8FF;
            border: 1px solid #2E8B57;
            font-family: 'Arial', sans-serif;
            color: #2E8B57;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QPushButton {
            font-size: 16px;
            background-color: #3CB371;
            color: white;
            border: 2px solid #2E8B57;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #2E8B57;
        }
        QPushButton#editButton, QPushButton#deleteButton {
            background-color: #E1F4F3;
            font-size: 16px;
            padding: 10px;
            border: 2px solid #8E5724;
            border-radius: 5px;
            color: black;
        }
    """)

    login_form = LoginForm()  # Instantiate the login form
    if login_form.exec():  # Check if the login is successful
        main_window = AutoShopManagementApp(login_form.logged_in_user, login_form.user_role)
        main_window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
