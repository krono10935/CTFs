"""Hard challenge (app screen) — placeholder until the challenge is built.

Hard is the only phase whose simulation boots the real robot (RobotBase.startRobot
in Main), rather than running a plain-Java challenge.
"""

from levels.challengelevel import ChallengeLevel


class HardChallenge(ChallengeLevel):
    number = 8
    display_name = "Hard"
    expected_password = None  # placeholder

    def __init__(self, app):
        super().__init__(app)
        self.greeting = (
            "Robot challenge — HARD. This challenge is still under construction. "
            "It will boot the real robot (RobotBase). Check back soon."
        )
