from sqlite3.dbapi2 import IntegrityError, Error
from database_connection import get_connection

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
    connection = get_connection()
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
    """
    Method for reading crypto id's from database

    Returns:
        list: crypto id's
    """
    connection = get_connection()
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


def read_crypto_names_and_ids():
    """
    Method for reading crypto id's from database

    Returns:
        dict: Dictionary where crypto_ids are stored as keys and crypto names as values
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT id, name FROM cryptos"
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Error as error:
        print(error)
    connection.close()
    result = {}
    for row in rows:
        result[row[0]] = row[1]
    return result
