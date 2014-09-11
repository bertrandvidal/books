""" A simple program that reads in records from various input files and then
outputs the list with command line options to sort or filter them.
"""

from argparse import ArgumentParser
from collections import namedtuple, deque
import csv
import os
import sys


class Book(namedtuple("Book", ["first_name", "last_name", "title",
                               "publication_date"])):
    """Represent a book with its most important fields."""

    __slots__ = ()

    def concat_fields(self):
        """Returns a string made from the concatenation of all fields."""
        return "".join(getattr(self, field) for field in self._fields)

    def __repr__(self):
        """Returns a printable version of a book."""
        return ", ".join([self.last_name, self.first_name, self.title,
                         self.publication_date])


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
pipe_to_book = lambda b: Book._make(b)


# Slash file requires to rotate the fields to create a book
def slash_to_book(book_fields):
    """Returns a book instance given fields read from a slash book.

    Arg:
        book_fields -- the list of fields as read from the slash file
    """
    slash_book = deque(book_fields)
    slash_book.rotate(-1)
    return Book._make(slash_book)


# Csv file needs a complete reorder of the fields
csv_to_book = lambda b: Book._make([b[2], b[1], b[0], b[3]])


def get_books_from_files(parse_info):
    """Yields the books parsed from the input files.

    Arg:
        parse_info -- list of 3-tuples as follow (file_path, delimiter,
                      book_converter)
    """
    for (file_path, delimiter, book_converter) in parse_info:
        for row in rows_from_file(file_path, delimiter):
            yield book_converter(row)


def filter_books(books, search_term):
    """Returns a subset of books, looks for the argument as a substring of any
    of the fields

    Note:
        Search is case sensitive

    Arg:
        books -- an iterable of book instances
        search_term -- the string used to filter book on their fields
    """
    if not search_term:
        return books
    return filter(lambda book: search_term in book.concat_fields(), books)


def sort_books(books, sort_by_publication_date=False, reverse_sort=False):
    """Returns the given list of Books sorted.

    Arg:
        books -- an iterable of book instances
        sort_by_publication_date -- define if the year should be used to sort
                                    the Books in ascending order
        reverse_sort -- define if the sorting should be reversed
    """
    cmp_key = str
    if sort_by_publication_date:
        cmp_key = lambda b: b.publication_date
    return sorted(books, key=cmp_key, reverse=reverse_sort)


def process_books(books, search_term, year, reverse_sort):
    """Returns the books according to the given parameters.

    Arg:
      books -- a book iterable
      search_term -- a string used to filter books on their fields
      year -- should the books sorted by ascending publication date
      reverse_sort -- should the sort be reversed
    """
    filtered_books = filter_books(books, search_term)
    return sort_books(filtered_books, year, reverse_sort)


if __name__ == "__main__":
    parser = ArgumentParser(description=("Show a list of books, alphabetical "
                                         "ascending by author's last name"))
    parser.add_argument("--filter", nargs=1, help=("show a subset of books, "
                                                   "looks for the argument as"
                                                   " a substring of any of the"
                                                   " fields"))
    parser.add_argument("--year", action="store_true", default=False,
                        help=("sort the books by year, ascending instead of "
                              "default sort"))
    parser.add_argument("--reverse", action="store_true", default=False,
                        help="reverse the sort")
    # We remove 'books.py' from the command line arguments
    arguments = parser.parse_args(sys.argv[1:])
    converters = [pipe_to_book, slash_to_book, csv_to_book]
    file_parse_info = zip(get_input_files(), ["|", "/", ","], converters)
    books = get_books_from_files(file_parse_info)
    search_term = arguments.filter[0] if arguments.filter else None
    books = process_books(books, search_term, arguments.year, arguments.reverse)
    print "\n".join(str(book) for book in books)

