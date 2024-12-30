# technician_db_functions.py

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

##################################
# TECHNICIANS PAGE
##################################
def read_technicians():
    """
    Fetches all technicians from the Operations_Technician table.
    Returns:
        list: A list of tuples, where each tuple represents a row from the table.
    """
    rows = []
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Operations_Technician")
            rows = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return rows

def add_technicians(name, specialty, hourly_rate):
    """Adds a new technician to the Operations_Technician table."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO Operations_Technician (name, specialty, hourly_rate) VALUES (%s, %s, %s)"
            values = (name, specialty, hourly_rate)
            cursor.execute(query, values)
            conn.commit()
            print(f"Technician {name} added successfully.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_technician_name(technician_id, new_name):
    """Updates the name of an existing technician."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Technician SET name = %s WHERE technician_id = %s"
            values = (new_name, technician_id)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_technician_specialty(technician_id, new_specialty):
    """Updates the specialty of an existing technician."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Technician SET specialty = %s WHERE technician_id = %s"
            values = (new_specialty, technician_id)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_technician_hourly_rate(technician_id, new_hourly_rate):
    """Updates the hourly rate of an existing technician."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Technician SET hourly_rate = %s WHERE technician_id = %s"
            values = (new_hourly_rate, technician_id)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def delete_technician(technician_id):
    """Deletes a technician from the Operations_Technician table."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "DELETE FROM Operations_Technician WHERE technician_id = %s"
            cursor.execute(query, (technician_id,))
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def view_daily_wage():
    """Displays the wages of all technicians."""
    rows = []
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """SELECT D.date AS Date, T.name AS Technician_name, J.hours AS Hours_worked, T.hourly_rate AS Hourly_rate, J.job_amount AS Job_Amount, (J.job_amount * 0.6) AS Wage
                        FROM operations_jobpart AS JP
                        JOIN operations_job AS J ON JP.job_id = J.job_id
                        JOIN operations_technician AS T ON J.technician_id = T.technician_id
                        JOIN analytics_date as D ON D.date =  J.start_date"""
            cursor.execute(query)
            rows = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return rows

def assign_technician(customer_name, plate_num, description, technician_name):
    """Assigns a technician to handle a particular job."""
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """UPDATE operations_job AS J
                        JOIN operations_vehicle AS V ON V.vehicle_id = J.vehicle_id
                        JOIN operations_customer AS C ON V.customer_id = C.customer_id
                        SET technician_id = (SELECT technician_id
                                            FROM operations_technician
                                            WHERE name = %s
                                            LIMIT 1)
                        WHERE C.name = %s
                        AND V.plate_num = %s
                        AND J.job_type = %s"""
            values = (technician_name, customer_name, plate_num, description)
            cursor.execute(query, values)
            conn.commit()
            print(f"""{technician_name} has been assigned to handle the job for {customer_name}'s vehicle with plate number {plate_num}.""")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
