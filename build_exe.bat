@echo off
REM Build script to compile launcher.py to Archium.exe

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
pyinstaller --onefile --console launcher.py --name=Archium --distpath=. --buildpath=build --specpath=.

echo.
if exist "Archium.exe" (
    echo ========================================
    echo   Build Successful!
    echo ========================================
    echo.
    echo Archium.exe has been created
    echo.
    echo Next Steps:
    echo 1. Edit launcher.py and set your GitHub repo:
    echo    self.github_repo = "your-username/archium"
    echo.
    echo 2. Create a GitHub Release with version tag (e.g., v2.0.0)
    echo.
    echo 3. Attach your app files as a .zip to the release
    echo.
    echo 4. Run Archium.exe to test
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
