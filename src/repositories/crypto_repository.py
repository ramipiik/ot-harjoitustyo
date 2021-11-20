import sqlite3
from sqlite3.dbapi2 import IntegrityError, Error
from config import DATABASE_PATH

CRYPTO_NAMES = [
    "ADA",
    "BCH",
    "BTC",
    "Dash",
    "DOGE",
    "EOS",
    "ETC",
    "ETH",
    "LTC",
    "MIOTA",
    "NEO",
    "TRX",
    "USDT",
    "VEN",
    "XEM",
    "XLM",
    "XMR",
    "XRP",
    "XTC",
]


def store_cryptos():
    """Method for storing crypto labels to database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    for crypto in CRYPTO_NAMES:
        sql = f"INSERT INTO cryptos (name) VALUES('{crypto}')"
        try:
            cursor.execute(sql)
        except IntegrityError:
            print(f"Error: Name {crypto} exists already.")
    connection.commit()
    connection.close()


def read_crypto_ids():
    """Method for reading crypto id's from database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT id FROM cryptos"
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Error as error:
        print(error)
    connection.close()
    ids = []
    for row in rows:
        ids.append(row[0])
    return ids
