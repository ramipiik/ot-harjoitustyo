import sqlite3
from sqlite3.dbapi2 import Error
from entities.content import Content
from config import DATABASE_PATH


def store_content_first_time(portfolio, first_day, initial_capital):
    """Method for storing portfolio content to database the first time"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO contents (portfolio_id, created, change_id) \
            VALUES (:portfolio_id, CURRENT_TIMESTAMP, 1)"
        cursor.execute(sql, {"portfolio_id": portfolio.id})
    except Error as error:
        print(error)
        return False
    try:
        sql = "INSERT INTO contents_support (portfolio_id, portfolio_day, cash, created, change_id)\
                VALUES (:portfolio_id, :first_day, :cash, CURRENT_TIMESTAMP, 1)"
        cursor.execute(
            sql,
            {
                "portfolio_id": portfolio.id,
                "first_day": first_day,
                "cash": initial_capital,
            },
        )
    except Error as error:
        print(error)
        return False
    connection.commit()
    connection.close()
    initial_content = [portfolio.id, first_day, initial_capital, 1]
    return initial_content

def store_content(contents: Content, rates):
    """Method for storing portfolio content to database after the first time"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    total_value = contents.cash
    if len(contents.cryptos.keys()) > 0:
        for crypto_id, status in contents.cryptos.items():
            if status:
                amount = status["amount"]
                value = amount * rates[crypto_id]["close"]
                total_value += value
                try:
                    sql = "INSERT INTO contents (portfolio_id, change_id, crypto_id, amount, value) \
                        VALUES (:portfolio_id, :change_id, :crypto_id, :amount, :value)"
                    cursor.execute(
                        sql,
                        {
                            "portfolio_id": contents.portfolio_id,
                            "change_id": contents.change_id,
                            "crypto_id": crypto_id,
                            "amount": amount,
                            "value": value,
                        },
                    )
                except Error as error:
                    print(error)
                    return False
        try:
            sql = "INSERT INTO contents_support \
                (portfolio_id, portfolio_day, cash, created, change_id, total_value) \
                VALUES (:portfolio_id, :portfolio_day, :cash, CURRENT_TIMESTAMP, :change_id, :total_value)"
            cursor.execute(
                sql,
                {
                    "portfolio_id": contents.portfolio_id,
                    "portfolio_day": contents.portfolio_day,
                    "cash": contents.cash,
                    "change_id": contents.change_id,
                    "total_value": total_value,
                },
            )
        except Error as error:
            print(error)
            return False
        connection.commit()
        connection.close()
        return True

    if len(contents.cryptos.keys()) == 0:
        try:
            sql = "INSERT INTO contents (portfolio_id, change_id) VALUES (:portfolio_id, :change_id)"
            cursor.execute(
                sql,
                {
                    "portfolio_id": contents.portfolio_id,
                    "change_id": contents.change_id,
                },
            )
        except Error as error:
            print(error)
            return False
        try:
            sql = "INSERT INTO contents_support \
                (portfolio_id, portfolio_day, cash, created, change_id, total_value) \
                VALUES (:portfolio_id, :portfolio_day, :cash, CURRENT_TIMESTAMP, :change_id, :total_value)"
            cursor.execute(
                sql,
                {
                    "portfolio_id": contents.portfolio_id,
                    "portfolio_day": contents.portfolio_day,
                    "cash": contents.cash,
                    "change_id": contents.change_id,
                    "total_value": total_value,
                },
            )
        except Error as error:
            print(error)
            return False
        connection.commit()
        connection.close()

    return True


def read_portfolio_content(portfolio_id):
    """Method for reading portfolio content of the latest period from the database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    # SQL query finds firstthe latest entry and after that fetches all rows related to that entry.
    sql = "SELECT cs.portfolio_day, cs.cash, c.crypto_id, c.amount, c.change_id, c.value, cs.total_value \
        FROM contents_support cs LEFT JOIN contents c ON c.change_id=cs.change_id \
        LEFT JOIN cryptos cr ON cr.id=c.crypto_id \
        WHERE cs.portfolio_id=:portfolio_id AND c.portfolio_id=:portfolio_id \
        AND cs.change_id=(select max(change_id) from contents \
        WHERE portfolio_id=:portfolio_id) ORDER BY crypto_id"
    rows = None
    try:
        cursor.execute(sql, {"portfolio_id": portfolio_id})
        rows = cursor.fetchall()
    except Error as error:
        print(error)
    connection.close()
    return rows


def read_portfolio_history(portfolio_id):
    """Method for reading historical valuations of the portfolio from the database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    sql = "select total_value from contents_support where portfolio_id=:portfolio_id"

    rows = None
    try:
        cursor.execute(sql, {"portfolio_id": portfolio_id})
        rows = cursor.fetchall()
    except Error as error:
        print(error)
    values = []
    for row in rows:
        values.append(row[0])
    connection.close()
    return values
