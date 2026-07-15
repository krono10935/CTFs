"""Shared base for levels that validate the player's code by really compiling and
running Java (Level 4, Level 5, ...).

A JavaLevel owns the code-editor UI, the static guards, and the compile/run/judge
orchestration. Concrete levels fill in the small hooks:
    _source(code)        -> the full .java source with the player's code injected
    _build_canvas(app)   -> build self.canvas for the visualization
    _render(state)       -> draw a state (initial list, or parsed result order)
    _is_win(order)       -> bool: did the run reach the goal?
    _fail_message()      -> warden line shown when the run ran but didn't win
and set: MAIN_CLASS, array_var, require_loop, initial_state, greeting, EDITOR_LABEL.
"""

import re
import secrets
import tkinter as tk

import javasandbox
from theme import BG_SOFT, BG_WHITE, MUTED
from levels.base import Level

_JDK_HELP = ("This level runs real Java, but I can't find a JDK (javac). Install "
             "one (e.g. Adoptium Temurin from adoptium.net), or use a JetBrains "
             "IDE's bundled JDK — I'll re-check each time you press Run.")

_NEW_RE = re.compile(r"\bnew\b")
_DECL_RE = re.compile(r"\b(class|interface|enum|void|static|import|package|native)\b")
_RETURN_RE = re.compile(r"\breturn\b")
_SECURITY_RE = re.compile(r"System\s*\.\s*exit|Runtime|ProcessBuilder|\bexec\b"
                          r"|Thread|forName|getClass|reflect|Unsafe")
_LOOP_RE = re.compile(r"\b(for|while)\b")


class JavaLevel(Level):
    MAIN_CLASS = "Level"
    array_var = "arr"
    require_loop = False
    forbid_new = True
    GEOMETRY = "780x680"
    EDITOR_LABEL = "Your code:"

    def __init__(self, app):
        super().__init__(app)
        self.nonce = "RESULT_" + secrets.token_hex(4)

    # -- layout ------------------------------------------------------------
    def build(self):
        app = self.app
        app.clear_container()
        app.root.geometry(self.GEOMETRY)

        self._build_header()
        self._build_input(app)     # editor + Run, packed to the bottom
        self._build_canvas(app)    # visualization, just above the editor

        body = tk.Frame(app.container, bg=BG_WHITE)
        body.pack(side="top", fill="both", expand=True)
        self._build_log(body)

        if self.greeting:
            self.add_warden(self.greeting)
        if javasandbox.find_jdk() is None:
            self.add_warden(_JDK_HELP)

        self._render(self.initial_state)

    def _build_input(self, app):
        panel = tk.Frame(app.container, bg=BG_SOFT, padx=12, pady=10)
        panel.pack(side="bottom", fill="x")

        tk.Label(panel, text=self.EDITOR_LABEL, font=app.f_small, bg=BG_SOFT,
                 fg=MUTED).pack(anchor="w")

        self.editor = self._make_editor(panel, height=7)
        self.editor.pack(fill="x", pady=(4, 8))
        self.editor.focus_set()

        row = tk.Frame(panel, bg=BG_SOFT)
        row.pack(fill="x")
        self.hint = tk.Label(row, text="", font=app.f_small, bg=BG_SOFT,
                             fg=MUTED)
        self.hint.pack(side="left")
        self.run_btn = app.make_button(row, "Run  ▶", self.on_run)
        self.run_btn.pack(side="right")

    def _lock_input(self):
        self.editor.config(state="disabled")
        self.run_btn.config(state="disabled", bg="#94a3b8")

    # -- static guards -----------------------------------------------------
    @staticmethod
    def _strip(code):
        """Remove // and /* */ comments and string/char literals."""
        out = []
        i, n = 0, len(code)
        while i < n:
            two = code[i:i + 2]
            if two == "//":
                i += 2
                while i < n and code[i] != "\n":
                    i += 1
            elif two == "/*":
                i += 2
                while i < n and code[i:i + 2] != "*/":
                    i += 1
                i += 2
            elif code[i] in ('"', "'"):
                quote = code[i]
                i += 1
                while i < n and code[i] != quote:
                    i += 2 if code[i] == "\\" else 1
                i += 1
            else:
                out.append(code[i])
                i += 1
        return "".join(out)

    def _check(self, code):
        """Return a teaching message if the code is disallowed, else None."""
        if not code.strip():
            return "The editor is empty, write some code."
        if len(code) > 4000:
            return "That's a lot more code than this needs."

        stripped = self._strip(code)

        depth = 0
        for ch in stripped:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth < 0:
                    return "Unbalanced braces — remove the stray `}`."
        if depth != 0:
            return "Unbalanced braces — every `{` needs a matching `}`."

        if self.forbid_new and _NEW_RE.search(stripped):
            return "No `new` here, use the array that's already given."
        if _DECL_RE.search(stripped):
            return "Just write statements — no new declarations of that kind."
        if _RETURN_RE.search(stripped):
            return "No need to `return` — just do the work."
        if _SECURITY_RE.search(stripped):
            return "That command isn't allowed in here."
        if re.search(r"\b" + re.escape(self.array_var) + r"\s*=(?!=)", stripped):
            return (f"The array is `final` — change its elements "
                    f"({self.array_var}[i] = ...), don't replace the whole array.")
        if self.require_loop and not _LOOP_RE.search(stripped):
            return "Use a loop (for or while) to go through the array."
        return None

    # -- compile / run / judge --------------------------------------------
    def _parse_result(self, stdout):
        prefix = self.nonce + ":"
        for line in stdout.splitlines():
            if line.startswith(prefix):
                body = line[len(prefix):].strip()
                return [p for p in body.split(",") if p]
        return None

    @staticmethod
    def _first_error(text):
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for ln in lines:
            if "error:" in ln:
                return ln
        return lines[0] if lines else "unknown error"

    def _oob_message(self):
        n = len(self.initial_state)
        return (f"Out of bounds! Arrays start at index 0 — there are {n} items "
                f"(indices 0..{n - 1}), so the last is {n - 1}.")

    def on_run(self):
        if self.solved:
            return
        code = self.editor.get("1.0", "end")

        problem = self._check(code)
        if problem:
            self.add_warden(problem)
            return

        res = javasandbox.compile_and_run(self._source(code), self.MAIN_CLASS)
        phase = res["phase"]

        if phase == "no_jdk":
            self.add_warden(_JDK_HELP)
            return
        if phase == "compile":
            self.add_warden("Java didn't compile: " +
                            self._first_error(res["stderr"]))
            return
        if res["timed_out"]:
            self.add_warden("Your code took too long — is there an endless loop?")
            return
        if phase == "run":
            if "ArrayIndexOutOfBoundsException" in res["stderr"]:
                self.add_warden(self._oob_message())
            else:
                self.add_warden("Your code crashed: " +
                                self._first_error(res["stderr"]))
            return

        order = self._parse_result(res["stdout"])
        if order is None:
            self.add_warden("I couldn't read the result — did your code finish "
                            "without exiting early?")
            return

        self._render(order)
        if self._is_win(order):
            self.win()
        else:
            self.add_warden(self._fail_message())
