import sqlite3
from sqlite3.dbapi2 import Error
from config import DATABASE_PATH


def store_portfolio(user_id, portfolio):
    """Method for storing a new portfolio to database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO portfolios (name, user_id, frequency, periods) VALUES (:name,:user_id, :frequency, :periods)"
        cursor.execute(
            sql,
            {
                "name": portfolio.name,
                "user_id": user_id,
                "frequency": portfolio.frequency,
                "periods": portfolio.periods,
            },
        )
        connection.commit()
        connection.close()
    except Error as e:
        print(e)
        return False
    return True


def read_portfolio_id(user_id, portfolio_name):
    """Method for reading portfolio id from database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT id FROM portfolios WHERE user_id=:user_id AND name=:portfolio_name"
    row = None
    try:
        cursor.execute(sql, {"user_id": user_id, "portfolio_name": portfolio_name})
        row = cursor.fetchone()
    except Error as e:
        print(e)
    connection.close()
    return row[0]


def read_portfolios(user_id):
    """Method for reading user's portfolios from database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT id, name FROM portfolios WHERE user_id=:user_id ORDER BY id"
    rows = None
    try:
        cursor.execute(sql, {"user_id": user_id})
        rows = cursor.fetchall()
    except Error as e:
        print(e)
    connection.close()
    return rows


def read_portfolio_frequency(portfolio_id):
    """Method for reading investment frequency of a portfolio from the database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT frequency FROM portfolios WHERE id=:portfolio_id"
    row = None
    try:
        cursor.execute(sql, {"portfolio_id": portfolio_id})
        row = cursor.fetchone()
    except Error as e:
        print(e)
    connection.close()
    return row
