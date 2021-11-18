import sqlite3
import csv
from sqlite3.dbapi2 import IntegrityError
from sqlite3.dbapi2 import Error


DATABASE_PATH='../data/database/data.db'


'''Method for reading prices from data base'''
def read_prices(i):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = f"SELECT c.id, c.name, p.close, p.open, p.high, p.low FROM cryptos c LEFT JOIN prices p ON c.id=p.crypto_id WHERE date='{i}'"
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


'''Method for reading prices from CSV file and storing them to data base'''
def store_prices():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    filenames=['ADA', 'BCH', 'BTC', 'Dash', 'DOGE', 'EOS', 'ETC', 'ETH', 'LTC', 'MIOTA', 'NEO', 'TRX', 'USDT', 'VEN', 'XEM', 'XLM', 'XMR', 'XRP', 'XTC']
    for filename in filenames:
        sql = f"SELECT id FROM cryptos WHERE name='{filename}'"
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            crypto_id=result[0]
        except Error as e:
            print(e)
        file = open('../../data/CSV/'+filename+'.csv')
        content = csv.reader(file)
        #modify date format to yyyy-mm-dd"
        new_content=[]
        for row in content:
            original_date=(row[0])
            month=original_date[0:2]
            day=original_date[3:5]
            year=original_date[6:10]
            new_date=year+'-'+month+'-'+day
            row[0]=new_date
            new_content.append(row)
        sql = f"INSERT INTO prices (crypto_id, date, close, volume, open, high, low) VALUES('{crypto_id}', ?, ?, ?, ?, ?, ?)"
        try:
            cursor.executemany(sql, new_content)
        except IntegrityError:
            print("Error: Overlapping data in", filename+'.csv.')
    connection.commit()
    connection.close()