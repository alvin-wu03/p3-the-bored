import sqlite3


def create_db(db_name):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS "users" ("id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "user_id"	TEXT NOT NULL UNIQUE, "username"	TEXT NOT NULL UNIQUE, "password"	TEXT NOT NULL, "description"	TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS "movie_reviews" ("id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "movie_id"	TEXT NOT NULL, "uuid"	TEXT NOT NULL, "title"	TEXT NOT NULL, "rating"	INTEGER NOT NULL, "content"	TEXT NOT NULL, "date_posted"	INTEGER NOT NULL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS "book_reviews" ("id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "book_id"	TEXT NOT NULL, "uuid"	TEXT NOT NULL, "title"	TEXT NOT NULL, "rating"	INTEGER NOT NULL, "content"	TEXT NOT NULL, "date_posted"	INTEGER NOT NULL)')
    db.commit()
    db.close()


if __name__ == "__main__":
    create_db("the_board.db")
