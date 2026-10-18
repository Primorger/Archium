import tkinter as tk
from pathlib import Path

from .book_management import BookManagementMixin
from .clipboard import ClipboardMixin
from .library_management import LibraryManagementMixin
from .settings import SettingsMixin
from .translations import LANGUAGES
from .ui import UIMixin


class ArchiumApp(
    SettingsMixin,
    LibraryManagementMixin,
    BookManagementMixin,
    ClipboardMixin,
    UIMixin,
):
    def __init__(self, root):
        self.root = root

        app_dir = Path(__file__).resolve().parent.parent
        self.db_path = app_dir / "db"
        self.db_path.mkdir(exist_ok=True)

        self.settings_path = app_dir / "settings"
        self.settings_path.mkdir(exist_ok=True)
        self.settings_file = self.settings_path / "settings.json"

        self.current_library = None
        self.libraries = {}

        self.settings = self.load_settings()
        self.language = self.settings.get("language", "en")
        if self.language not in LANGUAGES:
            self.language = "en"
        self.ui_font_size = self.settings.get("ui_font_size", 10)

        self.root.title(LANGUAGES[self.language]["title"])
        self.root.geometry("1200x700")
        icon_paths = (
            app_dir / "Archium.ico",
            app_dir.parent / "Archium.ico",
        )
        for icon_path in icon_paths:
            if icon_path.is_file():
                try:
                    self.root.iconbitmap(str(icon_path))
                except tk.TclError:
                    pass
                break

        self.create_widgets()
        self.load_libraries()

    def _(self, key: str) -> str:
        result = LANGUAGES.get(self.language, {}).get(key)
        return result if result is not None else key
