"""End-to-end check of the Easy challenge's Room logic using the local JDK.

Compiles the real Room.java (package line stripped) with a small driver for each
scenario and asserts the console output. Run: python selftest_easy.py
Expected: correct loop -> "The library is open"; start before 99 -> "You need to
start from the 100th slot"; skip 99 -> "You must start exactly from the 100th slot".
"""

import subprocess
import tempfile
from pathlib import Path

import javasandbox

ROOM_SRC = (Path(__file__).resolve().parent / "levels" / "challenges" /
            "Challenges" / "src" / "main" / "java" / "frc" / "robot" /
            "challenges" / "Room.java")

TRIGGER = 250

DRIVERS = {
    "correct (loop from 99)":
        f"for (int i = 99; i < rooms.length; i++) rooms[i].check();",
    "start before 99 (from 50)":
        f"for (int i = 50; i < rooms.length; i++) rooms[i].check();",
    "skip 99 (from 150)":
        f"for (int i = 150; i < rooms.length; i++) rooms[i].check();",
}


def _room_without_package():
    lines = ROOM_SRC.read_text(encoding="utf-8").splitlines()
    return "\n".join(l for l in lines if not l.strip().startswith("package "))


def _driver(loop):
    return f"""public class Driver {{
  public static void main(String[] args) {{
    Room.begin({TRIGGER});
    Room[] rooms = new Room[1000];
    for (int i = 0; i < rooms.length; i++) rooms[i] = new Room(i);
    {loop}
  }}
}}
"""


def run(loop):
    jdk = javasandbox.find_jdk()
    if not jdk:
        return "NO_JDK"
    work = Path(tempfile.mkdtemp(prefix="easy_test_"))
    (work / "Room.java").write_text(_room_without_package(), encoding="utf-8")
    (work / "Driver.java").write_text(_driver(loop), encoding="utf-8")
    comp = subprocess.run([jdk["javac"], "Room.java", "Driver.java"],
                          cwd=work, capture_output=True, text=True)
    if comp.returncode != 0:
        return "COMPILE ERROR: " + comp.stderr.strip()
    out = subprocess.run([jdk["java"], "-cp", str(work), "Driver"],
                         cwd=work, capture_output=True, text=True)
    return out.stdout.strip() or "(no output)"


def main():
    if not javasandbox.find_jdk():
        print("No JDK found.")
        return
    for name, loop in DRIVERS.items():
        print(f"{name:26} -> {run(loop)!r}")


if __name__ == "__main__":
    main()
