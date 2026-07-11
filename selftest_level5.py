"""Standalone end-to-end check for Level 5's real-Java pipeline.

Run after a JDK is available (javac/java on PATH, JAVA_HOME, or a JetBrains IDE):

    python selftest_level5.py

Expected: reference & if-guarded loops -> win, no-loop hardcode -> rejected,
out-of-bounds -> run/AIOOBE, infinite loop -> timed out, partial -> wrong.
"""

import javasandbox
from levels.level5 import Level5

CAMERAS = [True, False, True, True, False, True]

REFERENCE = """
for (int i = 0; i < cameras.length; i++) {
    cameras[i] = false;
}
"""

IF_GUARDED = """
for (int i = 0; i < cameras.length; i++) {
    if (cameras[i]) {
        cameras[i] = false;
    }
}
"""

NO_LOOP = "cameras[0] = false; cameras[1] = false;"
OUT_OF_BOUNDS = "for (int i = 0; i <= cameras.length; i++) { cameras[i] = false; }"
INFINITE_LOOP = "int i = 0; while (i < 1) { }"
PARTIAL = "for (int i = 1; i < cameras.length; i++) { cameras[i] = false; }"


def _make(cameras):
    lvl = Level5.__new__(Level5)
    lvl.cameras = list(cameras)
    lvl.initial_state = list(cameras)
    lvl.nonce = "RESULT_selftest"
    return lvl


def judge(code):
    lvl = _make(CAMERAS)
    problem = lvl._check(code)
    if problem:
        return "rejected: " + problem
    res = javasandbox.compile_and_run(lvl._source(code), "Level5")
    if res["timed_out"]:
        return "timed out"
    if res["phase"] != "ok":
        detail = (res["stderr"] or res["stdout"]).strip().splitlines()
        return f"{res['phase']}: {detail[0] if detail else ''}"
    order = lvl._parse_result(res["stdout"])
    return "win" if lvl._is_win(order) else f"wrong: {order}"


def main():
    if not javasandbox.find_jdk():
        print("No JDK found. Install one (e.g. Adoptium Temurin) and retry.")
        return
    print("JDK:", javasandbox.find_jdk())
    for name, code in [("reference", REFERENCE), ("if-guarded", IF_GUARDED),
                       ("no-loop", NO_LOOP), ("out-of-bounds", OUT_OF_BOUNDS),
                       ("infinite-loop", INFINITE_LOOP), ("partial", PARTIAL)]:
        print(f"{name:15} -> {judge(code)}")


if __name__ == "__main__":
    main()
