from PyQt6.QtWidgets import QVBoxLayout,QDialog, QWidget, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QFormLayout
import funtions.invoice_db_functions as af  # Importing the invoice database functions
import mysql.connector

class InvoicePage(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.layout = QVBoxLayout(self)

        # Top buttons
        button_layout = QHBoxLayout()
        add_invoice_btn = QPushButton("Add Invoice")
        view_all_btn = QPushButton("View All Invoices")
        unpaid_btn = QPushButton("Unpaid Invoices")
        paid_btn = QPushButton("Paid Invoices")
        update_status_btn = QPushButton("Update Payment Status")
        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)
        back_button.setStyleSheet("""
            font-size: 18px;
            padding: 10px;
            background-color: #3CB371;
            color: white;
            border: 2px solid #8E5724;
            font-weight: bold;
        """)
        back_button.clicked.connect(self.show_main_page)

        for btn in [add_invoice_btn, view_all_btn, unpaid_btn, paid_btn, update_status_btn]:
            btn.setFixedHeight(100)
            btn.setStyleSheet("""
                font-size: 18px;
                padding: 20px;
                background-color: #3CB371;
                color: white;
                border: 2px solid #8E5724;
                font-weight: bold;
            """)

        add_invoice_btn.clicked.connect(self.add_invoice)
        view_all_btn.clicked.connect(self.view_all_invoices)
        unpaid_btn.clicked.connect(self.view_unpaid_invoices)
        paid_btn.clicked.connect(self.view_paid_invoices)
        update_status_btn.clicked.connect(self.update_payment_status)

        button_layout.addWidget(add_invoice_btn)
        button_layout.addWidget(view_all_btn)
        button_layout.addWidget(unpaid_btn)
        button_layout.addWidget(paid_btn)
        button_layout.addWidget(update_status_btn)
        self.layout.addWidget(back_button)
        self.layout.addLayout(button_layout)

        # Invoice table
        self.invoice_table = QTableWidget()
        self.invoice_table.setColumnCount(16)
        self.invoice_table.setHorizontalHeaderLabels(["Invoice ID", "Customer Name", "Address", "Issued Date", "Make", "Model", "Year", "Colour", "VIN", "Plate Number", "Mileage", "Job Performed", "No. of Parts Used", "Part Price", "Labour", "Sales Tax", "Total Amount", "Payment Status"])
        self.invoice_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.invoice_table.horizontalHeader().setStretchLastSection(True)

        self.layout.addWidget(self.invoice_table)
        self.layout.setStretch(1, 1)  # Ensure the table occupies the remaining space

    def populate_invoices(self, rows):
        # Clear existing rows
        self.invoice_table.setRowCount(0)
        if rows:
            for row_index, row_data in enumerate(rows):
                self.invoice_table.insertRow(row_index)
                for column_index, data in enumerate(row_data):
                    self.invoice_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

    def add_invoice(self):
        form = InvoiceForm(self)  # Assuming you have a form for adding invoices
        if form.exec():
            invoice_data = form.get_invoice_data()
            af.add_invoice(invoice_data['invoice_id'], invoice_data['jobpart_id'], invoice_data['issued_date'], invoice_data['sales_tax'])
            self.view_all_invoices()

    def view_all_invoices(self):
        rows = af.view_invoices()
        self.populate_invoices(rows)

    def view_unpaid_invoices(self):
        rows = af.view_unpaid_invoices()
        self.populate_invoices(rows)

    def view_paid_invoices(self):
        rows = af.view_paid_invoices()
        self.populate_invoices(rows)

    def update_payment_status(self):
        form = UpdatePaymentStatusForm(self)  # Assuming you have a form for updating payment status
        if form.exec():
            status_data = form.get_status_data()
            af.update_payment_status(status_data['invoice_id'], status_data['new_status'])
            self.view_all_invoices()

    def show_main_page(self):
        self.main_app.stack.setCurrentWidget(self.main_app.main_page)

# Additional forms if required
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
