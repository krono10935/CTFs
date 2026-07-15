"""Level 5 — Kill the Cameras.

The player gets a  final boolean[] cameras  (true = on, false = off) and must use
a loop to walk the array and switch every camera off. A loop is required; the pass
condition is behavioral (all elements false at the end). Same real-Java sandbox as
Level 4.

Reference solution:

    for (int i = 0; i < cameras.length; i++) {
        cameras[i] = false;
    }
"""

import random
import tkinter as tk

from theme import BG_WHITE, INK, MUTED
from levels.javalevel import JavaLevel

CANVAS_W = 700
CAM_ON = "#ef4444"
CAM_OFF = "#94a3b8"
LENS_ON = "#1f2937"
LENS_OFF = "#e5e7eb"

_TEMPLATE = """public class Level5 {
    public static void main(String[] args) {
        final boolean[] cameras = { __INIT__ };
        // ---- player code ----
__PLAYER__
        // ---- checker ----
        StringBuilder __out = new StringBuilder();
        for (int __i = 0; __i < cameras.length; __i++) {
            if (__i > 0) __out.append(",");
            __out.append(cameras[__i]);
        }
        System.out.println("__NONCE__:" + __out.toString());
    }
}
"""


class Level5(JavaLevel):
    number = 5
    title = "Kill the Cameras"
    MAIN_CLASS = "Level5"
    array_var = "cameras"
    require_loop = True
    EDITOR_LABEL = "Your code (loop through the cameras and switch them off):"
    approval = "Every lens goes dark. The hall is blind. Move."
    takeaway_code = "for (int i = 0; i < cameras.length; i++)"
    takeaway_text = ("A loop visits each index 0..length-1; read and write "
                     "elements with cameras[i] as you go.")

    N = 6

    def __init__(self, app):
        super().__init__(app)
        self.cameras = self._make_cameras()
        self.initial_state = list(self.cameras)
        self.greeting = (
            "Six security cameras guard the hall — true means on. Loop through "
            "the boolean[] cameras and switch every one off (false). Write your "
            "loop and press Run."
        )

    @staticmethod
    def _make_cameras():
        while True:
            arr = [random.choice((True, False)) for _ in range(Level5.N)]
            if any(arr):  # at least one on, so it isn't already solved
                return arr

    # -- hooks: compile / judge -------------------------------------------
    def _source(self, code):
        init = ", ".join("true" if v else "false" for v in self.cameras)
        return (_TEMPLATE
                .replace("__INIT__", init)
                .replace("__PLAYER__", code)
                .replace("__NONCE__", self.nonce))

    def _is_win(self, order):
        return bool(order) and all(v == "false" for v in order)

    def _fail_message(self):
        return ("Some cameras are still on — loop through them all and switch "
                "each to off.")

    # -- hooks: visualization ---------------------------------------------
    def _build_canvas(self, app):
        wrap = tk.Frame(app.container, bg=BG_WHITE)
        wrap.pack(side="bottom", fill="x")
        self.canvas = tk.Canvas(wrap, width=CANVAS_W, height=190,
                                bg=BG_WHITE, highlightthickness=0)
        self.canvas.pack(pady=(6, 0))

    @staticmethod
    def _cell_x(i, n=6):
        return 60 + i * ((CANVAS_W - 120) / (n - 1))

    @staticmethod
    def _is_on(v):
        return v is True or v == "true"

    def _render(self, state):
        states = [self._is_on(v) for v in state]
        c = self.canvas
        c.delete("all")
        c.create_text(20, 16, text="Cameras", anchor="w", fill=INK,
                      font=self.app.f_small)
        for i, on in enumerate(states):
            self._draw_camera(self._cell_x(i), 52, on)
            c.create_text(self._cell_x(i), 74, text="ON" if on else "OFF",
                          fill=CAM_ON if on else MUTED, font=self.app.f_small)
            c.create_text(self._cell_x(i), 92, text=str(i), fill=MUTED,
                          font=self.app.f_small)
        c.create_text(20, 120, text="Goal: all off", anchor="w", fill=MUTED,
                      font=self.app.f_small)
        for i in range(len(states)):
            self._draw_camera(self._cell_x(i), 152, False, faded=True, small=True)

    def _draw_camera(self, x, y, on, faded=False, small=False):
        c = self.canvas
        color = CAM_OFF if (faded or not on) else CAM_ON
        outline = "#cbd5e1" if faded else INK
        w, h = (13, 9) if small else (20, 14)
        c.create_rectangle(x - w, y - h, x + w, y + h, fill=color,
                           outline=outline, width=2)
        lr = 4 if small else 6
        c.create_oval(x - lr, y - lr, x + lr, y + lr,
                      fill=LENS_OFF if faded else (LENS_ON if on else LENS_OFF),
                      outline=outline, width=1)
