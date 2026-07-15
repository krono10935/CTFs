"""Level base class: the shared 'chat with the warden' screen and machinery.

Subclasses live in their own files (level1.py, level2.py, ...). A single-step
level just declares its content and (optionally) overrides `is_correct` /
`fail_response`. A multi-step level overrides `submit` to drive its own flow.
"""

import re
import tkinter as tk

from theme import (
    ACCENT, ACCENT_DARK, BG_SOFT, BG_WHITE, INK, MUTED,
    STUDENT_BUBBLE, WARDEN_BUBBLE,
)

# Matches  System.out.println( <inner> )  with optional trailing ';'.
# Group 1 captures the raw argument text between the parentheses.
_PRINTLN_RE = re.compile(
    r"^\s*system\s*\.\s*out\s*\.\s*println\s*\(\s*(.*?)\s*\)\s*;\s*$",
    re.IGNORECASE | re.DOTALL,
)


class Level:
    """Shared screen + answer machinery for a single level."""

    number = 0
    title = "Level"
    greeting = ""                 # warden's opening line
    approval = "The warden nods."  # shown when the answer is accepted
    takeaway_code = ""            # snippet shown in the completion popup
    takeaway_text = ""            # explanation shown in the completion popup

    def __init__(self, app):
        self.app = app
        self.fails = 0
        self.solved = False

    @property
    def display_name(self):
        """Name shown in the header and completion popup (e.g. 'Easy')."""
        return f"Level {self.number}"

    # -- answer parsing helper (shared by all levels) ----------------------
    @staticmethod
    def parse_println(text):
        """Return the inner argument of System.out.println( ... ), or None."""
        match = _PRINTLN_RE.match(text)
        return match.group(1) if match else None

    # -- single-step defaults (override for custom levels) -----------------
    def is_correct(self, text):
        return self.parse_println(text) is not None

    def fail_response(self, fails):
        """Return (message, is_code) for the given cumulative fail count."""
        return ("The warden is unimpressed.", False)

    def decorate_header(self, header):
        """Hook: subclasses may add widgets to the top bar. No-op by default."""

    def submit(self, text):
        """Default single-step evaluation. Multi-step levels override this."""
        if self.is_correct(text):
            self.win()
        else:
            self.fails += 1
            message, is_code = self.fail_response(self.fails)
            self.add_warden(message, code=is_code)

    # -- screen ------------------------------------------------------------
    def build(self):
        app = self.app
        app.clear_container()

        self._build_header()

        # Input area is packed to the bottom FIRST so it always reserves its
        # space; the conversation log then fills whatever remains. (Packing the
        # expanding log first would let it starve a tall input like Level 3's
        # code editor and leave it unmapped.)
        self._build_input(app)

        # Conversation log (the "white box")
        body = tk.Frame(app.container, bg=BG_WHITE)
        body.pack(side="top", fill="both", expand=True)
        self._build_log(body)

        if self.greeting:
            self.add_warden(self.greeting)

    def _build_header(self):
        """Build the dark top bar; calls decorate_header for level extras."""
        app = self.app
        header = tk.Frame(app.container, bg=INK, height=52)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="⚔  The Warden", font=app.f_btn,
                 bg=INK, fg="white").pack(side="left", padx=18)
        tk.Label(header, text=self.display_name, font=app.f_small,
                 bg=INK, fg="#94a3b8").pack(side="right", padx=18)
        # Universal reset control — rebuilds the current level from scratch.
        tk.Button(header, text="⟲ Reset", font=app.f_small, bg=INK,
                  fg="#94a3b8", activebackground=INK, activeforeground="white",
                  relief="flat", bd=0, cursor="hand2",
                  command=self.app.restart_level).pack(side="right", padx=(0, 4))
        self.decorate_header(header)
        return header

    def _build_log(self, parent):
        """Build the read-only conversation log (warden/you bubbles)."""
        app = self.app
        self.log = tk.Text(parent, bg=BG_WHITE, fg=INK, font=app.f_body,
                           wrap="word", relief="flat", padx=18, pady=16,
                           state="disabled", cursor="arrow", height=5,
                           spacing1=4, spacing3=8)
        self.log.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(parent, command=self.log.yview)
        scroll.pack(side="right", fill="y")
        self.log.config(yscrollcommand=scroll.set)

        # Text tags for the two speakers.
        self.log.tag_configure("warden_name", foreground=ACCENT_DARK,
                               font=app.f_small, spacing1=8)
        self.log.tag_configure("warden", background=WARDEN_BUBBLE,
                               foreground=INK, lmargin1=10, lmargin2=10,
                               rmargin=140, font=app.f_body)
        self.log.tag_configure("warden_code", background=WARDEN_BUBBLE,
                               foreground="#0f172a", lmargin1=10, lmargin2=10,
                               rmargin=140, font=app.f_mono)
        self.log.tag_configure("you_name", foreground=MUTED,
                               font=app.f_small, justify="right", spacing1=8)
        self.log.tag_configure("you", background=STUDENT_BUBBLE,
                               foreground=INK, lmargin1=140, rmargin=10,
                               justify="right", font=app.f_body)

    def _make_editor(self, parent, height=8):
        """Return a configured monospace code editor (used by L3 & L4)."""
        app = self.app
        return tk.Text(parent, height=height, font=app.f_mono, wrap="none",
                       bg=BG_WHITE, fg=INK, insertbackground=INK,
                       relief="flat", padx=8, pady=6,
                       highlightbackground="#cbd5e1", highlightthickness=1)

    def _build_input(self, app):
        """Bottom input area. Default: single-line chat bar + Send button.

        Levels needing a different input (e.g. a code editor) override this.
        """
        bar = tk.Frame(app.container, bg=BG_SOFT, padx=12, pady=12)
        bar.pack(side="bottom", fill="x")

        self.entry = tk.Entry(bar, font=app.f_mono, relief="flat",
                              bg=BG_WHITE, fg=INK, insertbackground=INK,
                              highlightbackground="#cbd5e1",
                              highlightthickness=1)
        self.entry.pack(side="left", fill="x", expand=True, ipady=9, ipadx=8)
        self.entry.bind("<Return>", lambda e: self.on_send())
        self.entry.focus_set()

        self.send_btn = app.make_button(bar, "Send", self.on_send)
        self.send_btn.pack(side="right", padx=(10, 0))

    # -- conversation helpers ---------------------------------------------
    def _append(self, name, name_tag, text, text_tag):
        self.log.config(state="normal")
        self.log.insert("end", f"{name}\n", name_tag)
        self.log.insert("end", f" {text} \n", text_tag)
        self.log.insert("end", "\n")
        self.log.config(state="disabled")
        self.log.see("end")

    def add_warden(self, text, code=False):
        self._append("The Warden", "warden_name", text,
                     "warden_code" if code else "warden")

    def add_you(self, text):
        self._append("You", "you_name", text, "you")

    # -- send / evaluate ---------------------------------------------------
    def on_send(self):
        if self.solved:
            return
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self.add_you(text)
        self.submit(text)

    def win(self):
        self.solved = True
        self.add_warden(self.approval)
        self._lock_input()
        self.app.root.after(500, self.show_level_complete)

    def _lock_input(self):
        """Disable input after a win. Overridden by levels with custom input."""
        self.entry.config(state="disabled")
        self.send_btn.config(state="disabled", bg="#94a3b8")

    # -- level complete popup ---------------------------------------------
    def show_level_complete(self):
        app = self.app
        pop = tk.Toplevel(app.root)
        pop.title("Level Complete")
        pop.configure(bg=BG_WHITE)
        pop.resizable(False, False)
        pop.transient(app.root)
        pop.grab_set()

        w, h = 460, 400
        app.root.update_idletasks()
        x = app.root.winfo_rootx() + (app.root.winfo_width() - w) // 2
        y = app.root.winfo_rooty() + (app.root.winfo_height() - h) // 2
        pop.geometry(f"{w}x{h}+{max(x, 0)}+{max(y, 0)}")

        # Accent header band
        band = tk.Frame(pop, bg=ACCENT, height=110)
        band.pack(fill="x")
        band.pack_propagate(False)
        tk.Label(band, text="✓", font=("Segoe UI", 44, "bold"),
                 bg=ACCENT, fg="white").pack(pady=(18, 0))

        tk.Label(pop, text=f"{self.display_name} Complete!", font=app.f_title,
                 bg=BG_WHITE, fg=INK).pack(pady=(22, 6))
        tk.Label(pop, text="You answered the warden in fluent Java.",
                 font=app.f_body, bg=BG_WHITE, fg=MUTED).pack()

        if self.takeaway_code or self.takeaway_text:
            box = tk.Frame(pop, bg=BG_SOFT, padx=16, pady=12)
            box.pack(fill="x", padx=30, pady=20)
            tk.Label(box, text="What you learned", font=app.f_small,
                     bg=BG_SOFT, fg=MUTED).pack(anchor="w")
            if self.takeaway_code:
                tk.Label(box, text=self.takeaway_code, font=app.f_mono,
                         bg=BG_SOFT, fg=ACCENT_DARK).pack(anchor="w",
                                                          pady=(2, 4))
            if self.takeaway_text:
                tk.Label(box, text=self.takeaway_text, font=app.f_small,
                         bg=BG_SOFT, fg=INK, wraplength=380,
                         justify="left").pack(anchor="w")

        # Whether another level follows determines the button label/action.
        has_next = app.has_next_level()

        def do_continue():
            pop.destroy()
            app.advance()

        btn = app.make_button(pop, "Continue  →" if has_next else "Finish",
                              do_continue)
        btn.pack(pady=(0, 8))

        pop.bind("<Return>", lambda e: do_continue())
        pop.bind("<Escape>", lambda e: do_continue())
        btn.focus_set()
