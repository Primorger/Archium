# Archium 📚

**Archium** is a library management helper application built with Python and Tkinter. It requires **zero setup** - just run the executable and everything works automatically.

## ⚡ Quick Start (Users)

### Option 1: **Recommended - Just run the batch file**

```bash
Archium.bat
```

**That's it!** The batch file will:
- ✅ Check if Python is installed
- ✅ Automatically install Python if needed
- ✅ Set up the app environment
- ✅ Launch the application

### Option 2: If you have Python already installed

```bash
git clone https://github.com/Primorger/Archium.git
cd Archium
Archium.exe
```

**No Python?** Use Option 1 instead - `Archium.bat` handles everything.

## Features ✨

- 🔍 **Full-text search** across all book attributes (title, author, genre, year, etc.)
- 📖 **Book management** - Add, edit, delete, and move books between libraries
- 💾 **Persistent storage** - Books stored in `.archium/db/` with your data safe
- 🌍 **Multi-language support** - English and Bulgarian
- ⚙️ **Settings** - Customizable UI font size and results text size
- 🔄 **Auto-update** - Automatically checks GitHub for new versions
- 🎨 **Modern UI** - Tkinter ttk widgets for native look
- ⚙️ **Zero setup** - No manual configuration needed

## What You Get

## What You Get

When you clone the repository, you'll see:
- `Archium.exe` - **Just run this** (does everything automatically)
- `.archium/` - Hidden folder containing the app (you don't need to touch this)
- Other files for developers (can be ignored)

## Installation & Running

### For Users

The **only** step needed:

```bash
git clone https://github.com/Primorger/Archium.git
cd Archium
Archium.exe
```

That's literally it. The exe will:
1. Create a Python environment automatically
2. Check for updates
3. Download updates if available
4. Launch the application

You don't need Python installed on your machine - the exe handles everything.

### For Developers

If you want to work on the code:

```bash
python .archium/archium.py          # Run directly from repo
```

## Usage 📖

### Using the Application

1. **Open in library dropdown** - Select a library or create new one
2. **Add Book** - Click "Add Book" and enter details
3. **Search** - Type in search box and press Enter
4. **Sort** - Use dropdown to sort by any attribute
5. **Edit/Delete** - Select a book and use buttons
6. **Move** - Double-click another library name to move selected book

## Project Structure 📁

```
Archium/
├── Archium.exe                # ← RUN THIS (user-facing executable)
├── launcher.py                # Bootstrapper that builds everything
│
├── .archium/                  # ← Hidden app wrapper
│   ├── archium.py             # Main GUI application  
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
│   ├── build_exe.ps1
│   └── LAUNCHER_SETUP.md
│
├── .github/workflows/         # CI/CD automation
│   └── build.yml
│
├── Documentation              # Guides
│   ├── README.md              # This file
│   ├── SETUP_GUIDE.md         # Complete setup & deploy guide
│   ├── QUICKSTART.md          # Developer quick start
│   └── REPO_STRUCTURE.md      # Detailed structure
│
└── .venv/                     # Created automatically on first run
```

**Hidden files**: `.archium/`, `.venv/`, `.git/` on Windows are hidden from normal view

## Development 🛠️

### Requirements for Developers
- Python 3.6+ (to build exe locally)
- Git (to clone and push code)

### Making Changes

1. Edit files in `.archium/` folder
2. Test: `python .archium/archium.py`
3. Commit: `git add . && git commit -m "message"`
4. Push: `git push origin main`

### Building the Executable (Optional)

GitHub Actions automatically builds the exe when you create a release. To build locally:

```bash
cd scripts

# Windows PowerShell
./build_exe.ps1

# Windows Command Prompt
build_exe.bat
```

## Publishing Updates 📤

Only two steps needed:

### 1. Update Version
Edit `.archium/version.json`:
```json
{
  "version": "2.0.1",
  "last_updated": "2026-04-11T14:00:00"
}
```

### 2. Create GitHub Release
1. Go to Releases → Create New Release
2. Tag: `v2.0.1` (MUST match version.json)
3. Add release notes
4. Attach `.zip` with `.archium/` folder + launcher.py
5. GitHub Actions auto-builds exe

**That's it!** Users will get the update automatically when they run Archium.exe.

### Release Archive Contents

Create a `.zip` file with:
```
archium-2.0.1.zip
├── .archium/
│   ├── archium.py
│   ├── version.json (2.0.1)
│   ├── classes_and_funcs/
│   ├── settings/
│   └── db/
├── launcher.py
└── scripts/
```

## How It Works 🔍

### Auto-Bootstrap on First Run

When user runs `Archium.exe`:

1. **Creates Python environment**
   - If `.venv/` doesn't exist, creates it
   - Isolated from system Python

2. **Installs dependencies**
   - Upgrades pip
   - Currently uses only standard library (no external packages needed)

3. **Checks for updates**
   - Reads `.archium/version.json`
   - Queries GitHub API for latest release
   - If newer version: downloads, backs up data, extracts, restores data

4. **Launches application**
   - Runs `archium.py` inside the venv
   - GUI opens in separate window

### File Storage

**Database** (`.archium/db/`)
- One `.txt` file per library
- Pipe-delimited format:
  ```
  title|author|genre|year|length|country|place
  The Hobbit|J.R.R. Tolkien|Fantasy|1937|310|UK|London
  ```

**Settings** (`.archium/settings/settings.json`)
- JSON format with user preferences:
  ```json
  {
    "language": "en",
    "ui_font_size": 10,
    "results_text_size": 9
  }
  ```

## Data Format 💾

### Book Storage
Books are stored in `.archium/db/*.txt` as pipe-delimited values:
```
title|author|genre|year|length|country|place
The Hobbit|J.R.R. Tolkien|Fantasy|1937|310|UK|London
```

### Settings
User preferences in `.archium/settings/settings.json`:
```json
{
  "language": "en",
  "ui_font_size": 10,
  "results_text_size": 9,
  "last_updated": "2026-04-11T14:00:00"
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
