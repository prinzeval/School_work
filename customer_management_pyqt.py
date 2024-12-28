import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QSplitter, QTabWidget, QGridLayout, QStackedWidget, QFormLayout, QDialog
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QFont

class CustomerForm(QDialog):
    def __init__(self, parent=None, customer_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add Customer" if customer_data is None else "Edit Customer")
        self.setGeometry(300, 300, 400, 300)

        layout = QFormLayout(self)

        self.fullname_input = QLineEdit(customer_data['fullname'] if customer_data else "")
        self.email_input = QLineEdit(customer_data['email'] if customer_data else "")
        self.phone_input = QLineEdit(customer_data['phone'] if customer_data else "")
        self.address_input = QLineEdit(customer_data['address'] if customer_data else "")

        layout.addRow("Fullname", self.fullname_input)
        layout.addRow("Email", self.email_input)
        layout.addRow("Phonenumber", self.phone_input)
        layout.addRow("Address", self.address_input)

        self.save_button = QPushButton("Save")
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.accept)

    def get_customer_data(self):
        return {
            "fullname": self.fullname_input.text(),
            "email": self.email_input.text(),
            "phone": self.phone_input.text(),
            "address": self.address_input.text()
        }

class EnquiryForm(QDialog):
    def __init__(self, parent=None, enquiry_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add Enquiry" if enquiry_data is None else "Edit Enquiry")
        self.setGeometry(300, 300, 400, 300)

        layout = QFormLayout(self)

        self.name_input = QLineEdit(enquiry_data['name'] if enquiry_data else "")
        self.plate_number_input = QLineEdit(enquiry_data['plate_number'] if enquiry_data else "")
        self.enquiry_date_input = QLineEdit(enquiry_data['enquiry_date'] if enquiry_data else "")
        self.problem_description_input = QLineEdit(enquiry_data['problem_description'] if enquiry_data else "")
        self.technician_assigned_input = QLineEdit(enquiry_data['technician_assigned'] if enquiry_data else "")

        layout.addRow("Name", self.name_input)
        layout.addRow("Plate number", self.plate_number_input)
        layout.addRow("Enquiry Date", self.enquiry_date_input)
        layout.addRow("Problem Description", self.problem_description_input)
        layout.addRow("Technician assigned", self.technician_assigned_input)

        self.save_button = QPushButton("Save")
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.accept)

    def get_enquiry_data(self):
        return {
            "name": self.name_input.text(),
            "plate_number": self.plate_number_input.text(),
            "enquiry_date": self.enquiry_date_input.text(),
            "problem_description": self.problem_description_input.text(),
            "technician_assigned": self.technician_assigned_input.text()
        }

class InvoiceForm(QDialog):
    def __init__(self, parent=None, invoice_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add Invoice" if invoice_data is None else "Edit Invoice")
        self.setGeometry(300, 300, 600, 400)

        layout = QFormLayout(self)

        self.name_input = QLineEdit(invoice_data['name'] if invoice_data else "")
        self.part_used_input = QLineEdit(invoice_data['part_used'] if invoice_data else "")
        self.num_parts_used_input = QLineEdit(invoice_data['num_parts_used'] if invoice_data else "")
        self.part_amount_input = QLineEdit(invoice_data['part_amount'] if invoice_data else "")
        self.job_amount_input = QLineEdit(invoice_data['job_amount'] if invoice_data else "")
        self.total_cost_input = QLineEdit(invoice_data['total_cost'] if invoice_data else "")

        layout.addRow("Name", self.name_input)
        layout.addRow("Part used", self.part_used_input)
        layout.addRow("Number of parts used", self.num_parts_used_input)
        layout.addRow("Part amount", self.part_amount_input)
        layout.addRow("Job amount", self.job_amount_input)
        layout.addRow("Total cost", self.total_cost_input)

        self.save_button = QPushButton("Save")
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.accept)

    def get_invoice_data(self):
        return {
            "name": self.name_input.text(),
            "part_used": self.part_used_input.text(),
            "num_parts_used": self.num_parts_used_input.text(),
            "part_amount": self.part_amount_input.text(),
            "job_amount": self.job_amount_input.text(),
            "total_cost": self.total_cost_input.text()
        }

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

        self.enquiry_page = QWidget()
        self.create_enquiry_page()
        self.stack.addWidget(self.enquiry_page)

        self.invoice_page = QWidget()
        self.create_invoice_page()
        self.stack.addWidget(self.invoice_page)

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
        self.add_container(grid_layout, "💳 Invoices", 1, 2, self.show_invoices)

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

        # Placeholder for vehicle images (remove database aspect)
        self.vehicle_images = ["path/to/image1.jpg", "path/to/image2.jpg", "path/to/image3.jpg"]
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

        add_customer_btn.clicked.connect(self.add_customer)
        enquiry_btn.clicked.connect(self.show_enquiries)
        customer_invoice_btn.clicked.connect(self.show_invoices)

        