"""Generates the 100-page "book" for the Medium WPILIB challenge.

Mirrors make_files.py: a small, idempotent generator. It writes book.txt into the
WPILib project's deploy directory (the same folder as example.txt), where the Java
harness reads it in simulation via Filesystem.getDeployDirectory().

Format: 100 pages joined by a sentinel delimiter line so a page may span multiple
lines (the riddle page does). The Java side splits on the same delimiter.

    page0<NL>~~~<NL>page1<NL>~~~<NL>...<NL>page99

98 pages are garbage word-salad; two are real. Reproducible (fixed RNG seed).
Run:  python make_book.py
"""

import random
from pathlib import Path

# Same deploy dir the WPILib example.txt lives in.
DEPLOY_DIR = (Path(__file__).resolve().parent / "levels" / "challenges" /
              "Challenges" / "src" / "main" / "deploy")
BOOK_FILE = DEPLOY_DIR / "book.txt"

PAGE_COUNT = 100
DELIM = "~~~"            # sentinel line between pages
SEED = 1114             # fixed so the book is identical every run

# The two real pages, and where they hide in the 100 (non-obvious, not first/last).
FIRST_TWO_INDEX = 42
RIDDLE_INDEX = 73

FIRST_TWO_PAGE = (
    'The first word is "Swerve". The second word is "Drive". '
    'The third word is hidden.'
)

# Acrostic: the first letter of each line spells KINEMATICS.
RIDDLE_PAGE = "\n".join([
    "Know the path before the wheels are turned,",
    "In angles, arcs, and headings it is learned.",
    "No mass, no motor, and no force applied —",
    "Each pose and heading carefully implied.",
    "Motion described by geometry alone,",
    "A robot's place from wheel speeds can be known.",
    "Track only where it goes, not why it fights,",
    "Ignore the push; just plot the turns and flights.",
    "Compute the vectors; let the forces be.",
    "So name this study — movement's geometry.",
])

# Plain word pool for the garbage pages. Deliberately excludes anything that could
# be mistaken for the answer (swerve, drive, kinematics) or the delimiter.
_WORDS = (
    "gear bolt flux servo cache widget lumen ferrite gasket relay quartz "
    "cobalt lattice photon ember drift signal token amber vellum cinder "
    "moss thistle harbor plume ledger vertex marrow onyx cipher basalt "
    "willow tundra pixel rivet cargo mangle fathom borax dapple ripple "
    "murmur lantern cobweb bramble kettle saffron velvet gravel pumice "
    "hollow beacon copper meadow orchid pebble sprocket tunnel bishop"
).split()


def _garbage_page(rng):
    """One long single line of random word-salad."""
    n = rng.randint(45, 70)
    return " ".join(rng.choice(_WORDS) for _ in range(n))


def build_pages():
    """Return the list of 100 page strings (deterministic)."""
    rng = random.Random(SEED)
    pages = [_garbage_page(rng) for _ in range(PAGE_COUNT)]
    pages[FIRST_TWO_INDEX] = FIRST_TWO_PAGE
    pages[RIDDLE_INDEX] = RIDDLE_PAGE
    return pages


def is_generated():
    return BOOK_FILE.exists()


def generate():
    DEPLOY_DIR.mkdir(parents=True, exist_ok=True)
    pages = build_pages()
    separator = f"\n{DELIM}\n"
    BOOK_FILE.write_text(separator.join(pages), encoding="utf-8")
    return BOOK_FILE


def ensure_generated():
    """Generate the book only if it isn't already there."""
    if not is_generated():
        generate()
    return BOOK_FILE


if __name__ == "__main__":
    path = generate()
    print(f"Wrote {PAGE_COUNT} pages to {path}")
