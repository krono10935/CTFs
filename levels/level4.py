"""Level 4 — The Reversal Lock.

The player must reverse a  final Shape[]  of 5 shapes *in place* by hand — swap
index 0<->4 and 1<->3, leaving the middle — using a temp variable of type Shape.
No `new`, the array is `final`, loops are allowed. Their code is injected into a
real .java file, compiled with javac, and run; we check the array came out reversed.

Reference solution (length-based indices also work — the check is behavioral):

    Shape temp = shapes[0];
    shapes[0] = shapes[4];
    shapes[4] = temp;
    temp = shapes[1];
    shapes[1] = shapes[3];
    shapes[3] = temp;
"""

import random
import tkinter as tk

from theme import ACCENT, BG_WHITE, INK, MUTED
from levels.javalevel import JavaLevel

SHAPE_KINDS = ("SQUARE", "TRIANGLE", "CIRCLE")
SHAPE_COLORS = {"SQUARE": "#3b82f6", "TRIANGLE": ACCENT, "CIRCLE": "#10b981"}

CANVAS_W = 700

_TEMPLATE = """public class Level4 {
    enum Shape { SQUARE, TRIANGLE, CIRCLE }

    public static void main(String[] args) {
        final Shape[] shapes = { __INIT__ };
        // ---- player code ----
__PLAYER__
        // ---- checker ----
        StringBuilder __out = new StringBuilder();
        for (int __i = 0; __i < shapes.length; __i++) {
            if (__i > 0) __out.append(",");
            __out.append(shapes[__i].name());
        }
        System.out.println("__NONCE__:" + __out.toString());
    }
}
"""


class Level4(JavaLevel):
    number = 4
    title = "The Reversal Lock"
    MAIN_CLASS = "Level4"
    array_var = "shapes"
    require_loop = False
    EDITOR_LABEL = "Your code (reverse the array in place):"
    approval = "The lock turns. The shapes align. The prison opens."
    takeaway_code = "Shape temp = shapes[0];"
    takeaway_text = ("Arrays are 0-indexed (0..length-1). Swap through a temp "
                     "variable; `final` locks the array reference, not its "
                     "contents.")

    def __init__(self, app):
        super().__init__(app)
        self.shapes = self._make_shapes()
        self.goal = list(reversed(self.shapes))
        self.initial_state = list(self.shapes)
        self.greeting = (
            "A lock of 5 shapes bars the way. Reverse the array in place so it "
            "matches the goal below. Use a temp variable — `Shape temp = "
            "shapes[0];` — and swap the ends inward. Arrays start at index 0 "
            "(so the last of 5 is index 4). Don't use `new`; the array is "
            "final. Write your code and press Run."
        )

    @staticmethod
    def _make_shapes():
        while True:
            arr = [random.choice(SHAPE_KINDS) for _ in range(5)]
            if len(set(arr)) == 3 and arr != arr[::-1]:
                return arr

    # -- hooks: compile / judge -------------------------------------------
    def _source(self, code):
        init = ", ".join("Shape." + s for s in self.shapes)
        return (_TEMPLATE
                .replace("__INIT__", init)
                .replace("__PLAYER__", code)
                .replace("__NONCE__", self.nonce))

    def _is_win(self, order):
        return order == self.goal

    def _fail_message(self):
        return ("Not reversed yet. Look at the Current row versus the Goal and "
                "keep swapping.")

    # -- hooks: visualization ---------------------------------------------
    def _build_canvas(self, app):
        wrap = tk.Frame(app.container, bg=BG_WHITE)
        wrap.pack(side="bottom", fill="x")
        self.canvas = tk.Canvas(wrap, width=CANVAS_W, height=185,
                                bg=BG_WHITE, highlightthickness=0)
        self.canvas.pack(pady=(6, 0))

    @staticmethod
    def _cell_x(i, n=5):
        return 70 + i * ((CANVAS_W - 140) / (n - 1))

    def _render(self, values):
        c = self.canvas
        c.delete("all")
        c.create_text(20, 20, text="Current", anchor="w", fill=INK,
                      font=self.app.f_small)
        for i, val in enumerate(values):
            self._draw_shape(self._cell_x(i), 55, 26, val)
            c.create_text(self._cell_x(i), 92, text=str(i), fill=MUTED,
                          font=self.app.f_small)
        c.create_text(20, 120, text="Goal", anchor="w", fill=MUTED,
                      font=self.app.f_small)
        for i, val in enumerate(self.goal):
            self._draw_shape(self._cell_x(i), 150, 18, val, faded=True)

    def _draw_shape(self, x, y, half, kind, faded=False):
        c = self.canvas
        color = SHAPE_COLORS[kind]
        outline = "#cbd5e1" if faded else INK
        if kind == "SQUARE":
            c.create_rectangle(x - half, y - half, x + half, y + half,
                               fill=color, outline=outline, width=2)
        elif kind == "CIRCLE":
            c.create_oval(x - half, y - half, x + half, y + half,
                          fill=color, outline=outline, width=2)
        else:  # TRIANGLE
            c.create_polygon(x, y - half, x - half, y + half, x + half,
                             y + half, fill=color, outline=outline, width=2)
