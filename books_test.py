import os
import unittest

from books import (get_input_files, rows_from_file, pipe_to_book, slash_to_book,
    csv_to_book, get_books_from_files)


class BooksTest(unittest.TestCase):

    def test_get_input_files(self):
        for file_path in get_input_files():
            self.assertTrue(os.path.isfile(file_path))

    def test_row_from_file(self):
        for (file_path, nb_lines, delimiter) in zip(get_input_files(),
                                                    [4, 3, 2], ["|", "/", ","]):
            self.assertEquals(len(list(rows_from_file(file_path, delimiter))),
                              nb_lines)

    def _assert_book_convertion(self, book, fields):
        self.assertEquals(book.first_name, fields[0])
        self.assertEquals(book.last_name, fields[1])
        self.assertEquals(book.title, fields[2])
        self.assertEquals(book.publication_date, fields[3])

    def test_pipe_convertion(self):
        fields = ["Kent", "Beck", "Test-Driven Development", "2002"]
        self._assert_book_convertion(pipe_to_book(fields), fields)

    def test_slash_convertion(self):
        slash_book = slash_to_book(["1993", "Steve", "McConnell",
                                    "Code Complete"])
        self._assert_book_convertion(slash_book, ["Steve", "McConnell",
                                                  "Code Complete", "1993"])

    def test_csv_convertion(self):
        csv_book = csv_to_book(["Clean Code", "Martin", "Robert", "2008"])
        self._assert_book_convertion(csv_book, ["Robert", "Martin",
                                                "Clean Code", "2008"])

    def test_get_books_from_files(self):
        parse_info = zip(get_input_files(), ["|", "/", ","],
                         [pipe_to_book, slash_to_book, csv_to_book])
        self.assertEquals(len(list(get_books_from_files(parse_info))), 9)


if __name__ == "__main__":
    unittest.main()

