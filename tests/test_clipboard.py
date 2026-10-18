import sys
import tkinter as tk
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[1] / ".archium"))

from classes_and_funcs.clipboard import ClipboardMixin


class FakeEntry:
    def __init__(self, value, selection=None, clipboard_text=""):
        self.value = value
        self.selection = selection
        self.clipboard_text = clipboard_text
        self.clipboard_value = None
        self.insert_cursor = 0

    def selection_present(self):
        return self.selection is not None

    def get(self):
        return self.value

    def index(self, index):
        if index == tk.SEL_FIRST:
            return self.selection[0]
        if index == tk.SEL_LAST:
            return self.selection[1]
        raise AssertionError(f"Unexpected index: {index}")

    def clipboard_clear(self):
        self.clipboard_value = ""

    def clipboard_append(self, value):
        self.clipboard_value += value

    def clipboard_get(self):
        if self.clipboard_text is None:
            raise tk.TclError("clipboard is empty")
        return self.clipboard_text

    def delete(self, first, last):
        start = self.index(first)
        end = self.index(last)
        self.value = self.value[:start] + self.value[end:]
        self.insert_cursor = start
        self.selection = None

    def insert(self, index, text):
        if index != tk.INSERT:
            raise AssertionError(f"Unexpected insertion index: {index}")
        self.value = (
            self.value[: self.insert_cursor]
            + text
            + self.value[self.insert_cursor :]
        )
        self.insert_cursor += len(text)


class ClipboardTests(unittest.TestCase):
    def test_copy_entry_selection_uses_entry_value_and_selection_indices(self):
        entry = FakeEntry("hello world", selection=(6, 11))

        result = ClipboardMixin.copy_entry_selection(entry)

        self.assertEqual(entry.clipboard_value, "world")
        self.assertEqual(entry.value, "hello world")
        self.assertEqual(result, "break")

    def test_cut_entry_selection_copies_then_removes_selected_text(self):
        entry = FakeEntry("hello world", selection=(6, 11))

        result = ClipboardMixin.cut_entry_selection(entry)

        self.assertEqual(entry.clipboard_value, "world")
        self.assertEqual(entry.value, "hello ")
        self.assertEqual(result, "break")

    def test_paste_replaces_selected_text(self):
        entry = FakeEntry("abcd", selection=(1, 3), clipboard_text="XY")

        result = ClipboardMixin.paste_entry_clipboard(entry)

        self.assertEqual(entry.value, "aXYd")
        self.assertEqual(result, "break")

    def test_paste_with_empty_clipboard_leaves_entry_unchanged(self):
        entry = FakeEntry("abcd", selection=(1, 3), clipboard_text=None)

        result = ClipboardMixin.paste_entry_clipboard(entry)

        self.assertEqual(entry.value, "abcd")
        self.assertEqual(result, "break")


if __name__ == "__main__":
    unittest.main()
