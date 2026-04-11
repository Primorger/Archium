# Archium - User Quick Start Guide

Welcome to **Archium** - a simple, fast library management application for organizing your book collection!

## What You Need

**Minimum Requirements:**
- Windows 10 or later
- ~100 MB free disk space
- Internet connection (for first launch only - optional)

**That's it!** No installation needed.

## Getting Started

### Option 1: Using Archium.bat (Recommended for most users)

1. **Download** the repository from GitHub or extract the ZIP file
2. **Double-click `Archium.bat`**
   - If Python is not installed, the batch file will automatically install it
   - First run may take 1-2 minutes
   - Subsequent runs will be instant
3. **Archium window opens** - Ready to use!

**Advantages:**
- Simplest method
- Automatic Python installation if needed
- Works even if Python is not on your computer

### Option 2: Using Archium.exe (For users with Python already installed)

1. **Extract the repository** or download the compiled `.exe` from the release page
2. **Double-click `Archium.exe`**
3. **Archium launches immediately**

**Advantages:**
- Fastest startup if Python is already installed
- No setup needed

### Option 3: Using Archium.ps1 (PowerShell - Advanced users)

1. **Right-click on `Archium.ps1`** → **Run with PowerShell**
   - If prompted about execution policy, select **"Yes to All"**
2. **Archium launches**

## First Time Setup

When you first launch Archium:
1. **It checks for updates** (connects to GitHub - this is optional and takes ~2 seconds)
2. **Creates local data folders** automatically
3. **Opens the main window**

That's all! No configuration needed.

## Basic Usage

### Creating a Library

1. Click **"New Library"** button (left panel)
2. Enter a name (e.g., "Sci-Fi", "My Favorites", "To Read")
3. **Done!** Your library is created and appears in the list

### Adding Books

1. **Double-click a library** to select it (or single-click then wait)
2. Click **"Add Book"**
3. Fill in the book details:
   - **Title** - Book name
   - **Author** - Writer's name
   - **Genre** - Category (Sci-Fi, Mystery, etc.)
   - **Year** - Publication year
   - **Length** - Page count or duration
   - **Country** - Country of origin
   - **Place** - Publishing location
4. Press **Enter** after each field or click the button to save
5. **Book added!** You'll see it immediately in the list

*Tip: Only Title is required. Other fields can be left empty or filled with "N/A"*

### Finding Books

**Search:**
1. Type in the **Search box** (top of the right panel)
2. Press **Enter** or click outside
3. Results appear sorted by relevance

**Examples:**
- Search "Harry" → finds all books with "Harry" in title/author
- Search "1997" → finds all books from 1997
- Search "Tolkien" → finds all Tolkien books

**Sort:**
- Use the **"Sort by"** dropdown to arrange by:
  - Title, Author, Genre, Year, Length, Country, or Place

### Managing Books

**Edit a book:**
1. Select the book in results
2. Click **"Edit Book"**
3. Modify any field
4. Click the button to save

**Move a book:**
1. Select the book
2. Click **"Move Book"**
3. Choose destination library
4. Double-click or click to move

**Delete a book:**
1. Select the book
2. Click **"Delete Book"**
3. Confirm deletion

**Clear results:**
- Click **"Clear Results"** to reset the view

## Settings

Click **"Settings"** to customize:
- **Language** - Switch between English and Bulgarian
- **UI Text Size** - Adjust interface text size (8-16)
- **Results Text Size** - Adjust book list text size (8-16)

Changes to text size apply immediately. Language changes require restart.

## Where Your Data Is Stored

Your libraries and settings are stored locally (never sent anywhere):
- **Libraries**: `.archium/db/` folder (one file per library)
- **Settings**: `.archium/settings/settings.json` (your preferences)
- **Version**: `.archium/version.json` (current app version)

These are created automatically in the same folder as `Archium.bat`.

## Updates

Archium automatically checks for new versions:
- **On startup**: Looks for available updates on GitHub
- **If update available**: Notifies you with a message
- **Your choice**: Accept or skip (automatic rollback if something goes wrong)

Updates are safe - they backup your old version before updating and restore it if there's any issue.

## Troubleshooting

### "Python not found" error
- **Solution**: Run `Archium.bat` instead of `Archium.exe`
- The batch file will automatically install Python for you

### Books not appearing after add
- **Solution**: Make sure you selected a library first (double-click it)
- If still not working, restart the application

### Application crashes on startup
- **Solution**: Delete the `.archium` folder and restart
- This resets the app to factory settings (your libraries remain if in separate backups)

### Update failed
- **Solution**: Don't worry! The app automatically restores the previous version
- Try running again - it will attempt the update

### Text is too small/too big
- **Solution**: Open Settings and adjust text size sliders
- Restart app if language settings were changed

### Can't find my library
- **Solution**: Make sure the `.archium` folder wasn't moved or deleted
- Libraries are stored in `.archium/db/` - keep this folder safe!

## Tips & Tricks

- **Multiple libraries**: Create separate libraries for different genres, moods, or purposes
- **Search is smart**: It rates matches - exact title matches appear first
- **No internet required**: After first launch, Archium works completely offline
- **Portable**: The entire app can be moved to a USB drive and run from any Windows computer
- **Backup**: Copy the entire folder to create a backup (includes all your libraries)

## Support & Questions

- Check the **README.md** file for more information
- See **QUICKSTART.md** for fast walkthrough
- For bugs, feature requests, or questions: Check the GitHub issues page

## What's Next?

1. Create your first library ✓
2. Add some books ✓
3. Search and organize ✓
4. Enjoy managing your collection! ✓

---

**Enjoy Archium!** 📚

*Last updated for Archium 2.0.0*
