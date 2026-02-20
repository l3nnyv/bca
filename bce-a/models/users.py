from db import get_connection

def insert_user(user_email, user_dob, user_phone, user_lname, user_fname, user_postcode, user_address, user_password_hash, role_id):
    cnx = get_connection()
    cursor = cnx.cursor()

    query = ("INSERT INTO users "
            "( "
            "user_dob, "
            "user_email, "
            "user_phone, "
            "user_lname, "
            "user_fname, "
            "user_postcode, "
            "user_address, "
            "user_hashed_password, "
            "role_id "
            ") "
            "VALUES "
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
    
    values = (user_dob, user_email,  user_phone, user_lname, user_fname, user_postcode, user_address, user_password_hash, role_id)
    cursor.execute(query, values)

    cnx.commit()

    user_id = cursor.lastrowid

    cursor.close()
    cnx.close()

    return user_id

def get_hashed_password_by_email(user_email):
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)

    query = ("SELECT user_hashed_password FROM users u "
            "WHERE u.user_email = %s")
    values = (user_email,)

    cursor.execute(query, values)
    user_hashed_password = cursor.fetchone()

    cursor.close()
    cnx.close()

    return user_hashed_password

def check_email(user_email):
    cnx = get_connection()
    cursor = cnx.cursor()

    query = ("SELECT user_email FROM users "
             "WHERE user_email = %s")
    values = (user_email,)

    cursor.execute(query, values)

    result = cursor.fetchone()

    cursor.close()
    cnx.close()

    return result is not None

def get_user_by_email(user_email):
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)

    query = ("SELECT user_id, user_dob, user_email,  user_phone, user_lname, user_fname, user_postcode, user_address, role_id  FROM users "
             "WHERE user_email = %s")
    values = (user_email, )

    cursor.execute(query, values)

    user = cursor.fetchone()

    cursor.close()
    cnx.close()

    return user