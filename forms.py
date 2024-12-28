from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton

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
