
import mysql.connector

# Establishing the connection to the MySQL database
def connect_db():
    """
    Establishes a connection to the MySQL database.
    Returns:
        conn: The MySQL connection object.
    """
    try:
        return mysql.connector.connect(
            host="localhost",  # Database host
            port=3306,         # MySQL default port
            user="root",       # Your MySQL username
            password="Vondabaic2020",  # Replace with your MySQL password
            database="Autoshop"   # The database you want to connect to
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Create (Insert data into the table)
def create_customer():
    """
    Adds a new customer to the Operations_Customer table.
    """
    try:
        customer_id = int(input("Enter customer ID: "))
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")
        phone_num = input("Enter customer phone number: ")
        address = input("Enter customer address: ")

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO Operations_Customer (customer_id, name, email, phone_num, address) VALUES (%s, %s, %s, %s, %s)"
            values = (customer_id, name, email, phone_num, address)
            cursor.execute(query, values)
            conn.commit()
            print(f"Customer {name} added successfully.")
    except ValueError:
        print("Invalid input. Customer ID must be an integer.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Read (Select data from the table)
def read_customers():
    """
    Fetches and displays all customers from the Operations_Customer table.
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

# Update (Update existing data)
def update_customer():
    """
    Updates the name of an existing customer in the Operations_Customer table.
    """
    try:
        customer_id = int(input("Enter customer ID to update: "))
        new_name = input("Enter the new name for the customer: ")

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE Operations_Customer SET name = %s WHERE customer_id = %s"
            values = (new_name, customer_id)
            cursor.execute(query, values)
            conn.commit()
            print(f"Customer {customer_id} updated to {new_name}.")
    except ValueError:
        print("Invalid input. Customer ID must be an integer.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Delete (Delete a record)
def delete_customer():
    """
    Deletes a customer from the Operations_Customer table.
    """
    try:
        customer_id = int(input("Enter customer ID to delete: "))

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "DELETE FROM Operations_Customer WHERE customer_id = %s"
            cursor.execute(query, (customer_id,))
            conn.commit()
            print(f"Customer {customer_id} deleted successfully.")
    except ValueError:
        print("Invalid input. Customer ID must be an integer.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Main program loop to choose an operation
if __name__ == "__main__":
    while True:
        print("\nChoose an operation:")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("5. Exit")
        
        choice = input("Enter choice (1/2/3/4/5): ")
        
        if choice == '1':
            create_customer()
        elif choice == '2':
            read_customers()
        elif choice == '3':
            update_customer()
        elif choice == '4':
            delete_customer()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please enter a number between 1 and 5.")
