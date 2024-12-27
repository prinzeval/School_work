import mysql.connector
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

# Database connection function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Vondabaic2020",
        database="Autoshop"
    )

def fetch_vehicle_images():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT image FROM Operations_Vehicle")
    images = [item[0] for item in cursor.fetchall()]
    cursor.close()
    connection.close()
    return images

def populate_table(table, table_name):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()

    table.setRowCount(len(records))
    table.setColumnCount(len(records[0]))

    for row_index, row_data in enumerate(records):
        for column_index, data in enumerate(row_data):
            table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

    cursor.close()
    connection.close()
