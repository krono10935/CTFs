# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller build spec for KronoCTF (onedir, windowed).
# Build on Windows:   pyinstaller KronoCTF.spec
# Output:             dist\KronoCTF\  (KronoCTF.exe + _internal\, incl. Challenges)
#
# The WPILib challenge project is bundled as data (absolute path via SPECPATH so it
# can't be silently skipped); on first launch the app copies it to a writable per-user
# folder (see robotproject.ensure_ready()). The installer also ships it next to the exe.

import os

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[(os.path.join(SPECPATH, 'levels', 'challenges', 'Challenges'), 'Challenges')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='KronoCTF',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # GUI app — no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,              # set to 'KronoCTF.ico' to give the app an icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='KronoCTF',
)
