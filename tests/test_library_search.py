import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[1] / ".archium"))

from classes_and_funcs.book import Book
from classes_and_funcs.library import Library


class LibrarySearchTests(unittest.TestCase):
    def setUp(self):
        self.library = Library("test")
        self.title_match = Book(title="Author's Journey", author="Other Writer", year=2000, length=300)
        self.author_match = Book(title="Different Title", author="Author Name", year=2001, length=250)
        self.library.books.extend((self.title_match, self.author_match))

    def test_search_uses_selected_attribute(self):
        self.assertEqual(self.library.search("author", "title"), [self.title_match])
        self.assertEqual(self.library.search("author", "author"), [self.author_match])
        self.assertEqual(self.library.search("writer", "author"), [self.title_match])

    def test_search_is_case_insensitive(self):
        self.assertEqual(self.library.search("AUTHOR", "author"), [self.author_match])

    def test_year_and_length_can_be_blank_and_sort_after_numbers(self):
        book_without_details = Book(title="No Details", year="", length="")
        self.assertEqual(book_without_details.year, "N/A")
        self.assertEqual(book_without_details.length, "N/A")
        self.library.books.append(book_without_details)

        self.assertEqual(
            self.library.sort_by_attribute("year"),
            [self.title_match, self.author_match, book_without_details],
        )
        self.assertEqual(
            self.library.sort_by_attribute("length"),
            [self.author_match, self.title_match, book_without_details],
        )

    def test_notes_round_trip_without_becoming_searchable(self):
        book = Book(title="Book", notes="private note\nwith | separator")
        serialized = str(book)
        stored_notes = serialized.split("|")[7].strip()

        self.assertNotIn("\n", serialized)
        self.assertEqual(Book.decode_notes(stored_notes), book.notes)
        with self.assertRaises(ValueError):
            self.library.search("private", "notes")
        with self.assertRaises(ValueError):
            self.library.sort_by_attribute("notes")


if __name__ == "__main__":
    unittest.main()
