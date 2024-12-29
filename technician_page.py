from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
import main_Customer_db_functions as af
from forms import TechnicianForm
import mysql.connector

class TechnicianPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Back button to return to the main page
        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)  # Adjust if needed
        back_button.clicked.connect(self.show_main_page)
        self.layout.addWidget(back_button)

        # Navigation bar
        nav_bar = QHBoxLayout()
        nav_bar.addWidget(QLabel("👨‍🔧 Technicians"))
        nav_bar.addStretch(1)
        self.layout.addLayout(nav_bar)

        # Technician table
        self.technician_table = QTableWidget()
        self.technician_table.setColumnCount(5)
        self.technician_table.setHorizontalHeaderLabels(["Technician ID", "Name", "Specialty", "Hourly Rate", "Edit", "Delete"])
        self.technician_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.technician_table.horizontalHeader().setStretchLastSection(True)
        
        self.layout.addWidget(self.technician_table)
        self.layout.setStretch(2, 1)  # Ensure the table occupies the remaining space

        # Placeholder for populating table (remove database aspect)
        self.populate_technicians()

    def show_main_page(self):
        self.parent().setCurrentWidget(self.parent().main_page)

    def populate_technicians(self):
        # Clear existing rows
        self.technician_table.setRowCount(0)

        try:
            conn = af.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Operations_Technician")
                rows = cursor.fetchall()
                for row_index, row_data in enumerate(rows):
                    self.technician_table.insertRow(row_index)
                    for column_index, data in enumerate(row_data):
                        self.technician_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
                    edit_button = QPushButton("Edit")
                    edit_button.clicked.connect(lambda _, ri=row_index: self.edit_technician(ri))
                    self.technician_table.setCellWidget(row_index, 3, edit_button)
                    delete_button = QPushButton("Delete")
                    delete_button.clicked.connect(lambda _, ri=row_index: self.delete_technician(ri))
                    self.technician_table.setCellWidget(row_index, 4, delete_button)
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def edit_technician(self, row_index):
        technician_id = self.technician_table.item(row_index, 0).text()
        technician_data = {
            "name": self.technician_table.item(row_index, 1).text(),
            "specialty": self.technician_table.item(row_index, 2).text(),
            "hourly_rate": self.technician_table.item(row_index, 3).text(),
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
