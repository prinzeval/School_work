import sys
from PyQt6.QtWidgets import QApplication
from pages.pages import AutoShopManagementApp

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply global style
    app.setStyleSheet("""
        QMainWindow {
            background-color: #F4E1C1;
            border: 3px solid #8E5724;
        }
        QLabel {
            font-size: 18px;
            color: #8E5724;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
        }
        QLineEdit {
            font-size: 16px;
            padding: 10px;
            border: 2px solid #8E5724;
            border-radius: 5px;
        }
        QTabWidget {
            font-size: 16px;
            background-color: #F4E1C1;
            border: 2px solid #8E5724;
            font-weight: bold;
        }
        QTabBar::tab {
            background-color: #D37F3A;
            color: white;
            padding: 10px;
        }
        QTabBar::tab:selected {
            background-color: #8E5724;
        }
        QTableWidget {
            font-size: 16px;
            background-color: #FFF8E1;
            border: 1px solid #8E5724;
            font-family: 'Arial', sans-serif;
            color: #8E5724;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QPushButton {
            font-size: 16px;
            background-color: #D37F3A;
            color: white;
            border: 2px solid #8E5724;
            border-radius: 5px;
        }
    """)

    main_window = AutoShopManagementApp()
    main_window.show()
    sys.exit(app.exec())
