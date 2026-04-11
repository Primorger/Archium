# Archium 📚

**Archium** is a library management helper application built with Python and Tkinter. It allows you to organize, search, and manage your book collections with a modern GUI.

## Features ✨

- 🔍 **Full-text search** across all book attributes (title, author, genre, year, etc.)
- 📖 **Book management** - Add, edit, delete, and move books between libraries
- 💾 **Persistent storage** - Books stored as individual `.txt` files per library
- 🌍 **Multi-language support** - English and Bulgarian (easily extensible)
- ⚙️ **Settings** - Customizable UI font size and results text size
- 🔄 **Auto-update** - Launcher checks GitHub for new versions and updates automatically
- 🎨 **Modern UI** - Built with Tkinter ttk widgets for native look and feel

## Installation 🚀

### Prerequisites
- Python 3.6+
- pip package manager

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Primorger/Archium.git
   cd Archium
   ```

2. **Create virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python archium.py
   ```

## Usage 📖

### Starting the App

**Option 1: Direct launch**
```bash
python archium.py
```

**Option 2: Using the launcher** (with auto-update)
```bash
python launcher.py
```
The launcher will automatically check GitHub for updates and download them if available.

### Creating a Library

1. Enter a library name in the input field
2. Click "Create Library"
3. Select it from the library list to start adding books

### Adding Books

1. Select a library
2. Click "Add Book"
3. Fill in book details:
   - **Title** - Book title
   - **Author** - Author name
   - **Genre** - Book genre
   - **Year** - Publication year
   - **Length** - Number of pages
   - **Country** - Author's country
   - **Place** - Publication place
4. Press Enter to save

### Searching Books

1. Type your search query in the search box
2. Press Enter or click "Search"
3. Results show books with matching attributes, sorted by relevance

### Managing Books

- **Edit**: Select a book and click "Edit Book"
- **Move**: Select a book and double-click another library to move it
- **Delete**: Select a book and click "Delete Book"
- **Sort**: Use the dropdown to sort by any attribute

## Project Structure 📁

```
Archium/
├── archium.py                # Main application
├── launcher.py              # Update launcher
├── version.json             # Current version info
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
├── README.md               # This file
├── classes_and_funcs/      # Application modules
│   ├── book.py             # Book class
│   └── library.py          # Library class
├── db/                     # Book databases (one .txt file per library)
│   └── *.txt               # Library files
├── settings/               # Application settings
│   └── settings.json       # User preferences
└── scripts/                # Build and utility scripts
    ├── build_exe.bat       # Build exe (Windows)
    └── build_exe.ps1       # Build exe (PowerShell)
```

## Building the Executable 🔧

### Step 1: Update version
Edit `version.json` with your new version:
```json
{
  "version": "2.0.1",
  "last_updated": "2026-04-11T12:00:00"
}
```

### Step 2: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 3: Build
**Windows (Command Prompt)**:
```bash
cd scripts
build_exe.bat
```

**Windows (PowerShell)**:
```powershell
cd scripts
.\build_exe.ps1
```

The `Archium.exe` will be created in the root folder.

## Publishing Updates 📤

### GitHub Release Process

1. **Create a release on GitHub**:
   - Go to your repo → Releases → Create New Release
   - Tag: `v2.0.1` (matches version.json)
   - Add release notes

2. **Attach application files**:
   - Create a `.zip` with:
     ```
     archium.zip
     ├── archium.py
     ├── launcher.py
     ├── version.json
     ├── classes_and_funcs/
     ├── settings/
     └── db/
     ```
   - Upload to the release

3. **Users will auto-update** when they run `Archium.exe`

## Data Format 💾

### Book File Format (db/*.txt)
Books are stored as pipe-delimited text:
```
title|author|genre|year|length|country|place
The Hobbit|J.R.R. Tolkien|Fantasy|1937|310|UK|London
```

### Settings (settings/settings.json)
```json
{
  "language": "en",
  "ui_font_size": 10,
  "results_text_size": 9
}
```

## Supported Languages 🌐

- **English** (en)
- **Bulgarian** (bg)

To add more languages, edit the `LANGUAGES` dictionary in `archium.py`.

## Troubleshooting 🔧

### Application won't start
- Verify Python 3.6+ is installed
- Check that `archium.py` exists in the root folder
- Ensure dependencies are installed: `pip install -r requirements.txt`

### Search not working with non-ASCII characters
- Application uses `.lower()` for case-insensitive search
- Should work with Cyrillic and other Unicode scripts

### Settings not saving
- Ensure `settings/` folder exists and is writable
- Check file permissions

### Updates fail
- Verify internet connection
- Check GitHub repo name in `launcher.py`
- Ensure release has a `.zip` file attached

## Contributing 🤝

Feel free to fork and submit pull requests!

## License 📄

This project is open source. Feel free to use and modify.

## Support 💬

For issues and questions, please use GitHub Issues.

---

**Made with ❤️ for book lovers**
