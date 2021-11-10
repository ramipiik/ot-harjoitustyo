import csv
import sqlite3
from sqlite3.dbapi2 import IntegrityError

connection = sqlite3.connect('../../data/database/data.db')

# Creating a cursor object to execute SQL queries on a database table
cursor = connection.cursor()
filenames=['ADA', 'BCH', 'BTC', 'Dash', 'DOGE', 'EOS', 'ETC', 'ETH', 'LTC', 'MIOTA', 'NEO', 'TRX', 'USDT', 'VEN', 'XEM', 'XLM', 'XMR', 'XRP', 'XTC']
for filename in filenames:
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
    sql = f"INSERT INTO prices (name, date, close, volume, open, high, low) VALUES('{filename}', ?, ?, ?, ?, ?, ?)"
    # print(sql)
    try:
        cursor.executemany(sql, new_content)
    except IntegrityError:
        print("Error: Overlapping data in", filename+'.csv.')

connection.commit()
connection.close()
