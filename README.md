# KronoCTF — "The Warden Only Speaks Java"

A small Tkinter game that teaches Java. Unlock the app with a passphrase, then work
through a series of levels — the last three (Easy/Medium/Hard) are solved inside a real
WPILib robot project in VS Code.

## How to play

**Windows:** double-click **`start.bat`**.

**macOS:** double-click **`Start CTF.command`**.

That's it — no IDE required.

### Requirements
- **Python 3** with `tkinter` (both come with the standard installer from
  [python.org](https://www.python.org/downloads/) — on Windows, tick *"Add Python to
  PATH"*). The game uses only the Python standard library, so there is nothing to `pip
  install`.
- For the **Easy/Medium/Hard** robot challenges: the **WPILib** VS Code install (the
  challenge screens open your solution file in it and you run *"Simulate Robot Code"*).

### Notes
- First launch generates the level-0 file-hunt folder under your home directory and may
  take a moment.
- Progress is saved to `~/.kronoctf/progress.txt`, so you resume where you left off (this
  file is also how the WPILib project knows which challenge to run).
