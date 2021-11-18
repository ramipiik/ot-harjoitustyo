import sqlite3
from sqlite3.dbapi2 import IntegrityError


'''Method for storing crypto labels to database'''
def store_cryptos():
    connection = sqlite3.connect('../../data/database/data.db')
    cursor = connection.cursor()
    cryptos=['ADA', 'BCH', 'BTC', 'Dash', 'DOGE', 'EOS', 'ETC', 'ETH', 'LTC', 'MIOTA', 'NEO', 'TRX', 'USDT', 'VEN', 'XEM', 'XLM', 'XMR', 'XRP', 'XTC']
    for crypto in cryptos:
        sql = f"INSERT INTO cryptos (name) VALUES('{crypto}')"
        try:
            cursor.execute(sql)
        except IntegrityError:
            print(f"Error: Name {crypto} exists already.")
    connection.commit()
    connection.close()
