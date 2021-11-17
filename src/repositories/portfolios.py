import sqlite3
from sqlite3.dbapi2 import Error
from entities.portfolio import Portfolio
from entities.content import Content

# def create_portfolio_repository(user_id, name, frequency):
#     connection = sqlite3.connect('../data/database/data.db')
#     cursor = connection.cursor()
#     try:
#         sql = "INSERT INTO portfolios (name, user_id, frequency) VALUES (:name,:user_id, :frequency)"
#         # print(sql)
#         cursor.execute(sql, {"name": name, "user_id": user_id, "frequency": frequency})
#         connection.commit()
#         connection.close()
#     except Error as e:
#         print(e)
#         return False
#     return True

def create_portfolio_repository(user_id, portfolio):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO portfolios (name, user_id, frequency, periods) VALUES (:name,:user_id, :frequency, :periods)"
        # print(sql)
        cursor.execute(sql, {"name": portfolio.name, "user_id": user_id, "frequency": portfolio.frequency, "periods":portfolio.periods})
        connection.commit()
        connection.close()
    except Error as e:
        print(e)
        return False
    return True

def fetch_portfolio_id(user_id, portfolio_name):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    sql = "SELECT id FROM portfolios WHERE user_id=:user_id AND name=:portfolio_name"
    # print(sql)
    rows=None
    try:
        cursor.execute(sql, {"user_id": user_id, "portfolio_name": portfolio_name})
        row = cursor.fetchone()
    except Error as e:
        print(e)
    connection.close()
    return row[0]

def store_first_time(portfolio:Portfolio, first_day, initial_capital):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO contents (portfolio_id, portfolio_day, cash, created, change_id) VALUES (:portfolio_id, :first_day, :cash, CURRENT_TIMESTAMP, 1)"
        # print(sql)
        cursor.execute(sql, {"portfolio_id": portfolio.id, "first_day": first_day, "cash": initial_capital})
        connection.commit()
        connection.close()
        initial_content=[portfolio.id, first_day, initial_capital, 1]
    except Error as e:
        print(e)
        return False
    return initial_content

def store_contents(contents:Content):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    if len(contents.cryptos.keys())>0:
        for crypto_id, amount in contents.cryptos.items():

            try:
                sql = "INSERT INTO contents (portfolio_id, portfolio_day, cash, created, change_id, crypto_id, amount) VALUES (:portfolio_id, :first_day, :cash, CURRENT_TIMESTAMP, :change_id, :crypto_id, :amount)"
                # print(sql)
                cursor.execute(sql, {"portfolio_id": contents.portfolio_id, "first_day": contents.portfolio_day, "cash": contents.cash, "change_id":contents.change_id, "crypto_id":crypto_id, "amount":amount})
            except Error as e:
                print(e)
                return False
        connection.commit()
        connection.close()
    return True

def read_user_porftfolios_repository(user_id):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    sql = "SELECT id, name FROM portfolios WHERE user_id=:user_id ORDER BY id"
    # print(sql)
    rows=None
    try:
        cursor.execute(sql, {"user_id": user_id})
        rows = cursor.fetchall()
    except Error as e:
        print(e)
    connection.close()
    return rows

def read_portfolio_content(portfolio_id):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    # fetches all events of the portfolio from the latest day.
    sql = "SELECT c.portfolio_day, c.cash, c.crypto_id, c.amount, c.change_id FROM contents c LEFT JOIN cryptos cr ON cr.id=c.crypto_id WHERE c.portfolio_id=:portfolio_id AND c.change_id=(select max(change_id) from contents where portfolio_id=:portfolio_id) ORDER BY created"
    # print(sql)
    rows=None
    try:
        cursor.execute(sql, {"portfolio_id":portfolio_id, "portfolio_id":portfolio_id})
        rows = cursor.fetchall()
    except Error as e:
        print(e)
    connection.close()
    # print("rows", rows)
    return rows