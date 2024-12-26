import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QSplitter, QTabWidget, QGridLayout
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QFont

# Database connection function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Vondabaic2020",
        database="Autoshop"
    )

class AutoShopManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Shop Management System")
        self.setGeometry(200, 200, 1200, 800)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        main_layout = QVBoxLayout(self.main_widget)

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
        self.add_container(grid_layout, "👤 Customers", 0, 1)
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
        self.add_table("Operations_Customer")
        self.add_table("Operations_Technician")
        self.add_table("Operations_Part")
        self.add_table("Operations_Job")

        table_layout.addWidget(self.table_tabs)
        splitter.addWidget(table_section)

        splitter.setSizes([600, 600])

        main_layout.addWidget(splitter)

        # Start image carousel
        self.vehicle_images = self.fetch_vehicle_images()
        self.current_image_index = 0
        self.update_vehicle_image()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_vehicle_image)
        self.timer.start(9000)

    def add_container(self, layout, text, row, col):
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
        layout.addWidget(container, row, col)

    def add_table(self, table_name):
        table = QTableWidget()
        self.populate_table(table, table_name)
        self.table_tabs.addTab(table, table_name.split('_')[1])

    def populate_table(self, table, table_name):
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()

        table.setRowCount(len(records))
        table.setColumnCount(len(records[0]))

        for row_index, row_data in enumerate(records):
            for column_index, data in enumerate(row_data):
                table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()

    def fetch_vehicle_images(self):
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT image FROM Operations_Vehicle")
        images = [item[0] for item in cursor.fetchall()]
        cursor.close()
        connection.close()
        return images

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
    """)

    main_window = AutoShopManagementApp()
    main_window.show()
    sys.exit(app.exec())
