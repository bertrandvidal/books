""" A simple programhat reads in records from various input files and then
outputs the list with command line options to sort or filter them.
"""

from collections import namedtuple
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


