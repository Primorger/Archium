@echo off
REM Build script to compile launcher.py to Archium.exe
REM Run from: scripts\build_exe.bat

cd ..

echo.
echo ========================================
echo   Archium Launcher - Build Script
echo ========================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Building Archium.exe...
echo.

REM Build the exe
pyinstaller --noconfirm --onefile --console --icon=Archium.ico launcher.py --name=Archium --distpath=. --workpath=build --specpath=.

echo.
if exist "Archium.exe" (
    echo ========================================
    echo   Build Successful!
    echo ========================================
    echo.
    echo Archium.exe has been created in the root folder
    echo.
    echo Next Steps:
    echo 1. Verify GitHub repo in launcher.py:
    echo    self.github_repo = "Primorger/Archium"
    echo.
    echo 2. Update version.json to current version
    echo.
    echo 3. Create a GitHub Release with version tag
    echo.
    echo 4. Attach app files as .zip to the release
    echo.
    echo 5. Run Archium.exe to test
    echo.
) else (
    echo Build failed! Check the errors above.
    pause
)

REM Clean up build artifacts (optional)
if exist "build" rmdir /s /q build
if exist "__pycache__" rmdir /s /q __pycache__
if exist "*.spec" del *.spec

pause
