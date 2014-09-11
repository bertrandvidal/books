""" A simple programhat reads in records from various input files and then
outputs the list with command line options to sort or filter them.
"""

import os


def get_input_files():
    """Returns the list of absolute path of the input files"""
    return [os.path.join(os.path.abspath(os.path.dirname(__file__)), "data",
                         file_name) for file_name in ["pipe", "slash", "csv"]]

