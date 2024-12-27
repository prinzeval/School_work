import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QSplitter, QTabWidget, QGridLayout, QStackedWidget
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QFont
from controller import connect_db, fetch_vehicle_images, populate_table

class AutoShopManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Shop Management System")
        self.setGeometry(200, 200, 1200, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_page = QWidget()
        self.create_main_page()
        self.stack.addWidget(self.main_page)

        self.customer_page = QWidget()
        self.create_customer_page()
        self.stack.addWidget(self.customer_page)

    def create_main_page(self):
        main_layout = QVBoxLayout(self.main_page)

        # --- Top Navigation Bar ---
        nav_bar = QHBoxLayout()
        search_box = QLineEdit()
        search_box.setPlaceholderText("What are you looking for...")
        search_box.setFixedWidth(400)
        nav_bar.addWidget(QLabel("🔧 Auto Shop Management System"))
        nav_bar.addStretch(1)
        nav_bar.addWidget(search_box)

        main_layout.addLayout(nav_bar)

        # --- Grid Layout for 6 Main Containers ---
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        self.add_container(grid_layout, "📊 Analytics", 0, 0)
        self.add_container(grid_layout, "👤 Customers", 0, 1, self.show_customers)
        self.add_container(grid_layout, "📋 Jobs", 0, 2)

        self.add_container(grid_layout, "🔧 Requests", 1, 0)
        self.add_container(grid_layout, "⚙️ Parts", 1, 1)
        self.add_container(grid_layout, "💳 Invoices", 1, 2)

        main_layout.addLayout(grid_layout)

        # --- Splitter for Vehicles and Table ---
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Vehicle Section (Left)
        self.vehicle_container = QLabel("🚗 Vehicles")
        self.vehicle_container.setStyleSheet("background-color: #D37F3A; font-size: 24px; border: 2px solid #8E5724;")
        self.vehicle_container.setFixedHeight(300)
        self.vehicle_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        splitter.addWidget(self.vehicle_container)

        # Table Section (Right)
        table_section = QWidget()
        table_layout = QVBoxLayout(table_section)

        self.table_tabs = QTabWidget()
        self.table_tabs.setFixedHeight(300)
        self.add_table(self.table_tabs, "Operations_Customer")
        self.add_table(self.table_tabs, "Operations_Technician")
        self.add_table(self.table_tabs, "Operations_Part")
        self.add_table(self.table_tabs, "Operations_Job")

        table_layout.addWidget(self.table_tabs)
        splitter.addWidget(table_section)

        splitter.setSizes([600, 600])

        main_layout.addWidget(splitter)

        # Start image carousel
        self.vehicle_images = fetch_vehicle_images()
        self.current_image_index = 0
        self.update_vehicle_image()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_vehicle_image)
        self.timer.start(9000)

    def create_customer_page(self):
        layout = QVBoxLayout(self.customer_page)

        # Back button to return to the main page
        back_button = QPushButton("🔙 Back")
        back_button.clicked.connect(self.show_main_page)
        layout.addWidget(back_button)

        # Navigation bar
        nav_bar = QHBoxLayout()
        nav_bar.addWidget(QLabel("👤 Customers"))
        nav_bar.addStretch(1)
        layout.addLayout(nav_bar)

        # Buttons at the top
        button_layout = QHBoxLayout()
        add_customer_btn = QPushButton("➕ Add Customer")
        enquiry_btn = QPushButton("🕒 Enquiry")
        customer_invoice_btn = QPushButton("💲 Customer Invoice")

        button_layout.addWidget(add_customer_btn)
        button_layout.addWidget(enquiry_btn)
        button_layout.addWidget(customer_invoice_btn)
        layout.addLayout(button_layout)

        # Customer table
        self.customer_table = QTableWidget()
        self.customer_table.setColumnCount(5)
        self.customer_table.setHorizontalHeaderLabels(["Customer ID", "Name", "Email", "Phone Number", "Address"])
        layout.addWidget(self.customer_table)

        populate_table(self.customer_table, "Operations_Customer")

    def add_container(self, layout, text, row, col, on_click=None):
        container = QPushButton(text)
        container.setFixedHeight(150)
        container.setStyleSheet("""
            font-size: 18px;
            padding: 20px;
            background-color: #D37F3A;
            color: white;
            border: 2px solid #8E5724;
            font-weight: bold;
        """)
        if on_click:
            container.clicked.connect(on_click)
        layout.addWidget(container, row, col)

    def add_table(self, table_widget, table_name):
        table = QTableWidget()
        populate_table(table, table_name)
        table_widget.addTab(table, table_name.split('_')[1])

    def update_vehicle_image(self):
        if self.vehicle_images:
            local_path = self.vehicle_images[self.current_image_index].replace("\\", "/")
            pixmap = QPixmap(local_path)
            if pixmap.isNull():
                pixmap = QPixmap("default_placeholder.png")
            self.vehicle_container.setPixmap(pixmap.scaled(500, 300, Qt.AspectRatioMode.KeepAspectRatio))

    def next_vehicle_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.vehicle_images)
        self.update_vehicle_image()

    def show_customers(self):
        self.stack.setCurrentWidget(self.customer_page)

    def show_main_page(self):
        self.stack.setCurrentWidget(self.main_page)

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
            padding: 10px;
            background-color: #D37F3A;
            color: white;
            border: 2px solid #8E5724;
            border-radius: 5px;
        }
    """)

    main_window = AutoShopManagementApp()
    main_window.show()
    sys.exit(app.exec())
