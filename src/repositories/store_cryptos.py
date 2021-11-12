import sqlite3
from sqlite3.dbapi2 import IntegrityError

connection = sqlite3.connect('../../data/database/data.db')

# Creating a cursor object to execute SQL queries on a database table
cursor = connection.cursor()
cryptos=['ADA', 'BCH', 'BTC', 'Dash', 'DOGE', 'EOS', 'ETC', 'ETH', 'LTC', 'MIOTA', 'NEO', 'TRX', 'USDT', 'VEN', 'XEM', 'XLM', 'XMR', 'XRP', 'XTC']
for crypto in cryptos:
    sql = f"INSERT INTO cryptos (name) VALUES('{crypto}')"
    # print(sql)
    try:
        cursor.execute(sql)
    except IntegrityError:
        print(f"Error: Name {crypto} exists already.")

connection.commit()
connection.close()
