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
            query = """WITH name_plate_num(Customer_Name, Plate_Number) AS
                            (SELECT DISTINCT C.name,  V.plate_num
                            FROM operations_customer AS C
                            JOIN operations_vehicle AS V ON C.customer_id = V.customer_id),
                        mech_job(Enquiry_date, Problem_Description, Technician_Assigned, Plate_Number) AS
                            (SELECT J.start_date, J.job_type, T.name,  V.plate_num
                            FROM operations_job AS J
                            JOIN Operations_Technician AS T ON J.technician_id = T.technician_id
                            JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id)
                        SELECT Customer_Name, NPN.Plate_Number AS Plate_Number, Enquiry_date, Problem_Description, Technician_Assigned
                        FROM name_plate_num AS NPN
                        JOIN mech_job AS MJ ON NPN.Plate_Number = MJ.Plate_Number
                    """
            cursor.execute(query)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def customer_invoice():
    """Displays all existing customers with the cost of reparing their car
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """SELECT C.name AS Customer_Name, P.part_name AS Part_Used, JP.quantity_part_used AS Number_of_Parts_Used, JP.part_amount AS Part_Amount, J.job_amount AS Job_Amount, JP.total_cost AS Total_Cost 
                       FROM operations_jobpart AS JP
                       JOIN operations_job AS J ON J.job_id = JP.job_id
                       JOIN operations_part AS P ON P.part_id = JP.part_id
                       JOIN operations_vehicle AS V ON V.vehicle_id = J.vehicle_id
                       JOIN operations_customer AS C ON C.customer_id = V.customer_id
                    """
            cursor.execute(query)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

#Fields to be calculated
def calculate_job_amount(job_id):
    """job_amount is calculated as hours * hourly_rate

    Args:
        job_id (int): primary key of Operations_Job table
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            query = """SELECT J.hours, T.hourly_rate
                    FROM Operations_Job AS J
                    JOIN Operations_Technician AS T ON J.technician_id = T.technician_id
                    WHERE J.job_id = %s;
                    """
            cursor.execute(query, (job_id))
            result = cursor.fetchone()

            #calculating job_amount
            if result:
                job_amount = result['hours'] * result['hourly_rate']
                return job_amount
            else:
                return None # Job not found
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
         if conn:
            cursor.close()
            conn.close()

def calculate_part_amount(jobpart_id):
    """ part_amount is calculated as quantity_part_used * unit_price
    Args:
        jobpart_id (int): primary key of Operations_JobPart table
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            query = """ SELECT JP.quantity_part_used, P.unit_price
                        FROM Operations_JobPart AS JP
                        JOIN Operations_Part AS P ON JP.part_id = P.part_id
                        WHERE JP.jobpart_id = %s;
                    """
            cursor.execute(query, (jobpart_id))
            result = cursor.fetchone()

            #calculating part_amount
            if result:
                part_amount = result['quantity_part_used'] * result['unit_price']
                return part_amount
            else:
                return None # Jobpart not found
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
         if conn:
            cursor.close()
            conn.close()

def calculate_total_cost(job_id, jobpart_id):
    job_amount = calculate_job_amount(job_id)
    part_amount = calculate_part_amount(jobpart_id)

    if job_amount is not None and part_amount is not None:
        total_cost = job_amount + part_amount
        return total_cost
    else:
        return None  # One of the components is missing

