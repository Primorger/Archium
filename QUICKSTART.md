## Running the Application

### Option 1: Direct Python Execution
```bash
python archium.py
```

### Option 2: Using the Launcher (with auto-updates)
```bash
python launcher.py
```

### Option 3: Using the Executable
```bash
Archium.exe
```

## Building the Executable

### Step 1: Navigate to scripts folder
```bash
cd scripts
```

### Step 2: Run the build script

**Windows Command Prompt:**
```bash
build_exe.bat
```

**Windows PowerShell:**
```powershell
.\build_exe.ps1
```

The `Archium.exe` will be created in the root folder.

## Publishing a New Version

### 1. Update version.json
```json
{
  "version": "2.0.1",
  "last_updated": "2026-04-11T12:00:00"
}
```

### 2. Commit changes to main branch
```bash
git add .
git commit -m "Version 2.0.1"
git push origin main
```

### 3. Create a GitHub Release
- Go to Releases
- Click "Create New Release"
- Tag: `v2.0.1` (matches version.json)
- Title: `Archium 2.0.1`
- Add release notes
- Attach `archium-2.0.1.zip` (see "Create Release Archive" below)

### 4. Create Release Archive
Zip the following files:
```
archium-2.0.1.zip
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

### 5. Users will auto-receive updates when they run Archium.exe

## Development Workflow

1. Make changes to your code
2. Test locally: `python archium.py`
3. Commit: `git commit -m "Your message"`
4. Push: `git push origin main`
5. When ready to release:
   - Update version.json
   - Create GitHub Release with version tag
   - Attach release archive

## Troubleshooting

**Script won't run:**
- Verify Python 3.6+ is installed: `python --version`
- Check tkinter is available: `python -m tkinter`

**Build fails:**
- Install PyInstaller: `pip install pyinstaller`
- Verify all source files exist: `dir` in root folder should show archium.py, launcher.py, classes_and_funcs/, etc.

**Auto-update not working:**
- Check internet connection
- Verify GitHub repo in launcher.py: `self.github_repo = "Primorger/Archium"`
- Ensure release has a `.zip` file attached on GitHub

## CI/CD with GitHub Actions

The `.github/workflows/build.yml` automatically:
1. Builds Archium.exe on every release tag push
2. Creates release archive zip file
3. Uploads both to the GitHub Release

No manual build needed when you create a GitHub Release!
