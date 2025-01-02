from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QSplitter, QTabWidget,
    QGridLayout, QStackedWidget, QHeaderView, QMessageBox
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap
from forms import CustomerForm, EnquiryForm
import funtions.main_Customer_db_functions as af
import mysql.connector
from pages.technician_page import TechnicianPage
from pages.part_page import PartPage
from pages.main_invoice_page import InvoicePage
from pages.vehicle_page import VehiclePage
from pages.job_page import JobPage
from change_password import ChangePasswordForm

class AutoShopManagementApp(QMainWindow):
    def __init__(self, logged_in_user, user_role, parent=None):
        super().__init__(parent)
        self.logged_in_user = logged_in_user  # Store the logged-in user
        self.user_role = user_role  # Store the user's role
        self.setWindowTitle("Auto Shop Management System")
        self.setGeometry(200, 200, 1200, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_page = QWidget()
        self.create_main_page()
        self.stack.addWidget(self.main_page)

        if self.user_role == "Admin":
            self.customer_page = QWidget()
            self.create_customer_page()
            self.stack.addWidget(self.customer_page)

            self.customer_invoice_page = QWidget()
            self.create_customer_invoice_page()
            self.stack.addWidget(self.customer_invoice_page)

            self.technician_page = TechnicianPage(self)
            self.stack.addWidget(self.technician_page)

            self.part_page = PartPage(self)
            self.stack.addWidget(self.part_page)

            self.vehicle_page = VehiclePage(self)  # Initializing the VehiclePage
            self.stack.addWidget(self.vehicle_page)

            self.enquiry_page = QWidget()
            self.create_enquiry_page()
            self.stack.addWidget(self.enquiry_page)

            self.invoice_page = InvoicePage(self)  # Initializing the main InvoicePage
            self.stack.addWidget(self.invoice_page)

            self.job_page = JobPage(self)  # Initializing the JobPage
            self.stack.addWidget(self.job_page)  # Adding the JobPage to the stack

            self.create_menu_bar()  # Create the menu bar
        elif self.user_role == "Technician":
            self.vehicle_page = VehiclePage(self)  # Initializing the VehiclePage
            self.stack.addWidget(self.vehicle_page)

            self.job_page = JobPage(self)  # Initializing the JobPage
            self.stack.addWidget(self.job_page)  # Adding the JobPage to the stack
            

        self.protect_access(self.user_role)  # Protect access based on user role

    def protect_access(self, role):
        if role != "Admin":
            self.add_container(self.grid_layout, "👨‍🔧 Technician", 0, 0, self.access_denied)
            self.add_container(self.grid_layout, "👤 Customers", 0, 1, self.access_denied)
            self.add_container(self.grid_layout, "📋 Jobs", 0, 2, self.show_jobs)
            self.add_container(self.grid_layout, "🚗 Vehicles", 1, 0, self.show_vehicles)
            self.add_container(self.grid_layout, "⚙️ Parts", 1, 1, self.access_denied)
            self.add_container(self.grid_layout, "💳 Invoices", 1, 2, self.access_denied)

    def access_denied(self):
        QMessageBox.warning(self, "Access Denied", "Only the Admin has access to this section.")

    def create_menu_bar(self):
        menubar = self.menuBar()
        account_menu = menubar.addMenu('Account')

        change_password_action = QAction('Change Password', self)
        change_password_action.triggered.connect(self.show_change_password)

        account_menu.addAction(change_password_action)

    def show_change_password(self):
        change_password_form = ChangePasswordForm(self.logged_in_user, self)
        change_password_form.exec()

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
        self.grid_layout = QGridLayout()  # Changed to self.grid_layout
        self.grid_layout.setSpacing(20)

        self.add_container(self.grid_layout, "👨‍🔧 Technician", 0, 0, self.show_technicians)
        self.add_container(self.grid_layout, "👤 Customers", 0, 1, self.show_customers)
        self.add_container(self.grid_layout, "📋 Jobs", 0, 2, self.show_jobs)

        self.add_container(self.grid_layout, "🚗 Vehicles", 1, 0, self.show_vehicles)
        self.add_container(self.grid_layout, "⚙️ Parts", 1, 1, self.show_parts)
        self.add_container(self.grid_layout, "💳 Invoices", 1, 2, self.show_invoices)

        main_layout.addLayout(self.grid_layout)

        # Only show the table section if the user is not a technician
        if self.user_role != "Technician":
            # --- Splitter for Vehicles and Table ---
            splitter = QSplitter(Qt.Orientation.Horizontal)

            # Vehicle Section (Left)
            self.vehicle_container = QLabel("🚗 Vehicles")
            self.vehicle_container.setStyleSheet("background-color: #3CB371; font-size: 24px; border: 2px solid #2E8B57;")
            self.vehicle_container.setFixedHeight(400)
            self.vehicle_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
            splitter.addWidget(self.vehicle_container)

            # Table Section (Right)
            table_section = QWidget()
            table_layout = QVBoxLayout(table_section)

            self.table_tabs = QTabWidget()
            self.table_tabs.setFixedHeight(300)
            self.table_tabs.addTab(self.create_data_table("Operations_Customer"), "Customers")
            self.table_tabs.addTab(self.create_data_table("Operations_Technician"), "Technicians")
            self.table_tabs.addTab(self.create_data_table("Operations_Part"), "Parts")
            self.table_tabs.addTab(self.create_data_table("Operations_Job"), "Jobs")

            table_layout.addWidget(self.table_tabs)
            splitter.addWidget(table_section)

            splitter.setSizes([600, 600])

            main_layout.addWidget(splitter)

            # Start image carousel
            self.vehicle_images = af.fetch_vehicle_images()
            self.current_image_index = 0
            self.update_vehicle_image()

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.next_vehicle_image)
            self.timer.start(2000)


    def create_data_table(self, table_name):
        table = QTableWidget()
        headers = {
            "Operations_Customer": ["Customer ID", "Name", "Email", "Phone Number", "Address"],
            "Operations_Technician": ["Technician ID", "Name", "Specialty", "Hourly Rate"],
            "Operations_Part": ["Part ID", "Part Name", "Unit Price", "Stock Quantity"],
            "Operations_Job": ["Job ID", "Vehicle ID", "Technician ID", "Job Type", "Start Date", "End Date", "Job Amount", "Hours", "Status"]
        }
        
        if table_name in headers:
            table.setColumnCount(len(headers[table_name]))
            table.setHorizontalHeaderLabels(headers[table_name])

        try:
            conn = af.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                rows = cursor.fetchall()
                table.setRowCount(len(rows))
                for row_index, row_data in enumerate(rows):
                    for column_index, data in enumerate(row_data):
                        table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
        return table

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

    def create_customer_page(self):
        layout = QVBoxLayout(self.customer_page)

        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)  # Adjust if needed
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

        # Set fixed height and width to match main containers
        for btn in [add_customer_btn, enquiry_btn, customer_invoice_btn]:
            btn.setFixedHeight(150)
            btn.setFixedWidth(400)
            btn.setStyleSheet("""
                font-size: 18px;
                padding: 20px;
                background-color: #3CB371;
                color: white;
                border: 2px solid #2E8B57;
                font-weight: bold;
            """)

        add_customer_btn.clicked.connect(self.add_customer)
        enquiry_btn.clicked.connect(self.show_enquiries)
        customer_invoice_btn.clicked.connect(self.show_customer_invoices)

        button_layout.addWidget(add_customer_btn)
        button_layout.addWidget(enquiry_btn)
        button_layout.addWidget(customer_invoice_btn)
        layout.addLayout(button_layout)

        # Customer table
        self.customer_table = QTableWidget()
        self.customer_table.setColumnCount(7)
        self.customer_table.setHorizontalHeaderLabels(["Customer ID", "Name", "Email", "Phone Number", "Address", "Edit", "Delete"])
        self.customer_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.customer_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.customer_table)
        layout.setStretch(3, 1)  # Ensure the table occupies the remaining space

        self.populate_customers()  # Populate customer table with data

    def populate_customers(self):
        self.customer_table.setRowCount(0)
        try:
            conn = af.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Operations_Customer")
                rows = cursor.fetchall()
                for row_index, row_data in enumerate(rows):
                    self.customer_table.insertRow(row_index)
                    for column_index, data in enumerate(row_data):
                        self.customer_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

                    # Edit button
                    edit_button = QPushButton("Edit")
                    edit_button.setStyleSheet("""
                        background-color: #E1F4F3;
                        font-size: 16px;
                        border: 2px solid #8E5724;
                        border-radius: 5px;
                        color: #000000;
                    """)
                    edit_button.clicked.connect(lambda _, ri=row_index: self.edit_customer(ri, self.customer_table))
                    self.customer_table.setCellWidget(row_index, 5, edit_button)

                    # Delete button
                    delete_button = QPushButton("Delete")
                    delete_button.setStyleSheet("""
                        background-color: #E1F4F3;
                        font-size: 16px;
                        border: 2px solid #8E5724;
                        border-radius: 5px;
                        color: #000000;
                    """)
                    delete_button.clicked.connect(lambda _, ri=row_index: self.delete_customer(ri, self.customer_table))
                    self.customer_table.setCellWidget(row_index, 6, delete_button)
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def create_customer_invoice_page(self):
        layout = QVBoxLayout(self.customer_invoice_page)

        # Back button to return to the customer page
        back_button = QPushButton("🔙 Back")
        back_button.clicked.connect(self.show_customers)
        layout.addWidget(back_button)

        nav_bar = QHBoxLayout()
        nav_bar.addWidget(QLabel("💲 Customer Invoices"))
        nav_bar.addStretch(1)
        layout.addLayout(nav_bar)

        self.invoice_table = QTableWidget()
        self.invoice_table.setColumnCount(6)
        self.invoice_table.setHorizontalHeaderLabels(["Name", "Part used", "Number of parts used", "Part amount", "Job amount", "Total cost"])
        self.invoice_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.invoice_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.invoice_table)
        layout.setStretch(2, 1)  # Ensure the table occupies the remaining space

        # Populate invoices when creating the invoice page
        rows = self.fetch_customer_invoices()
        self.populate_customer_invoices(rows)

    def fetch_customer_invoices(self):
        try:
            conn = af.connect_db()
            if conn:
                cursor = conn.cursor()
                query = """
                SELECT C.name AS Customer_Name, P.part_name AS Part_Used, JP.quantity_part_used AS Number_of_Parts_Used, 
                       JP.part_amount AS Part_Amount, J.job_amount AS Job_Amount, JP.total_cost AS Total_Cost 
                FROM operations_jobpart AS JP
                JOIN operations_job AS J ON J.job_id = JP.job_id
                JOIN operations_part AS P ON P.part_id = JP.part_id
                JOIN operations_vehicle AS V ON V.vehicle_id = J.vehicle_id
                JOIN operations_customer AS C ON C.customer_id = V.customer_id
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                cursor.close()
                conn.close()

    def populate_customer_invoices(self, rows):
        self.invoice_table.setRowCount(0)
        if rows:
            for row_index, row_data in enumerate(rows):
                self.invoice_table.insertRow(row_index)
                for column_index, data in enumerate(row_data):
                    self.invoice_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

    def create_enquiry_page(self):
        layout = QVBoxLayout(self.enquiry_page)

        # Back button to return to the customer page
        back_button = QPushButton("🔙 Back")
        back_button.clicked.connect(self.show_customers)
        layout.addWidget(back_button)

        nav_bar = QHBoxLayout()
        nav_bar.addWidget(QLabel("🕒 Enquiries"))
        nav_bar.addStretch(1)
        layout.addLayout(nav_bar)

        self.enquiry_table = QTableWidget()
        self.enquiry_table.setColumnCount(5)
        self.enquiry_table.setHorizontalHeaderLabels(["Name", "Plate number", "Enquiry Date", "Problem Description", "Technician assigned"])
        self.enquiry_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.enquiry_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.enquiry_table)
        layout.setStretch(2, 1)  # Ensure the table occupies the remaining space

        self.populate_enquiries()

    def populate_enquiries(self):
        self.enquiry_table.setRowCount(0)
        try:
            conn = af.connect_db()
            if conn:
                cursor = conn.cursor()
                query = """
                WITH name_plate_num(Customer_Name, Plate_Number) AS
                    (SELECT DISTINCT C.name, V.plate_num
                     FROM operations_customer AS C
                     JOIN operations_vehicle AS V ON C.customer_id = V.customer_id),
                     mech_job(Enquiry_date, Problem_Description, Technician_Assigned, Plate_Number) AS
                     (SELECT J.start_date, J.job_type, T.name, V.plate_num
                      FROM operations_job AS J
                      JOIN Operations_Technician AS T ON J.technician_id = T.technician_id
                      JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id)
                SELECT Customer_Name, NPN.Plate_Number AS Plate_Number, Enquiry_date, Problem_Description, Technician_Assigned
                FROM name_plate_num AS NPN
                JOIN mech_job AS MJ ON NPN.Plate_Number = MJ.Plate_Number
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                for row_index, row_data in enumerate(rows):
                    self.enquiry_table.insertRow(row_index)
                    for column_index, data in enumerate(row_data):
                        self.enquiry_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def create_invoice_page(self):
        layout = QVBoxLayout(self.invoice_page)

        back_button = QPushButton("🔙 Back")
        back_button.clicked.connect(self.show_customers)
        layout.addWidget(back_button)

        nav_bar = QHBoxLayout()
        nav_bar.addWidget(QLabel("💲 Customer Invoices"))
        nav_bar.addStretch(1)
        layout.addLayout(nav_bar)

        self.invoice_table = QTableWidget()
        self.invoice_table.setColumnCount(6)
        self.invoice_table.setHorizontalHeaderLabels(["Name", "Part used", "Number of parts used", "Part amount", "Job amount", "Total cost"])
        self.invoice_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.invoice_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.invoice_table)
        layout.setStretch(2, 1)  # Ensure the table occupies the remaining space

        # Populate invoices when creating the invoice page
        rows = self.fetch_customer_invoices()
        self.populate_customer_invoices(rows)

    def populate_customer_invoices(self, rows):
        self.invoice_table.setRowCount(0)
        if rows:
            for row_index, row_data in enumerate(rows):
                self.invoice_table.insertRow(row_index)
                for column_index, data in enumerate(row_data):
                    self.invoice_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

    def add_container(self, layout, text, row, col, on_click=None):
        container = QPushButton(text)
        container.setFixedHeight(150)
        container.setStyleSheet("""
            font-size: 18px;
            padding: 20px;
            background-color: #3CB371;
            color: white;
            border: 2px solid #2E8B57;
            font-weight: bold;
        """)
        if on_click:
            container.clicked.connect(on_click)
        layout.addWidget(container, row, col)

    def show_customers(self):
        self.stack.setCurrentWidget(self.customer_page)

    def show_customer_invoices(self):
        self.stack.setCurrentWidget(self.customer_invoice_page)

    def show_technicians(self):
        self.stack.setCurrentWidget(self.technician_page)

    def show_parts(self):
        self.stack.setCurrentWidget(self.part_page)

    def show_vehicles(self):
        self.stack.setCurrentWidget(self.vehicle_page)

    def show_enquiries(self):
        self.stack.setCurrentWidget(self.enquiry_page)

    def show_jobs(self):
        self.stack.setCurrentWidget(self.job_page)

    def show_main_page(self):
        self.stack.setCurrentWidget(self.main_page)

    def show_invoices(self):
        self.stack.setCurrentWidget(self.invoice_page)

    def add_customer(self):
        form = CustomerForm(self)
        if form.exec():
            customer_data = form.get_customer_data()
            af.add_customers(customer_data['fullname'], customer_data['email'], customer_data['phone'], customer_data['address'])
            self.populate_customers()

    def edit_customer(self, row_index, table):
        customer_id = table.item(row_index, 0).text()
        customer_data = {
            "fullname": table.item(row_index, 1).text(),
            "email": table.item(row_index, 2).text(),
            "phone": table.item(row_index, 3).text(),
            "address": table.item(row_index, 4).text()
        }

        form = CustomerForm(self, customer_data)
        if form.exec():
            updated_data = form.get_customer_data()
            af.edit_customer_name(customer_id, updated_data['fullname'])
            af.edit_customer_email(customer_id, updated_data['email'])
            af.edit_customer_phone_num(customer_id, updated_data['phone'])
            af.edit_customer_address(customer_id, updated_data['address'])
            self.populate_customers()

    def delete_customer(self, row_index, table):
        customer_id = table.item(row_index, 0).text()
        af.delete_customer(customer_id)
        self.populate_customers()

    def mainwindow_customers(self):
        table = self.create_data_table("Operations_Customer")
        self.table_tabs.removeTab(0)
        self.table_tabs.insertTab(0, table, "Customers")
        self.table_tabs.setCurrentWidget(table)

    def mainwindow_technicians(self):
        table = self.create_data_table("Operations_Technician")
        self.table_tabs.removeTab(1)
        self.table_tabs.insertTab(1, table, "Technicians")
        self.table_tabs.setCurrentWidget(table)

    def mainwindow_parts(self):
        table = self.create_data_table("Operations_Part")
        self.table_tabs.removeTab(2)
        self.table_tabs.insertTab(2, table, "Parts")
        self.table_tabs.setCurrentWidget(table)

    def mainwindow_jobs(self):
        table = self.create_data_table("Operations_Job")
        self.table_tabs.removeTab(3)
        self.table_tabs.insertTab(3, table, "Jobs")
        self.table_tabs.setCurrentWidget(table)

