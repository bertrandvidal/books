import os
import random
import unittest

from books import (get_input_files, rows_from_file, pipe_to_book, slash_to_book,
                   csv_to_book, get_books_from_files, Book, filter_books,
                   sort_books, process_books)


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

    def test_book_concat_fields(self):
        book = pipe_to_book(["Kent", "Beck", "Test-Driven Development", "2002"])
        self.assertEquals(book.concat_fields(),
                          "KentBeckTest-Driven Development2002")

    def test_filter_books(self):
        slash_book = slash_to_book(["1993", "Steve", "McConnell",
                                    "Code Complete"])
        csv_book = csv_to_book(["Clean Code", "Martin", "Robert", "2008"])
        self.assertEquals(filter_books([slash_book, csv_book], "20"),
                          [csv_book])
        self.assertEquals(filter_books([slash_book, csv_book], "ode"),
                          [slash_book, csv_book])
        self.assertEquals(filter_books([slash_book, csv_book], None),
                          [slash_book, csv_book])

    def test_book_repr(self):
        slash_book = slash_to_book(["2002", "Martin", "Fowler",
                                    "Patterns of Enterprise Application Architecture"])
        self.assertEquals(str(slash_book), "Fowler, Martin, Patterns of Enterprise Application Architecture, 2002")

    def test_sort_books(self):
        slash_book = slash_to_book(["1993", "Steve", "McConnell",
                                    "Code Complete"])
        csv_book = csv_to_book(["Clean Code", "Martin", "Robert", "2008"])
        kent_book_1 = pipe_to_book(["Kent", "Beck", "Test-Driven Development",
                                    "2002"])
        kent_book_2 = pipe_to_book(["Kent", "Beck", "Implementation Patterns",
                                   "2007"])
        books = [slash_book, kent_book_1, kent_book_2, csv_book]
        random.shuffle(books)
        self.assertEquals(sort_books(books), [kent_book_2, kent_book_1,
                                              csv_book, slash_book])
        self.assertEquals(sort_books(books, True), [slash_book, kent_book_1,
                                                    kent_book_2,csv_book])
        self.assertEquals(sort_books(books, True, True), [csv_book,
                                                          kent_book_2,
                                                          kent_book_1,
                                                          slash_book])

    def test_process_books(self):
        converters = [pipe_to_book, slash_to_book, csv_to_book]
        file_parse_info = zip(get_input_files(), ["|", "/", ","], converters)
        books = get_books_from_files(file_parse_info)
        self.assertEquals(len(process_books(books, "", False, False)), 9)
        books = get_books_from_files(file_parse_info)
        self.assertEquals(process_books(books, None, False, False)[0],
                          Book("Kent", "Beck", "Implementation Patterns",
                               "2007"))
        books = get_books_from_files(file_parse_info)
        self.assertEquals(process_books(books, None, False, True)[-1],
                          Book("Kent", "Beck", "Implementation Patterns",
                               "2007"))
        books = get_books_from_files(file_parse_info)
        self.assertEquals(process_books(books, None, True, False)[0],
                          Book("Fred", "Brooks", "The Mythical Man-Month",
                               "1975"))



if __name__ == "__main__":
    unittest.main()

