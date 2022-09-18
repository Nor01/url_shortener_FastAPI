import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_pass):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_pass
        )
    except Error as e:
        print(f"The error '{e}' ocurred.")

    return connection

connection = create_connection("localhost", "root", "")