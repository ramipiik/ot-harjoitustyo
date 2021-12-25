from repositories.crypto_repository import store_cryptos
from repositories.price_repository import store_prices
from database_connection import get_connection

def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
        drop table if exists contents;
    ''')
    cursor.execute('''
        drop table if exists cryptos;
    ''')
    cursor.execute('''
        drop table if exists portfolios;
    ''')
    cursor.execute('''
        drop table if exists users;
    ''')
    cursor.execute('''
        drop table if exists contents_support;
    ''')
    cursor.execute('''
        drop table if exists portfolio_support;
    ''')
    cursor.execute('''
        drop table if exists prices;
    ''')
    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE cryptos (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL 
        );
    ''')
    cursor.execute('''
        CREATE TABLE prices (
            id INTEGER PRIMARY KEY,
            crypto_id INTEGER REFERENCES cryptos,
            date TEXT NOT NULL,
            close NUMERIC NOT NULL,
            volume NUMERIC,
            open NUMERIC,
            high NUMERIC,
            low NUMERIC,
            UNIQUE(crypto_id, date)
        );
    ''')
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            created TIMESTAMP,
            is_admin BOOLEAN
        );
    ''')
    cursor.execute('''
        CREATE TABLE portfolios (
            id INTEGER PRIMARY KEY,
            name TEXT,
            user_id TEXT REFERENCES users,
            frequency TEXT,
            periods INTEGER,
            UNIQUE(user_id, name)
        );
    ''')
    cursor.execute('''
        CREATE TABLE portfolio_support (
            id INTEGER PRIMARY KEY,
            portfolio_id INTEGER REFERENCES portfolios,
            reference_portfolio_id INTEGER REFERENCES portfolios
        );
    ''')
    cursor.execute('''
        CREATE TABLE contents (
            id INTEGER PRIMARY KEY,
            portfolio_id INTEGER REFERENCES portfolios,
            portfolio_day TEXT,
            crypto_id INTEGER REFERENCES cryptos,
            amount NUMERIC,
            cash NUMERIC,
            created TEXT,
            change_id integer, value numeric
        );
    ''')
    cursor.execute('''
        CREATE TABLE contents_support (
            id INTEGER PRIMARY KEY,
            change_id INTEGER REFERENCES contents,
            cash NUMERIC,
            portfolio_id INTEGER REFERENCES portfolio,
            portfolio_day TEXT,
            created TEXT
        , total_value numeric);
    ''')

    connection.commit()


def initialize_database():
    connection=get_connection()  
    drop_tables(connection)
    create_tables(connection)
    store_cryptos()
    store_prices()

if __name__ == "__main__":
    initialize_database()