"""Level 3 — The Gauntlet.

The player writes ONE if/else script that runs every turn. Each turn the warden
declares  wardenDirection = "right"  (or "left"); the script must print `true` to
go right or `false` to go left. A wrong turn springs a trap — the player rewrites
(their script is preserved) and tries a fresh random gauntlet.

Target solution (whitespace-flexible; the full System.out.println is required):

    if (wardenDirection == "right") {
        System.out.println(true);
    } else {
        System.out.println(false);
    }
"""

import random
import re
import tkinter as tk

from theme import ACCENT, BG_SOFT, INK, MUTED
from levels.base import Level

# if ( wardenDirection == "<cond>" ) { <then> } [ else { <else> } ]
_BLOCK_RE = re.compile(
    r'if\s*\(\s*wardenDirection\s*==\s*"([^"]*)"\s*\)\s*'
    r'\{([^{}]*)\}'
    r'(?:\s*else\s*\{([^{}]*)\})?',
    re.IGNORECASE | re.DOTALL,
)
# A full print statement: System.out.print / println ( <arg> )
_FULL_PRINT_RE = re.compile(
    r'system\s*\.\s*out\s*\.\s*print(?:ln)?\s*\(\s*(.*?)\s*\)',
    re.IGNORECASE | re.DOTALL,
)
# Any print-like call (used to detect the `print(...)` shorthand).
_ANY_PRINT_RE = re.compile(r'\bprint(?:ln)?\s*\(', re.IGNORECASE)


class Level3(Level):
    number = 3
    title = "The Gauntlet"
    N_TURNS = 4
    greeting = (
        'The warden sets a gauntlet. Each turn it declares wardenDirection = '
        '"right" or "left". Write ONE script that prints true to go right, or '
        "false to go left — then step through the turns. Survive "
        f"{N_TURNS} turns. Use the full System.out.println( ... ), not print."
    )
    approval = "The corridor falls silent. Your script guided you through. The way is clear."
    takeaway_code = 'if (cond) { ... } else { ... }'
    takeaway_text = ("if / else runs different code depending on a condition. "
                     '== compares values — here it steered you each turn.')

    def __init__(self, app):
        super().__init__(app)
        self.in_gauntlet = False
        self.turns = []
        self.turn_index = 0
        self.match = None

    # -- header progress chip ---------------------------------------------
    def decorate_header(self, header):
        self.progress_label = tk.Label(
            header, text=f"Survived 0/{self.N_TURNS}", font=self.app.f_mono,
            bg=INK, fg=ACCENT)
        self.progress_label.pack(side="right", padx=18)

    def _update_progress(self):
        self.progress_label.config(
            text=f"Survived {self.turn_index}/{self.N_TURNS}")

    # -- code editor input (replaces the single-line chat bar) ------------
    def _build_input(self, app):
        panel = tk.Frame(app.container, bg=BG_SOFT, padx=12, pady=10)
        panel.pack(side="bottom", fill="x")

        tk.Label(panel, text="Your script (runs every turn):",
                 font=app.f_small, bg=BG_SOFT, fg=MUTED).pack(anchor="w")

        self.editor = self._make_editor(panel, height=8)
        self.editor.pack(fill="x", pady=(4, 8))
        self.editor.focus_set()

        row = tk.Frame(panel, bg=BG_SOFT)
        row.pack(fill="x")
        self.hint = tk.Label(row, text="", font=app.f_small, bg=BG_SOFT,
                             fg=MUTED)
        self.hint.pack(side="left")
        self.turn_btn = app.make_button(row, "Next turn  ▶", self.on_next_turn)
        self.turn_btn.pack(side="right")

    def _lock_input(self):
        self.editor.config(state="disabled")
        self.turn_btn.config(state="disabled", bg="#94a3b8")

    # -- interpreter (pure helpers) ---------------------------------------
    @staticmethod
    def _parse(script):
        return _BLOCK_RE.search(script)

    @staticmethod
    def _branch_output(body):
        """Return 'true'/'false' printed by a branch, else None."""
        if not body:
            return None
        m = _FULL_PRINT_RE.search(body)
        if not m:
            return None
        arg = m.group(1).strip().strip('"').strip("'").lower()
        return arg if arg in ("true", "false") else None

    def _run(self, match, direction):
        cond, then_body, else_body = match.group(1), match.group(2), match.group(3)
        body = then_body if direction == cond else else_body
        return self._branch_output(body)

    @staticmethod
    def _has_shorthand_print(script):
        full = len(_FULL_PRINT_RE.findall(script))
        total = len(_ANY_PRINT_RE.findall(script))
        return total > full

    def _validate(self, script):
        if self._has_shorthand_print(script):
            return ("print is shorthand — write it in full: "
                    "System.out.println( ... );")
        if self._parse(script) is None:
            return ('The warden waits. Write an if/else that checks '
                    'wardenDirection == "right".')
        return None

    def _make_sequence(self):
        while True:
            seq = [random.choice(("right", "left")) for _ in range(self.N_TURNS)]
            if "right" in seq and "left" in seq:
                return seq

    # -- turn flow ---------------------------------------------------------
    def on_next_turn(self):
        if self.solved:
            return

        if not self.in_gauntlet:
            script = self.editor.get("1.0", "end")
            problem = self._validate(script)
            if problem:
                self.add_warden(problem)
                return
            self.match = self._parse(script)
            self.turns = self._make_sequence()
            self.turn_index = 0
            self.in_gauntlet = True
            self.editor.config(state="disabled")
            self._update_progress()

        direction = self.turns[self.turn_index]
        self.add_warden(f'wardenDirection = "{direction}";', code=True)

        out = self._run(self.match, direction)
        if out is None:
            self.add_warden("script did not respond.")
        else:
            self.add_warden(f"script told me to go right: {out}")

        survived = ((direction == "right" and out == "true")
                    or (direction == "left" and out == "false"))
        if not survived:
            self._die(direction, out)
            return

        self.turn_index += 1
        self._update_progress()
        if self.turn_index >= self.N_TURNS:
            self.win()
        else:
            self.add_warden(
                f"You turn {direction}. Safe. "
                f"({self.turn_index}/{self.N_TURNS})")

    def _die(self, direction, out):
        if out is None:
            turned = "didn't turn at all"
        else:
            turned_dir = "right" if out == "true" else "left"
            turned = f"instead turned {turned_dir}"
        self.add_warden(
            f"A trap springs! Oh no — you should have turned {direction}, "
            f"but {turned}.")
        self.add_warden(
            "Rewrite your script and try again. (Your script is preserved.)")
        self.in_gauntlet = False
        self.turn_index = 0
        self.editor.config(state="normal")
        self.turn_btn.config(state="normal")
        self._update_progress()
        self.editor.focus_set()
