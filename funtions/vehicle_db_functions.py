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

def read_vehicles():
    """Fetches all vehicles from the Operations_Vehicle table."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Operations_Vehicle")
            rows = cursor.fetchall()
            return rows
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()

def add_vehicle(customer_name, make, model, year, colour, VIN, plate_num, Mileage, image):
    """Adds a vehicle entry."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """INSERT INTO Operations_Vehicle (customer_id, make, model, year, colour, VIN, plate_num, mileage, image) VALUES 
                        ((SELECT customer_id
                            FROM operations_customer
                            WHERE name = %s), %s, %s, %s, %s, %s, %s, %s, %s)
                    """
            values = (customer_name, make, model, year, colour, VIN, plate_num, Mileage, image)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_vehicle_field(vehicle_id, column_name, new_value):
    """
    Updates a specific field in the Operations_Vehicle table for a given vehicle_id.

    Args:
        vehicle_id (int): The ID of the job to update.
        column_name (string): The column name to update.
        new_value: The new value to set (type depends on the column).
    """
    try:
        conn = connect_db() 
        if conn:
            cursor = conn.cursor()

            allowed_columns = [
                "customer_id", "make", "model", "year", 
                "colour", "VIN", "plate_num", "mileage", "image"
            ]
            if column_name not in allowed_columns:
                raise ValueError(f"Invalid column name: {column_name}")

            # Construct the dynamic SQL query
            query = f"UPDATE Operations_Vehicle SET {column_name} = %s WHERE vehicle_id = %s"
            cursor.execute(query, (new_value, vehicle_id))
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    except ValueError as ve:
        print(ve)
    finally:
        if conn:
            cursor.close()
            conn.close()

def delete_vehicle(vehicle_id):
    """Deletes a record of a vehicle from the Operations_Vehicle table."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "DELETE FROM Operations_Vehicle WHERE vehicle_id = %s"
            cursor.execute(query, (vehicle_id,))
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def view_image(vehicle_id):
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT image FROM Operations_Vehicle WHERE vehicle_id = %s;"
            cursor.execute(query, (vehicle_id,))
            image = cursor.fetchone()
            return image if image else None
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()
