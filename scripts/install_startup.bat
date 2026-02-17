@echo off
setlocal

echo Installing backlightd to Windows startup...

:: startup folder
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

:: project root
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%\..

:: fallback
if not exist "%PYTHONW%" (
    set PYTHONW=pythonw.exe
)

:: launcher bat path
set LAUNCHER=%STARTUP_FOLDER%\backlightd.bat

echo Creating launcher at:
echo %LAUNCHER%

(
echo @echo off
echo cd /d "%PROJECT_ROOT%\backlightd"
echo start "" "%PYTHONW%" backlightd.py
exit
) > "%LAUNCHER%"

echo.
echo backlightd installed successfully.
echo It will run automatically on startup.
echo.

pause
