# Archium Launcher - Setup Instructions

## Step 1: Configure GitHub Repository

Edit `launcher.py` and change this line to your GitHub repository:
```python
self.github_repo = "your-username/archium"  # Change this to your repo
```

Example:
```python
self.github_repo = "johnsmith/archium"
```

## Step 2: Create GitHub Release

1. Go to your GitHub repository
2. Create a release with:
   - Tag name: `v2.0.0` (or your current version)
   - Release title: `Archium 2.0.0`
   - Attach a `.zip` file containing all app files including:
     - archium.py
     - classes_and_funcs/
     - settings/
     - db/
     - launcher.py
     - version.json

Example file structure in zip:
```
archium-2.0.0.zip
├── archium.py
├── launcher.py
├── version.json
├── classes_and_funcs/
│   ├── book.py
│   └── library.py
├── settings/
│   └── settings.json
└── db/
    └── (library files)
```

## Step 3: Install PyInstaller

```powershell
pip install pyinstaller
```

## Step 4: Compile Launcher to EXE

Navigate to your project directory and run:

```powershell
cd c:\All\Code\My_Projects\Python\Archium_2.0.0

pyinstaller --onefile --icon=app_icon.ico launcher.py --name=Archium
```

Optional parameters:
- `--icon=app_icon.ico` - Add an icon to your exe (create or provide an .ico file)
- `--windowed` - Hide the console window (add if you don't want console output)

The exe will be in `dist/Archium.exe`

## Step 5: Test the Setup

1. Copy `Archium.exe` to your project root
2. Run `Archium.exe`
3. It should:
   - Check for updates from GitHub
   - Update if new version found
   - Launch archium.py
   - Preserve db/ and settings/ folders during updates

## How It Works

**Update Flow:**
1. Launcher checks GitHub releases API for latest version
2. Compares local version with GitHub version using semantic versioning
3. If update available:
   - Downloads release zip file
   - Creates backup of db/ and settings/ folders
   - Extracts new files
   - Restores db/ and settings/ from backup
   - Saves new version to version.json
4. Runs archium.py

**Backup & Restore:**
- Important files (db/, settings/, version.json) are backed up before update
- If update fails, files are restored from backup
- Backup directory is not cleaned until next update

## Troubleshooting

**"No release files found"**
- The GitHub release must have a .zip attachment
- Check the release on github.com/your-repo/releases

**"Could not reach GitHub"**
- User has no internet connection
- GitHub is temporarily unavailable
- Launcher will run existing archium.py anyway

**"Update check failed"**
- Check launcher.py logs for error message
- Verify github_repo variable is correct

## Version Numbering

Uses semantic versioning (e.g., 2.0.0):
- Major.Minor.Patch
- Launcher compares by numeric parts
- Make sure GitHub tag is like `v2.0.1` (v prefix is stripped)
