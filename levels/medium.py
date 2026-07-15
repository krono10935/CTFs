"""Medium challenge (app screen) — placeholder until the challenge is built."""

from levels.challengelevel import ChallengeLevel


class MediumChallenge(ChallengeLevel):
    number = 7
    display_name = "Medium"
    expected_password = None  # placeholder

    def __init__(self, app):
        super().__init__(app)
        self.greeting = (
            "Robot challenge — MEDIUM. This challenge is still under "
            "construction. Check back soon."
        )
