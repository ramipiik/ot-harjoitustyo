import sqlite3
from sqlite3.dbapi2 import Error
from entities.portfolio import Portfolio
from entities.content import Content

DATABASE_PATH='../data/database/data.db'

'''Method for storing a new portfolio to database'''
def store_portfolio(user_id, portfolio):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO portfolios (name, user_id, frequency, periods) VALUES (:name,:user_id, :frequency, :periods)"
        cursor.execute(sql, {"name": portfolio.name, "user_id": user_id, "frequency": portfolio.frequency, "periods":portfolio.periods})
        connection.commit()
        connection.close()
    except Error as e:
        print(e)
        return False
    return True


'''Method for reading portfolio id from database'''
def read_portfolio_id(user_id, portfolio_name):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT id FROM portfolios WHERE user_id=:user_id AND name=:portfolio_name"
    row=None
    try:
        cursor.execute(sql, {"user_id": user_id, "portfolio_name": portfolio_name})
        row = cursor.fetchone()
    except Error as e:
        print(e)
    connection.close()
    return row[0]


'''Method for reading user's portfolios from database'''
def read_portfolios(user_id):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT id, name FROM portfolios WHERE user_id=:user_id ORDER BY id"
    rows=None
    try:
        cursor.execute(sql, {"user_id": user_id})
        rows = cursor.fetchall()
    except Error as e:
        print(e)
    connection.close()
    return rows


'''Method for reading investment frequency of a portfolio from the database'''
def read_portfolio_frequency(portfolio_id):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT frequency FROM portfolios WHERE id=:portfolio_id"
    row=None
    try:
        cursor.execute(sql, {"portfolio_id": portfolio_id})
        row = cursor.fetchone()
    except Error as e:
        print(e)
    connection.close()
    return row