"""
CTF: "The Warden Only Speaks Java"

A Python (Tkinter) game that teaches Java. Students unlock the app with a known
password, then progress through levels, each teaching a piece of Java syntax.

This file is the ENGINE only:
  * GameApp — owns the window, shared styling, the password gate, and level
              progression.

The levels themselves live in the `levels/` package (one class per file), and
shared colors/strings live in `theme.py`. To add a level, create
`levels/levelN.py` and append it to `ALL_LEVELS` in `levels/__init__.py`.

Standard library only — run with:  python main.py
"""

import threading
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

import make_files
import progress
import robotproject
from theme import (
    ACCENT, ACCENT_DARK, APP_TITLE, BG_SOFT, BG_WHITE, DANGER, INK, MUTED,
    PASSWORD,
)
from levels import ALL_LEVELS


class GameApp:
    LEVELS = ALL_LEVELS

    def __init__(self, root: tk.Tk):
        self.root = root
        self.level_index = 0
        self.current_level = None

        root.title(APP_TITLE)
        root.geometry("720x520")
        root.minsize(640, 460)
        root.configure(bg=BG_SOFT)

        # Fonts (created here because they need a live Tk instance).
        self.f_title = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.f_body = tkfont.Font(family="Segoe UI", size=11)
        self.f_small = tkfont.Font(family="Segoe UI", size=9)
        self.f_mono = tkfont.Font(family="Consolas", size=11)
        self.f_btn = tkfont.Font(family="Segoe UI", size=11, weight="bold")

        # Level 0 file hunt: the challenge files live in this folder.
        self.krono_folder = make_files.FOLDER_PATH
        self._files_ready = make_files.is_generated()

        # Root content container that we swap between screens.
        self.container = tk.Frame(root, bg=BG_SOFT)
        self.container.pack(fill="both", expand=True)

        self.build_login_screen()

        # On first launch, generate the challenge files in the background so the
        # 11k file writes don't freeze the window.
        if not self._files_ready:
            threading.Thread(target=self._generate_files, daemon=True).start()

    def _generate_files(self):
        """Runs on a worker thread (filesystem only — no Tk calls here)."""
        try:
            make_files.ensure_generated()
            self.root.after(0, self._on_files_ready)
        except Exception as exc:  # surface failure instead of dying silently
            message = str(exc)
            self.root.after(0, lambda: self._on_files_error(message))

    # -- utilities ---------------------------------------------------------
    def clear_container(self):
        for child in self.container.winfo_children():
            child.destroy()

    def make_button(self, parent, text, command, bg=ACCENT, active=ACCENT_DARK):
        return tk.Button(
            parent, text=text, command=command, font=self.f_btn,
            bg=bg, fg="white", activebackground=active,
            activeforeground="white", relief="flat", bd=0,
            padx=18, pady=8, cursor="hand2",
        )

    # -- login screen ------------------------------------------------------
    def build_login_screen(self):
        self.clear_container()

        wrap = tk.Frame(self.container, bg=BG_SOFT)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(wrap, bg=BG_WHITE, padx=40, pady=36,
                        highlightbackground="#e2e8f0", highlightthickness=1)
        card.pack()

        tk.Label(card, text="🔒", font=("Segoe UI", 34), bg=BG_WHITE).pack()
        tk.Label(card, text="The Warden", font=self.f_title,
                 bg=BG_WHITE, fg=INK).pack(pady=(6, 2))
        tk.Label(card, text="Enter the passphrase to face the warden.",
                 font=self.f_body, bg=BG_WHITE, fg=MUTED).pack(pady=(0, 12))

        # Point the player at the level-0 file hunt.
        tk.Label(card, text="The passphrase hides in one of the files in:",
                 font=self.f_small, bg=BG_WHITE, fg=MUTED).pack()
        tk.Label(card, text=str(self.krono_folder), font=self.f_mono,
                 bg=BG_WHITE, fg=INK, wraplength=340,
                 justify="center").pack(pady=(1, 6))
        self.gen_status = tk.Label(
            card,
            text=("" if self._files_ready
                  else "Preparing challenge files… (first run)"),
            font=self.f_small, bg=BG_WHITE, fg=MUTED)
        self.gen_status.pack(pady=(0, 14))

        self.pw_entry = tk.Entry(card, show="•", font=self.f_body, width=30,
                                 relief="flat", bg=BG_SOFT, fg=INK,
                                 insertbackground=INK)
        self.pw_entry.pack(ipady=8, ipadx=6)
        self.pw_entry.focus_set()
        self.pw_entry.bind("<Return>", lambda e: self.try_login())

        self.login_error = tk.Label(card, text="", font=self.f_small,
                                    bg=BG_WHITE, fg=DANGER)
        self.login_error.pack(pady=(8, 4))

        self.make_button(card, "Enter", self.try_login).pack(pady=(6, 0),
                                                             fill="x")

        # Quiet "start over" so a player can restart from Level 1 without
        # needing to know where progress is stored.
        tk.Button(card, text="Start over", font=self.f_small, bg=BG_WHITE,
                  fg=MUTED, activebackground=BG_WHITE, activeforeground=INK,
                  relief="flat", bd=0, cursor="hand2",
                  command=self._start_over).pack(pady=(12, 0))

    def _start_over(self):
        if messagebox.askyesno(
                "Start over",
                "Reset all progress and start again from the very beginning?"):
            progress.reset()
            self.level_index = 0
            self.login_error.config(
                text="Progress reset — enter the passphrase to begin.",
                fg=MUTED)

    def _on_files_ready(self):
        self._files_ready = True
        if self.gen_status is not None and self.gen_status.winfo_exists():
            self.gen_status.config(text="Challenge files ready ✓", fg=MUTED)

    def _on_files_error(self, message):
        if self.gen_status is not None and self.gen_status.winfo_exists():
            self.gen_status.config(
                text="Couldn't create challenge files: " + message, fg=DANGER)

    def try_login(self):
        if self.pw_entry.get().strip() == PASSWORD:
            # Resume at the saved phase (default: Level 1).
            self.level_index = progress.index_for(progress.load())
            self.start_current_level()
        else:
            self.login_error.config(text="Wrong password. Try again.")
            self.pw_entry.delete(0, "end")
            self.pw_entry.focus_set()

    # -- level progression -------------------------------------------------
    def has_next_level(self):
        return self.level_index + 1 < len(self.LEVELS)

    def start_current_level(self):
        level_cls = self.LEVELS[self.level_index]
        self.current_level = level_cls(self)
        self.current_level.build()
        # Persist the phase so we can resume and so the WPILib Main knows which
        # challenge to run.
        progress.save(progress.token_for(self.level_index))

    def restart_level(self):
        """Rebuild the current level from scratch (fresh state)."""
        self.start_current_level()

    def advance(self):
        """Called from a level's completion popup: go to the next level."""
        if self.has_next_level():
            self.level_index += 1
            self.start_current_level()
        else:
            # No more levels yet. For now, close the game.
            # TODO: replace with a "You beat the warden" end screen.
            progress.save("DONE")
            self.root.destroy()


def main():
    # In a packaged build, unpack the WPILib project to a writable spot on first
    # run (no-op from source). Done before the window so challenges can find it.
    robotproject.ensure_ready()

    root = tk.Tk()
    GameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
