import mysql.connector

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Vondabaic2020",
            database="Autoshop"
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def read_parts():
    """
    Fetches all parts from the Operations_Part table.
    Returns:
        list: A list of tuples, where each tuple represents a row from the table.
    """
    rows = []
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Operations_Part")
            rows = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return rows

def parts_low_in_stock():
    """
    Fetches parts that are low in stock from the Operations_Part table.
    Returns:
        list: A list of tuples, where each tuple represents a row from the table.
    """
    rows = []
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """SELECT *
                       FROM operations_part
                       ORDER BY stock_quantity ASC
                       LIMIT 5"""
            cursor.execute(query)
            rows = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return rows

def add_parts(part_name, unit_price, stock_quantity):
    """Adds a new part to the Operations_Part table."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO Operations_Part (part_name, unit_price, stock_quantity) VALUES (%s, %s, %s)"
            values = (part_name, unit_price, stock_quantity)
            cursor.execute(query, values)
            conn.commit()
            print(f"Part {part_name} added successfully.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_part_name(part_id, new_name):
    """Updates the name of an existing part."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Part SET part_name = %s WHERE part_id = %s"
            values = (new_name, part_id)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_part_stock_quantity(part_id, new_quantity):
    """Updates the stock quantity of an existing part."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Part SET stock_quantity = %s WHERE part_id = %s"
            values = (new_quantity, part_id)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_unit_price(part_id, new_price):
    """Updates the unit price of an existing part."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Part SET unit_price = %s WHERE part_id = %s"
            values = (new_price, part_id)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def delete_part(part_id):
    """Deletes a part from the Operations_Part table."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "DELETE FROM Operations_Part WHERE part_id = %s"
            cursor.execute(query, (part_id,))
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
