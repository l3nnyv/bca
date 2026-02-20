import mysql.connector

def get_connection():
    cnx = mysql.connector.connect(user='root',
                                password='****',
                                host='127.0.0.1',
                                database='bce',
                                use_pure=True) # Keeps same variable type as mysql instead of str.

    print("Connected to mysql")
    return cnx

    # Write SQL quesries here

    # cnx.close()
