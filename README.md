# Archium

**Archium** is a library management helper application built with Python and Tkinter.

## Quick Start

### Option 1: Batch launcher

```bash
Archium.bat
```

### Option 2: Executable launcher

```bash
git clone https://github.com/Primorger/Archium.git
cd Archium
Archium.exe
```

Both launchers check for Python 3.8 or newer. If Python is missing, they install Python 3.11 for the current user, then start Archium. An internet connection is needed for that first-time installation.

The executable starts the app without showing a console window; the Archium window remains visible.

## Features

- **Book management** - Add, edit, delete, and move books between libraries
- **Persistent storage** - Books stored in `.archium/db/` with your data safe
- **Multi-language support** - English and Bulgarian
- **Settings** - Customizable UI font size and results text size
- **Auto-update** - Automatically checks GitHub for new versions

## Usage

### Using the Application

1. **Open in library dropdown** - Select a library or create new one
2. **Add Book** - Click "Add Book" and enter details
3. **Search** - Type in search box and press Enter
4. **Sort** - Use dropdown to sort by any attribute
5. **Edit/Delete** - Select a book and use buttons
6. **Move** - Double-click another library name to move selected book

## Project Structure

```
Archium/
├── Archium.exe                # RUN THIS (user-facing executable)
├── Archium.ico                # App and window icon
├── launcher.py                # Update checker and application launcher
│
├── .archium/                  # Hidden app wrapper
│   ├── archium.py             # Main GUI application  
│   ├── languages.json         # English and Bulgarian UI strings
│   ├── version.json           # Current version
│   ├── classes_and_funcs/
│   │   ├── book.py            # Book class
│   │   └── library.py         # Library class
│   ├── db/                    # Your book database
│   │   └── *.txt              # One library per file
│   └── settings/              # Your preferences
│       └── settings.json
│
├── scripts/                   # Build scripts (for developers)
│   ├── build_exe.bat
│   └── build_exe.ps1
│
├── .github/workflows/         # CI/CD automation
│   └── build.yml
│
└── tests/                      # Launcher updater tests
```

## Supported Languages

- **English** (en)
- **Bulgarian** (bg)

Translations are stored in `.archium/languages.json`. Add a language there using the same keys as `en` and `bg`.

## Troubleshooting

### Application won't start
- Verify Python 3.8+ is installed, or start with `Archium.bat` to install it
- Check that `.archium/archium.py` and `.archium/languages.json` exist

### Search not working with non-ASCII characters
- Application uses `.lower()` for case-insensitive search
- Should work with Cyrillic and other Unicode scripts

### Settings not saving
- Ensure `.archium/settings/` exists and is writable
- Check file permissions

### Updates fail
- Verify internet connection
- Check GitHub repo name in `launcher.py`
- Ensure release has a `.zip` file attached