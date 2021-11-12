import csv
import sqlite3
from sqlite3.dbapi2 import IntegrityError
from sqlite3.dbapi2 import Error

connection = sqlite3.connect('../../data/database/data.db')

# Creating a cursor object to execute SQL queries on a database table
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
    #modify the date format to yyyy-mm-dd"
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
    # print(sql)
    try:
        cursor.executemany(sql, new_content)
    except IntegrityError:
        print("Error: Overlapping data in", filename+'.csv.')

connection.commit()
connection.close()
