# User Quick Start Guide

## 🚀 Getting Started (Users)

### Easiest Way - No Python Installation Needed

1. **Download/Clone** the repository
2. **Double-click** `Archium.bat`

Done! The batch file will:
- ✅ Detect if Python is installed
- ✅ Automatically download and install Python 3.11 (if needed)
- ✅ Set up the app environment
- ✅ Launch Archium

**No manual steps required.**

### Alternative Ways to Run

#### Method 1: Using the executable
```bash
Archium.exe
```
Requires Python to be already installed on your system.

#### Method 2: Using the batch file (Recommended if Python not installed)
```bash
Archium.bat
```
Automatically handles Python installation.

#### Method 3: Using PowerShell
```powershell
.\Archium.ps1
```
Alternative to batch file for PowerShell users.

#### Method 4: Direct Python (if you have Python installed)
```bash
python launcher.py
```

## 📋 System Requirements

**Minimum:**
- Windows 10 or later
- Internet connection (first run only - to check for updates)

**No need to pre-install:**
- Python (Archium.bat installs it automatically)
- Any libraries or dependencies

## ❓ Frequently Asked Questions

### Q: Do I need Python installed?
**A:** No! If Python isn't installed, `Archium.bat` will automatically download and install Python 3.11 for you.

### Q: Will Archium slow down my computer?
**A:** No. Python is installed in an isolated environment that only Archium uses.

### Q: How much disk space does it need?
**A:** About 200-300 MB for Python + virtual environment. Your book data adds minimal space.

### Q: Can I uninstall it?
**A:** Yes! Just delete the Archium folder. Python installed by Archium can also be uninstalled from Control Panel → Programs → Uninstall a Program.

### Q: Is my data safe?
**A:** Yes! All your book data is stored locally in the `.archium/db/` folder. Nothing leaves your computer.

### Q: Will it work if I'm offline?
**A:** Yes! It only needs internet to check for updates. The app works fine offline.

## 🐛 Troubleshooting

### "Archium.bat won't start"

1. Right-click `Archium.bat`
2. Select "Run as administrator"
3. Click "Yes" when prompted

### "Python won't install"

1. Make sure you have **Administrator** rights
2. Try running `Archium.bat` as administrator (right-click)
3. If that fails:
   - Download Python manually from https://www.python.org/downloads/
   - Make sure to check **"Add Python to PATH"** during installation
   - Then run `Archium.exe`

### "Application won't launch after installation"

1. Check your internet connection
2. Try closing and reopening the application
3. If problem persists, delete the `.venv` folder and try again

### "Updates not working"

1. Check your internet connection
2. Updates are optional - the app works with the current version
3. Try again later

## 📚 Using the Application

Once Archium launches:

1. **Create a Library** - Enter a name and click "Create"
2. **Add Books** - Click "Add Book" and fill in details
3. **Search** - Type in search box and press Enter
4. **Sort** - Use dropdown to sort by any field
5. **Manage** - Edit, delete, or move books between libraries

## 🔄 Updates

Archium automatically checks for updates every time you run it:
- If a new version is found, it's downloaded and installed
- Your books and settings are preserved
- No manual action needed

## 💬 Getting Help

If you encounter issues:

1. Check this troubleshooting section
2. Try running `Archium.bat` as administrator
3. Report issues on GitHub: https://github.com/Primorger/Archium/issues

## ✨ That's It!

You're all set. Just double-click `Archium.bat` and enjoy managing your library!

---

**Made simple so you can focus on your books.**
