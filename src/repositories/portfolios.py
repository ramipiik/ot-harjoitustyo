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
        sql = "INSERT INTO contents (portfolio_id, created, change_id) VALUES (:portfolio_id, CURRENT_TIMESTAMP, 1)"
        # print(sql)
        cursor.execute(sql, {"portfolio_id": portfolio.id})
    except Error as e:
        print(e)
        return False
    
    try:
        sql = "INSERT INTO contents_support (portfolio_id, portfolio_day, cash, created, change_id) VALUES (:portfolio_id, :first_day, :cash, CURRENT_TIMESTAMP, 1)"
        # print(sql)
        cursor.execute(sql, {"portfolio_id": portfolio.id, "first_day": first_day, "cash": initial_capital})

    except Error as e:
        print(e)
        return False
    
    connection.commit()
    connection.close()
    initial_content=[portfolio.id, first_day, initial_capital, 1]
    return initial_content

def store_contents(contents:Content, rates):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    total_value=contents.cash
    if len(contents.cryptos.keys())>0:
        for crypto_id, status in contents.cryptos.items():
            print("crypto_id", crypto_id)
            print("status", status)
            amount=status["amount"]
            value=amount*rates[crypto_id]["close"]
            total_value+=value
            try:
                sql = "INSERT INTO contents (portfolio_id, change_id, crypto_id, amount, value) VALUES (:portfolio_id, :change_id, :crypto_id, :amount, :value)"
                # print(sql)
                cursor.execute(sql, {"portfolio_id": contents.portfolio_id, "change_id":contents.change_id, "crypto_id":crypto_id, "amount":amount, "value":value})
            except Error as e:
                print(e)
                return False            
        try:
            sql = "INSERT INTO contents_support (portfolio_id, portfolio_day, cash, created, change_id, total_value) VALUES (:portfolio_id, :portfolio_day, :cash, CURRENT_TIMESTAMP, :change_id, :total_value)"
            # print(sql)
            cursor.execute(sql, {"portfolio_id": contents.portfolio_id, "portfolio_day": contents.portfolio_day, "cash": contents.cash, "change_id":contents.change_id, "total_value": total_value})
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

def read_portfolio_frequency(portfolio_id):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    sql = "SELECT frequency FROM portfolios WHERE id=:portfolio_id"
    # print(sql)
    row=None
    try:
        cursor.execute(sql, {"portfolio_id": portfolio_id})
        row = cursor.fetchone()
    except Error as e:
        print(e)
    connection.close()
    return row



def read_portfolio_content(portfolio_id):
    connection = sqlite3.connect('../data/database/data.db')
    cursor = connection.cursor()
    # fetches all events of the portfolio from the latest day.
    #sql = "SELECT c.portfolio_day, c.cash, c.crypto_id, c.amount, c.change_id, c.value FROM contents c LEFT JOIN cryptos cr ON cr.id=c.crypto_id WHERE c.portfolio_id=:portfolio_id AND c.change_id=(select max(change_id) from contents where portfolio_id=:portfolio_id) ORDER BY crypto_id"
    sql = "SELECT cs.portfolio_day, cs.cash, c.crypto_id, c.amount, c.change_id, c.value, cs.total_value FROM contents_support cs LEFT JOIN contents c ON c.change_id=cs.change_id LEFT JOIN cryptos cr ON cr.id=c.crypto_id WHERE cs.portfolio_id=:portfolio_id AND c.portfolio_id=:portfolio_id AND cs.change_id=(select max(change_id) from contents where portfolio_id=:portfolio_id) ORDER BY crypto_id"
    print(sql)
    rows=None
    try:
        cursor.execute(sql, {"portfolio_id":portfolio_id})
        rows = cursor.fetchall()
    except Error as e:
        print(e)
    connection.close()
    print("rows", rows)
    return rows