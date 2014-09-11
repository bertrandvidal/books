import os
import unittest

from books import get_input_files, rows_from_file


class BooksTest(unittest.TestCase):

    def test_get_input_files(self):
        for file_path in get_input_files():
            self.assertTrue(os.path.isfile(file_path))

    def test_row_from_file(self):
        for (file_path, nb_lines, delimiter) in zip(get_input_files(),
                                                    [4, 3, 2], ["|", "/", ","]):
            self.assertEquals(len(list(rows_from_file(file_path, delimiter))),
                              nb_lines)

if __name__ == "__main__":
    unittest.main()

