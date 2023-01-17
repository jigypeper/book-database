"""
This module contains the database class and methods.
All database methods in this class follow the same procedure:

open connection -> create cursor -> run command -> commit -> close database

This has been done to avoid blocking the database.
using the 'with' operator was considered, but closing the database explicitly is safer
"""

# import sqlite 3 and union for return type hints. custom class Book for access to instance variables
import sqlite3
from typing import Union
from books import Book
from os import path


# define class for database methods
class BookDatabase:
    # class variable for initializing
    initial_data: list = [
        (3001, "a tale of two cities", "Charles Dickens", 30),
        (3002, "harry potter and the philosopher's stone", "J.K. Rowling", 40),
        (3003, "the lion the witch and the wardrobe", "C.S. Lewis", 25),
        (3004, "the lord of the rings", "J.R.R. Tolkien", 37),
        (3005, "alice in wonderland", "Lewis Carrol", 12)
    ]

    # initialize with a database and data
    def __init__(self, database: str):
        # try to establish connection
        # create table if it doesn't exist, raise error otherwise, close database
        self.database = database

        # check db file exists
        # declare variable for checking if data needs initializing (for demo and testing)
        check: list = []
        if path.exists("./books.db"):
            check = self.get_data()

        try:
            # connect to database and create cursor
            self.db = sqlite3.connect(self.database)
            self.cursor = self.db.cursor()
            self.cursor.execute(
                """ CREATE TABLE IF NOT EXISTS books (
                                        id integer PRIMARY KEY UNIQUE NOT NULL,
                                        title text,
                                        author text,
                                        qty integer
                                    )"""
                )

            # initialize with data if the table is empty (for demo and testing)
            if len(check) == 0:
                self.cursor.executemany(
                    """INSERT OR REPLACE INTO books
                        VALUES (?, ?, ?, ?)""", BookDatabase.initial_data
                )

            # save changes
            self.db.commit()
        except Exception as error:
            # undo changes if error, raise error
            self.db.rollback()
            raise error

        finally:
            # close to stop blocking
            self.db.close()

    # method to get book data and return list of book objects
    def get_data(self) -> list:
        """
        Get data from database
        :return:
        """
        # declare list for storing books
        books_list: list = []

        # get list of data
        try:
            # connect to database and create cursor, execute command
            self.db = sqlite3.connect(self.database)
            self.cursor = self.db.cursor()
            raw_data = self.cursor.execute(
                """SELECT * FROM books"""
            ).fetchall()

            # loop through list and create book objects from data, append to books_list and return
            for row in raw_data:
                book_object = Book(row[0], row[1], row[2], row[3])

                books_list.append(book_object)

            return books_list

        except Exception as error:
            raise error

        finally:
            self.db.close()

    # method to add book or update a book
    def add_book(self, book: Book, update: bool = False):
        """
        Add or update a new book to the database.
        If the book already exists, update any values.
        If the book does not exist, create a new entry
        :param book:
        :param update:
        :return:
        """

        try:
            # connect to database and create cursor
            self.db = sqlite3.connect(self.database)
            self.cursor = self.db.cursor()

            # check book exists
            exists = self.cursor.execute(
                """SELECT * FROM books WHERE title=?""", (book.title,)
            ).fetchone()

            # update if exists
            if exists is not None and not update:
                # increment quantity, execute command
                book.qty += exists[3]

                self.cursor.execute(
                    "UPDATE books SET qty = ? WHERE id = ?",
                    (
                        book.qty,
                        book.id,
                    ),
                )
                self.db.commit()
            else:
                # insert if it doesn't exist, will also replace for update tasks
                self.cursor.execute(
                    """INSERT or REPLACE INTO books (id, title, author, qty)
                                                    VALUES (?, ?, ?, ?)""",
                    (
                        book.id,
                        book.title,
                        book.author,
                        book.qty,
                    ),
                )
                self.db.commit()
        except Exception as error:
            # rollback changes if error, and raise error
            self.db.rollback()
            raise error

        finally:
            self.db.close()

    # method to get books, returns a book or None
    def search_books(self, book_title: str) -> Union[Book, None]:
        """
        search for a book by title
        :param book_title:
        :return:
        """
        # get list of book objects from database
        try:
            book_obj_list = self.get_data()

            # count variable for search validation
            count = 0

            # loop through book objects and return the book object if title is present
            # increment the count variable
            for book_obj in book_obj_list:
                if book_obj.title == book_title:
                    return book_obj
                count += 1
        
        except Exception as error:
            raise error
        finally:
            self.db.close()

            # if count and length of book objects list are equal, book was not found, return none
            if count == len(book_obj_list):
                return None

    # method to delete a book
    def delete_book(self, book: Book):
        """
        Delete a book from the database.
        :param book:
        :return:
        """
        
        try:
            # connect to database and create cursor, execute command
            self.db = sqlite3.connect(self.database)
            self.cursor = self.db.cursor()

            # check book exists
            exists = self.cursor.execute(
                """SELECT * FROM books WHERE id = ?""", (book.id,)
            ).fetchone()

            # delete book if it exists
            if exists is not None:
                self.cursor.execute(
                    """DELETE FROM books WHERE id = ?""",
                    (book.id,)
                )
                self.db.commit()

        except Exception as error:
            # rollback changes if error, and raise error
            self.db.rollback()
            raise error

        finally:
            self.db.close()
