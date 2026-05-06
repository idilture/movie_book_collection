import sqlite3


DATABASE_NAME = "movie_book_collection.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    with open("schema.sql", "r") as file:
        connection.executescript(file.read())

    connection.commit()
    connection.close()
