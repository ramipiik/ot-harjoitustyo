CREATE TABLE prices (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    UNIQUE(name, date)
);