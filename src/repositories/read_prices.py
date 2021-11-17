import sqlite3
from sqlite3.dbapi2 import Error

def get_prices(i):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    sql = f"SELECT c.id, c.name, p.close, p.open, p.high, p.low FROM cryptos c LEFT JOIN prices p ON c.id=p.crypto_id WHERE date='{i}'"
    # print(sql)
    rows=None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Error as e:
        print(e)
    connection.close()
    rates={}
    if rows:
        for row in rows:
            values={}
            values["name"]=row[1]
            values["close"]=row[2]
            values["open"]=row[3]
            values["high"]=row[4]
            values["low"]=row[5]
            rates[row[0]]=values
    
    return rates

# get_prices('2021-10-10')