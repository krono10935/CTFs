"""Locate and launch the WPILib-flavored VS Code for the challenge screens.

The last levels are solved in a real WPILib project, and "Simulate Robot Code"
only works from the isolated VS Code the WPILib installer ships (bundled with its
own JDK). This module finds that install and opens the project folder focused on a
solution file, with JAVA_HOME pointed at the bundled JDK — the same environment the
WPILib "frccode" desktop shortcut sets up. Falls back to a generic `code` on PATH.

Structured like javasandbox.find_jdk(): probe once, cache, never raise.
"""

import os
import shutil
import subprocess
from pathlib import Path

_cache = "unset"  # "unset" until first probe; then a dict or None


def _wpilib_roots():
    """Yield candidate WPILib per-year install roots, newest first."""
    candidates = []

    # macOS / Linux (and a per-user Windows install): ~/wpilib/<YEAR>
    candidates.append(Path.home() / "wpilib")
    # Windows default: C:\Users\Public\wpilib\<YEAR>
    public = os.environ.get("PUBLIC")
    if public:
        candidates.append(Path(public) / "wpilib")
    candidates.append(Path("C:/Users/Public/wpilib"))

    roots = []
    for base in candidates:
        if not base.is_dir():
            continue
        for child in base.iterdir():
            # Year folders like "2024", "2025", "2026".
            if child.is_dir() and child.name.isdigit():
                roots.append(child)
    # Newest year first.
    roots.sort(key=lambda p: p.name, reverse=True)
    return roots


def _code_cli_in(root):
    """Path to the `code` CLI inside a WPILib install root, or None."""
    exe = ".cmd" if os.name == "nt" else ""
    candidates = [
        # macOS app bundle.
        root / "vscode" / "Visual Studio Code.app" / "Contents" / "Resources"
        / "app" / "bin" / "code",
        # Windows / Linux.
        root / "vscode" / "bin" / ("code" + exe),
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def find_wpilib_vscode(force=False):
    """Return {'code': <cli path>, 'jdk': <jdk home or None>} or None. Cached."""
    global _cache
    if _cache != "unset" and not force:
        return _cache

    result = None
    for root in _wpilib_roots():
        code = _code_cli_in(root)
        if code:
            jdk = root / "jdk"
            result = {"code": str(code),
                      "jdk": str(jdk) if (jdk / "bin").is_dir() else None}
            break

    # Fallback: a generic `code` on PATH (non-standard install).
    if result is None:
        generic = shutil.which("code")
        if generic:
            result = {"code": generic, "jdk": None}

    _cache = result
    return result


def open_in_vscode(folder, file):
    """Open `folder` as the workspace and reveal `file`, in WPILib VS Code.

    Returns True if VS Code was launched, False if it wasn't found. Never raises.
    """
    found = find_wpilib_vscode()
    if not found:
        return False

    env = os.environ.copy()
    if found.get("jdk"):
        env["JAVA_HOME"] = found["jdk"]
        env["PATH"] = str(Path(found["jdk"]) / "bin") + os.pathsep + env.get("PATH", "")

    try:
        subprocess.Popen(
            [found["code"], str(folder), str(file)],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except OSError:
        return False
