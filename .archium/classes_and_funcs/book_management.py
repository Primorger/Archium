import tkinter as tk
from tkinter import messagebox, ttk

from .book import Book


class BookManagementMixin:
    def edit_selected_book(self):
        """Edit the selected book."""
        book = self.get_selected_book()
        if not book:
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title(self._("edit_book"))
        edit_window.geometry("400x500")
        edit_window.transient(self.root)
        edit_window.grab_set()

        fields = {}
        values = {
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "year": book.year,
            "length": book.length,
            "country": book.country,
            "place": book.place,
            "notes": book.notes,
        }
        entry_list = []

        for index, (field, value) in enumerate(values.items()):
            label = (
                self._("notes")
                if field == "notes"
                else self._(f"column_{field}")
            )
            ttk.Label(edit_window, text=f"{label}:").grid(
                row=index, column=0, sticky=tk.W, padx=10, pady=5
            )
            if field == "notes":
                entry = tk.Text(
                    edit_window, width=30, height=8, wrap=tk.WORD
                )
                entry.insert("1.0", str(value))
            else:
                entry = ttk.Entry(edit_window, width=30)
                entry.insert(0, str(value))
            entry.grid(row=index, column=1, padx=10, pady=5)
            fields[field] = entry
            entry_list.append(entry)
            self.bind_clipboard_shortcuts(entry)
            self.bind_clipboard_menu(entry)

        def save_changes():
            try:
                book.edit_book(
                    title=fields["title"].get() or None,
                    author=fields["author"].get() or None,
                    genre=fields["genre"].get() or None,
                    year=fields["year"].get() or "N/A",
                    length=fields["length"].get() or "N/A",
                    country=fields["country"].get() or None,
                    place=fields["place"].get() or None,
                    notes=fields["notes"].get("1.0", "end-1c"),
                )
                self.save_library_to_file(self.current_library)
                messagebox.showinfo(
                    self._("success"), self._("book_updated")
                )
                edit_window.destroy()
                self.refresh_display()
            except (OSError, ValueError) as error:
                messagebox.showerror(
                    self._("error"), f"{self._('error')}: {error}"
                )

        self.add_book_context = {
            "entry_list": entry_list,
            "save_book": save_changes,
        }
        for index, entry in enumerate(entry_list):
            if not isinstance(entry, tk.Text):
                entry.bind(
                    "<Return>",
                    lambda event, field_index=index: self.on_add_book_enter(
                        event, field_index
                    ),
                )

        ttk.Button(
            edit_window, text=self._("confirm"), command=save_changes
        ).grid(
            row=len(values), column=0, columnspan=2, pady=10
        )

    def move_selected_book(self):
        """Move the selected book to another library."""
        book = self.get_selected_book()
        if not book:
            return

        other_libraries = [
            name for name in self.libraries if name != self.current_library
        ]
        if not other_libraries:
            messagebox.showwarning(
                self._("warning"), self._("no_other_libraries")
            )
            return

        select_window = tk.Toplevel(self.root)
        select_window.title(self._("move_book"))
        select_window.geometry("300x200")
        select_window.transient(self.root)
        select_window.grab_set()

        ttk.Label(
            select_window, text=self._("select_destination")
        ).pack(pady=10)
        library_listbox = tk.Listbox(select_window, height=10)
        library_listbox.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=5
        )
        for library_name in other_libraries:
            library_listbox.insert(tk.END, library_name)

        def move_book():
            selection = library_listbox.curselection()
            if not selection:
                messagebox.showwarning(
                    self._("warning"), self._("no_book_selected")
                )
                return

            destination = library_listbox.get(selection[0])
            self.libraries[self.current_library].remove_book(book)
            self.libraries[destination].add_book(book)
            self.save_library_to_file(self.current_library)
            self.save_library_to_file(destination)
            messagebox.showinfo(
                self._("success"),
                f"{self._('book_moved')} {destination}",
            )
            select_window.destroy()
            self.refresh_display()

        library_listbox.bind(
            "<Double-Button-1>", lambda event: move_book()
        )

    def delete_selected_book(self):
        """Delete the selected book."""
        book = self.get_selected_book()
        if not book:
            return

        if messagebox.askyesno(
            self._("confirm_delete"), f"Delete '{book.title}'?"
        ):
            self.libraries[self.current_library].remove_book(book)
            self.save_library_to_file(self.current_library)
            messagebox.showinfo(
                self._("success"), self._("book_deleted")
            )
            self.refresh_display()

    def add_book(self):
        """Open the dialog to add a book."""
        if not self.current_library:
            messagebox.showwarning(
                self._("warning"), self._("no_library_selected")
            )
            return

        add_window = tk.Toplevel(self.root)
        add_window.title(self._("add_book"))
        add_window.geometry("400x500")
        add_window.transient(self.root)
        add_window.grab_set()

        fields = {}
        default_values = {
            "title": "",
            "author": "",
            "genre": "",
            "year": "",
            "length": "",
            "country": "",
            "place": "",
            "notes": "",
        }
        entry_list = []

        for index, (field, default) in enumerate(default_values.items()):
            label = (
                self._("notes")
                if field == "notes"
                else self._(f"column_{field}")
            )
            ttk.Label(add_window, text=f"{label}:").grid(
                row=index, column=0, sticky=tk.W, padx=10, pady=5
            )
            if field == "notes":
                entry = tk.Text(
                    add_window, width=30, height=8, wrap=tk.WORD
                )
                entry.insert("1.0", default)
            else:
                entry = ttk.Entry(add_window, width=30)
                entry.insert(0, default)
            entry.grid(row=index, column=1, padx=10, pady=5)
            fields[field] = entry
            entry_list.append(entry)
            self.bind_clipboard_shortcuts(entry)
            self.bind_clipboard_menu(entry)

        def save_book():
            try:
                book = Book(
                    title=fields["title"].get() or "N/A",
                    author=fields["author"].get() or "N/A",
                    genre=fields["genre"].get() or "N/A",
                    year=fields["year"].get() or "N/A",
                    length=fields["length"].get() or "N/A",
                    country=fields["country"].get() or "N/A",
                    place=fields["place"].get() or "N/A",
                    notes=fields["notes"].get("1.0", "end-1c"),
                )
                library = self.libraries[self.current_library]
                library.add_book(book)
                self.save_library_to_file(self.current_library)
                messagebox.showinfo(
                    self._("success"), self._("book_added")
                )
                add_window.destroy()
                self.refresh_display()
            except (OSError, ValueError) as error:
                messagebox.showerror(
                    self._("error"), f"Failed to add book: {error}"
                )

        self.add_book_context = {
            "entry_list": entry_list,
            "save_book": save_book,
        }
        for index, entry in enumerate(entry_list):
            if not isinstance(entry, tk.Text):
                entry.bind(
                    "<Return>",
                    lambda event, field_index=index: self.on_add_book_enter(
                        event, field_index
                    ),
                )

        ttk.Button(
            add_window, text=self._("confirm"), command=save_book
        ).grid(
            row=len(default_values), column=0, columnspan=2, pady=10
        )

    def on_add_book_enter(self, event, field_index):
        """Move to the next empty field or save when all are filled."""
        entry_list = self.add_book_context["entry_list"]
        save_book = self.add_book_context["save_book"]
        input_fields = [
            entry for entry in entry_list if not isinstance(entry, tk.Text)
        ]

        if all(self.get_input_value(entry).strip() for entry in input_fields):
            save_book()
        else:
            for entry in input_fields[field_index + 1 :]:
                if not self.get_input_value(entry).strip():
                    entry.focus()
                    return "break"
            for entry in input_fields:
                if not self.get_input_value(entry).strip():
                    entry.focus()
                    return "break"

        return "break"
