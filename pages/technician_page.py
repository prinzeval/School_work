from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QFormLayout
import funtions.technician_db_functions as af  # Importing the technician database functions
from forms import TechnicianForm  # Assuming you have a form for technicians
import mysql.connector

class TechnicianPage(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.layout = QVBoxLayout(self)

        # Top buttons
        button_layout = QHBoxLayout()
        add_technician_btn = QPushButton("Add Technician")
        daily_wage_btn = QPushButton("Daily Wage")
        assign_job_btn = QPushButton("Assign Job")
        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)
        back_button.setStyleSheet("""
            font-size: 18px;
            padding: 10px;
            background-color: #D37F3A;
            color: white;
            border: 2px solid #8E5724;
            font-weight: bold;
        """)
        back_button.clicked.connect(self.show_main_page)

        for btn in [add_technician_btn, daily_wage_btn, assign_job_btn]:
            btn.setFixedHeight(100)
            btn.setStyleSheet("""
                font-size: 18px;
                padding: 20px;
                background-color: #D37F3A;
                color: white;
                border: 2px solid #8E5724;
                font-weight: bold;
            """)

        add_technician_btn.clicked.connect(self.add_technician)
        daily_wage_btn.clicked.connect(self.show_daily_wage)
        assign_job_btn.clicked.connect(self.assign_job)

        button_layout.addWidget(add_technician_btn)
        button_layout.addWidget(daily_wage_btn)
        button_layout.addWidget(assign_job_btn)
        self.layout.addWidget(back_button)
        self.layout.addLayout(button_layout)

        # Technician table
        self.technician_table = QTableWidget()
        self.technician_table.setColumnCount(7)
        self.technician_table.setHorizontalHeaderLabels(["Technician ID", "Name", "Specialty", "Hourly Rate", "Edit", "Delete"])
        self.technician_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.technician_table.horizontalHeader().setStretchLastSection(True)

        self.layout.addWidget(self.technician_table)
        self.layout.setStretch(1, 1)  # Ensure the table occupies the remaining space

        # Populate table with technicians
        self.populate_technicians()

    def populate_technicians(self):
        # Clear existing rows
        self.technician_table.setRowCount(0)

        try:
            rows = af.read_technicians()
            if rows:
                for row_index, row_data in enumerate(rows):
                    self.technician_table.insertRow(row_index)
                    for column_index, data in enumerate(row_data):
                        self.technician_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
                    edit_button = QPushButton("Edit")
                    edit_button.clicked.connect(lambda _, ri=row_index: self.edit_technician(ri))
                    self.technician_table.setCellWidget(row_index, 4, edit_button)
                    delete_button = QPushButton("Delete")
                    delete_button.clicked.connect(lambda _, ri=row_index: self.delete_technician(ri))
                    self.technician_table.setCellWidget(row_index, 5, delete_button)
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def add_technician(self):
        form = TechnicianForm(self)
        if form.exec():
            technician_data = form.get_technician_data()
            af.add_technicians(technician_data['name'], technician_data['specialty'], technician_data['hourly_rate'])
            self.populate_technicians()

    def edit_technician(self, row_index):
        technician_id = self.technician_table.item(row_index, 0).text()
        technician_data = {
            "name": self.technician_table.item(row_index, 1).text(),
            "specialty": self.technician_table.item(row_index, 2).text(),
            "hourly_rate": self.technician_table.item(row_index, 3).text()
        }

        form = TechnicianForm(self, technician_data)
        if form.exec():
            updated_data = form.get_technician_data()
            af.edit_technician_name(technician_id, updated_data['name'])
            af.edit_technician_specialty(technician_id, updated_data['specialty'])
            af.edit_technician_hourly_rate(technician_id, updated_data['hourly_rate'])
            self.populate_technicians()

    def delete_technician(self, row_index):
        technician_id = self.technician_table.item(row_index, 0).text()
        af.delete_technician(technician_id)
        self.populate_technicians()

    def show_daily_wage(self):
        daily_wage_page = DailyWagePage(self.main_app, self)
        self.main_app.stack.addWidget(daily_wage_page)
        self.main_app.stack.setCurrentWidget(daily_wage_page)

    def assign_job(self):
        assign_job_page = AssignJobPage(self.main_app, self)
        self.main_app.stack.addWidget(assign_job_page)
        self.main_app.stack.setCurrentWidget(assign_job_page)

    def show_main_page(self):
        self.main_app.stack.setCurrentWidget(self.main_app.main_page)

class DailyWagePage(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.layout = QVBoxLayout(self)

        # Back button
        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.show_technician_page)
        self.layout.addWidget(back_button)

        # Wage table
        self.wage_table = QTableWidget()
        self.wage_table.setColumnCount(6)
        self.wage_table.setHorizontalHeaderLabels(["Date", "Technician Name", "Hours Worked", "Hourly Rate", "Job Amount", "Wage"])
        self.wage_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.wage_table.horizontalHeader().setStretchLastSection(True)

        self.layout.addWidget(self.wage_table)
        self.layout.setStretch(1, 1)  # Ensure the table occupies the remaining space

        # Populate table with wages
        self.populate_wages()

    def populate_wages(self):
        # Clear existing rows
        self.wage_table.setRowCount(0)

        try:
            rows = af.view_daily_wage()
            if rows:
                for row_index, row_data in enumerate(rows):
                    self.wage_table.insertRow(row_index)
                    for column_index, data in enumerate(row_data):
                        self.wage_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def show_technician_page(self):
        self.main_app.stack.setCurrentWidget(self.main_app.technician_page)

class AssignJobPage(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.layout = QVBoxLayout(self)

        # Back button
        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.show_technician_page)
        self.layout.addWidget(back_button)

        # Assign Job Form
        form_layout = QFormLayout()
        
        self.customer_name_input = QLineEdit()
        self.plate_num_input = QLineEdit()
        self.problem_description_input = QLineEdit()
        self.technician_name_input = QLineEdit()
        
        form_layout.addRow("Customer Name", self.customer_name_input)
        form_layout.addRow("Vehicle Plate Number", self.plate_num_input)
        form_layout.addRow("Problem Description", self.problem_description_input)
        form_layout.addRow("Technician Name", self.technician_name_input)
        
        self.layout.addLayout(form_layout)
        
        approve_button = QPushButton("Approve")
        approve_button.setFixedHeight(50)
        approve_button.setStyleSheet("""
            font-size: 18px;
            padding: 10px;
            background-color: #D37F3A;
            color: white;
            border: 2px solid #8E5724;
            font-weight: bold;
        """)
        approve_button.clicked.connect(self.assign_job)
        
        self.layout.addWidget(approve_button)
        
    def assign_job(self):
        customer_name = self.customer_name_input.text()
        plate_num = self.plate_num_input.text()
        problem_description = self.problem_description_input.text()
        technician_name = self.technician_name_input.text()
        
        af.assign_technician(customer_name, plate_num, problem_description, technician_name)
        
        # Clear the form inputs
        self.customer_name_input.clear()
        self.plate_num_input.clear()
        self.problem_description_input.clear()
        self.technician_name_input.clear()
        
        # Show success message (optional)
        # QMessageBox.information(self, "Success", "Technician assigned successfully!")

    def show_technician_page(self):
        self.main_app.stack.setCurrentWidget(self.main_app.technician_page)
