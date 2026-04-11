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
            
    def search(self, query: str) -> list[Book]:
        query = normalize('NFD', query).casefold()
        
        def relevance_score(book):
            normalized_book = normalize('NFD', str(book)).casefold()
            if query not in normalized_book:
                return (0, 0, 0)
            
            position = normalized_book.find(query)
            count = normalized_book.count(query)
            return (1, -position, count)
        
        return sorted(self.books, key=relevance_score, reverse=True)
            
    def sort_by_attribute(self, attribute: str, reverse=False) -> list[Book]:
        if not self.books:
            return []
        if not hasattr(self.books[0], attribute):
            raise ValueError(f"Attribute '{attribute}' does not exist in Book class")
        # Sorting helper function
        def sort_key(book):
            value = getattr(book, attribute)
            if isinstance(value, str):
                return normalize('NFD', value).casefold()
            return value
        
        return sorted(self.books, key=sort_key, reverse=reverse)