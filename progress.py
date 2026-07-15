"""Shared progress token between the Tkinter app and the WPILIB Java project.

The app writes the current phase whenever it enters a level; it reads it at launch
to resume. The Java `frc.robot.Progress` reads the same file to know which challenge
`Main` should run. Format: a single line holding one of PHASES.
"""

from pathlib import Path

PROGRESS_DIR = Path.home() / ".kronoctf"
PROGRESS_FILE = PROGRESS_DIR / "progress.txt"

# Ordered phases. The first 8 line up 1:1 with GameApp.ALL_LEVELS; DONE = finished.
PHASES = [
    "LEVEL_1", "LEVEL_2", "LEVEL_3", "LEVEL_4", "LEVEL_5",
    "EASY", "MEDIUM", "HARD", "DONE",
]

DEFAULT = "LEVEL_1"


def save(token):
    """Persist the current phase token."""
    if token not in PHASES:
        token = DEFAULT
    PROGRESS_DIR.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(token, encoding="utf-8")


def load():
    """Return the saved phase token, or DEFAULT if missing/invalid."""
    try:
        token = PROGRESS_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return DEFAULT
    return token if token in PHASES else DEFAULT


def token_for(index):
    """Phase token for a level index (clamped into range)."""
    index = max(0, min(index, len(PHASES) - 1))
    return PHASES[index]


def index_for(token):
    """Level index for a phase token; DONE and unknowns clamp to the last level."""
    if token in PHASES:
        idx = PHASES.index(token)
        # DONE has no level screen; resume at the last playable level.
        return min(idx, len(PHASES) - 2)
    return 0
