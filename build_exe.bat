@echo off
echo ================================================
echo  Entity Recognition System - EXE Builder
echo ================================================
echo.
echo This script will create a standalone executable (.exe)
echo that users can run without installing Python.
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo Warning: Virtual environment not detected.
    echo It's recommended to run this in a virtual environment.
    echo.
)

REM Install PyInstaller if not present
echo Installing/Checking PyInstaller...
pip install pyinstaller

REM Create dist directory if it doesn't exist
if not exist "dist" mkdir dist

REM Build the executable using the spec file
echo.
echo Building executable...
echo This may take several minutes...
echo.

pyinstaller build.spec

REM Check if build was successful
if exist "dist\Entity Recognition System.exe" (
    echo.
    echo ================================================
    echo SUCCESS! Executable created successfully!
    echo ================================================
    echo.
    echo Moving executable to project root...
    move "dist\Entity Recognition System.exe" "Entity Recognition System.exe"
    echo.
    echo ================================================
    echo Executable ready for distribution!
    echo ================================================
    echo.
    echo Location: %CD%\Entity Recognition System.exe
    dir /b "Entity Recognition System.exe" | for %%A in ("Entity Recognition System.exe") do echo Size: %%~zA bytes
    echo.
    echo Instructions for users:
    echo 1. Copy the .exe file to any Windows computer
    echo 2. Double-click to run (no installation required)
    echo 3. The application will automatically:
    echo    - Check for required components
    echo    - Download necessary models (first run only)
    echo    - Start the web server
    echo    - Open your browser to http://localhost:5000
    echo.
    echo Note: First run may take longer due to model download.
    echo ================================================
) else (
    echo.
    echo ================================================
    echo BUILD FAILED
    echo ================================================
    echo.
    echo Please check the error messages above.
    echo Common issues:
    echo - Missing dependencies
    echo - Insufficient disk space
    echo - Antivirus blocking the build
    echo.
)

echo Press any key to exit...
pause >nul