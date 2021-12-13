import sqlite3
from sqlite3.dbapi2 import Error
from config import DATABASE_PATH


def store_portfolio(user_id, portfolio):
    """
    Method for storing a new portfolio to database

    Args:
        user_id (str),
        portfolio (Portfolio)

    Returns:
        True if succesful. False if not successful.
    """ """"""

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
    """
    Method for storing a new reference portfolio to database

    Args:
        portfolio_id (int): Portfolio id
        strategies (list): List of reference strategies
        frequency (str): Decision making frequency. Daily, weekly or monthly
        periods (int): Not used at the moment

    Returns:
        True if succesful,
        False if not successful
    """
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    for strategy in strategies:
        user_id = "ref-" + str(portfolio_id)
        try:
            sql = "INSERT INTO portfolios (name, user_id, frequency, periods) VALUES (:name, :user_id, :frequency, :periods)"
            cursor.execute(
                sql,
                {
                    "name": strategy,
                    "user_id": user_id,
                    "frequency": frequency,
                    "periods": periods,
                },
            )
        except Error as error:
            print(error)
            return False

        # SQlite doesn't seem to support RETURNING ,so have to fetch the id of the added reference portfolio manually
        sql = "SELECT max(id) FROM portfolios"
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
        except Error as error:
            print(error)
        reference_portfolio_id = row[0]

        # Link the reference portfolio to the actual portfolio
        try:
            sql = "INSERT INTO portfolio_support (portfolio_id, reference_portfolio_id) VALUES (:portfolio_id, :reference_portfolio_id)"
            cursor.execute(
                sql,
                {
                    "portfolio_id": portfolio_id,
                    "reference_portfolio_id": reference_portfolio_id,
                },
            )
        except Error as error:
            print(error)
            return False

    connection.commit()
    connection.close()
    return True


def read_portfolio_id(user_id, portfolio_name):
    """
    Method for reading portfolio id from database

    Args:
        user_id (str): username
        portfolio_name (str): portfolio name

    Returns:
        int: portfolio id
    """
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT id FROM portfolios WHERE user_id=:user_id AND name=:portfolio_name"
    row = None
    try:
        cursor.execute(sql, {"user_id": user_id, "portfolio_name": portfolio_name})
        row = cursor.fetchone()
    except Error as error:
        print(error)
    connection.close()
    return row[0]


def read_reference_portfolios(portfolio_id):
    """
    Method for reading reference portfolio of a given user portfolio from database

    Args:
        portfolio_id (int): portfolio id

    Returns:
        dict: Dictionary where reference portfolio names are stored keys and ids as values
    """
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT id, name FROM portfolios WHERE id in (SELECT reference_portfolio_id FROM portfolio_support WHERE portfolio_id=:portfolio_id)"
    rows = None
    try:
        cursor.execute(sql, {"portfolio_id": portfolio_id})
        rows = cursor.fetchall()
    except Error as error:
        print(error)
    connection.close()
    portfolios = {}
    for row in rows:
        portfolios[row[1]] = row[0]
    return portfolios


def read_portfolios(user_id):
    """
    Method for reading user's portfolios from database

    Args:
        user_id (str): username

    Returns:
        list: List of lists containing portfolio id and portfolio name ordered by id
    """
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
    """
    Method for reading investment frequency of a portfolio from the database

    Args:
        portfolio_id (int): portfolio id

    Returns:
        list: portfolio frequency
    """
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


def delete_user_portfolios(username):
    """
    Method for deleting a portfolio from the database

    Args:
        username (str): username

    Returns:
        True if successful. Otherwise False.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM portfolios WHERE user_id=:username"
        cursor.execute(sql, {"username": username})
        connection.commit()
        connection.close()
    except Error as error:
        print(error)
        return False
    return True
