import sqlite3
import csv
import datetime
from sqlite3.dbapi2 import IntegrityError, Error
from config import DATABASE_PATH
from repositories.crypto_repository import CRYPTO_NAMES


def read_prices(date):
    """Method for reading prices from data base"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    sql = f"SELECT c.id, c.name, p.close, p.open, p.high, p.low \
        FROM cryptos c LEFT JOIN prices p ON c.id=p.crypto_id WHERE date='{date}'"
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Error as error:
        print(error)

    rates = {}
    if rows:
        for number, row in enumerate(rows):
            # print("n", n)
            values = {}
            values["name"] = rows[number][1]
            try:
                values["close"] = rows[number][2]
            except Error:
                values["close"] = '--'
            try:
                values["open"] = rows[number][3]
            except Error:
                values["open"] = '--'
            try:
                values["high"] = rows[number][4]
            except Error:
                values["high"] = '--'
            try:
                values["low"] = rows[number][4]
            except Error:
                values["low"] = '--'
            rates[row[0]] = values
    return rates


def read_prices_for_statistics(date):
    """Method for reading prices including statistics from data base"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    date_object = datetime.datetime(
        int(date[0:4]), int(date[5:7]), int(date[8:10])
    ).date()

    date_object += datetime.timedelta(-1)
    date_d = str(date_object)

    date_object += datetime.timedelta(+1-7)
    date_w = str(date_object)

    date_object += datetime.timedelta(+7-30)
    date_m = str(date_object)

    date_object += datetime.timedelta(+30-365)
    date_y = str(date_object)

    sql = f"SELECT c.id, c.name, p.close, p.open, p.high, p.low \
        FROM cryptos c LEFT JOIN prices p ON c.id=p.crypto_id WHERE date='{date}'"
    rows_today = None
    try:
        cursor.execute(sql)
        rows_today = cursor.fetchall()
    except:
        rows_today = [None, None, None, None, None, None]

    # print("rows_today", rows_today)

    sql = f"SELECT c.id, c.name, p.close, p.open, p.high, p.low \
        FROM cryptos c LEFT JOIN prices p ON c.id=p.crypto_id WHERE date='{date_d}'"
    rows_d = None
    try:
        cursor.execute(sql)
        rows_d = cursor.fetchall()
    except:
        rows_d = [None, None, None, None, None, None]

    # print("rows_d", rows_d)

    sql = f"SELECT c.id, c.name, p.close, p.open, p.high, p.low \
        FROM cryptos c LEFT JOIN prices p ON c.id=p.crypto_id WHERE date='{date_w}'"
    rows_w = None
    try:
        cursor.execute(sql)
        rows_w = cursor.fetchall()
    except:
        rows_w = [None, None, None, None, None, None]

    # print("rows_w", rows_w)

    sql = f"SELECT c.id, c.name, p.close, p.open, p.high, p.low \
        FROM cryptos c LEFT JOIN prices p ON c.id=p.crypto_id WHERE date='{date_m}'"
    rows_m = None
    try:
        cursor.execute(sql)
        rows_m = cursor.fetchall()
    except:
        rows_m = [None, None, None, None, None, None]

    # print("rows_m", rows_m)

    sql = f"SELECT c.id, c.name, p.close, p.open, p.high, p.low \
        FROM cryptos c LEFT JOIN prices p ON c.id=p.crypto_id WHERE date='{date_y}'"
    rows_y = None
    try:
        cursor.execute(sql)
        rows_y = cursor.fetchall()
    except:
        rows_y = [None, None, None, None, None, None]

    # print("rows_d", rows_y)

    connection.close()

    data = {}
    data["today"] = rows_today
    data["d"] = rows_d
    data["w"] = rows_w
    data["m"] = rows_m
    data["y"] = rows_y
    return data


def store_prices():
    """Method for reading prices from CSV file and storing them to data base"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    for filename in CRYPTO_NAMES:
        sql = f"SELECT id FROM cryptos WHERE name='{filename}'"
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            crypto_id = result[0]
        except Error as error:
            print(error)
        with open("data/CSV/" + filename + ".csv", "r", encoding="utf8") as file:
            content = csv.reader(file)
            # modify date format to yyyy-mm-dd"
            new_content = []
            for row in content:
                original_date = row[0]
                month = original_date[0:2]
                day = original_date[3:5]
                year = original_date[6:10]
                new_date = year + "-" + month + "-" + day
                row[0] = new_date
                new_content.append(row)
        sql = f"INSERT INTO prices (crypto_id, date, close, volume, open, high, low) \
            VALUES('{crypto_id}', ?, ?, ?, ?, ?, ?)"
        try:
            cursor.executemany(sql, new_content)
        except IntegrityError:
            print("Error: Overlapping data in", filename + ".csv.")
    connection.commit()
    connection.close()


def read_volatility_data(end_day):
    """Method for reading price data for the last year"""
    date_object = datetime.datetime(
        int(end_day[0:4]), int(end_day[5:7]), int(end_day[8:10])
    ).date()

    start_day_object = date_object - datetime.timedelta(365)
    start_day = str(start_day_object)
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = f"SELECT crypto_id, close from prices where date between :start and :end"
    rows = None
    try:
        cursor.execute(sql, {"start": start_day, "end": end_day})
        rows = cursor.fetchall()
    except Error as error:
        print(error)
    return rows


def read_max_day():
    """Method for reading the latest day with prices from data base"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    sql = f"SELECT max(date) from prices"
    row = None
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
    except Error as error:
        print(error)
    return row
