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
def add_user(first_name,last_name,email):
    cur.execute("INSERT INTO users (first_name,last_name,email) VALUES (?,?,?)",(first_name,last_name,email))
    con.commit()
# def add_book(name,surname,email):
is_finished = False
while not is_finished:
    print("1. Dodaj książkę")
    print("2. Dodaj użytkownika")
    print("3. Wypożycz książkę")
    print("4. Zwróć książkę")
    print("@. Zakończ program")
    match input():
        case "1":
            print("Dodaje książkę")

        case "2":
            print("Dodaje użytkownika")
            add_user("a","a","b")
        case "3":
            print("Wypożycz książkę")
        case "4":
            print("Zwrócono książkę")
        case "@":
            is_finished = True
        case _:
            print("Niepoprawna komenda")

