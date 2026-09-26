# Archium 📚

**Archium** is a library management helper application built with Python and Tkinter. Run `Archium.bat` to install Python if needed, or run `Archium.exe` when Python is already installed.

## ⚡ Quick Start (Users)

### Option 1: **Recommended - Just run the batch file**

```bash
Archium.bat
```

**That's it!** The batch file will:
- ✅ Check if Python is installed
- ✅ Automatically install Python if needed
- ✅ Start the launcher and check for updates
- ✅ Launch the application

### Option 2: If you have Python already installed

```bash
git clone https://github.com/Primorger/Archium.git
cd Archium
Archium.exe
```

**No Python?** Use Option 1. `Archium.bat` installs Python before starting Archium.

## Features ✨

- 🔍 **Full-text search** across all book attributes (title, author, genre, year, etc.)
- 📖 **Book management** - Add, edit, delete, and move books between libraries
- 💾 **Persistent storage** - Books stored in `.archium/db/` with your data safe
- 🌍 **Multi-language support** - English and Bulgarian
- ⚙️ **Settings** - Customizable UI font size and results text size
- 🔄 **Auto-update** - Automatically checks GitHub for new versions
- 🎨 **Modern UI** - Tkinter ttk widgets for native look

## Development

```bash
cd .archium
python archium.py
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
├── launcher.py                # Update checker and application launcher
│
├── .archium/                  # ← Hidden app wrapper
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

On Windows, `.archium/` and `.git/` are hidden by default.

## Development 🛠️

### Requirements for Developers
- Python 3.8+ (to run the launcher and build the exe locally)
- Git (to clone and push code)

### Making Changes

1. Edit files in `.archium/` folder
2. Test from the app directory:
  ```powershell
  cd .archium
  python archium.py
  ```
3. Review `git status` and stage only intended source files, not local `db/` or `settings/` data
4. Commit and push the changes to `main`

### Building the Executable (Optional)

GitHub Actions automatically builds the exe when you create a release. To build locally:

```bash
cd scripts

# Windows PowerShell
./build_exe.ps1

# Windows Command Prompt
build_exe.bat
```

Run the updater tests with `python -m unittest discover -s tests -v` from the repository root.

## Publishing a Release

1. Set the version in `.archium/version.json` to the release number without a `v` prefix, for example `2.1.1`.
2. Run the tests from the repository root:
   ```powershell
   python -m unittest discover -s tests -v
   ```
3. Review `git status` and stage only the intended source, test, and documentation changes. Do not stage local `db/` or `settings/` data. Then commit and push to `main`:
   ```powershell
   git add <intended paths>
   git commit -m "Release v2.1.1"
   git push origin main
   ```
4. Create and push a tag whose version matches `version.json`:
   ```powershell
   git tag v2.1.1
   git push origin v2.1.1
   ```
5. GitHub Actions runs on the pushed tag, builds `Archium.exe`, creates the app ZIP, and publishes both as release assets. No manual ZIP upload is needed.
6. Check the Actions run and the GitHub release. Confirm it contains `Archium.exe` and `archium-v2.1.1.zip` before announcing the release.

Users receive the update the next time they launch Archium.

### Release Archive Contents

GitHub Actions creates a `.zip` file containing the application files (not user data):
```
archium-v2.1.1.zip
├── archium.py
├── languages.json
├── version.json
└── classes_and_funcs/
```

## How It Works 🔍

### Startup and Updates

When user runs `Archium.exe`:

1. **Checks for updates**
   - Reads `.archium/version.json`
   - Queries GitHub API for latest release
  - If newer version: validates and stages it, preserving `db/` and `settings/`

2. **Launches the application**
  - Runs `.archium/archium.py` from its application directory
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

## Supported Languages 🌐

- **English** (en)
- **Bulgarian** (bg)

Translations are stored in `.archium/languages.json`. Add a language there using the same keys as `en` and `bg`.

## Troubleshooting 🔧

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

## Contributing 🤝

Feel free to fork and submit pull requests!

## License 📄

This project is open source. Feel free to use and modify.

## Support 💬

For issues and questions, please use GitHub Issues.

---

**Made with ❤️ for book lovers**
