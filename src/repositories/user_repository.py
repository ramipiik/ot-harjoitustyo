import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from sqlite3.dbapi2 import Error


DATABASE_PATH='../data/database/data.db'

'''Method for verifying username and password'''
def verify_user(username, password):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT id, username, is_admin, password FROM users WHERE username=:username"
    try:
        cursor.execute(sql, {"username": username})
        user = cursor.fetchone()
    except Error as e:
        print(e)
    connection.close()
    if not user:
        print ("user not found")
        return None
    else:
        if check_password_hash(user[3], password):
            return user[0]
        else:
            print ("passwords don't match")
            return None


def logout():
    #to be done
    pass


'''Method for storing a new user to database'''
def store_user(username, password):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, created, is_admin) VALUES (:username,:password, CURRENT_TIMESTAMP, False)"
        cursor.execute(sql, {"username": username, "password": hash_value})
        connection.commit()
        connection.close()
    except Error as e:
        print(e)
        return False
    return True
