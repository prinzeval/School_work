from PyQt6.QtWidgets import QTableWidgetItem, QPushButton

def populate_table(app, table):
    sample_data = [
        [1, "John Doe", "john@example.com", "555-555-5555", "123 Elm St"],
        [2, "Jane Smith", "jane@example.com", "555-123-4567", "456 Oak St"]
    ]

    table.setRowCount(len(sample_data))
    table.setColumnCount(len(sample_data[0]) + 2)

    for row_index, row_data in enumerate(sample_data):
        for column_index, data in enumerate(row_data):
            table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda _, ri=row_index: app.edit_customer(ri, table))
        table.setCellWidget(row_index, len(row_data), edit_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda _, ri=row_index: app.delete_customer(ri, table))
        table.setCellWidget(row_index, len(row_data) + 1, delete_button)

def populate_enquiry_table(table):
    sample_data = [
        ["John Doe", "ABC123", "2024-12-01", "Engine Noise", "Technician A"],
        ["Jane Smith", "XYZ789", "2024-12-02", "Brake Issue", "Technician B"]
    ]

    table.setRowCount(len(sample_data))
    table.setColumnCount(len(sample_data[0]))

    for row_index, row_data in enumerate(sample_data):
        for column_index, data in enumerate(row_data):
            table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

def populate_invoice_table(table):
    sample_data = [
        ["John Doe", "Oil Filter", "2", "50", "100", "200"],
        ["Jane Smith", "Brake Pads", "4", "80", "150", "230"]
    ]

    table.setRowCount(len(sample_data))
    table.setColumnCount(len(sample_data[0]))

    for row_index, row_data in enumerate(sample_data):
        for column_index, data in enumerate(row_data):
            table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
