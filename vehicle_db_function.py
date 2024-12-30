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

def read_vehicles():
    """
    displays all vehicles from the Operations_Vehicle table.
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Operations_Vehicle")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No Vehicles found.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def add_vehicle(customer_name, make, model, year, colour, VIN, plate_num, Mileage, image):
    """add a vehicle entry

    Args:
        customer_name (string): _
        make (string): _
        model (string): _
        year (string): _
        colour (string): _
        VIN (string): _
        plate_num (string): _
        Mileage (string): _
        image (string)
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """INSERT INTO Operations_Vehicle (customer_id, make, model, year, colour, VIN, plate_num, mileage, image) VALUES 
                        ((SELECT customer_id
                            FROM operations_customer
                            WHERE customer_name = %s), %s, %s, %s, %s, %s, %s, %s, %s)  
                    """
            values = (customer_name, make, model, year, colour, VIN, plate_num, Mileage, image)
            cursor.execute(query, values)
            conn.commit()
            print(f"{customer_name}'s vehicle has been added successfully.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
