import os
import unittest

from books import get_input_files


class BooksTest(unittest.TestCase):

    def test_get_input_files(self):
        for file_path in get_input_files():
            self.assertTrue(os.path.isfile(file_path))


if __name__ == "__main__":
    unittest.main()

