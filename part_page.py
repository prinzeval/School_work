from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
import Parts_db_functions as af  # Updated import statement
from forms import PartForm
import mysql.connector  

class PartPage(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.layout = QVBoxLayout(self)

        # Top buttons
        button_layout = QHBoxLayout()
        add_part_btn = QPushButton("Add Part")
        parts_low_in_stock_btn = QPushButton("Parts low in stock")
        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.show_main_page)

        for btn in [add_part_btn, parts_low_in_stock_btn]:
            btn.setFixedHeight(100)
            btn.setStyleSheet("""
                font-size: 18px;
                padding: 20px;
                background-color: #D37F3A;
                color: white;
                border: 2px solid #8E5724;
                font-weight: bold;
            """)

        add_part_btn.clicked.connect(self.add_part)
        parts_low_in_stock_btn.clicked.connect(self.show_parts_low_in_stock)

        button_layout.addWidget(add_part_btn)
        button_layout.addWidget(parts_low_in_stock_btn)
        self.layout.addWidget(back_button)
        self.layout.addLayout(button_layout)

        # Part table
        self.part_table = QTableWidget()
        self.part_table.setColumnCount(6)
        self.part_table.setHorizontalHeaderLabels(["Part ID", "Part Name", "Unit Price", "Stock Quantity", "Edit", "Delete"])
        self.part_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.part_table.horizontalHeader().setStretchLastSection(True)

        self.layout.addWidget(self.part_table)
        self.layout.setStretch(1, 1)  # Ensure the table occupies the remaining space

        # Populate table with parts
        self.populate_parts()

    def populate_parts(self):
        # Clear existing rows
        self.part_table.setRowCount(0)

        try:
            rows = af.read_parts()
            if rows:
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
        except Exception as e:
            print(f"Error populating parts: {e}")

    def add_part(self):
        form = PartForm(self)
        if form.exec():
            part_data = form.get_part_data()
            af.add_parts(part_data['part_name'], part_data['unit_price'], part_data['stock_quantity'])
            self.populate_parts()

    def edit_part(self, row_index):
        part_id = self.part_table.item(row_index, 0).text()
        part_data = {
            "part_name": self.part_table.item(row_index, 1).text(),
            "unit_price": self.part_table.item(row_index, 2).text(),
            "stock_quantity": self.part_table.item(row_index, 3).text(),
        }

        form = PartForm(self, part_data)
        if form.exec():
            updated_data = form.get_part_data()
            af.edit_part_name(part_id, updated_data['part_name'])
            af.edit_unit_price(part_id, updated_data['unit_price'])
            af.edit_part_stock_quantity(part_id, updated_data['stock_quantity'])
            self.populate_parts()

    def delete_part(self, row_index):
        part_id = self.part_table.item(row_index, 0).text()
        af.delete_part(part_id)
        self.populate_parts()

    def show_parts_low_in_stock(self):
        low_stock_page = PartsLowInStockPage(self.main_app, self)
        self.main_app.stack.addWidget(low_stock_page)
        self.main_app.stack.setCurrentWidget(low_stock_page)

    def show_main_page(self):
        self.main_app.stack.setCurrentWidget(self.main_app.main_page)

class PartsLowInStockPage(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.layout = QVBoxLayout(self)

        # Back button
        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.show_add_part_page)
        self.layout.addWidget(back_button)

        # Part table
        self.part_table = QTableWidget()
        self.part_table.setColumnCount(6)
        self.part_table.setHorizontalHeaderLabels(["Part ID", "Part Name", "Unit Price", "Stock Quantity", "Edit", "Delete"])
        self.part_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.part_table.horizontalHeader().setStretchLastSection(True)

        self.layout.addWidget(self.part_table)
        self.layout.setStretch(1, 1)  # Ensure the table occupies the remaining space

        # Populate table with low stock parts
        self.populate_parts_low_in_stock()

    def populate_parts_low_in_stock(self):
        # Clear existing rows
        self.part_table.setRowCount(0)

        try:
            rows = af.parts_low_in_stock()
            if rows:
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
        except Exception as e:
            print(f"Error populating parts low in stock: {e}")

    def edit_part(self, row_index):
        part_id = self.part_table.item(row_index, 0).text()
        part_data = {
            "part_name": self.part_table.item(row_index, 1).text(),
            "unit_price": self.part_table.item(row_index, 2).text(),
            "stock_quantity": self.part_table.item(row_index, 3).text(),
        }

        form = PartForm(self, part_data)
        if form.exec():
            updated_data = form.get_part_data()
            af.edit_part_name(part_id, updated_data['part_name'])
            af.edit_unit_price(part_id, updated_data['unit_price'])
            af.edit_part_stock_quantity(part_id, updated_data['stock_quantity'])
            self.populate_parts_low_in_stock()

    def delete_part(self, row_index):
        part_id = self.part_table.item(row_index, 0).text()
        af.delete_part(part_id)
        self.populate_parts_low_in_stock()

    def show_add_part_page(self):
        self.main_app.stack.setCurrentWidget(self.main_app.part_page)
