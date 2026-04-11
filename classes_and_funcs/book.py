class Book:
    def __init__(self, title = "N/A", author = "N/A", genre = "N/A", year = "N/A", length = "N/A", country = "N/A", place = "N/A") -> None:
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.length = length
        self.country = country
        self.place = place
    
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, value) -> None:
        if value is not None:
            try:
                int(value)
            except ValueError:
                raise ValueError("Year must be a valid integer")
            self._year = int(value)
        else:
            self._year = "N/A"
            
    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value) -> None:
        if value is not None:
            try:
                int(value)
            except ValueError:
                raise ValueError("Length must be a valid integer")
            self._length = int(value)
        else:
            self._length = "N/A"
            
    def _set_attribute(self, attr_name, value):
        if value is not None:
            setattr(self, attr_name, value)
        
    def edit_book(self, title = "N/A", author = "N/A", genre = "N/A", year = "N/A", length = "N/A", country = "N/A", place = "N/A"):
        self._set_attribute('title', title)
        self._set_attribute('author', author)
        self._set_attribute('genre', genre)
        self._set_attribute('year', year)
        self._set_attribute('length', length)
        self._set_attribute('country', country)
        self._set_attribute('place', place)

    def __str__(self) -> str:
        return " | ".join([self.title, self.author, self.genre, str(self.year), str(self.length), self.country, self.place])