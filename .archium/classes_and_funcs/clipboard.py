import tkinter as tk


class ClipboardMixin:
    @staticmethod
    def has_input_selection(widget):
        if isinstance(widget, tk.Text):
            return bool(widget.tag_ranges(tk.SEL))
        return widget.selection_present()

    def bind_clipboard_shortcuts(self, widget):
        widget.bind(
            "<Control-c>",
            lambda event: self.copy_entry_selection(event.widget),
        )
        widget.bind(
            "<Control-x>",
            lambda event: self.cut_entry_selection(event.widget),
        )
        widget.bind(
            "<Control-v>",
            lambda event: self.paste_entry_clipboard(event.widget),
        )
        widget.bind(
            "<Control-Insert>",
            lambda event: self.copy_entry_selection(event.widget),
        )
        widget.bind(
            "<Shift-Insert>",
            lambda event: self.paste_entry_clipboard(event.widget),
        )

    def bind_clipboard_menu(self, widget):
        menu = tk.Menu(widget, tearoff=False)
        menu.add_command(
            label=self._("cut"),
            command=lambda: self.cut_entry_selection(widget),
        )
        menu.add_command(
            label=self._("copy"),
            command=lambda: self.copy_entry_selection(widget),
        )
        menu.add_command(
            label=self._("paste"),
            command=lambda: self.paste_entry_clipboard(widget),
        )

        def show_menu(event):
            event.widget.focus_set()
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
            return "break"

        widget.bind("<Button-3>", show_menu)

    @classmethod
    def get_selected_text(cls, widget):
        if isinstance(widget, tk.Text):
            return widget.get(tk.SEL_FIRST, tk.SEL_LAST)

        value = widget.get()
        start = widget.index(tk.SEL_FIRST)
        end = widget.index(tk.SEL_LAST)
        return value[start:end]

    @classmethod
    def copy_entry_selection(cls, widget):
        if cls.has_input_selection(widget):
            widget.clipboard_clear()
            widget.clipboard_append(cls.get_selected_text(widget))
        return "break"

    @classmethod
    def cut_entry_selection(cls, widget):
        if cls.has_input_selection(widget):
            widget.clipboard_clear()
            widget.clipboard_append(cls.get_selected_text(widget))
            widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        return "break"

    @staticmethod
    def paste_entry_clipboard(widget):
        try:
            text = widget.clipboard_get()
        except tk.TclError:
            return "break"

        if ClipboardMixin.has_input_selection(widget):
            widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        widget.insert(tk.INSERT, text)
        return "break"

    @staticmethod
    def get_input_value(widget):
        if isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c")
        return widget.get()
