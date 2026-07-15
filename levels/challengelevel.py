"""Base for the WPILIB challenge screens (Easy/Medium/Hard).

These challenges are solved in the WPILib Java project (VS Code); the app just
shows instructions and gates progress behind the password the challenge prints.
Reuses Level 1's single-answer pattern: instructions as the greeting, a one-line
input that must match the password the challenge revealed.
"""

from levels.base import Level


class ChallengeLevel(Level):
    display_name = "Challenge"
    expected_password = None    # None => placeholder / not built yet
    approval = "Correct. The next gate opens."

    def is_correct(self, text):
        return (self.expected_password is not None
                and text.strip() == self.expected_password)

    def fail_response(self, fails):
        return ("That's not the passphrase the challenge printed. Solve it in "
                "VS Code and read the console.", False)

    def build(self):
        super().build()
        if self.expected_password is None:
            # Placeholder: nothing to type yet — lock the input.
            self.entry.config(state="disabled")
            self.send_btn.config(state="disabled", bg="#94a3b8")
