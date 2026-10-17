from classes_and_funcs.book import Book
from unicodedata import normalize

BOOK_ATTRIBUTES = ("title", "author", "genre", "year", "length", "country", "place")


class Library:
    def __init__(self, name):
        self.name = name
        self.books: list[Book] = []
        
    def add_book(self, book: Book):
        if str(book).lower() not in [str(b).lower() for b in self.books]:
            self.books.append(book)
        
    def remove_book(self, book: Book):
        if book in self.books:
            self.books.remove(book)
            
    def search(self, query: str, attribute: str = "title") -> list[Book]:
        if attribute not in BOOK_ATTRIBUTES:
            raise ValueError(f"Attribute '{attribute}' does not exist in Book class")

        normalized_query = normalize('NFD', query).casefold()

        def searchable_value(book):
            return normalize('NFD', str(getattr(book, attribute))).casefold()

        def relevance_score(book):
            value = searchable_value(book)
            position = value.find(normalized_query)
            count = value.count(normalized_query)
            return (-position, count)

        matches = [
            book for book in self.books
            if normalized_query in searchable_value(book)
        ]
        return sorted(matches, key=relevance_score, reverse=True)
            
    def sort_by_attribute(self, attribute: str, reverse=False) -> list[Book]:
        if not self.books:
            return []
        if attribute not in BOOK_ATTRIBUTES:
            raise ValueError(f"Attribute '{attribute}' does not exist in Book class")
        # Sorting helper function
        def sort_key(book):
            value = getattr(book, attribute)
            if value == "N/A":
                return (True, 0)
            if isinstance(value, str):
                return (False, normalize('NFD', value).casefold())
            return (False, value)
        
        return sorted(self.books, key=sort_key, reverse=reverse)