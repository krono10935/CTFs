"""Easy challenge (app screen) — the file hunt over Room objects.

Solved in the WPILib project by editing EasySolution.solve(Room[]). The console
prints "The library is open"; entering it here advances to Medium.
"""

from levels.challengelevel import ChallengeLevel


class EasyChallenge(ChallengeLevel):
    number = 6
    display_name = "Easy"
    expected_password = "The library is open"
    approval = "The library is open. The way to the Medium challenge is clear."
    takeaway_text = ("Arrays of objects + methods: loop from the right index and "
                     "call check() on each room.")
    solution_filename = "EasySolution.java"

    def __init__(self, app):
        super().__init__(app)
        self.greeting = (
            "Robot challenge — EASY. This one runs in the WPILib project.\n\n"
            "Click  📂 Open in VS Code  (top right) to open your solution file. "
            "Edit  EasySolution.solve(Room[] rooms) — loop over the 1000 rooms and "
            "call check() on each, starting at the 100th room. Then run "
            "\"Simulate Robot Code\" and read the console. When you do it right it "
            "prints a passphrase — type it below to continue. (Start before or skip "
            "the 100th room and you get nothing.)"
        )
