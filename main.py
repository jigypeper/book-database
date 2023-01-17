"""
This is a book database that can be used to keep track of books in stock.
You will need python 3.10 and above.

The application uses the rich package so please install rich, otherwise
there will be errors:
'pip3 install rich'
or
'pip install rich'
see documentation for more info: https://rich.readthedocs.io/en/latest/introduction.html#
"""

# imports custom classes and rich package components, union from typing for type hints (multiple return types)
from database import BookDatabase
from books import Book
from rich.console import Console
from rich.table import Table
from typing import Union

# create console
console = Console()

# initialize database
book_stock = BookDatabase("./books.db")


# function to display menu, returns a string
def menu() -> str:
    # ask user for choice
    choice = console.input(f"""
--------------------------------------
            :books:[bold blue]BOOK MANAGER[/]
--------------------------------------
Welcome! Please choose what you want
to do (enter a number).
--------------------------------------
1. [green]Enter book[/]      :green_book:
2. [yellow]Update book[/]     :bookmark:
3. [red]Delete book[/]     :cross_mark:
4. [blue]Search books[/]    :mag_right:
5. [blue]View books[/]      :books:
0. [blue]Exit[/]            :waving_hand:
--------------------------------------
> """)

    return choice


# function to generate table layout, returns a table
def generate_table() -> Table:
    # create table object
    table = Table(title="Books Table")

    # add columns
    table.add_column("ID", justify="center", header_style="cyan", style="cyan", no_wrap=True)
    table.add_column("Title", justify="center", header_style="magenta", style="magenta")
    table.add_column("Author", justify="center", header_style="green", style="green")
    table.add_column("Quantity", justify="center", header_style="blue", style="blue")

    return table


# function to enter book into database
def enter_book():
    try:
        # ask for details, lower on book title for ease of data retrieve
        book_id = int(console.input("\nEnter the book ID:- "))
        book_title = console.input("\nEnter the book title:- ").lower()
        book_author = console.input("\nEnter the book author:- ")
        book_qty = int(console.input("\nEnter the book quantity:- "))

        # create book object
        book = Book(book_id, book_title, book_author, book_qty)

        # insert book into database
        book_stock.add_book(book)

    except ValueError:
        console.print("\n[bold red]Please make sure you enter numbers for ID and quantity![/]")


# function to update an existing book, returns a string for validation
def update_book() -> str:
    # ask for book title and search for book
    book_title, book_search_result = search_book(data_required=True)

    # check if book exists
    if book_search_result is None:
        console.print(f"\n'[bold red]{book_title}[/]' is not in the database!\n")
    else:
        # create empty dictionary to hold update requirements
        update_check = {}

        # loop through list of variables to ask for update, match on choice and add to dictionary
        for variable in ["Title", "Author", "Quantity"]:
            choice = console.input(f"Would like to update the {variable}? (y/n):- ").lower()
            match choice:
                case "y" | "n":
                    update_check[variable] = choice
                case _:
                    console.print(f"'[bold red]{choice}[/]' is not a valid option")
                    return "fail"
        try:
            # loop through update dictionary, check if update required, ask user for new data if required
            for key, value in update_check.items():
                if key == "Title" and value == "y":
                    new_book_title = console.input("\nEnter the new book title:- ").lower()
                    book_search_result.title = new_book_title

                if key == "Author" and value == "y":
                    new_author = console.input("\nEnter the new author name:- ")
                    book_search_result.author = new_author

                if key == "Quantity" and value == "y":
                    new_qty = int(console.input("\nEnter the new quantity:- "))
                    book_search_result.qty = new_qty

            # update the book record and return string for validation
            book_stock.add_book(book_search_result, update=True)
            return "done"
        except ValueError:
            console.print("\n[bold red]Please make sure you enter a number for the quantity![/]")
            return "fail"


# function to delete a book
def delete_book():
    # ask for book title and search for book
    book_title, book_search_result = search_book(data_required=True)

    # check if book exists, delete if it does
    if book_search_result is None:
        console.print(f"\n'[bold red]{book_title}[/]' is not in the database!\n")
    else:
        book_stock.delete_book(book_search_result)
        console.print(f"\n'[bold]{book_title}[/]' has been\nsuccessfully deleted from the database!\n")


# function to search for books, returns a tuple if data required
def search_book(data_required: bool = False) -> Union[tuple, None]:
    # ask for book title and search for book
    book_title = console.input("\nEnter the book title:- ").lower()
    search_result = book_stock.search_books(book_title)

    # return data if required
    if data_required:
        return book_title, search_result

    # check book exists, display table if it exists
    if search_result is None:
        console.print(f"\n'[bold red]{book_title}[/]' is not in the database!\n")
    else:
        search_table = generate_table()
        search_table.add_row(
            str(search_result.id),
            search_result.title,
            search_result.author,
            str(search_result.qty)
        )

        console.print(search_table)


# function to display books
def view_books():
    # get book objects from database
    book_object_data = book_stock.get_data()

    # make table
    books_table = generate_table()

    # add data to table and display, will be empty if no data in database
    for book_object in book_object_data:
        books_table.add_row(str(book_object.id), book_object.title, book_object.author, str(book_object.qty))

    console.print(books_table)


# loop until user exits with '0'
while True:
    # display menu and ask for choice
    user_choice = menu()

    # match on the choice
    match user_choice:
        case "1":
            enter_book()
        case "2":
            # check status and display message if failed
            status = update_book()
            if status == "fail":
                console.print("Please try again!\n")
        case "3":
            delete_book()
        case "4":
            search_book()
        case "5":
            view_books()
        case "0":
            console.print("\n[bold]Goodbye![/] :waving_hand:\n")
            quit()
        case _:
            console.print(f"\n'{user_choice}' is [bold underline]not[/] a valid option\nplease enter a number (0-5)\n")
