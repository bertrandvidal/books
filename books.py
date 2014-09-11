""" A simple programhat reads in records from various input files and then
outputs the list with command line options to sort or filter them.
"""

from collections import namedtuple, deque
import csv
import os


# Define the data structure we'll use to represent a book and its fields
book = namedtuple("Book", ["first_name", "last_name", "title",
                           "publication_date"])


def get_input_files():
    """Returns the list of absolute path of the input files"""
    return [os.path.join(os.path.abspath(os.path.dirname(__file__)), "data",
                         file_name) for file_name in ["pipe", "slash", "csv"]]


def rows_from_file(file_path, delimiter):
    """Yields the row in a file after parsing using the given delimiter.

    A row is an array of fields representing a book, each field have been
    stripped of whitespaces.

    Args:
        file_path -- absolute path to a file
        delimiter -- the delimiter used in the file to separate book fields
    """
    with open(file_path, "r") as input_file:
        for row in csv.reader(input_file, delimiter=delimiter):
            yield [field.strip() for field in row]


# We define a series of lambda functions to convert a row from a specific
# input_file into a book. We use the '_make' classmethod of the
# namedtuple to create an instance of book from an iterable.


# Pipe file just need to create the book instance
pipe_to_book = lambda b: book._make(b)


# Slash file requires to rotate the fields to create a book
def slash_to_book(book_fields):
    """Returns a book instance given fields read from a slash book.

    Arg:
        book_fields -- the list of fields as read from the slash file
    """
    slash_book = deque(book_fields)
    slash_book.rotate(-1)
    return book._make(slash_book)


# Csv file needs a complete reorder of the fields
csv_to_book = lambda b: book._make([b[2], b[1], b[0], b[3]])


def get_books_from_files(parse_info):
    """Yields the books parsed from the input files.

    Arg:
        parse_info -- list of 3-tuples as follow (file_path, delimiter,
                      book_converter)
    """
    for (file_path, delimiter, book_converter) in parse_info:
        for row in rows_from_file(file_path, delimiter):
            yield book_converter(row)

