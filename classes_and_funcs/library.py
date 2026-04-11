from classes_and_funcs.book import Book
from unicodedata import normalize

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
            
    @staticmethod
    def sort_by_attribute(books: list[Book], attribute: str, reverse=False) -> list[Book]:
        if not books:
            return []
        if not hasattr(books[0], attribute):
            raise ValueError(f"Attribute '{attribute}' does not exist in Book class")
        # Sortiing helper function
        def sort_key(book):
            value = getattr(book, attribute)
            if isinstance(value, str):
                return normalize('NFD', value).casefold()
            return value
        
        return sorted(books, key=sort_key, reverse=reverse)