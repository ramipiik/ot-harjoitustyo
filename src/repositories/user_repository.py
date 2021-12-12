import sqlite3
from sqlite3.dbapi2 import Error
from werkzeug.security import check_password_hash, generate_password_hash
from config import DATABASE_PATH


def verify_user(username, password):
    """Method for verifying username and password"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT id, username, is_admin, password FROM users WHERE username=:username"
    try:
        cursor.execute(sql, {"username": username})
        user = cursor.fetchone()
    except Error as error:
        print(error)
        return False
    connection.close()
    if not user:
        return False
    if check_password_hash(user[3], password):
        return [user[0], user[1], user[2]]
    return None


def store_user(username, password):
    """Method for storing a new user to database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, created, is_admin) \
            VALUES (:username,:password, CURRENT_TIMESTAMP, False)"
        cursor.execute(sql, {"username": username, "password": hash_value})
        connection.commit()
        connection.close()
    except Error as error:
        print(error)
        return False
    return True


def delete_user(username):
    """Method for deleting a user from the database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM users WHERE username=:username"
        cursor.execute(sql, {"username": username})
        connection.commit()
        connection.close()
    except Error as error:
        print(error)
        return False
    return True
