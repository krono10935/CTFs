@echo off
rem ============================================================
rem  KronoCTF launcher (Windows) — double-click to start the game.
rem  Requires Python 3 (with tkinter, which ships with the standard
rem  python.org installer). No pip installs needed.
rem ============================================================

rem Run from this file's own folder so the "levels" package resolves.
cd /d "%~dp0"

rem Prefer the windowless interpreters (pyw / pythonw) so no console
rem window lingers behind the game. "start" launches detached.
where pyw     >nul 2>nul && ( start "" pyw -3 main.py     & exit /b )
where py      >nul 2>nul && ( start "" py -3 main.py      & exit /b )
where pythonw >nul 2>nul && ( start "" pythonw main.py    & exit /b )
where python  >nul 2>nul && ( start "" python main.py     & exit /b )

echo.
echo   Python 3 was not found on this PC.
echo   Install it from https://www.python.org/downloads/
echo   and tick "Add Python to PATH", then double-click this file again.
echo.
pause
