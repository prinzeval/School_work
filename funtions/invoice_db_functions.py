# invoice_db_functions.py

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

def add_invoice(invoice_id, jobpart_id, issued_date, sales_tax):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = """INSERT INTO Operations_Invoice (invoice_id, jobpart_id, issued_date, sales_tax) VALUES
                   (%s, %s, %s, %s);
                """
        values = (invoice_id, jobpart_id, issued_date, sales_tax)
        cursor.execute(query, values)
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def update_payment_status(invoice_id, new_status):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "UPDATE operations_invoice SET payment_status = %s WHERE invoice_id = %s;"
        values = (new_status, invoice_id)
        cursor.execute(query, values)
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def view_invoices():
    rows = []
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """SELECT I.invoice_id, C.name AS Customer_Name, C.address AS Address, I.issued_date AS Issued_Date, V.make AS Make, V.model AS Model,
                        V.year AS Year, V.colour AS Colour, V.VIN, V.plate_num AS Plate_Number, V.mileage AS Mileage, J.job_type AS Job_Performed,
                        JP.quantity_part_used AS No_of_Parts_Used, JP.part_amount AS Part_Price, J.job_amount AS Labour, I.sales_tax AS Sales_Tax, 
                        I.total_amount AS Total_amount, I.payment_status AS Payment_Status
                        FROM operations_invoice  AS I
                        JOIN operations_jobpart AS JP ON I.jobpart_id = JP.jobpart_id
                        JOIN operations_job AS J ON JP.job_id = J.job_id
                        JOIN operations_part AS P ON JP.part_id = P.part_id
                        JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id
                        JOIN operations_customer AS C ON V.customer_id = C.customer_id;
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return rows

def view_unpaid_invoices():
    rows = []
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """SELECT I.invoice_id, C.name AS Customer_Name, C.address AS Address, I.issued_date AS Issued_Date, V.make AS Make, V.model AS Model,
                        V.year AS Year, V.colour AS Colour, V.VIN, V.plate_num AS Plate_Number, V.mileage AS Mileage, J.job_type AS Job_Performed,
                        JP.quantity_part_used AS No_of_Parts_Used, JP.part_amount AS Part_Price, J.job_amount AS Labour, I.sales_tax AS Sales_Tax, 
                        I.total_amount AS Total_amount, I.payment_status AS Payment_Status
                        FROM operations_invoice  AS I
                        JOIN operations_jobpart AS JP ON I.jobpart_id = JP.jobpart_id
                        JOIN operations_job AS J ON JP.job_id = J.job_id
                        JOIN operations_part AS P ON JP.part_id = P.part_id
                        JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id
                        JOIN operations_customer AS C ON V.customer_id = C.customer_id
                        WHERE I.payment_status = "Unpaid";
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return rows

def view_paid_invoices():
    rows = []
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """SELECT I.invoice_id, C.name AS Customer_Name, C.address AS Address, I.issued_date AS Issued_Date, V.make AS Make, V.model AS Model,
                        V.year AS Year, V.colour AS Colour, V.VIN, V.plate_num AS Plate_Number, V.mileage AS Mileage, J.job_type AS Job_Performed,
                        JP.quantity_part_used AS No_of_Parts_Used, JP.part_amount AS Part_Price, J.job_amount AS Labour, I.sales_tax AS Sales_Tax, 
                        I.total_amount AS Total_amount, I.payment_status AS Payment_Status
                        FROM operations_invoice  AS I
                        JOIN operations_jobpart AS JP ON I.jobpart_id = JP.jobpart_id
                        JOIN operations_job AS J ON JP.job_id = J.job_id
                        JOIN operations_part AS P ON JP.part_id = P.part_id
                        JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id
                        JOIN operations_customer AS C ON V.customer_id = C.customer_id
                        WHERE I.payment_status = "paid";
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return rows
