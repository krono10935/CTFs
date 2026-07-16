"""End-to-end check of the Medium challenge harness using the local JDK.

Compiles the real MediumChallenge.java (package line + the one WPILib coupling
stripped so it needs no wpilib jars) against a stub MediumSolution that returns a
controllable phrase, then runs it and asserts the console output. This exercises
the real loadBook() + delimiter split against the real book.txt, plus the phrase
check. Run: python selftest_medium.py

Expected: the exact phrase (any case, with surrounding space) -> "Holonomic Drive";
a wrong phrase -> "That's not the phrase..."; an empty return -> "You returned
nothing...".
"""

import subprocess
import tempfile
from pathlib import Path

import javasandbox
import make_book

ROOT = Path(__file__).resolve().parent
CHALLENGES = (ROOT / "levels" / "challenges" / "Challenges" / "src" / "main" /
              "java" / "frc" / "robot" / "challenges")
CHALLENGE_SRC = CHALLENGES / "MediumChallenge.java"
DEPLOY_DIR = ROOT / "levels" / "challenges" / "Challenges" / "src" / "main" / "deploy"

# (returned phrase, substring expected in the console output)
CASES = [
    ("Swerve Drive Kinematics", "Holonomic Drive"),
    ("swerve drive kinematics", "Holonomic Drive"),      # case-insensitive
    ("  Swerve Drive Kinematics  ", "Holonomic Drive"),  # trimmed
    ("Swerve Drive", "That's not the phrase"),           # wrong phrase
    ("", "You returned nothing"),                        # empty return
]


def _challenge_without_wpilib():
    """Real MediumChallenge source, minus the package line and WPILib coupling."""
    deploy_literal = str(DEPLOY_DIR).replace("\\", "\\\\")
    out = []
    for line in CHALLENGE_SRC.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("package "):
            continue
        if stripped.startswith("import edu.wpi.first"):
            continue
        # Swap the deploy-dir lookup for a plain path to the real deploy folder.
        line = line.replace(
            "Filesystem.getDeployDirectory().toPath()",
            f'java.nio.file.Paths.get("{deploy_literal}")')
        out.append(line)
    return "\n".join(out)


def _solution_stub(phrase):
    escaped = phrase.replace("\\", "\\\\").replace('"', '\\"')
    return f"""public final class MediumSolution {{
  private MediumSolution() {{}}
  public static String solve(String[] book) {{
    return "{escaped}";
  }}
}}
"""


_DRIVER = """public class Driver {
  public static void main(String[] args) {
    MediumChallenge.run();
  }
}
"""


def run_case(jdk, phrase):
    work = Path(tempfile.mkdtemp(prefix="medium_test_"))
    (work / "MediumChallenge.java").write_text(_challenge_without_wpilib(),
                                               encoding="utf-8")
    (work / "MediumSolution.java").write_text(_solution_stub(phrase),
                                              encoding="utf-8")
    (work / "Driver.java").write_text(_DRIVER, encoding="utf-8")
    comp = subprocess.run(
        [jdk["javac"], "MediumChallenge.java", "MediumSolution.java", "Driver.java"],
        cwd=work, capture_output=True, text=True)
    if comp.returncode != 0:
        return "COMPILE ERROR: " + comp.stderr.strip()
    out = subprocess.run([jdk["java"], "-cp", str(work), "Driver"],
                         cwd=work, capture_output=True, text=True)
    return out.stdout.strip() or "(no output)"


def main():
    jdk = javasandbox.find_jdk()
    if not jdk:
        print("No JDK found.")
        return
    make_book.ensure_generated()  # the harness reads the real book.txt

    all_ok = True
    for phrase, expected in CASES:
        output = run_case(jdk, phrase)
        ok = expected in output
        all_ok = all_ok and ok
        label = repr(phrase) if phrase else "'' (empty)"
        print(f"[{'PASS' if ok else 'FAIL'}] return {label:34} -> "
              f"expected {expected!r}; got {output.splitlines()[-1]!r}")
    print("\nAll cases passed." if all_ok else "\nSome cases FAILED.")


if __name__ == "__main__":
    main()
