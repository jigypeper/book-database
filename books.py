"""
This module contains the book class and is the data structure for book objects
"""


class Book:
    # initialize with book details
    def __init__(self, id: int, title: str, author: str, qty: int):
        self.id = id
        self.title = title
        self.author = author
        self.qty = qty

    # string method for debugging
    def __str__(self) -> str:

        return f"""
        Book Object
        ---------------------------------------------
        ID:         {self.id}
        Title:      {self.title}
        Author:     {self.author}
        QTY:        {self.qty}
        ---------------------------------------------
        """
