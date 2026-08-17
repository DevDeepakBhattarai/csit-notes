"""Render a lab-report HTML in headless Chrome/Edge and report page count + overflow.

    python check_pages.py <report.html> [--pdf out.pdf]

Prints one line:  PAGES=<n> OVERFLOW=<page numbers or none>
OVERFLOW lists pages whose .page-content is taller than the printable box, i.e.
pages that will be silently clipped on paper. Any overflow means the report is
not finished -- shorten the block or let it start a new page.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

PROBE = """
<script>
window.addEventListener('load', function () {
  setTimeout(function () {
    var pages = document.querySelectorAll('.report-page, .paper');
    var bad = [];
    document.querySelectorAll('.page-content').forEach(function (pc, i) {
      if (pc.scrollHeight > pc.clientHeight + 2) bad.push(i + 1);
    });
    document.title = 'PAGECHECK|' + pages.length + '|' + (bad.join(',') || 'none');
  }, 2500);
});
</script>
"""


def find_browser() -> str:
    for path in BROWSERS:
        if Path(path).exists():
            return path
    sys.exit("No Chrome/Edge found - edit BROWSERS in check_pages.py")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html")
    parser.add_argument("--pdf", help="also write a PDF here")
    args = parser.parse_args()

    source = Path(args.html).resolve()
    browser = find_browser()
    tmp_dir = Path(tempfile.mkdtemp(prefix="labcheck_"))
    try:
        probe_html = tmp_dir / source.name
        text = source.read_text(encoding="utf-8")
        probe_html.write_text(text.replace("</body>", PROBE + "</body>"), encoding="utf-8")

        profile = tmp_dir / "profile"
        common = [browser, "--headless=new", f"--user-data-dir={profile}", "--no-sandbox",
                  "--disable-gpu", "--allow-file-access-from-files", "--virtual-time-budget=9000"]
        dom = subprocess.run(common + ["--dump-dom", probe_html.as_uri()],
                             capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180).stdout
        match = re.search(r"PAGECHECK\|(\d+)\|([^<]*)", dom or "")
        if match:
            print(f"PAGES={match.group(1)} OVERFLOW={match.group(2)}")
        else:
            print("PAGES=? OVERFLOW=? (probe did not run - open the file in a browser and check the console)")

        if args.pdf:
            out = Path(args.pdf).resolve()
            subprocess.run(common + [f"--print-to-pdf={out}", "--no-pdf-header-footer", source.as_uri()],
                           capture_output=True, text=True, timeout=300)
            print(f"PDF={out}")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
