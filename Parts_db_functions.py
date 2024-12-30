import mysql.connector

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost", 
            port=3306,        
            user="root",       
            password="Immaculata",  
            database="Autoshop"   
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

##################################
# PARTS PAGE
##################################
def read_parts():
    """
    displays all parts from the Operations_Part table.
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Operations_Part")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No Parts found.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def add_Parts(part_name, unit_price, stock_quantity):
    """Adds a new part to the Operations_Part table
    """
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

def edit_Part_name(part_id, new_name):
    """updates the name of an existing part

    Args:
        part_id (int)
        new_name (string)
    """
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
    """updates the stock quantity of an existing part

    Args:
        part_id (int)
        new_quantity (string)
    """
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
    """updates the unit price of an existing part

    Args:
        part_id (int)
        new_price (string)
    """
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
    """Deletes a record  of a part from the Operations_Part table.
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "DELETE FROM Operations_Part WHERE part_id = %s"
            cursor.execute(query, (part_id))
            conn.commit
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def parts_low_in_stock():
    """Displays the parts about to finish
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """SELECT *
                        FROM operations_part
                        ORDER BY stock_quantity ASC
                        LIMIT 5;
                    """
            cursor.execute(query)
            conn.commit
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_job_field(job_id, column_name, new_value):
    """
    Updates a specific field in the Operations_Job table for a given job_id.

    Args:
        job_id (int): The ID of the job to update.
        column_name (string): The column name to update.
        new_value: The new value to set (type depends on the column).
    """
    try:
        conn = connect_db()  # Replace with your DB connection function
        if conn:
            cursor = conn.cursor()

            # Sanitize column_name to avoid SQL injection
            allowed_columns = [
                "vehicle_id", "technician_id", "job_type", "start_date", 
                "end_date", "job_amount", "hours", "status"
            ]
            if column_name not in allowed_columns:
                raise ValueError(f"Invalid column name: {column_name}")

            # Construct the dynamic SQL query
            query = f"UPDATE Operations_Job SET {column_name} = %s WHERE job_id = %s"
            cursor.execute(query, (new_value, job_id))
            conn.commit()
            print(f"Updated {column_name} for job_id {job_id} successfully!")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    except ValueError as ve:
        print(ve)
    finally:
        if conn:
            cursor.close()
            conn.close()



