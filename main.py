import sqlite3
con = sqlite3.connect("library.db")
cur = con.cursor()


# cur.execute("""
#     CREATE TABLE  IF NOT EXISTS books (
#     id int PRIMARY KEY,
#     title text,
#     author text,
#     year int
#     )
#
# """)

# cur.execute("""
#     CREATE TABLE  IF NOT EXISTS users (
#     id int PRIMARY KEY,
#     first_name text,
#     last_name text,
#     email text
#     )
# """)

cur.execute("""
    CREATE TABLE  IF NOT EXISTS rented_books (
    id int PRIMARY KEY,
    book_id int,
    user_id int,
    rented_date date,
    finish_date date,
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
    ) 
""")

is_finished = False