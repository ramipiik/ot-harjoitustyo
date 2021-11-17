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
    created TEXT,
    is_admin BOOLEAN
);

CREATE TABLE portfolios (
    id INTEGER PRIMARY KEY,
    name TEXT,
    user_id INTEGER REFERENCES users,
    frequency TEXT,
    periods INTEGER,
    UNIQUE(user_id, name)
)

CREATE TABLE contents (
    id INTEGER PRIMARY KEY,
    portfolio_id INTEGER REFERENCES portfolios,
    portfolio_day TEXT,
    crypto_id INTEGER REFERENCES cryptos,
    amount NUMERIC,
    cash NUMERIC,
    created TEXT
);
