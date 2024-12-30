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
# JOBS PAGE
##################################
def read_technicians():
    """
    displays all Jobs from the Operations_Job table.
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Operations_Job")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No Jobs found.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

#YOU WILL ONLY USE THESE THREE PARAMETERS TO ADD NEW JOBS
def add_job(plate_num, problem_description, start_date):
    """Adds a new job to the Operations_Job table
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """INSERT INTO Operations_Job(vehicle_id, job_type, start_date) VALUES
                        ( (SELECT vehicle_id
                            FROM Operations_Vehicle
                            WHERE plate_num = %s), %s, %s )
                    """
            values = (plate_num, problem_description, start_date)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def veiw_jobs_in_progress():
    """Displays all jobs still being done
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """SELECT C.name AS Customer_Name, V.make AS Make, V.plate_num AS Plate_Number, J.job_type AS Problem_Description, J.start_date AS Start_date, J.hours AS Hours, J.job_amount AS Job_Amount
                        FROM operations_job  AS J
                        JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id
                        JOIN operations_customer AS C ON V.customer_id = C.customer_id
                        WHERE J.status = 'In progress';
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No Jobs found.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def veiw_jobs_completed():
    """Displays all jobs that have been completed
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """SELECT C.name AS Customer_Name, V.make AS Make, V.plate_num AS Plate_Number, J.job_type AS Problem_Description, J.start_date AS Start_date, J.end_date AS End_date, J.hours AS Hours, J.job_amount AS Job_Amount
                        FROM operations_job  AS J
                        JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id
                        JOIN operations_customer AS C ON V.customer_id = C.customer_id
                        WHERE J.status = 'Completed';
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No Jobs found.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def finish_job(plate_num, problem_description, Technician_assigned, end_date, new_status):
    """Used to log finished jobs

    Args:
        plate_num (string): plate number of car worked on, used to identify the car to be worked on
        problem_description (string): decribes what is being worked on
        Technician_assigned (string): a technician's name
        end_date (string): Date job was completed
        new_status (string): new job status, probably 'completed'
    """
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """UPDATE operations_job AS J
                        JOIN operations_technician AS T ON J.technician_id = T.technician_id
                        JOIN operations_vehicle AS V ON V.vehicle_id = J.vehicle_id
                        SET J.status = %s, J.end_date = %s
                        WHERE V.plate_num = %s
                        AND J.job_type = %s
                        AND T.name = %s
                    """
            values = (new_status, end_date, plate_num, problem_description, Technician_assigned)
            cursor.execute(query, values)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


    