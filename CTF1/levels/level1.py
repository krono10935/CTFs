"""Level 1 — "Say hello back" -> System.out.println();"""

from levels.base import Level


class Level1(Level):
    number = 1
    title = "The Greeting"
    greeting = "The warden greets you. Say hello back."
    approval = "The warden nods. You speak Java after all."
    takeaway_code = 'System.out.println("...");'
    takeaway_text = "prints a line of text to the console in Java."

    def is_correct(self, text):
        # Any well-formed System.out.println( ... ); counts as a hello.
        return self.parse_println(text) is not None

    def fail_response(self, fails):
        if fails == 1:
            return ("What bro?", False)
        if fails == 2:
            return ("I only speak Java!", False)
        return ('System.out.println("I only speak Java!");', True)
