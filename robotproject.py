"""Locates the live WPILib challenge project, and (in a packaged build) unpacks a
writable copy on first run.

From source the project is edited in-repo. In a packaged (PyInstaller) build the app
is installed read-only, so on first launch we copy the project out to a writable
per-user folder (`~/.kronoctf/Challenges`) that the student edits in VS Code and that
gradle can build in. `~/.kronoctf/` already holds progress.txt, so the game and the
Java side stay colocated.

The template project is shipped two ways for robustness: the installer drops it next
to the exe (`{app}/Challenges`), and PyInstaller also bundles it as data. We copy from
whichever is present.
"""

import shutil
import sys
from pathlib import Path

# Writable per-user copy used by packaged builds.
_PERSIST = Path.home() / ".kronoctf" / "Challenges"
# In-repo project when running from source (this file is at the repo root).
_SOURCE = (Path(__file__).resolve().parent / "levels" / "challenges"
           / "Challenges")
# A file that must exist for a copy to count as complete (guards partial unpacks).
_SENTINEL = Path("src") / "main" / "java" / "frc" / "robot" / "challenges" / "EasySolution.java"


def _is_frozen():
    return getattr(sys, "frozen", False)


def project_dir():
    """Path to the live, editable WPILib project."""
    return _PERSIST if _is_frozen() else _SOURCE


def _bundled_source():
    """Where the packaged project template lives, or None if not found."""
    candidates = [Path(sys.executable).resolve().parent / "Challenges"]  # next to exe
    base = getattr(sys, "_MEIPASS", None)                                # PyInstaller data
    if base:
        candidates.append(Path(base) / "Challenges")
    for c in candidates:
        if (c / _SENTINEL).is_file():
            return c
    return None


def ensure_ready():
    """In a packaged build, copy the project template to the writable spot.

    No-op when running from source, or when the writable copy is already complete.
    Self-healing: a missing/partial `~/.kronoctf/Challenges` is (re)copied.
    """
    if not _is_frozen():
        return
    if (_PERSIST / _SENTINEL).is_file():
        return  # already unpacked and complete

    src = _bundled_source()
    if src is None:
        # Nothing to copy — leave a breadcrumb instead of failing silently.
        try:
            _PERSIST.parent.mkdir(parents=True, exist_ok=True)
            (_PERSIST.parent / "unpack_error.txt").write_text(
                "Could not find the bundled 'Challenges' project next to the exe "
                "or in the PyInstaller bundle.\n", encoding="utf-8")
        except OSError:
            pass
        return

    _PERSIST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        src, _PERSIST, dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("build", ".gradle", "bin"),
    )
