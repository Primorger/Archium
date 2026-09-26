import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog, font as tkfont
from pathlib import Path
import os
import json
from classes_and_funcs.library import Library
from classes_and_funcs.book import Book


with (Path(__file__).parent / "languages.json").open(encoding="utf-8") as language_file:
    LANGUAGES = json.load(language_file)


class ArchiumApp:
    def __init__(self, root):
        self.root = root

        app_dir = Path(__file__).resolve().parent
        self.db_path = app_dir / "db"
        self.db_path.mkdir(exist_ok=True)

        self.settings_path = app_dir / "settings"
        self.settings_path.mkdir(exist_ok=True)
        self.settings_file = self.settings_path / "settings.json"
        
        self.current_library = None
        self.libraries = {}  # name -> Library object
        
        # Load settings
        self.settings = self.load_settings()
        self.language = self.settings.get('language', 'en')
        if self.language not in LANGUAGES:
            self.language = 'en'
        self.ui_font_size = self.settings.get('ui_font_size', 10)
        
        self.root.title(LANGUAGES[self.language]['title'])
        self.root.geometry("1200x700")
        
        # Create UI
        self.create_widgets()
        self.load_libraries()
    
    def load_settings(self):
        """Load settings from JSON file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'language': 'en', 'ui_font_size': 10, 'results_text_size': 10}
        return {'language': 'en', 'ui_font_size': 10, 'results_text_size': 10}
    
    def save_settings(self):
        """Save settings to JSON file"""
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)
    
    def _(self, key: str) -> str:
        """Get translated string"""
        result = LANGUAGES.get(self.language, {}).get(key)
        return result if result is not None else key
        
    def create_widgets(self):
        """Create the main UI layout"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left sidebar for library management
        left_frame = ttk.LabelFrame(main_frame, text=self._('libraries'), width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        
        # Library listbox
        scrollbar = ttk.Scrollbar(left_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.library_listbox = tk.Listbox(left_frame, yscrollcommand=scrollbar.set, height=15)
        self.library_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.library_listbox.yview)
        self.library_listbox.bind('<Double-Button-1>', self.load_selected_library)
        
        # Buttons for library management
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text=self._('new_library'), command=self.create_new_library).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text=self._('delete_library'), command=self.delete_library).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text=self._('settings'), command=self.open_settings).pack(fill=tk.X, pady=2)
        
        # Right side - main content
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Library title
        self.library_label = ttk.Label(right_frame, text=self._('no_library_selected'), font=("Arial", 14, "bold"))
        self.library_label.pack(pady=5)
        
        # Search frame
        search_frame = ttk.LabelFrame(right_frame, text=self._('search'), padding=5)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Search box
        ttk.Label(search_frame, text=self._('search')+":").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.search_query = ttk.Entry(search_frame, width=30)
        self.search_query.grid(row=0, column=1, padx=5, sticky=tk.EW)
        self.search_query.bind('<Return>', self.on_search_enter)
        
        # Sort options
        ttk.Label(search_frame, text=self._('sort_by')+":").grid(row=0, column=2, sticky=tk.W, padx=20)
        self.sort_var = tk.StringVar(value="title")
        self.sort_var.trace('w', lambda *args: self.refresh_display())
        sort_combo = ttk.Combobox(search_frame, textvariable=self.sort_var, 
                                  values=["title", "author", "genre", "year", "length", "country", "place"], state="readonly", width=15)
        sort_combo.grid(row=0, column=3, padx=5)
        
        search_frame.columnconfigure(1, weight=1)
        
        # Results frame
        results_frame = ttk.LabelFrame(right_frame, text=self._('results'), padding=5)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for results with scrollbars
        tree_scroll_y = ttk.Scrollbar(results_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.results_tree = ttk.Treeview(results_frame,
                                         columns=("Title", "Author", "Genre", "Year", "Length", "Country", "Place"),
                                         yscrollcommand=tree_scroll_y.set,
                                         xscrollcommand=tree_scroll_x.set,
                                         height=12)
        tree_scroll_y.config(command=self.results_tree.yview)
        tree_scroll_x.config(command=self.results_tree.xview)
        
        # Create a custom font for the tree
        self.tree_font = tkfont.Font(family="TkDefaultFont", size=self.settings.get('results_text_size', 10))
        self.results_tree.tag_configure('default', font=self.tree_font)
        
        # Configure columns
        self.results_tree.column("#0", width=0, stretch=tk.NO)
        self.results_tree.column("Title", anchor=tk.W, width=100)
        self.results_tree.column("Author", anchor=tk.W, width=90)
        self.results_tree.column("Genre", anchor=tk.W, width=70)
        self.results_tree.column("Year", anchor=tk.CENTER, width=50)
        self.results_tree.column("Length", anchor=tk.CENTER, width=50)
        self.results_tree.column("Country", anchor=tk.W, width=70)
        self.results_tree.column("Place", anchor=tk.W, width=70)
        
        # Configure headings
        self.results_tree.heading("#0", text="", anchor=tk.W)
        self.results_tree.heading("Title", text=self._('column_title'), anchor=tk.W)
        self.results_tree.heading("Author", text=self._('column_author'), anchor=tk.W)
        self.results_tree.heading("Genre", text=self._('column_genre'), anchor=tk.W)
        self.results_tree.heading("Year", text=self._('column_year'), anchor=tk.CENTER)
        self.results_tree.heading("Length", text=self._('column_length'), anchor=tk.CENTER)
        self.results_tree.heading("Country", text=self._('column_country'), anchor=tk.W)
        self.results_tree.heading("Place", text=self._('column_place'), anchor=tk.W)
        
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        self.current_results = []  # Store book objects
        
        # Action buttons frame
        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(action_frame, text=self._('add_book'), command=self.add_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=self._('edit_book'), command=self.edit_selected_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=self._('move_book'), command=self.move_selected_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=self._('delete_book'), command=self.delete_selected_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=self._('clear_results'), command=self.clear_results).pack(side=tk.LEFT, padx=5)
        
    def load_libraries(self):
        """Load all libraries from db folder"""
        self.library_listbox.delete(0, tk.END)
        self.libraries.clear()
        
        for file in self.db_path.glob("*.txt"):
            lib_name = file.stem
            self.libraries[lib_name] = self.load_library_from_file(lib_name)
            self.library_listbox.insert(tk.END, lib_name)
    
    def load_library_from_file(self, library_name):
        """Load a library from a file"""
        lib = Library(library_name)
        file_path = self.db_path / f"{library_name}.txt"
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 7:
                            try:
                                book = Book(
                                    title=parts[0].strip(),
                                    author=parts[1].strip(),
                                    genre=parts[2].strip(),
                                    year=parts[3].strip(),
                                    length=parts[4].strip(),
                                    country=parts[5].strip(),
                                    place=parts[6].strip()
                                )
                                lib.add_book(book)
                            except Exception as e:
                                print(f"Error loading book: {e}")
        
        return lib
    
    def save_library_to_file(self, library_name):
        """Save a library to a file"""
        if library_name not in self.libraries:
            return
        
        file_path = self.db_path / f"{library_name}.txt"
        lib = self.libraries[library_name]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for book in lib.books:
                f.write(str(book) + '\n')
    
    def populate_results_tree(self, books):
        """Populate the results tree with books"""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Store the results
        self.current_results = books
        
        # Add books to tree
        for book in books:
            self.results_tree.insert('', 'end', values=(
                str(book.title)[:25],
                str(book.author)[:20],
                str(book.genre)[:15],
                str(book.year)[:8],
                str(book.length)[:8],
                str(book.country)[:12],
                str(book.place)[:10]
            ))
    
    def get_selected_book(self):
        """Get the selected book from the tree"""
        selection = self.results_tree.selection()
        if not selection:
            messagebox.showwarning(self._('warning'), self._('no_book_selected'))
            return None
        
        # Get the row index
        item_id = selection[0]
        index = self.results_tree.index(item_id)
        
        if 0 <= index < len(self.current_results):
            return self.current_results[index]
        return None
    
    def load_selected_library(self, event=None):
        """Load the selected library"""
        selection = self.library_listbox.curselection()
        if not selection:
            return
        
        lib_name = self.library_listbox.get(selection[0])
        self.current_library = lib_name
        self.library_label.config(text=f"Library: {lib_name}")
        self.search_query.delete(0, tk.END)
        self.search()
    
    def search(self):
        """Search the current library when user presses Enter"""
        if not self.current_library:
            return
        
        # Use refresh_display to show results
        self.refresh_display()
    
    def on_search_enter(self, event):
        """Handle Enter key press in search box"""
        self.search()
        return 'break'  # Prevent the default Enter behavior
    
    def clear_results(self):
        """Clear the search box and results display"""
        self.search_query.delete(0, tk.END)
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.current_results = []
    
    def edit_selected_book(self):
        """Edit the selected book"""
        book = self.get_selected_book()
        if not book:
            return
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title(self._('edit_book'))
        edit_window.geometry("400x400")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        fields = {}
        values = {
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'year': book.year,
            'length': book.length,
            'country': book.country,
            'place': book.place
        }
        
        entry_list = []
        
        for i, (field, value) in enumerate(values.items()):
            ttk.Label(edit_window, text=f"{field.capitalize()}:").grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(edit_window, width=30)
            entry.insert(0, str(value))
            entry.grid(row=i, column=1, padx=10, pady=5)
            fields[field] = entry
            entry_list.append(entry)
        
        def save_changes():
            try:
                book.edit_book(
                    title=fields['title'].get() or None,
                    author=fields['author'].get() or None,
                    genre=fields['genre'].get() or None,
                    year=fields['year'].get() or None,
                    length=fields['length'].get() or None,
                    country=fields['country'].get() or None,
                    place=fields['place'].get() or None
                )
                
                self.save_library_to_file(self.current_library)
                messagebox.showinfo(self._('success'), self._('book_updated'))
                edit_window.destroy()
                self.refresh_display()
            except Exception as e:
                messagebox.showerror(self._('error'), f"{self._('error')}: {str(e)}")
        
        self.add_book_context = {'entry_list': entry_list, 'save_book': save_changes}
        for i, entry in enumerate(entry_list):
            entry.bind('<Return>', lambda event, idx=i: self.on_add_book_enter(event, idx))
        
        ttk.Button(edit_window, text=self._('confirm_move'), command=save_changes).grid(row=len(values), column=0, columnspan=2, pady=10)
    
    def move_selected_book(self):
        """Move the selected book to another library"""
        book = self.get_selected_book()
        if not book:
            return
        
        # Create a list of other libraries
        other_libs = [lib for lib in self.libraries.keys() if lib != self.current_library]
        
        if not other_libs:
            messagebox.showwarning(self._('warning'), self._('no_other_libraries'))
            return
        
        # Create selection window
        select_window = tk.Toplevel(self.root)
        select_window.title(self._('move_book'))
        select_window.geometry("300x200")
        select_window.transient(self.root)
        select_window.grab_set()
        
        ttk.Label(select_window, text=self._('select_destination')).pack(pady=10)
        
        lib_listbox = tk.Listbox(select_window, height=10)
        lib_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for lib_name in other_libs:
            lib_listbox.insert(tk.END, lib_name)
        
        def move_book():
            selection = lib_listbox.curselection()
            if not selection:
                messagebox.showwarning(self._('warning'), self._('no_book_selected'))
                return
            
            dest_lib_name = lib_listbox.get(selection[0])
            
            # Remove from current library and add to destination
            self.libraries[self.current_library].remove_book(book)
            self.libraries[dest_lib_name].add_book(book)
            
            # Save both libraries
            self.save_library_to_file(self.current_library)
            self.save_library_to_file(dest_lib_name)
            
            messagebox.showinfo(self._('success'), f"{self._('book_moved')} {dest_lib_name}")
            select_window.destroy()
            self.refresh_display()
        
        lib_listbox.bind('<Double-Button-1>', lambda e: move_book())
    
    def delete_selected_book(self):
        """Delete the selected book"""
        book = self.get_selected_book()
        if not book:
            return
        
        if messagebox.askyesno(self._('confirm_delete'), f"Delete '{book.title}'?"):
            self.libraries[self.current_library].remove_book(book)
            self.save_library_to_file(self.current_library)
            messagebox.showinfo(self._('success'), self._('book_deleted'))
            self.refresh_display()
    
    def refresh_display(self):
        """Refresh the display with current books sorted by relevance to search query"""
        if not self.current_library:
            return
        
        lib = self.libraries[self.current_library]
        query = self.search_query.get().strip()
        
        # Get results - lib.search() already returns relevance-scored results
        if query:
            results = lib.search(query)
        else:
            # If no query, sort by the selected attribute
            sort_attr = self.sort_var.get()
            try:
                results = lib.sort_by_attribute(sort_attr, reverse=False)
            except:
                results = lib.books[:]
        
        # Display results in tree
        self.populate_results_tree(results)
    
    def add_book(self):
        """Open dialog to add a new book"""
        if not self.current_library:
            messagebox.showwarning(self._('warning'), self._('no_library_selected'))
            return
        
        # Create a new window for adding a book
        add_window = tk.Toplevel(self.root)
        add_window.title(self._('add_book'))
        add_window.geometry("400x400")
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Create entry fields
        fields = {}
        default_values = {
            'title': '',
            'author': '',
            'genre': '',
            'year': '',
            'length': '',
            'country': '',
            'place': ''
        }
        
        entry_list = []  # Keep track of entries in order
        
        for i, (field, default) in enumerate(default_values.items()):
            ttk.Label(add_window, text=f"{field.capitalize()}:").grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(add_window, width=30)
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=10, pady=5)
            fields[field] = entry
            entry_list.append(entry)
        
        def save_book():
            try:
                book = Book(
                    title=fields['title'].get() or "N/A",
                    author=fields['author'].get() or "N/A",
                    genre=fields['genre'].get() or "N/A",
                    year=fields['year'].get() or "N/A",
                    length=fields['length'].get() or "N/A",
                    country=fields['country'].get() or "N/A",
                    place=fields['place'].get() or "N/A"
                )
                
                lib = self.libraries[self.current_library]
                lib.add_book(book)
                self.save_library_to_file(self.current_library)
                messagebox.showinfo(self._('success'), self._('book_added'))
                add_window.destroy()
                self.refresh_display()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add book: {str(e)}")
        
        # Store context for Enter key handling
        self.add_book_context = {
            'entry_list': entry_list,
            'save_book': save_book
        }
        
        # Add Enter key bindings to each field
        for i, entry in enumerate(entry_list):
            entry.bind('<Return>', lambda event, idx=i: self.on_add_book_enter(event, idx))
        
        ttk.Button(add_window, text=self._('confirm_move'), command=save_book).grid(row=len(default_values), column=0, columnspan=2, pady=10)
    
    def on_add_book_enter(self, event, field_index):
        """Handle Enter key press in add book dialog"""
        entry_list = self.add_book_context['entry_list']
        save_book = self.add_book_context['save_book']
        
        # Check if all fields are filled
        all_filled = all(entry.get().strip() != '' for entry in entry_list)
        
        if all_filled:
            # All fields filled, save the book
            save_book()
        else:
            # Find next empty field
            for i in range(field_index + 1, len(entry_list)):
                if entry_list[i].get().strip() == '':
                    entry_list[i].focus()
                    return 'break'
            # If no empty field after current, loop back to find first empty
            for i in range(len(entry_list)):
                if entry_list[i].get().strip() == '':
                    entry_list[i].focus()
                    return 'break'
        
        return 'break'
    
    def open_settings(self):
        """Open the settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title(self._('settings'))
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Language selection
        ttk.Label(settings_window, text="Language:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        lang_var = tk.StringVar(value=self.language)
        lang_combo = ttk.Combobox(settings_window, textvariable=lang_var, values=['en', 'bg'], state="readonly", width=20)
        lang_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # UI Text Size
        ttk.Label(settings_window, text="UI Text Size:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        ui_size_var = tk.IntVar(value=self.settings.get('ui_font_size', 10))
        ui_size_label = ttk.Label(settings_window, text=str(ui_size_var.get()))
        ui_size_label.grid(row=1, column=2, padx=5, pady=10)
        ui_size_slider = ttk.Scale(settings_window, from_=8, to=16, orient=tk.HORIZONTAL, variable=ui_size_var,
                                    command=lambda v: ui_size_label.config(text=str(int(float(v)))))
        ui_size_slider.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Results Text Size
        ttk.Label(settings_window, text="Results Text Size:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        results_size_var = tk.IntVar(value=self.settings.get('results_text_size', 10))
        results_size_label = ttk.Label(settings_window, text=str(results_size_var.get()))
        results_size_label.grid(row=2, column=2, padx=5, pady=10)
        results_size_slider = ttk.Scale(settings_window, from_=8, to=16, orient=tk.HORIZONTAL, variable=results_size_var,
                                        command=lambda v: results_size_label.config(text=str(int(float(v)))))
        results_size_slider.grid(row=2, column=1, padx=10, pady=10, sticky=tk.EW)
        
        settings_window.columnconfigure(1, weight=1)
        
        def save_settings():
            self.language = lang_var.get()
            self.settings['language'] = self.language
            self.settings['ui_font_size'] = ui_size_var.get()
            self.settings['results_text_size'] = results_size_var.get()
            
            # Apply results text size immediately
            self.tree_font = tkfont.Font(family="TkDefaultFont", size=self.settings['results_text_size'])
            self.results_tree.tag_configure('default', font=self.tree_font)
            
            self.save_settings()
            messagebox.showinfo(self._('success'), "Settings saved! Please restart the application for language changes to take effect.")
            settings_window.destroy()
        
        ttk.Button(settings_window, text="Save", command=save_settings).grid(row=3, column=0, columnspan=3, pady=20)
    
    def create_new_library(self):
        """Create a new library"""
        lib_name = simpledialog.askstring(self._('new_library'), "Enter library name:")
        
        if not lib_name:
            return
        
        if lib_name in self.libraries:
            messagebox.showwarning(self._('warning'), "Library already exists")
            return
        
        # Create new library
        self.libraries[lib_name] = Library(lib_name)
        self.save_library_to_file(lib_name)
        self.load_libraries()
        messagebox.showinfo(self._('success'), f"Library '{lib_name}' created!")
    
    def delete_library(self):
        """Delete the selected library"""
        selection = self.library_listbox.curselection()
        if not selection:
            messagebox.showwarning(self._('warning'), self._('no_library_selected'))
            return
        
        lib_name = self.library_listbox.get(selection[0])
        
        if messagebox.askyesno(self._('confirm_delete'), f"Delete library '{lib_name}'?"):
            file_path = self.db_path / f"{lib_name}.txt"
            file_path.unlink(missing_ok=True)
            
            if lib_name in self.libraries:
                del self.libraries[lib_name]
            
            if self.current_library == lib_name:
                self.current_library = None
                self.library_label.config(text=self._('no_library_selected'))
                self.clear_results()
            
            self.load_libraries()
            messagebox.showinfo(self._('success'), f"Library '{lib_name}' deleted!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ArchiumApp(root)
    root.mainloop()
