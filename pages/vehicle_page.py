from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QDialog
from PyQt6.QtGui import QPixmap  # Add this import
import funtions.vehicle_db_functions as vf  # Importing the vehicle database functions
import mysql.connector
from forms import VehicleForm  # Importing the VehicleForm from forms.py
class VehiclePage(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.layout = QVBoxLayout(self)

        # Top buttons
        button_layout = QHBoxLayout()
        add_vehicle_btn = QPushButton("Add Vehicle")
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

        for btn in [add_vehicle_btn]:
            btn.setFixedHeight(100)
            btn.setStyleSheet("""
                font-size: 18px;
                padding: 20px;
                background-color: #D37F3A;
                color: white;
                border: 2px solid #8E5724;
                font-weight: bold;
            """)

        add_vehicle_btn.clicked.connect(self.add_vehicle)

        button_layout.addWidget(add_vehicle_btn)
        self.layout.addWidget(back_button)
        self.layout.addLayout(button_layout)

        # Vehicle table
        self.vehicle_table = QTableWidget()
        self.vehicle_table.setColumnCount(13)  # Adjusted to include Edit, Delete, and View Image buttons
        self.vehicle_table.setHorizontalHeaderLabels(["Vehicle ID", "Customer ID", "Make", "Model", "Year", "Colour", "VIN", "Plate Number", "Mileage", "Image Path", "Edit", "Delete", "View Image"])
        
        # Manually set column widths
        self.vehicle_table.setColumnWidth(0, 80)   # Vehicle ID
        self.vehicle_table.setColumnWidth(1, 100)  # Customer ID
        self.vehicle_table.setColumnWidth(2, 100)  # Make
        self.vehicle_table.setColumnWidth(3, 100)  # Model
        self.vehicle_table.setColumnWidth(4, 60)   # Year
        self.vehicle_table.setColumnWidth(5, 80)   # Colour
        self.vehicle_table.setColumnWidth(6, 150)  # VIN
        self.vehicle_table.setColumnWidth(7, 100)  # Plate Number
        self.vehicle_table.setColumnWidth(8, 100)  # Mileage
        self.vehicle_table.setColumnWidth(9, 150)  # Image Path
        self.vehicle_table.setColumnWidth(10, 50)  # Edit
        self.vehicle_table.setColumnWidth(11, 50)  # Delete
        self.vehicle_table.setColumnWidth(12, 100) # View Image
        
        self.vehicle_table.horizontalHeader().setStretchLastSection(True)

        self.layout.addWidget(self.vehicle_table)
        self.layout.setStretch(1, 1)  # Ensure the table occupies the remaining space

        # Populate table with vehicles
        self.populate_vehicles()

    def show_main_page(self):
        self.main_app.show_main_page()

    def populate_vehicles(self):
        # Clear existing rows
        self.vehicle_table.setRowCount(0)

        try:
            rows = vf.read_vehicles()
            if rows:
                for row_index, row_data in enumerate(rows):
                    self.vehicle_table.insertRow(row_index)
                    for column_index, data in enumerate(row_data):
                        self.vehicle_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
                    edit_button = QPushButton("Edit")
                    delete_button = QPushButton("Delete")
                    view_image_button = QPushButton("View Image")
                    
                    # Set fixed width for buttons
                    edit_button.setFixedWidth(50)
                    delete_button.setFixedWidth(50)
                    view_image_button.setFixedWidth(100)

                    edit_button.clicked.connect(lambda _, ri=row_index: self.edit_vehicle(ri))
                    delete_button.clicked.connect(lambda _, ri=row_index: self.delete_vehicle(ri))
                    view_image_button.clicked.connect(lambda _, ri=row_index: self.view_vehicle_image(ri))

                    self.vehicle_table.setCellWidget(row_index, 10, edit_button)
                    self.vehicle_table.setCellWidget(row_index, 11, delete_button)
                    self.vehicle_table.setCellWidget(row_index, 12, view_image_button)
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def add_vehicle(self):
        form = VehicleForm(self)  # Using the form from forms.py
        if form.exec():
            vehicle_data = form.get_vehicle_data()
            vf.add_vehicle(vehicle_data['customer_name'], vehicle_data['make'], vehicle_data['model'], vehicle_data['year'], vehicle_data['colour'], vehicle_data['VIN'], vehicle_data['plate_num'], vehicle_data['mileage'], vehicle_data['image'])
            self.populate_vehicles()

    def edit_vehicle(self, row_index):
        vehicle_id = self.vehicle_table.item(row_index, 0).text()
        vehicle_data = {
            "customer_id": self.vehicle_table.item(row_index, 1).text(),
            "make": self.vehicle_table.item(row_index, 2).text(),
            "model": self.vehicle_table.item(row_index, 3).text(),
            "year": self.vehicle_table.item(row_index, 4).text(),
            "colour": self.vehicle_table.item(row_index, 5).text(),
            "VIN": self.vehicle_table.item(row_index, 6).text(),
            "plate_num": self.vehicle_table.item(row_index, 7).text(),
            "mileage": self.vehicle_table.item(row_index, 8).text(),
            "image": self.vehicle_table.item(row_index, 9).text()
        }

        form = VehicleForm(self, vehicle_data)
        if form.exec():
            updated_data = form.get_vehicle_data()
            vf.edit_vehicle_field(vehicle_id, 'customer_id', updated_data['customer_name'])
            vf.edit_vehicle_field(vehicle_id, 'make', updated_data['make'])
            vf.edit_vehicle_field(vehicle_id, 'model', updated_data['model'])
            vf.edit_vehicle_field(vehicle_id, 'year', updated_data['year'])
            vf.edit_vehicle_field(vehicle_id, 'colour', updated_data['colour'])
            vf.edit_vehicle_field(vehicle_id, 'VIN', updated_data['VIN'])
            vf.edit_vehicle_field(vehicle_id, 'plate_num', updated_data['plate_num'])
            vf.edit_vehicle_field(vehicle_id, 'mileage', updated_data['mileage'])
            vf.edit_vehicle_field(vehicle_id, 'image', updated_data['image'])
            self.populate_vehicles()

    def delete_vehicle(self, row_index):
        vehicle_id = self.vehicle_table.item(row_index, 0).text()
        vf.delete_vehicle(vehicle_id)
        self.populate_vehicles()

    def view_vehicle_image(self, row_index):
        image_path = self.vehicle_table.item(row_index, 9).text()

        # Create a dialog to display the image
        image_dialog = QDialog(self)
        image_dialog.setWindowTitle("Vehicle Image")

        # Set the fixed size for the dialog
        image_dialog.setFixedSize(400, 300)  # Width: 400px, Height: 300px

        dialog_layout = QVBoxLayout()

        image_label = QLabel()
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)  # Ensure the image scales to fit the label

        dialog_layout.addWidget(image_label)
        image_dialog.setLayout(dialog_layout)
        image_dialog.exec()
