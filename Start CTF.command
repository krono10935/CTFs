#!/bin/bash
# KronoCTF launcher (macOS) — double-click in Finder to start the game.
# Requires Python 3 (with tkinter). Mainly for dev testing; students run start.bat.

cd "$(dirname "$0")" || exit 1

if command -v python3 >/dev/null 2>&1; then
  exec python3 main.py
fi

osascript -e 'display alert "Python 3 not found" message "Install Python 3 to run KronoCTF (https://www.python.org/downloads/)."'
