import sqlite3
from sqlite3.dbapi2 import Error

def get_prices(i):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    sql = f"SELECT * FROM  prices WHERE date='{i}'"
    # print(sql)
    rows=None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Error as e:
        print(e)

    for row in rows:
        print(row)

    connection.close()
