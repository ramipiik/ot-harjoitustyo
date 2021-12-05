import sqlite3
from sqlite3.dbapi2 import Error
from config import DATABASE_PATH


def store_portfolio(user_id, portfolio):
    """Method for storing a new portfolio to database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO portfolios (name, user_id, frequency, periods) \
            VALUES (:name,:user_id, :frequency, :periods)"
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
    except Error as error:
        print(error)
        return False
    return True

def store_reference_portfolios(portfolio_id, strategies, frequency, periods):
    """Method for storing a new reference portfolio to database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    for strategy in strategies:
        try:
            sql = "INSERT INTO reference_portfolios (strategy, portfolio_id, frequency, periods) VALUES (:strategy,:portfolio_id, :frequency, :periods)"
            cursor.execute(
                sql,
                {
                    "strategy": strategy,
                    "portfolio_id": portfolio_id,
                    "frequency": frequency,
                    "periods": periods,
                },
            )
            connection.commit() #TESTAA VOIKO TÄMÄN LAITTAA MYÖHEMMÄKSI.
            
        except Error as error:
            print(error)
            return False
        
        #SQlite doesn't seem to support RETURNING ,so I need to fetch the id of the added reference portfolio manually
        sql = "SELECT max(id) FROM reference_portfolios"
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
        except Error as error:
            print(error)
        reference_portfolio_id=row[0]
        
        #Link the reference portfolio to the actual portfolio
        try:
            sql = "INSERT INTO portfolio_support (portfolio_id, reference_portfolio_id) VALUES (:portfolio_id, :reference_portfolio_id)"
            cursor.execute(
                sql,
                {
                    "portfolio_id": portfolio_id,
                    "reference_portfolio_id": reference_portfolio_id
                },
            )
            connection.commit() #TESTAA SIJOITUST
            
        except Error as error:
            print(error)
            return False


    

    connection.close()
    # print("id", row[0])
    return True



def read_portfolio_id(user_id, portfolio_name):
    """Method for reading portfolio id from database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT id FROM portfolios WHERE user_id=:user_id AND name=:portfolio_name"
    row = None
    try:
        cursor.execute(
            sql, {"user_id": user_id, "portfolio_name": portfolio_name})
        row = cursor.fetchone()
    except Error as error:
        print(error)
    connection.close()
    return row[0]

def read_reference_portfolios(portfolio_id):
    """Method for reading reference portfolio ids from database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT ps.reference_portfolio_id, rp.strategy FROM portfolio_support ps LEFT JOIN reference_portfolios rp ON ps.reference_portfolio_id=rp.id WHERE ps.portfolio_id=:portfolio_id AND rp.portfolio_id=:portfolio_id"
    rows=None
    try:
        cursor.execute(
            sql, {"portfolio_id": portfolio_id})
        rows = cursor.fetchall()
    except Error as error:
        print(error)
    connection.close()
    portfolios={}
    for row in rows:
        portfolios[row[1]]=row[0]
    return portfolios


def read_portfolios(user_id):
    """Method for reading user's portfolios from database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT id, name FROM portfolios WHERE user_id=:user_id ORDER BY id"
    rows = None
    try:
        cursor.execute(sql, {"user_id": user_id})
        rows = cursor.fetchall()
    except Error as error:
        print(error)
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
    except Error as error:
        print(error)
    connection.close()
    return row
