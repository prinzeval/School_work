from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
import main_Customer_db_functions as af
from forms import PartForm
import mysql.connector

class PartPage(QWidget):
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
        nav_bar.addWidget(QLabel("⚙️ Parts"))
        nav_bar.addStretch(1)
        self.layout.addLayout(nav_bar)

        # Part table
        self.part_table = QTableWidget()
        self.part_table.setColumnCount(6)
        self.part_table.setHorizontalHeaderLabels(["Part ID", "Part Name", "Part Number", "Unit Price", "Stock Quantity", "Edit", "Delete"])
        self.part_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.part_table.horizontalHeader().setStretchLastSection(True)

        self.layout.addWidget(self.part_table)
        self.layout.setStretch(2, 1)  # Ensure the table occupies the remaining space

        # Placeholder for populating table (remove database aspect)
        self.populate_parts()

    def show_main_page(self):
        self.parent().setCurrentWidget(self.parent().main_page)

    def populate_parts(self):
        # Clear existing rows
        self.part_table.setRowCount(0)

        try:
            conn = af.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Operations_Part")
                rows = cursor.fetchall()
                for row_index, row_data in enumerate(rows):
                    self.part_table.insertRow(row_index)
                    for column_index, data in enumerate(row_data):
                        self.part_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
                    edit_button = QPushButton("Edit")
                    edit_button.clicked.connect(lambda _, ri=row_index: self.edit_part(ri))
                    self.part_table.setCellWidget(row_index, 4, edit_button)
                    delete_button = QPushButton("Delete")
                    delete_button.clicked.connect(lambda _, ri=row_index: self.delete_part(ri))
                    self.part_table.setCellWidget(row_index, 5, delete_button)
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def edit_part(self, row_index):
        part_id = self.part_table.item(row_index, 0).text()
        part_data = {
            "part_name": self.part_table.item(row_index, 1).text(),
            "part_number": self.part_table.item(row_index, 2).text(),
            "unit_price": self.part_table.item(row_index, 3).text(),
            "stock_quantity": self.part_table.item(row_index, 4).text(),
        }

        form = PartForm(self, part_data)
        if form.exec():
            updated_data = form.get_part_data()
            af.edit_part_name(part_id, updated_data['part_name'])
            af.edit_part_number(part_id, updated_data['part_number'])
            af.edit_part_unit_price(part_id, updated_data['unit_price'])
            af.edit_part_stock_quantity(part_id, updated_data['stock_quantity'])
            self.populate_parts()

    def delete_part(self, row_index):
        part_id = self.part_table.item(row_index, 0).text()
        af.delete_part(part_id)
        self.populate_parts()
