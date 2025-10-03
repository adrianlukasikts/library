import sqlite3
from datetime import datetime

con = sqlite3.connect("library.db")
cur = con.cursor()


def now():
    return datetime.today().date()


def days_between(d1, d2):
    d1 = datetime.strptime(str(d1), "%Y-%m-%d")
    d2 = datetime.strptime(str(d2), "%Y-%m-%d")
    return abs((d2 - d1).days)


cur.execute("""
            CREATE TABLE IF NOT EXISTS books
            (
                id
                integer
                PRIMARY
                KEY
                AUTOINCREMENT,
                title
                text,
                author
                text,
                year
                int
            )
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS users
            (
                id
                integer
                PRIMARY
                KEY
                AUTOINCREMENT,
                first_name
                text,
                last_name
                text,
                email
                text
            )
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS rented_books
            (
                id
                integer
                PRIMARY
                KEY
                AUTOINCREMENT,
                book_id
                int,
                user_id
                int,
                rented_date
                date,
                finish_date
                date,
                FOREIGN
                KEY
            (
                book_id
            ) REFERENCES books
            (
                id
            ),
                FOREIGN KEY
            (
                user_id
            ) REFERENCES users
            (
                id
            )
                )
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS fees
            (
                id
                integer
                PRIMARY
                KEY
                AUTOINCREMENT,
                user_id
                int,
                fee
                int,
                add_date
                date,
                FOREIGN
                KEY
            (
                user_id
            ) REFERENCES users
            (
                id
            )
                )
            """)


def add_book(title, author, year):
    cur.execute("INSERT INTO books(title, author, year) VALUES (?,?,?)", (title, author, year))
    con.commit()


def add_user(first_name, last_name, email):
    cur.execute("INSERT INTO users (first_name,last_name,email) VALUES (?,?,?)", (first_name, last_name, email))
    con.commit()

def get_user_id():
    user_id = input("Podaj użytkownika id: ")
    result = cur.execute("SELECT * FROM users WHERE id=?", [user_id])
    if result.fetchone() is None:
        return None
    return user_id
def get_book_id():
    book_id = input("Podaj id książki: ")
    result = cur.execute("SELECT * FROM books WHERE id=?", [book_id])
    if result.fetchone() is None:
        return None
    return book_id

is_finished = False
while not is_finished:
    print("1. Dodaj książkę")
    print("2. Dodaj użytkownika")
    print("3. Wypożycz książkę")
    print("4. Zwróć książkę")
    print("5. Stan Należności")
    print("6. Zapłata Należności")
    print("@. Zakończ program")
    match input():
        case "1":
            print("Dodaje książkę")
            title = input("title:")
            author = input("author:")
            year = input("year:")
            add_book(title, author, year)
        case "2":
            print("Dodaje użytkownika")
            first_name = input("First name:")
            last_name = input("Last name:")
            email = input("Email:")
            add_user(first_name, last_name, email)
        case "3":
            print("Wypożycz książkę")
            book_id = get_book_id()
            if  book_id is None:
                print("Brak książki")
                break
            result2 = cur.execute("SELECT * FROM rented_books WHERE finish_date IS NULL AND book_id = ?", (book_id,))
            if result2.fetchone() is not None:
                print("Ksiazka jest wypozyczona")
                break
            user_id = get_user_id()
            if not user_id:
                print("Nie ma takiego uzytkownika: ")
                break
            cur.execute("INSERT INTO rented_books (book_id,user_id,rented_date) VALUES(?,?,?)",
                        (book_id, user_id, now()))
            con.commit()
        case "4":
            book_id = get_book_id()
            if not book_id:
                print("Brak książki")
                break
            result2 = cur.execute("SELECT * FROM rented_books WHERE finish_date IS NULL AND book_id = ?", (book_id,))
            book_info = result2.fetchone()
            if book_info is None:
                print("Ksiazka jest niewypozyczona")
                break
            user_id = get_user_id()
            if user_id is None:
                print("Nie ma takiego uzytkownika: ")
                break

            # book_info[3]
            days_diff = days_between(now(), str(book_info[3]).split()[0])
            if days_diff > 30:
                cur.execute("INSERT INTO fees(user_id, fee, add_date) VALUES(?,?,?)",
                            (user_id, days_diff - 30, now()))

            cur.execute("UPDATE rented_books SET finish_date = ? WHERE user_id = ? AND finish_date IS NULL",
                        (now(), user_id))
            con.commit()

        case "5":
            print("Stan Należności")
            user_id = get_user_id()
            if not user_id:
                print("Nie ma takiego uzytkownika: ")
                break
            result5 = cur.execute("SELECT SUM(fee) FROM fees WHERE user_id=?", [user_id])
            print(result5.fetchone()[0])

        case "6":
            user_id = get_user_id()
            if not user_id:
                print("Nie ma takiego uzytkownika: ")
                break
        case "@":
            is_finished = True
        case _:
            print("Niepoprawna komenda")
