"""Medium challenge (app screen) — the 100-page book hunt over a String[].

Solved in the WPILib project by editing MediumSolution.solve(String[] book): print
every page, read the two real pages, and return "Swerve Drive Kinematics". The
console then prints "Holonomic Drive"; entering it here advances to Hard.
"""

from levels.challengelevel import ChallengeLevel


class MediumChallenge(ChallengeLevel):
    number = 7
    display_name = "Medium"
    expected_password = "Holonomic Drive"
    approval = "Holonomic Drive. The path to the Hard challenge is open."
    takeaway_text = ("Loop over a String[] and read each element — then a little "
                     "detective work to piece the answer together.")
    solution_filename = "MediumSolution.java"

    def __init__(self, app):
        super().__init__(app)
        self.greeting = (
            "Robot challenge — MEDIUM. This one also runs in the WPILib project.\n\n"
            "Click  📂 Open in VS Code  (top right) to open your solution file. "
            "Edit  MediumSolution.solve(String[] book) — it hands you a 100-page "
            "book as an array of Strings. Figure out the three words the book is "
            "hiding. Return them as one phrase, then run \"Simulate Robot Code\" and "
            "read the console. When you get it right it prints a passphrase — type "
            "it below to continue."
        )
