"""Locates the live WPILib challenge project, and (in a packaged build) unpacks a
writable copy on first run.

From source the project is edited in-repo. In a PyInstaller build the app is
installed read-only (Program Files), so on first launch we copy the bundled project
out to a writable per-user folder (`~/.kronoctf/Challenges`) that the student edits
in VS Code and that gradle can build in. `~/.kronoctf/` already holds progress.txt,
so the game and the Java side stay colocated.
"""

import shutil
import sys
from pathlib import Path

# Writable per-user copy used by packaged builds (Program Files is read-only).
_PERSIST = Path.home() / ".kronoctf" / "Challenges"
# In-repo project when running from source (this file is at the repo root).
_SOURCE = (Path(__file__).resolve().parent / "levels" / "challenges"
           / "Challenges")


def _is_frozen():
    return getattr(sys, "frozen", False)


def project_dir():
    """Path to the live, editable WPILib project."""
    return _PERSIST if _is_frozen() else _SOURCE


def ensure_ready():
    """In a packaged build, copy the bundled project to the writable spot once.

    No-op when running from source. Safe to call on every launch — it only copies
    if the writable copy doesn't exist yet, so student edits/progress survive.
    """
    if not _is_frozen():
        return
    base = getattr(sys, "_MEIPASS", None)  # where PyInstaller unpacks bundled datas
    if not base:
        return
    src = Path(base) / "Challenges"
    if src.is_dir() and not _PERSIST.exists():
        _PERSIST.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            src, _PERSIST,
            ignore=shutil.ignore_patterns("build", ".gradle", "bin"),
        )
