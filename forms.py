from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton,QHBoxLayout, QVBoxLayout

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

class TechnicianForm(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Technician")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.name_field = QLineEdit()
        self.specialty_field = QLineEdit()
        self.hourly_rate_field = QLineEdit()

        if data:
            self.name_field.setText(data["name"])
            self.specialty_field.setText(data["specialty"])
            self.hourly_rate_field.setText(data["hourly_rate"])

        self.form_layout.addRow("Name:", self.name_field)
        self.form_layout.addRow("Specialty:", self.specialty_field)
        self.form_layout.addRow("Hourly Rate:", self.hourly_rate_field)

        self.layout.addLayout(self.form_layout)

        self.buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.save_button)

        self.layout.addLayout(self.buttons_layout)

    def get_technician_data(self):
        return {
            "name": self.name_field.text(),
            "specialty": self.specialty_field.text(),
            "hourly_rate": self.hourly_rate_field.text()
        }

# forms.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QFormLayout, QPushButton, QHBoxLayout

class PartForm(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Part" if data else "Add Part")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.part_name_field = QLineEdit()
        self.unit_price_field = QLineEdit()
        self.stock_quantity_field = QLineEdit()

        if data:
            self.part_name_field.setText(data["part_name"])
            self.unit_price_field.setText(data["unit_price"])
            self.stock_quantity_field.setText(data["stock_quantity"])

        self.form_layout.addRow("Part Name:", self.part_name_field)
        self.form_layout.addRow("Unit Price:", self.unit_price_field)
        self.form_layout.addRow("Stock Quantity:", self.stock_quantity_field)

        self.layout.addLayout(self.form_layout)

        self.buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.save_button)

        self.layout.addLayout(self.buttons_layout)

    def get_part_data(self):
        return {
            "part_name": self.part_name_field.text(),
            "unit_price": self.unit_price_field.text(),
            "stock_quantity": self.stock_quantity_field.text()
        }
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QPushButton

class InvoiceForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Invoice")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.invoice_id_input = QLineEdit()
        self.jobpart_id_input = QLineEdit()
        self.issued_date_input = QLineEdit()
        self.sales_tax_input = QLineEdit()

        self.form_layout.addRow("Invoice ID:", self.invoice_id_input)
        self.form_layout.addRow("Job Part ID:", self.jobpart_id_input)
        self.form_layout.addRow("Issued Date:", self.issued_date_input)
        self.form_layout.addRow("Sales Tax:", self.sales_tax_input)

        self.layout.addLayout(self.form_layout)

        self.buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.save_button)

        self.layout.addLayout(self.buttons_layout)

    def get_invoice_data(self):
        return {
            "invoice_id": self.invoice_id_input.text(),
            "jobpart_id": self.jobpart_id_input.text(),
            "issued_date": self.issued_date_input.text(),
            "sales_tax": self.sales_tax_input.text()
        }

class UpdatePaymentStatusForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Payment Status")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.invoice_id_input = QLineEdit()
        self.new_status_input = QLineEdit()

        self.form_layout.addRow("Invoice ID:", self.invoice_id_input)
        self.form_layout.addRow("New Status:", self.new_status_input)

        self.layout.addLayout(self.form_layout)

        self.buttons_layout = QHBoxLayout()
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.update_button)

        self.layout.addLayout(self.buttons_layout)

    def get_status_data(self):
        return {
            "invoice_id": self.invoice_id_input.text(),
            "new_status": self.new_status_input.text()
        }
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QPushButton

class VehicleForm(QDialog):
    def __init__(self, parent=None, vehicle_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Vehicle")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.customer_name_input = QLineEdit()
        self.make_input = QLineEdit()
        self.model_input = QLineEdit()
        self.year_input = QLineEdit()
        self.colour_input = QLineEdit()
        self.vin_input = QLineEdit()
        self.plate_num_input = QLineEdit()
        self.mileage_input = QLineEdit()
        self.image_input = QLineEdit()

        self.form_layout.addRow("Customer Name:", self.customer_name_input)
        self.form_layout.addRow("Make:", self.make_input)
        self.form_layout.addRow("Model:", self.model_input)
        self.form_layout.addRow("Year:", self.year_input)
        self.form_layout.addRow("Colour:", self.colour_input)
        self.form_layout.addRow("VIN:", self.vin_input)
        self.form_layout.addRow("Plate Number:", self.plate_num_input)
        self.form_layout.addRow("Mileage:", self.mileage_input)
        self.form_layout.addRow("Image Path:", self.image_input)

        self.layout.addLayout(self.form_layout)

        self.buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.save_button)

        self.layout.addLayout(self.buttons_layout)

        if vehicle_data:
            self.customer_name_input.setText(vehicle_data["customer_id"])
            self.make_input.setText(vehicle_data["make"])
            self.model_input.setText(vehicle_data["model"])
            self.year_input.setText(vehicle_data["year"])
            self.colour_input.setText(vehicle_data["colour"])
            self.vin_input.setText(vehicle_data["VIN"])
            self.plate_num_input.setText(vehicle_data["plate_num"])
            self.mileage_input.setText(vehicle_data["mileage"])
            self.image_input.setText(vehicle_data["image"])

    def get_vehicle_data(self):
        return {
            "customer_name": self.customer_name_input.text(),
            "make": self.make_input.text(),
            "model": self.model_input.text(),
            "year": self.year_input.text(),
            "colour": self.colour_input.text(),
            "VIN": self.vin_input.text(),
            "plate_num": self.plate_num_input.text(),
            "mileage": self.mileage_input.text(),
            "image": self.image_input.text()
        }
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QDateEdit
from PyQt6.QtCore import QDate

class JobForm(QDialog):
    def __init__(self, parent=None, job_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Job")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.plate_num_input = QLineEdit()
        self.problem_description_input = QLineEdit()
        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())
        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate())
        self.technician_input = QLineEdit()
        self.status_input = QLineEdit()

        self.form_layout.addRow("Vehicle Plate Number:", self.plate_num_input)
        self.form_layout.addRow("Description:", self.problem_description_input)
        self.form_layout.addRow("Start Date:", self.start_date_input)
        self.form_layout.addRow("End Date:", self.end_date_input)
        self.form_layout.addRow("Technician:", self.technician_input)
        self.form_layout.addRow("Status:", self.status_input)

        self.layout.addLayout(self.form_layout)

        self.buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.save_button)

        self.layout.addLayout(self.buttons_layout)

        if job_data:
            self.plate_num_input.setText(job_data["plate_num"])
            self.problem_description_input.setText(job_data["problem_description"])
            self.start_date_input.setDate(QDate.fromString(job_data["start_date"], 'yyyy-MM-dd'))
            self.end_date_input.setDate(QDate.fromString(job_data["end_date"], 'yyyy-MM-dd'))
            self.technician_input.setText(job_data["technician"])
            self.status_input.setText(job_data["status"])

    def get_job_data(self):
        return {
            "plate_num": self.plate_num_input.text(),
            "problem_description": self.problem_description_input.text(),
            "start_date": self.start_date_input.date().toString('yyyy-MM-dd'),
            "end_date": self.end_date_input.date().toString('yyyy-MM-dd'),
            "technician": self.technician_input.text(),
            "status": self.status_input.text()
        }
