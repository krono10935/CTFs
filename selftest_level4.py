"""Standalone end-to-end check for Level 4's real-Java pipeline.

Run this AFTER installing a JDK (javac/java on PATH or JAVA_HOME):

    python selftest_level4.py

It exercises the actual compile-and-run path (which the GUI can't be driven to do
in an automated test) against several sample solutions and prints the verdict for
each. Expected: reference & length-based -> win, out-of-bounds -> run/AIOOBE,
infinite loop -> timed out, partial -> wrong.
"""

import javasandbox
from levels.level4 import Level4

SHAPES = ["SQUARE", "TRIANGLE", "CIRCLE", "SQUARE", "TRIANGLE"]

REFERENCE = """
Shape temp = shapes[0];
shapes[0] = shapes[4];
shapes[4] = temp;
temp = shapes[1];
shapes[1] = shapes[3];
shapes[3] = temp;
"""

LENGTH_BASED = """
Shape temp = shapes[0];
shapes[0] = shapes[shapes.length - 1];
shapes[shapes.length - 1] = temp;
temp = shapes[1];
shapes[1] = shapes[shapes.length - 2];
shapes[shapes.length - 2] = temp;
"""

OUT_OF_BOUNDS = "Shape temp = shapes[5];"
# `i` never changes, but the condition isn't a compile-time constant, so javac
# can't prove it loops forever — it compiles and then spins, hitting our timeout.
INFINITE_LOOP = "int i = 0; while (i < 1) { }"
PARTIAL = "Shape t = shapes[0]; shapes[0] = shapes[4]; shapes[4] = t;"


def _make(shapes):
    lvl = Level4.__new__(Level4)
    lvl.shapes = list(shapes)
    lvl.goal = list(reversed(shapes))
    lvl.nonce = "RESULT_selftest"
    return lvl


def judge(code):
    lvl = _make(SHAPES)
    problem = lvl._check(code)
    if problem:
        return "rejected: " + problem
    res = javasandbox.compile_and_run(lvl._source(code), "Level4")
    if res["timed_out"]:
        return "timed out"
    if res["phase"] != "ok":
        detail = (res["stderr"] or res["stdout"]).strip().splitlines()
        return f"{res['phase']}: {detail[0] if detail else ''}"
    order = lvl._parse_result(res["stdout"])
    return "win" if order == lvl.goal else f"wrong: {order}"


def main():
    if not javasandbox.find_jdk():
        print("No JDK found. Install one (e.g. Adoptium Temurin) and retry.")
        return
    print("JDK:", javasandbox.find_jdk())
    for name, code in [("reference", REFERENCE), ("length-based", LENGTH_BASED),
                       ("out-of-bounds", OUT_OF_BOUNDS),
                       ("infinite-loop", INFINITE_LOOP), ("partial", PARTIAL)]:
        print(f"{name:15} -> {judge(code)}")


if __name__ == "__main__":
    main()
