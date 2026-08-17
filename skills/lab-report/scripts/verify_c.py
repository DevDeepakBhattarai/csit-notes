"""Compile + run every program in a lab report and check the printed output.

    python verify_c.py <report.html|items.json>            # check only
    python verify_c.py <report.html|items.json> --write     # paste real stdout into "output"

Reads the `report-data` JSON block (see templates/). For each item it compiles
`code` according to the extension of `filename` (.c -> gcc, .cpp/.cc -> g++,
.py -> python), runs it with `stdin` if present, and compares real stdout with
the declared `output`.

{NAME}/{ROLL}/{SECTION} are substituted with the same dummy values on both
sides, so token-bearing printf lines are checked too.

Exit code is non-zero if anything failed to build, crashed, or mismatched.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOKENS = {"{NAME}": "Test Student", "{ROLL}": "00", "{SECTION}": "A"}
DATA_RE = re.compile(
    r'(<script type="application/json" id="report-data">\s*)(.*?)(\s*</script>)',
    re.DOTALL,
)
COMPILERS = {".c": ["gcc", "-O0", "-w"], ".cpp": ["g++", "-O0", "-w"], ".cc": ["g++", "-O0", "-w"]}


def fill(text: str) -> str:
    for token, value in TOKENS.items():
        text = str(text or "").replace(token, value)
    return text


def load(path: Path) -> tuple[list[dict], str | None]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text), None
    match = DATA_RE.search(text)
    if not match:
        sys.exit(f"No <script type=\"application/json\" id=\"report-data\"> block in {path}")
    return json.loads(match.group(2)), text


def save(path: Path, items: list[dict], original: str | None) -> None:
    body = json.dumps(items, ensure_ascii=False, indent=2)
    if original is None:
        path.write_text(body + "\n", encoding="utf-8")
        return
    path.write_text(DATA_RE.sub(lambda m: m.group(1) + body + m.group(3), original, count=1), encoding="utf-8")


def toolchain_ok(workdir: Path) -> tuple[bool, str]:
    """Compile a hello-world first, so a broken compiler is never reported as a failing program."""
    probe = workdir / "_probe.c"
    probe.write_text('#include <stdio.h>\nint main(){printf("ok\\n");return 0;}\n', encoding="utf-8")
    exe = workdir / "_probe.exe"
    try:
        build = subprocess.run(["gcc", "-O0", "-w", str(probe), "-o", str(exe)],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    except FileNotFoundError:
        return False, "gcc is not on PATH"
    if build.returncode != 0 or not exe.exists():
        return False, f"gcc exited {build.returncode} on a hello-world: {(build.stderr or '<no stderr>').strip()}"
    return True, ""


def run_item(item: dict, workdir: Path) -> tuple[bool, str, str]:
    """Returns (ok, actual_stdout, note)."""
    filename = item.get("filename") or "program.c"
    suffix = Path(filename).suffix.lower() or ".c"
    source = workdir / Path(filename).name
    source.write_text(fill(item.get("code", "")), encoding="utf-8")
    stdin = fill(item.get("stdin", "")) or None

    if suffix == ".py":
        cmd = [sys.executable, str(source)]
    elif suffix in COMPILERS:
        exe = workdir / (source.stem + ".exe")
        build = subprocess.run(COMPILERS[suffix] + [str(source), "-o", str(exe)],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
        if build.returncode != 0:
            return False, "", "BUILD FAILED\n" + (build.stderr or "").strip()
        cmd = [str(exe)]
    else:
        return True, "", f"SKIPPED ({suffix} is not compiled here - verify by hand)"

    try:
        run = subprocess.run(cmd, input=stdin, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=20, cwd=workdir)
    except subprocess.TimeoutExpired:
        return False, "", "TIMEOUT after 20s (infinite loop or waiting on input?)"
    if run.returncode != 0:
        return False, run.stdout or "", f"EXIT CODE {run.returncode}\n{(run.stderr or '').strip()}"
    return True, run.stdout, ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("report")
    parser.add_argument("--write", action="store_true", help="store the real stdout as the item's output")
    parser.add_argument("--only", help="comma separated item 'no' values")
    args = parser.parse_args()

    path = Path(args.report).resolve()
    items, original = load(path)
    wanted = {s.strip() for s in args.only.split(",")} if args.only else None

    failures = 0
    changed = 0
    with tempfile.TemporaryDirectory(prefix="labverify_") as tmp:
        workdir = Path(tmp)
        needs_cc = any(Path(i.get("filename", "x.c")).suffix.lower() in COMPILERS for i in items)
        if needs_cc:
            ok, why = toolchain_ok(workdir)
            if not ok:
                print(f"TOOLCHAIN UNAVAILABLE: {why}")
                print("Nothing was verified. Do NOT claim the outputs are tested -- either fix the")
                print("compiler, or ask the user to run this script on their machine.")
                sys.exit(2)
        for item in items:
            no = str(item.get("no", "?"))
            if wanted and no not in wanted:
                continue
            if not item.get("code"):
                print(f"[{no}] SKIP  no code")
                continue

            ok, actual, note = run_item(item, workdir)
            if not ok:
                failures += 1
                print(f"[{no}] FAIL  {item.get('title', '')}\n      {note.replace(chr(10), chr(10) + '      ')}")
                continue
            if note:
                print(f"[{no}] SKIP  {note}")
                continue

            expected = fill(item.get("output", ""))
            if actual.strip() == expected.strip():
                print(f"[{no}] PASS  {item.get('title', '')}")
                continue

            if args.write:
                # store with tokens back in place so the browser can re-fill them
                stored = actual.rstrip("\n")
                for token, value in TOKENS.items():
                    stored = stored.replace(value, token)
                item["output"] = stored
                changed += 1
                print(f"[{no}] WROTE real output ({len(stored.splitlines())} lines)")
            else:
                failures += 1
                diff = difflib.unified_diff(expected.splitlines(), actual.splitlines(),
                                            "declared", "actual", lineterm="", n=1)
                print(f"[{no}] DIFF  {item.get('title', '')}")
                for line in list(diff)[:24]:
                    print("      " + line)

    if args.write and changed:
        save(path, items, original)
        print(f"\nupdated {changed} item(s) in {path.name}")
    print(f"\n{len(items)} items, {failures} problem(s)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
