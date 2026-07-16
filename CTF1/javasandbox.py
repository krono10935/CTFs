"""Minimal Java compile-and-run helper for the CTF's Level 4.

Locates a JDK (PATH / JAVA_HOME / common Windows install dirs / a bundled ./jdk),
then compiles a single source file and runs it in a throwaway temp directory with a
timeout. This executes real Java, so it is only meant for the trusted, sandboxed
snippets the level assembles (with its own static guards + a random result marker).
"""

import glob
import os
import shutil
import subprocess
import tempfile

_jdk_cache = "unset"  # "unset" until first probe; then a dict or None


def _candidate_bins():
    """Yield possible directories that may contain javac/java."""
    seen = set()

    def add(path):
        if path and path not in seen:
            seen.add(path)
            return path
        return None

    # 1. On PATH.
    which = shutil.which("javac")
    if which:
        yield os.path.dirname(which)

    # 2. JAVA_HOME/bin.
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        d = add(os.path.join(java_home, "bin"))
        if d:
            yield d

    # 3. A JDK bundled next to the game (./jdk/bin).
    here = os.path.dirname(os.path.abspath(__file__))
    d = add(os.path.join(here, "jdk", "bin"))
    if d:
        yield d

    # 4. Common Windows install locations (jdk-*/bin), plus JDKs bundled inside
    #    JetBrains IDEs (their JBR is a full JDK with javac).
    patterns = [
        r"C:\Program Files\Java\*\bin",
        r"C:\Program Files\Eclipse Adoptium\*\bin",
        r"C:\Program Files\Microsoft\jdk*\bin",
        r"C:\Program Files\Amazon Corretto\*\bin",
        r"C:\Program Files (x86)\Java\*\bin",
        r"C:\Program Files\JetBrains\*\jbr\bin",
        r"C:\Program Files (x86)\JetBrains\*\jbr\bin",
        os.path.join(os.environ.get("LOCALAPPDATA", ""),
                     r"Programs\*\jbr\bin"),
    ]
    for pat in patterns:
        if not pat:
            continue
        for match in sorted(glob.glob(pat)):
            d = add(match)
            if d:
                yield d


def find_jdk(force=False):
    """Return {'javac': path, 'java': path} or None. Cached after first call."""
    global _jdk_cache
    if _jdk_cache != "unset" and not force:
        return _jdk_cache

    exe = ".exe" if os.name == "nt" else ""
    result = None
    for bin_dir in _candidate_bins():
        javac = os.path.join(bin_dir, "javac" + exe)
        java = os.path.join(bin_dir, "java" + exe)
        if os.path.isfile(javac) and os.path.isfile(java):
            result = {"javac": javac, "java": java}
            break

    _jdk_cache = result
    return result


def _result(phase, stdout="", stderr="", timed_out=False):
    return {"phase": phase, "stdout": stdout, "stderr": stderr,
            "timed_out": timed_out}


def compile_and_run(source, main_class, timeout=8):
    """Compile `source` and run `main_class`, returning a result dict.

    phase is one of:
      "no_jdk"  – no JDK found (nothing was run)
      "compile" – javac failed (stderr holds the diagnostics)
      "run"     – the program ran but exited non-zero / threw (or timed out)
      "ok"      – compiled and exited 0 (stdout holds the program output)
    """
    jdk = find_jdk()
    if not jdk:
        return _result("no_jdk")

    workdir = tempfile.mkdtemp(prefix="warden_lvl4_")
    try:
        src_path = os.path.join(workdir, main_class + ".java")
        with open(src_path, "w", encoding="utf-8") as fh:
            fh.write(source)

        # --- compile ---
        try:
            comp = subprocess.run(
                [jdk["javac"], src_path],
                cwd=workdir, capture_output=True, text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return _result("compile", stderr="javac timed out.", timed_out=True)
        if comp.returncode != 0:
            return _result("compile", stdout=comp.stdout, stderr=comp.stderr)

        # --- run ---
        try:
            run = subprocess.run(
                [jdk["java"], "-cp", workdir, main_class],
                cwd=workdir, capture_output=True, text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            out = exc.stdout or ""
            if isinstance(out, bytes):
                out = out.decode("utf-8", "replace")
            return _result("run", stdout=out, stderr="Program timed out.",
                           timed_out=True)

        if run.returncode != 0:
            return _result("run", stdout=run.stdout, stderr=run.stderr)
        return _result("ok", stdout=run.stdout, stderr=run.stderr)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
