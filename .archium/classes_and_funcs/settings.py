import json
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkfont


class SettingsMixin:
    def load_settings(self):
        """Load settings from the JSON file."""
        defaults = {
            "language": "en",
            "ui_font_size": 10,
            "results_text_size": 10,
        }
        if not self.settings_file.exists():
            return defaults

        try:
            with self.settings_file.open("r", encoding="utf-8") as file:
                settings = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            print(f"Unable to load settings: {error}")
            return defaults

        if not isinstance(settings, dict):
            print("Unable to load settings: expected a JSON object")
            return defaults
        return settings

    def save_settings(self):
        """Save settings to the JSON file."""
        with self.settings_file.open("w", encoding="utf-8") as file:
            json.dump(self.settings, file, ensure_ascii=False, indent=2)

    def open_settings(self):
        """Open the settings dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title(self._("settings"))
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()

        ttk.Label(
            settings_window, text=f"{self._('language')}:"
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        language_var = tk.StringVar(value=self.language)
        language_combo = ttk.Combobox(
            settings_window,
            textvariable=language_var,
            values=["en", "bg"],
            state="readonly",
            width=20,
        )
        language_combo.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(
            settings_window, text=f"{self._('ui_text_size')}:"
        ).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        ui_size_var = tk.IntVar(
            value=self.settings.get("ui_font_size", 10)
        )
        ui_size_label = ttk.Label(
            settings_window, text=str(ui_size_var.get())
        )
        ui_size_label.grid(row=1, column=2, padx=5, pady=10)
        ui_size_slider = ttk.Scale(
            settings_window,
            from_=8,
            to=16,
            orient=tk.HORIZONTAL,
            variable=ui_size_var,
            command=lambda value: ui_size_label.config(
                text=str(int(float(value)))
            ),
        )
        ui_size_slider.grid(
            row=1, column=1, padx=10, pady=10, sticky=tk.EW
        )

        ttk.Label(
            settings_window, text=f"{self._('results_text_size')}:"
        ).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        results_size_var = tk.IntVar(
            value=self.settings.get("results_text_size", 10)
        )
        results_size_label = ttk.Label(
            settings_window, text=str(results_size_var.get())
        )
        results_size_label.grid(row=2, column=2, padx=5, pady=10)
        results_size_slider = ttk.Scale(
            settings_window,
            from_=8,
            to=16,
            orient=tk.HORIZONTAL,
            variable=results_size_var,
            command=lambda value: results_size_label.config(
                text=str(int(float(value)))
            ),
        )
        results_size_slider.grid(
            row=2, column=1, padx=10, pady=10, sticky=tk.EW
        )
        settings_window.columnconfigure(1, weight=1)

        def save_settings():
            search_query = self.search_query.get()
            sort_attribute = self.sort_var.get()
            self.language = language_var.get()
            self.settings["language"] = self.language
            self.settings["ui_font_size"] = ui_size_var.get()
            self.settings["results_text_size"] = results_size_var.get()

            self.tree_font = tkfont.Font(
                family="TkDefaultFont",
                size=self.settings["results_text_size"],
            )
            self.results_tree.tag_configure(
                "default", font=self.tree_font
            )

            self.save_settings()
            settings_window.destroy()
            self.apply_language(search_query, sort_attribute)
            messagebox.showinfo(
                self._("success"), self._("settings_saved")
            )

        ttk.Button(
            settings_window,
            text=self._("save"),
            command=save_settings,
        ).grid(row=3, column=0, columnspan=3, pady=20)

    def apply_language(self, search_query, sort_attribute):
        self.root.title(self._("title"))
        self.main_frame.destroy()
        self.create_widgets()

        selected_index = None
        for index, library_name in enumerate(self.libraries):
            self.library_listbox.insert(tk.END, library_name)
            if library_name == self.current_library:
                selected_index = index

        if selected_index is not None:
            self.library_listbox.selection_set(selected_index)
            self.library_label.config(
                text=f"{self._('library')}: {self.current_library}"
            )

        self.sort_var.set(sort_attribute)
        self.search_query.insert(0, search_query)
        self.refresh_display()
