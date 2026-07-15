# Building `KronoCTF.exe` on Windows

This produces a standalone Windows executable so students can run the game without
installing Python. **It must be built on a Windows PC** — PyInstaller cannot
cross-compile from macOS/Linux.

> If your students already have Python 3, you don't need this at all — they can just
> double-click `start.bat` (see [README.md](README.md)). Build the `.exe` only if you want
> a no-Python-needed download.

## Prerequisites

- A **Windows 10/11** PC.
- **Python 3** from <https://www.python.org/downloads/> — during install tick
  **"Add Python to PATH"**.
- A copy of this **KronoCTF project folder** on that PC.

## Steps

1. **Open a terminal in the project folder.**
   In File Explorer open the folder, click the address bar, type `cmd`, press Enter.

2. **(Recommended) create a clean build environment:**
   ```
   python -m venv build-env
   build-env\Scripts\activate
   ```

3. **Install PyInstaller:**
   ```
   pip install pyinstaller
   ```

4. **Build the exe** (windowed = no console window; *onedir* is the default and is
   preferred over `--onefile` — it starts faster and trips antivirus less often):
   ```
   pyinstaller --noconfirm --windowed --name KronoCTF main.py
   ```
   Output appears in `dist\KronoCTF\` — `KronoCTF.exe` plus an `_internal` folder.

5. **Ship the WPILib project next to the exe.** Copy the folder
   `levels\challenges\Challenges`  →  `dist\KronoCTF\Challenges`
   so that `Challenges` sits **right beside** `KronoCTF.exe`.

   This is required: the Easy/Medium/Hard challenges open a real, editable WPILib project
   in VS Code, so it can't live inside the exe. The app is already written to look for a
   `Challenges` folder next to the executable when it's running as a build (see the
   `sys.frozen` branch in `levels/challengelevel.py`).

6. **Distribute.** Zip the whole `dist\KronoCTF\` folder. Students unzip it and
   double-click `KronoCTF.exe`.

## Verify (on the Windows PC)

1. Double-click `dist\KronoCTF\KronoCTF.exe` → the login window appears.
2. Log in and progress to the **Easy** challenge → click **📂 Open in VS Code** →
   it opens the sibling `Challenges` project (needs WPILib VS Code installed) and
   "Simulate Robot Code" works.

## Optional

- **App icon:** add `--icon KronoCTF.ico` to the build command in step 4.
- **Single-file build:** use `--onefile --windowed` for one `.exe` instead of a folder.
  Trade-offs: slower startup (it unpacks to a temp dir each launch) and more antivirus
  false-positives. `--onedir` (the default) is the safer choice.

## Troubleshooting

- **"Windows protected your PC" / SmartScreen:** unsigned exes trigger this. Click
  *More info → Run anyway*, or code-sign the exe if distributing widely.
- **Antivirus quarantines the exe:** a known PyInstaller false-positive, more common with
  `--onefile`. Prefer `--onedir`, or add an AV exception.
- **Easy/Medium/Hard can't find the project:** you skipped step 5 — the `Challenges`
  folder must sit next to `KronoCTF.exe`.
