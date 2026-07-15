"""Base for the WPILIB challenge screens (Easy/Medium/Hard).

These challenges are solved in the WPILib Java project (VS Code); the app just
shows instructions, opens the right solution file in VS Code, and gates progress
behind the password the challenge prints. Reuses Level 1's single-answer pattern:
instructions as the greeting, a one-line input that must match the password the
challenge revealed.
"""

import tkinter as tk
from tkinter import messagebox

import robotproject
import vscode
from levels.base import Level
from theme import ACCENT, ACCENT_DARK, INK

# The WPILib project these challenges live in. From source it's the in-repo folder;
# in a packaged build it's a writable per-user copy (see robotproject / BUILD_WINDOWS.md).
PROJECT_DIR = robotproject.project_dir()
# Where the per-challenge solution files live inside that project.
CHALLENGES_JAVA = (PROJECT_DIR / "src" / "main" / "java" / "frc" / "robot"
                   / "challenges")


class ChallengeLevel(Level):
    display_name = "Challenge"
    expected_password = None    # None => placeholder / not built yet
    approval = "Correct. The next gate opens."
    solution_filename = None    # e.g. "MediumSolution.java"; enables the open button

    @property
    def solution_path(self):
        """Absolute path to this challenge's solution file, or None."""
        if not self.solution_filename:
            return None
        return CHALLENGES_JAVA / self.solution_filename

    def is_correct(self, text):
        return (self.expected_password is not None
                and text.strip() == self.expected_password)

    def fail_response(self, fails):
        return ("That's not the passphrase the challenge printed. Solve it in "
                "VS Code and read the console.", False)

    # -- header "Open in VS Code" button -----------------------------------
    def decorate_header(self, header):
        """Add an 'Open in VS Code' button to the top bar (if a solution file)."""
        if not self.solution_filename:
            return
        tk.Button(
            header, text="📂 Open in VS Code", font=self.app.f_small,
            bg=ACCENT, fg="white", activebackground=ACCENT_DARK,
            activeforeground="white", relief="flat", bd=0, cursor="hand2",
            padx=12, pady=4, command=self.open_solution,
        ).pack(side="right", padx=(0, 8))

    def open_solution(self):
        """Open the WPILib project in VS Code, focused on the solution file."""
        opened = vscode.open_in_vscode(PROJECT_DIR, self.solution_path)
        if not opened:
            messagebox.showinfo(
                "Open your solution file",
                "Couldn't find the WPILib VS Code automatically.\n\n"
                "Open this file yourself:\n\n"
                f"{self.solution_path}",
            )

    def build(self):
        super().build()
        if self.expected_password is None:
            # Placeholder: nothing to type yet — lock the input.
            self.entry.config(state="disabled")
            self.send_btn.config(state="disabled", bg="#94a3b8")
