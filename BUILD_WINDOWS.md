# Building the KronoCTF Windows installer (`KronoCTF-Setup.exe`)

This produces a real installer — students download `KronoCTF-Setup.exe`, run it, get a
**Desktop shortcut**, and double-click to play. **No Python needed on their machines.**

Two tools do the work:
1. **PyInstaller** turns the Python game into a standalone app folder.
2. **Inno Setup** wraps that folder into an installer with shortcuts + an uninstaller.

> **Must be done on a Windows PC.** PyInstaller can't cross-compile from macOS, and Inno
> Setup is Windows-only. You only build once; students never need Python.

---

## One-time setup on the build PC

- **Python 3** — <https://www.python.org/downloads/> (tick *"Add Python to PATH"*).
- **Inno Setup** — <https://jrsoftware.org/isdl.php> (free).
- A copy of this **KronoCTF project folder**. Best from a **clean checkout** (no `build/`
  or `.gradle/` folders inside `levels\challenges\Challenges`, so the bundle stays small).

---

## Step 1 — Build the app with PyInstaller

Open a terminal in the project folder (in Explorer: click the address bar, type `cmd`,
Enter), then:

```
pip install pyinstaller
pyinstaller KronoCTF.spec
```

This uses the committed [`KronoCTF.spec`](KronoCTF.spec) and produces `dist\KronoCTF\` —
`KronoCTF.exe` plus an `_internal\` folder that contains the bundled WPILib project.

> The spec bundles `levels\challenges\Challenges` into the app. At first launch the app
> copies it to a **writable** folder, `%USERPROFILE%\.kronoctf\Challenges` — because the
> install folder (Program Files) is read-only, but the student needs to edit the project
> and gradle needs to build it. This is handled by `robotproject.ensure_ready()`; you don't
> do anything for it.

## Step 2 — Build the installer with Inno Setup

- **GUI:** open [`installer\KronoCTF.iss`](installer/KronoCTF.iss) in Inno Setup, then
  **Build → Compile**.
- **Command line:** `iscc installer\KronoCTF.iss`

Output: **`installer\Output\KronoCTF-Setup.exe`** — that's the file you distribute.

## Step 3 — Distribute

Give students `KronoCTF-Setup.exe`. They run it → it installs and creates a Desktop (and
Start-Menu) shortcut → they double-click the shortcut → the game starts. On the very first
run it unpacks the robot project to `%USERPROFILE%\.kronoctf\Challenges`.

---

## Verify (on the Windows PC)

1. After Step 1: `dist\KronoCTF\KronoCTF.exe` exists, and `dist\KronoCTF\_internal\Challenges\`
   contains the WPILib project.
2. After Step 2: `installer\Output\KronoCTF-Setup.exe` exists.
3. Run the installer → a **KronoCTF** shortcut appears on the Desktop.
4. Launch it → the login window opens; `%USERPROFILE%\.kronoctf\Challenges` gets created.
5. Progress to **Easy** → click **📂 Open in VS Code** → it opens
   `%USERPROFILE%\.kronoctf\Challenges` and *"Simulate Robot Code"* works.

## Requirements for students

- **WPILib VS Code** must be installed (the robot challenges open the project in it and run
  *"Simulate Robot Code"*). Nothing else — Python is bundled inside the app.

## Optional

- **App icon:** put a `KronoCTF.ico` next to `KronoCTF.spec`, set `icon='KronoCTF.ico'` in
  the spec's `EXE(...)`, and add `SetupIconFile=..\KronoCTF.ico` under `[Setup]` in the
  `.iss`.
- **Version bump:** edit `AppVersion` in the `.iss`.

## Troubleshooting

- **"Windows protected your PC" / SmartScreen** on the setup or the app: unsigned
  installers trigger this. Click *More info → Run anyway*, or code-sign if distributing
  widely.
- **Antivirus flags the exe:** a known PyInstaller false-positive; add an exception, or
  code-sign.
- **Easy/Medium/Hard can't open the project:** delete `%USERPROFILE%\.kronoctf\Challenges`
  and relaunch to force a fresh unpack; confirm Step 1 bundled `_internal\Challenges\`.
