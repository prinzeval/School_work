import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLineEdit, QPushButton, QLabel, QTextEdit, QFormLayout, QMessageBox, QStackedWidget, QHBoxLayout, QTableWidget, QTableWidgetItem
)
import mysql.connector

# Database connection function
def connect_db():
    return mysql.connector.connect(
        host="localhost",  # Database host
        port=3306,         # MySQL default port
        user="root",       # Your MySQL username
        password="Vondabaic2020",  # Replace with your MySQL password
        database="Autoshop"  
    )

class CustomerManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Management System")
        self.setGeometry(100, 100, 800, 600)

        # Central stacked widget for "pages"
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Create pages
        self.home_page = self.create_home_page()
        self.add_customer_page = self.create_add_customer_page()
        self.view_customers_page = self.create_view_customers_page()  # New page for viewing customers

        # Add pages to stacked widget
        self.central_widget.addWidget(self.home_page)
        self.central_widget.addWidget(self.add_customer_page)
        self.central_widget.addWidget(self.view_customers_page)  # Add new page to the stacked widget

        # Apply styles
        self.apply_styles()

    # Create home page
    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Header
        header = QLabel("Customer Management System")
        header.setStyleSheet("font-size: 24px; color: #ECF0F1; text-align: center;")
        layout.addWidget(header)

        # CRUD buttons
        add_button = QPushButton("Add Customer")
        view_button = QPushButton("View Customers")
        delete_button = QPushButton("Delete Customer")

        add_button.clicked.connect(self.go_to_add_customer_page)
        view_button.clicked.connect(self.go_to_view_customers_page)

        layout.addWidget(add_button)
        layout.addWidget(view_button)
        layout.addWidget(delete_button)

        # Footer
        footer = QLabel("© 2024 Customer Management System")
        footer.setStyleSheet("font-size: 12px; color: #ECF0F1; text-align: center;")
        layout.addWidget(footer)

        layout.setSpacing(20)
        page.setLayout(layout)
        return page

    # Create "Add Customer" page
    def create_add_customer_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Header
        header = QLabel("Add Customer")
        header.setStyleSheet("font-size: 24px; color: #ECF0F1; text-align: center;")
        layout.addWidget(header)

        # Input fields
        form_layout = QFormLayout()
        self.customer_id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()

        form_layout.addRow("Customer ID:", self.customer_id_input)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone:", self.phone_input)
        form_layout.addRow("Address:", self.address_input)

        layout.addLayout(form_layout)

        # Buttons
        save_button = QPushButton("Save")
        back_button = QPushButton("Back")

        save_button.clicked.connect(self.add_customer)
        back_button.clicked.connect(self.go_to_home_page)

        layout.addWidget(save_button)
        layout.addWidget(back_button)

        # Footer
        footer = QLabel("© 2024 Customer Management System")
        footer.setStyleSheet("font-size: 12px; color: #ECF0F1; text-align: center;")
        layout.addWidget(footer)

        layout.setSpacing(20)
        page.setLayout(layout)
        return page

    # Create "View Customers" page
    def create_view_customers_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Header
        header = QLabel("View Customers")
        header.setStyleSheet("font-size: 24px; color: #ECF0F1; text-align: center;")
        layout.addWidget(header)

        # Table to display customers
        self.customer_table = QTableWidget()
        self.customer_table.setColumnCount(6)  # Add an extra column for the edit button
        self.customer_table.setHorizontalHeaderLabels(["Customer ID", "Name", "Email", "Phone", "Address", "Edit"])

        layout.addWidget(self.customer_table)

        # Footer
        footer = QLabel("© 2024 Customer Management System")
        footer.setStyleSheet("font-size: 12px; color: #ECF0F1; text-align: center;")
        layout.addWidget(footer)

        layout.setSpacing(20)
        page.setLayout(layout)
        return page

    # Navigate to "Add Customer" page
    def go_to_add_customer_page(self):
        self.central_widget.setCurrentWidget(self.add_customer_page)

    # Navigate to "View Customers" page
    def go_to_view_customers_page(self):
        self.central_widget.setCurrentWidget(self.view_customers_page)
        self.load_customers()

    # Navigate back to home page
    def go_to_home_page(self):
        self.central_widget.setCurrentWidget(self.home_page)

    # Add a new customer
    def add_customer(self):
        try:
            customer_id = int(self.customer_id_input.text())
            name = self.name_input.text()
            email = self.email_input.text()
            phone = self.phone_input.text()
            address = self.address_input.text()

            conn = connect_db()
            cursor = conn.cursor()
            query = "INSERT INTO Operations_Customer (customer_id, name, email, phone_num, address) VALUES (%s, %s, %s, %s, %s)"
            values = (customer_id, name, email, phone, address)
            cursor.execute(query, values)
            conn.commit()

            QMessageBox.information(self, "Success", f"Customer {name} added successfully!")
            self.clear_inputs()
            self.go_to_home_page()

        except ValueError:
            QMessageBox.critical(self, "Error", "Customer ID must be an integer.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            if conn:
                cursor.close()
                conn.close()

    # Load customers into table
    def load_customers(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Operations_Customer")
            rows = cursor.fetchall()

            self.customer_table.setRowCount(len(rows))
            for row_num, row_data in enumerate(rows):
                for col_num, data in enumerate(row_data):
                    self.customer_table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

                # Add edit button to each row
                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(lambda _, r=row_data: self.edit_customer(r))
                self.customer_table.setCellWidget(row_num, 5, edit_button)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            if conn:
                cursor.close()
                conn.close()

    # Edit customer details
    def edit_customer(self, row_data):
        customer_id, name, email, phone, address = row_data
        self.customer_id_input.setText(str(customer_id))
        self.name_input.setText(name)
        self.email_input.setText(email)
        self.phone_input.setText(phone)
        self.address_input.setText(address)
        self.central_widget.setCurrentWidget(self.add_customer_page)

    # Clear input fields
    def clear_inputs(self):
        self.customer_id_input.clear()
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.address_input.clear()

    # Apply styles
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2C3E50;
            }
            QLabel {
                color: #ECF0F1;
                text-align: center;
            }
            QPushButton {
                background-color: #1ABC9C;
                color: #ECF0F1;
                font-size: 14px;
                padding: 8px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
            QLineEdit {
                background-color: #34495E;
                color: #ECF0F1;
                border: 1px solid #1ABC9C;
                border-radius: 5px;
                padding: 5px;
            }
            QTableWidget {
                background-color: #34495E;
                color: #ECF0F1;
                border: 1px solid #1ABC9C;
            }
        """)

# Main function
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CustomerManagementApp()
    main_window.show()
    sys.exit(app.exec())
