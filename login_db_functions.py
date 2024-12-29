import mysql.connector
import bcrypt #used for password hashing(encryption)

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

#VAL USE THIS FUNCTION ONLY TO INSERT USERS INTO THE DATABASE ON YOUR END
#IT IS NOT A BACKEND FUNCTION THAT NEEDS TO BE INTEGRATED TO YOUR FRONEND CODE
def hash_and_insert_users():
    users = [
        {"username": "admin", "password": "admin1234", "role": "Admin"},
        {"username": "tech1", "password": "tech12345", "role": "Technician"},
        {"username": "tech2", "password": "tech67890", "role": "Technician"},
        {"username": "admin2", "password": "admin5678", "role": "Admin"},
        {"username": "tech3", "password": "tech4321", "role": "Technician"}
    ]

    try:
        conn = connect_db()
        cursor = conn.cursor()

        for user in users:
            hashed_password = bcrypt.hashpw(user["password"].encode('utf-8'), bcrypt.gensalt())
            query = "INSERT INTO Users (username, password_hash, role) VALUES (%s, %s, %s)"
            cursor.execute(query, (user["username"], hashed_password.decode('utf-8'), user["role"]))

        conn.commit()
        print("Users inserted successfully!")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

#password validation
def verify_login(username, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT password_hash, role FROM Users WHERE username = %s;"
        cursor.execute(query, (username))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return user['role'] #succesful login, returns the role
        else:
            return None # invalid credentials
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


###THIS WILL BE FOR A SIGN UP PAGE#####
def add_new_user(username, password, role):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        #Hashing the password for security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query = "INSERT INTO Users (username, password_hash, role) VALUES (%s, %s, %s);"
        cursor.execute(query, (username, hashed_password.decode('utf-8'), role))
        conn.commit()
        print("New user added successfully!")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def change_password(username, current_password, new_password):
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)#fecthing it as a dictionary makes slicing easier

        #fetching current hashed password
        query = "SELECT password_hash FROM Users WHERE username = %s;"
        cursor.execute(query, (username))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(current_password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            # Hash the new password
            new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            # Update the password in the database
            update_query = "UPDATE Users SET password_hash = %s WHERE username = %s;"
            cursor.execute(update_query, (new_hashed_password.decode('utf-8'), username))
            conn.commit()
            print("Password updated successfully!")
        else:
            print("Current password is incorrect.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

