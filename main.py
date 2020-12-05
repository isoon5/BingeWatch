import sqlite3

conn = sqlite3.connect('movies.db')

c = conn.cursor()

c.execute(""" CREATE TABLE movies(
    name VARCHAR(255),
    link VARCHAR(255),
    current_season INTEGER,
    last_episode INTEGER,
    last_watch DATETIME,
    score DECIMAL(3,2),
    trailer_link VARCHAR(255)
) 
    """)