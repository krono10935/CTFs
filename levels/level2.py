"""Level 2 — The warden's interrogation.

Three questions, each answered through System.out.println( ... ); :
  1. Name    -> a String, e.g.  System.out.println("Alice");
  2. Badge   -> badgeNumber / 2 as an int (teaches integer division)
  3. Allowed -> a boolean;  true  passes,  false  resets the level.
"""

import random
import re
import tkinter as tk

from theme import ACCENT, INK
from levels.base import Level

# Warden prompts.
Q_NAME = ('The warden blocks the gate. "State your name." '
          '(A name is text — remember your double quotes.)')
Q_BADGE = ('"Now your badge." The warden points at the number in the corner. '
           '"What is badgeNumber / 2?"')
Q_BOOL = '"Last question — are you allowed to enter the prison?" (true or false)'


class Level2(Level):
    number = 2
    title = "The Interrogation"
    greeting = Q_NAME
    approval = "The gate creaks open. Welcome inside."
    takeaway_code = 'System.out.println("name" / n / 2 / true);'
    takeaway_text = ('Strings use double quotes "...", the / operator on ints is '
                     'integer division (it drops the remainder), and true / false '
                     "are booleans.")

    def __init__(self, app):
        super().__init__(app)
        self.step = 0
        # Odd badge so that badge / 2 clearly loses a remainder.
        self.badge = random.randrange(1001, 10000, 2)
        self.answer = self.badge // 2

    # -- badge chip in the top-right corner --------------------------------
    def decorate_header(self, header):
        tk.Label(header, text=f"int badgeNumber = {self.badge};",
                 font=self.app.f_mono, bg=INK, fg=ACCENT).pack(side="right",
                                                               padx=18)

    # -- helpers -----------------------------------------------------------
    @staticmethod
    def _is_int(s):
        return bool(re.fullmatch(r"[+-]?\d+", s.strip()))

    @staticmethod
    def _is_string_literal(s):
        return bool(re.fullmatch(r'"[^"]*"', s.strip()))

    # -- state machine -----------------------------------------------------
    def submit(self, text):
        inner = self.parse_println(text)
        if inner is None:
            self.add_warden(
                "I hear no Java. Answer through System.out.println( ... );")
            return

        if self.step == 0:
            self._answer_name(inner)
        elif self.step == 1:
            self._answer_badge(inner)
        elif self.step == 2:
            self._answer_boolean(inner)

    def _answer_name(self, inner):
        if self._is_string_literal(inner):
            self.step = 1
            self.add_warden(Q_BADGE)
        else:
            self.add_warden('A name is text — put it in double quotes, e.g. '
                            'System.out.println("Alice");')

    def _answer_badge(self, inner):
        if self._is_int(inner) and int(inner) == self.answer:
            self.step = 2
            self.add_warden(Q_BOOL)
        else:
            self.add_warden("Integer division drops the remainder — try "
                            "System.out.println(badgeNumber / 2);")

    def _answer_boolean(self, inner):
        value = inner.strip().lower()
        if value == "true":
            self.win()
        elif value == "false":
            self.add_warden('"FALSE?! Then you do not belong here."')
            # Reset the whole level: a fresh Level2 (new badge), back to Q1.
            self.solved = True  # block further input during the pause
            self.app.root.after(1000, self.app.restart_level)
        else:
            self.add_warden("That's not a boolean. Answer true or false.")
