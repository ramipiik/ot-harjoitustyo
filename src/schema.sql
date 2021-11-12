CREATE TABLE cryptos (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL 
)

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

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    created TIMESTAMP,
    is_admin BOOLEAN
);

CREATE TABLE portfolios (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    frequency TEXT,
    periods INTEGER,
)

CREATE TABLE contents (
    id INTEGER PRIMARY KEY,
    portfolio_id INTEGER REFERENCES portfolios,
    date TIMESTAMP,
    crypto_id INTEGER REFERENCES cryptos,
    amount NUMERIC,
    cash NUMERIC
);
