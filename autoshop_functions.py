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
    
# MAIN WINDOW
def mainwindow_customers():
    """
    Displays 5 rows from Operations_Customer table
    """
    try:
        conn = connect_db
        if conn:
            cursor = connect_db.cursor()
            cursor.execute("SELECT * FROM Operations_Customer LIMIT 5")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No customers found.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def mainwindow_technicians():
    """
    Displays 5 rows from Operations_Technician table
    """
    try:
        conn = connect_db
        if conn:
            cursor = connect_db.cursor()
            cursor.execute("SELECT * FROM Operations_Technician LIMIT 5")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No Technicians found.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def mainwindow_parts():
    """
    Displays 5 rows from Operations_Part table
    """
    try:
        conn = connect_db
        if conn:
            cursor = connect_db.cursor()
            cursor.execute("SELECT * FROM Operations_Part LIMIT 5")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No parts found.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def mainwindow_jobs():
    """
    Displays 5 rows from Operations_Job table
    """
    try:
        conn = connect_db
        if conn:
            cursor = connect_db.cursor()
            cursor.execute("SELECT * FROM Operations_Job LIMIT 5")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No jobs found.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# CUSTOMER PAGE
def read_customers():
    """
    displays all customers from the Operations_Customer table.
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Operations_Customer")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No customers found.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def add_customers(name, email, phone_num, address):
    """Adds a new customer to the Operations_Customer table
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO Operations_Customer (customer_id, name, email, phone_num, address) VALUES (%s, %s, %s, %s, %s)"
            values = (name, email, phone_num, address)
            cursor.execute(query, values)
            conn.commit()
            print(f"Customer {name} added successfully.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_customer_name(customer_id, new_name):
    """updates the name of an existing customer

    Args:
        customer_id (int)
        new_name (string)
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Customer SET name = %s WHERE customer_id = %s"
            values = (new_name, customer_id)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_customer_email(customer_id, new_email):
    """updates the email of an existing customer

    Args:
        customer_id (int)
        new_email (string)
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Customer SET email = %s WHERE customer_id = %s"
            values = (new_email, customer_id)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_customer_phone_num(customer_id, new_phone_num):
    """updates the phone number of an existing customer

    Args:
        customer_id (int)
        new_phone_num (string)
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Customer SET phone_num = %s WHERE customer_id = %s"
            values = (new_phone_num, customer_id)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def edit_customer_address(customer_id, new_address):
    """updates the address of an existing customer

    Args:
        customer_id (int)
        new_address (string)
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Customer SET address = %s WHERE customer_id = %s"
            values = (new_address, customer_id)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def delete_customer(customer_id):
    """Deletes a customer from the Operations_Customer table.
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "DELETE FROM Operations_Customer WHERE customer_id = %s"
            cursor.execute(query, (customer_id))
            conn.commit
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def customer_enqiries():
    """Displays all enquiries made by customers
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "" 


