# KronoCTF — "The Warden"

A small Tkinter game that teaches Java. Unlock the app with a passphrase, then work
through a series of levels. the last three (Easy/Medium/Hard) are solved inside a real
WPILib robot project in VS Code.

## How to play

1. **Download the installer:**
   [KronoCTF-Setup.exe](https://github.com/krono10935/CTFs/releases/download/ctf1-latest/KronoCTF-Setup.exe)
2. **Run it.** Windows may warn *"Windows protected your PC"* (the app isn't code-signed) -
   click **More info → Run anyway**. It installs just for you, no admin needed.
3. **Launch the game** from the **KronoCTF** shortcut in your Start Menu (or the desktop
   shortcut, if you ticked that box during install).

### For the robot challenges (Easy / Medium / Hard)
These are solved in a real robot project, so you'll also need the **WPILib VS Code** install.
The challenge screens open your solution file in it, and you run *"Simulate Robot Code"* to
check your answer.

### Notes
- First launch generates the level-0 file-hunt folder under your home directory and may take
  a moment.
- Your progress is saved automatically, so you resume where you left off each time you open
  the game.
- Want to replay from the beginning? Click **Start over** on the passphrase screen.

---

## Running from source (developers)
No installer needed — run the Python directly:
- **Windows:** double-click **`start.bat`**
- **macOS:** double-click **`Start CTF.command`**
