import sqlite3
from sqlite3.dbapi2 import Error

def get_prices(i):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    sql = f"SELECT c.name, p.close, p.open, p.high, p.low FROM cryptos c LEFT JOIN prices p ON c.id=p.crypto_id WHERE date='{i}'"
    # print(sql)
    rows=None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Error as e:
        print(e)
    connection.close()
    rates={}
    for row in rows:
        values={}
        values["close"]=row[1]
        values["open"]=row[2]
        values["high"]=row[3]
        values["low"]=row[4]
        rates[row[0]]=values

    for key, value in rates.items():
        print(f"{key} {value}")
    
    return rates

get_prices('2021-10-10')