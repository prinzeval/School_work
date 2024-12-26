import mysql.connector

# Establishing the connection to the MySQL database
def connect_db():
    """
    Establishes a connection to the MySQL database.
    Returns:
        conn: The MySQL connection object.
    """
    try:
        return mysql.connector.connect(
            host="localhost",  # Database host
            port=3306,         # MySQL default port
            user="root",       # Your MySQL username
            password="Vondabaic2020",  # Replace with your MySQL password
            database="Autoshop"   # The database you want to connect to
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Create (Insert data into the table)
def create_customer():
    """
    Adds a new customer to the Operations_Customer table.
    """
    try:
        customer_id = int(input("Enter customer ID: "))
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")
        phone_num = input("Enter customer phone number: ")
        address = input("Enter customer address: ")

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO Operations_Customer (customer_id, name, email, phone_num, address) VALUES (%s, %s, %s, %s, %s)"
            values = (customer_id, name, email, phone_num, address)
            cursor.execute(query, values)
            conn.commit()
            print(f"Customer {name} added successfully.")
    except ValueError:
        print("Invalid input. Customer ID must be an integer.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Read (Select data from the table)
def read_customers():
    """
    Fetches and displays all customers from the Operations_Customer table.
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Operations_Customer")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No customers found.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Update (Update existing data)
def update_customer():
    """
    Updates the name of an existing customer in the Operations_Customer table.
    """
    try:
        customer_id = int(input("Enter customer ID to update: "))
        new_name = input("Enter the new name for the customer: ")

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Customer SET name = %s WHERE customer_id = %s"
            values = (new_name, customer_id)
            cursor.execute(query, values)
            conn.commit()
            print(f"Customer {customer_id} updated to {new_name}.")
    except ValueError:
        print("Invalid input. Customer ID must be an integer.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Delete (Delete a record)
def delete_customer():
    """
    Deletes a customer from the Operations_Customer table.
    """
    try:
        customer_id = int(input("Enter customer ID to delete: "))

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "DELETE FROM Operations_Customer WHERE customer_id = %s"
            cursor.execute(query, (customer_id,))
            conn.commit()
            print(f"Customer {customer_id} deleted successfully.")
    except ValueError:
        print("Invalid input. Customer ID must be an integer.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Main program loop to choose an operation
if __name__ == "__main__":
    while True:
        print("\nChoose an operation:")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("5. Exit")
        
        choice = input("Enter choice (1/2/3/4/5): ")
        
        if choice == '1':
            create_customer()
        elif choice == '2':
            read_customers()
        elif choice == '3':
            update_customer()
        elif choice == '4':
            delete_customer()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please enter a number between 1 and 5.")


from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QSplitter, QLabel, QTabWidget, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt, QTimer


class AutoShopApp(QMainWindow):
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
        vehicle_container = QLabel("🚗 Vehicles")
        vehicle_container.setStyleSheet("background-color: #ddd; font-size: 24px; border: 2px solid #aaa;")
        vehicle_container.setFixedHeight(300)
        vehicle_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        splitter.addWidget(vehicle_container)

        # Table Section (Right)
        table_section = QWidget()
        table_layout = QVBoxLayout(table_section)

        # Tabbed Table for Customers/Parts/Jobs
        self.table_tabs = QTabWidget()
        self.table_tabs.setFixedHeight(300)
        self.add_table("Customers")
        self.add_table("Technicians")
        self.add_table("Parts")
        self.add_table("Jobs")

        table_layout.addWidget(self.table_tabs)
        splitter.addWidget(table_section)

        splitter.setSizes([600, 600])  # Adjust initial size

        main_layout.addWidget(splitter)

    # --- Helper to Add Containers ---
    def add_container(self, layout, text, row, col):
        container = QPushButton(text)
        container.setFixedHeight(150)
        container.setStyleSheet("font-size: 18px; padding: 20px;")
        layout.addWidget(container, row, col)

    # --- Helper to Add Tables to Tabs ---
    def add_table(self, name):
        table = QTableWidget(5, 4)
        table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone"])
        for i in range(5):
            for j in range(4):
                table.setItem(i, j, QTableWidgetItem(f"{name} {i+1}-{j+1}"))
        self.table_tabs.addTab(table, name)


if __name__ == "__main__":
    app = QApplication([])
    window = AutoShopApp()
    window.show()
    app.exec()
