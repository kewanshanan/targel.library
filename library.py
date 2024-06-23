import sqlite3
import datetime
from book import Book  # Assuming Book class is defined in book.py

class Library:
    def __init__(self, db_path='library.db'):
        self.db_path = db_path
        self.create_tables()
        self.load_library()

    def create_tables(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS books
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      author TEXT NOT NULL,
                      publication_year INTEGER NOT NULL,
                      genre TEXT NOT NULL,
                      last_updated TEXT)''')
        conn.commit()
        conn.close()

    def load_library(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM books')
        rows = c.fetchall()
        self.books = [Book(row[1], row[2], row[3], row[4], row[5]) for row in rows]
        conn.close()

    def save_library(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM books')
        for book in self.books:
            c.execute('INSERT INTO books (title, author, publication_year, genre, last_updated) VALUES (?, ?, ?, ?, ?)',
                      (book.title, book.author, book.publication_year, book.genre, str(book.last_updated)))
        conn.commit()
        conn.close()

    def add_book(self, book):
        if not self.book_exists(book.title, book.author):
            self.books.append(book)
            self.save_library()
            print("Book added successfully.")
            self.print_library()
        else:
            print(f"Book '{book.title}' by {book.author} already exists in the library. Cannot add.")

    def edit_book(self, index, title=None, author=None, publication_year=None, genre=None):
        if 0 <= index < len(self.books):
            self.books[index].title = title or self.books[index].title
            self.books[index].author = author or self.books[index].author
            self.books[index].publication_year = publication_year or self.books[index].publication_year
            self.books[index].genre = genre or self.books[index].genre
            self.books[index].last_updated = datetime.datetime.now().replace(microsecond=0)
            self.save_library()
            print("Book edited successfully.")
            self.print_library()
        else:
            print("Invalid book index.")

    def delete_book(self, index):
        if 0 <= index < len(self.books):
            del self.books[index]
            self.save_library()
            print("Book deleted successfully.")
            self.print_library()
        else:
            print("Invalid book index.")

    def print_library(self):
        if self.books:
            print("\nCurrent Library:")
            for i, book in enumerate(self.books):
                print(f"{i}. {book}")
        else:
            print("\nThe library is empty.")

    def list_books(self):
        return self.books

    def book_exists(self, title, author):
        for existing_book in self.books:
            if existing_book.title == title and existing_book.author == author:
                return True
        return False

    def save_and_exit(self):
        self.save_library()
        print("Library saved. Exiting...")
        self.print_library()

    def filter_books(self, author=None, genre=None):
        filtered_books = self.books[:]
        if author:
            filtered_books = [book for book in filtered_books if book.author == author]
        if genre:
            filtered_books = [book for book in filtered_books if book.genre == genre]
        return filtered_books
