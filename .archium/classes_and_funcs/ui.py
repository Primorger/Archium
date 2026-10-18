import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


class UIMixin:
    def create_widgets(self):
        """Create the main UI layout."""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_frame = ttk.LabelFrame(
            self.main_frame, text=self._("libraries"), width=200
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(left_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.library_listbox = tk.Listbox(
            left_frame, yscrollcommand=scrollbar.set, height=15
        )
        self.library_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.library_listbox.yview)
        self.library_listbox.bind(
            "<Double-Button-1>", self.load_selected_library
        )

        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            button_frame,
            text=self._("new_library"),
            command=self.create_new_library,
        ).pack(fill=tk.X, pady=2)
        ttk.Button(
            button_frame,
            text=self._("delete_library"),
            command=self.delete_library,
        ).pack(fill=tk.X, pady=2)
        ttk.Button(
            button_frame,
            text=self._("settings"),
            command=self.open_settings,
        ).pack(fill=tk.X, pady=2)

        right_frame = ttk.Frame(self.main_frame)
        right_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5
        )

        self.library_label = ttk.Label(
            right_frame,
            text=self._("no_library_selected"),
            font=("Arial", 14, "bold"),
        )
        self.library_label.pack(pady=5)

        search_frame = ttk.LabelFrame(
            right_frame, text=self._("search"), padding=5
        )
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(search_frame, text=self._("search") + ":").grid(
            row=0, column=0, sticky=tk.W, padx=5
        )
        self.search_query = ttk.Entry(search_frame, width=30)
        self.search_query.grid(row=0, column=1, padx=5, sticky=tk.EW)
        self.search_query.bind("<Return>", self.on_search_enter)
        self.bind_clipboard_shortcuts(self.search_query)
        self.bind_clipboard_menu(self.search_query)

        ttk.Label(search_frame, text=self._("sort_by") + ":").grid(
            row=0, column=2, sticky=tk.W, padx=20
        )
        self.sort_var = tk.StringVar(value="title")
        sort_combo = ttk.Combobox(
            search_frame,
            textvariable=self.sort_var,
            values=[
                "title",
                "author",
                "genre",
                "year",
                "length",
                "country",
                "place",
            ],
            state="readonly",
            width=15,
        )
        sort_combo.grid(row=0, column=3, padx=5)
        sort_combo.bind("<<ComboboxSelected>>", self.on_sort_selected)
        search_frame.columnconfigure(1, weight=1)

        results_frame = ttk.LabelFrame(
            right_frame, text=self._("results"), padding=5
        )
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tree_scroll_y = ttk.Scrollbar(results_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x = ttk.Scrollbar(
            results_frame, orient=tk.HORIZONTAL
        )
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.results_tree = ttk.Treeview(
            results_frame,
            columns=(
                "Title",
                "Author",
                "Genre",
                "Year",
                "Length",
                "Country",
                "Place",
            ),
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            height=12,
        )
        tree_scroll_y.config(command=self.results_tree.yview)
        tree_scroll_x.config(command=self.results_tree.xview)

        self.tree_font = tkfont.Font(
            family="TkDefaultFont",
            size=self.settings.get("results_text_size", 10),
        )
        self.results_tree.tag_configure("default", font=self.tree_font)

        self.results_tree.column("#0", width=0, stretch=tk.NO)
        self.results_tree.column("Title", anchor=tk.W, width=100)
        self.results_tree.column("Author", anchor=tk.W, width=90)
        self.results_tree.column("Genre", anchor=tk.W, width=70)
        self.results_tree.column("Year", anchor=tk.CENTER, width=50)
        self.results_tree.column("Length", anchor=tk.CENTER, width=50)
        self.results_tree.column("Country", anchor=tk.W, width=70)
        self.results_tree.column("Place", anchor=tk.W, width=70)

        self.results_tree.heading("#0", text="", anchor=tk.W)
        self.results_tree.heading(
            "Title", text=self._("column_title"), anchor=tk.W
        )
        self.results_tree.heading(
            "Author", text=self._("column_author"), anchor=tk.W
        )
        self.results_tree.heading(
            "Genre", text=self._("column_genre"), anchor=tk.W
        )
        self.results_tree.heading(
            "Year", text=self._("column_year"), anchor=tk.CENTER
        )
        self.results_tree.heading(
            "Length", text=self._("column_length"), anchor=tk.CENTER
        )
        self.results_tree.heading(
            "Country", text=self._("column_country"), anchor=tk.W
        )
        self.results_tree.heading(
            "Place", text=self._("column_place"), anchor=tk.W
        )

        self.results_tree.pack(fill=tk.BOTH, expand=True)
        self.current_results = []

        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            action_frame,
            text=self._("add_book"),
            command=self.add_book,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            action_frame,
            text=self._("edit_book"),
            command=self.edit_selected_book,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            action_frame,
            text=self._("move_book"),
            command=self.move_selected_book,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            action_frame,
            text=self._("delete_book"),
            command=self.delete_selected_book,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            action_frame,
            text=self._("clear_results"),
            command=self.clear_results,
        ).pack(side=tk.LEFT, padx=5)

    def populate_results_tree(self, books):
        """Populate the results tree with books."""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        self.current_results = books
        for book in books:
            self.results_tree.insert(
                "",
                "end",
                values=(
                    str(book.title)[:25],
                    str(book.author)[:20],
                    str(book.genre)[:15],
                    str(book.year)[:8],
                    str(book.length)[:8],
                    str(book.country)[:12],
                    str(book.place)[:10],
                ),
            )
        self.results_tree.yview_moveto(0)

    def get_selected_book(self):
        """Get the selected book from the results tree."""
        selection = self.results_tree.selection()
        if not selection:
            from tkinter import messagebox

            messagebox.showwarning(
                self._("warning"), self._("no_book_selected")
            )
            return None

        index = self.results_tree.index(selection[0])
        if 0 <= index < len(self.current_results):
            return self.current_results[index]
        return None

    def search(self):
        """Refresh results for the current library."""
        if self.current_library:
            self.refresh_display()

    def on_search_enter(self, event):
        self.search()
        return "break"

    def on_sort_selected(self, event):
        self.refresh_display()

    def clear_results(self):
        self.search_query.delete(0, tk.END)
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.current_results = []

    def refresh_display(self):
        """Refresh the display using the selected search and sort options."""
        if not self.current_library:
            return

        library = self.libraries[self.current_library]
        query = self.search_query.get().strip()
        sort_attribute = self.sort_var.get()

        if query:
            results = library.search(query, sort_attribute)
        else:
            try:
                results = library.sort_by_attribute(
                    sort_attribute, reverse=False
                )
            except ValueError:
                results = library.books[:]

        self.populate_results_tree(results)
