import tkinter as tk
from tkinter import messagebox, simpledialog

from .book import Book
from .library import Library


class LibraryManagementMixin:
    def load_libraries(self):
        """Load all libraries from the database folder."""
        self.library_listbox.delete(0, tk.END)
        self.libraries.clear()

        for file_path in self.db_path.glob("*.txt"):
            library_name = file_path.stem
            self.libraries[library_name] = self.load_library_from_file(
                library_name
            )
            self.library_listbox.insert(tk.END, library_name)

    def load_library_from_file(self, library_name):
        """Load a library from its text file."""
        library = Library(library_name)
        file_path = self.db_path / f"{library_name}.txt"

        if file_path.exists():
            with file_path.open("r", encoding="utf-8") as library_file:
                for line in library_file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split("|")
                    if len(parts) < 7:
                        continue

                    try:
                        book = Book(
                            title=parts[0].strip(),
                            author=parts[1].strip(),
                            genre=parts[2].strip(),
                            year=parts[3].strip(),
                            length=parts[4].strip(),
                            country=parts[5].strip(),
                            place=parts[6].strip(),
                            notes=(
                                Book.decode_notes(parts[7].strip())
                                if len(parts) > 7
                                else ""
                            ),
                        )
                        library.add_book(book)
                    except (ValueError, TypeError, IndexError) as error:
                        print(f"Error loading book: {error}")

        return library

    def save_library_to_file(self, library_name):
        """Save a library to its text file."""
        if library_name not in self.libraries:
            return

        file_path = self.db_path / f"{library_name}.txt"
        library = self.libraries[library_name]
        with file_path.open("w", encoding="utf-8") as library_file:
            for book in library.books:
                library_file.write(str(book) + "\n")

    def load_selected_library(self, event=None):
        """Load the selected library into the main view."""
        selection = self.library_listbox.curselection()
        if not selection:
            return

        library_name = self.library_listbox.get(selection[0])
        self.current_library = library_name
        self.library_label.config(
            text=f"{self._('library')}: {library_name}"
        )
        self.search_query.delete(0, tk.END)
        self.search()

    def create_new_library(self):
        """Create a new library."""
        library_name = simpledialog.askstring(
            self._("new_library"), "Enter library name:"
        )
        if not library_name:
            return

        if library_name in self.libraries:
            messagebox.showwarning(
                self._("warning"), "Library already exists"
            )
            return

        self.libraries[library_name] = Library(library_name)
        self.save_library_to_file(library_name)
        self.load_libraries()
        messagebox.showinfo(
            self._("success"), f"Library '{library_name}' created!"
        )

    def delete_library(self):
        """Delete the selected library."""
        selection = self.library_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                self._("warning"), self._("no_library_selected")
            )
            return

        library_name = self.library_listbox.get(selection[0])
        if not messagebox.askyesno(
            self._("confirm_delete"),
            f"Delete library '{library_name}'?",
        ):
            return

        file_path = self.db_path / f"{library_name}.txt"
        file_path.unlink(missing_ok=True)

        if library_name in self.libraries:
            del self.libraries[library_name]

        if self.current_library == library_name:
            self.current_library = None
            self.library_label.config(text=self._("no_library_selected"))
            self.clear_results()

        self.load_libraries()
        messagebox.showinfo(
            self._("success"), f"Library '{library_name}' deleted!"
        )
