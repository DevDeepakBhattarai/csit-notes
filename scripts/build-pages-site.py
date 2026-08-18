from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'
MANIFEST = ROOT / 'pages-manifest.json'


def copy_file(source: Path) -> None:
    rel = source.relative_to(ROOT)
    target = SITE / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def copy_local_refs(page: Path) -> None:
    text = page.read_text(encoding='utf-8', errors='ignore')
    refs = re.findall(r'''(?:src|href)\s*=\s*["']([^"'#]+)''', text, re.IGNORECASE)
    for raw in refs:
        parsed = urlsplit(raw.strip())
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        candidate = (page.parent / unquote(parsed.path)).resolve()
        try:
            candidate.relative_to(ROOT)
        except ValueError:
            continue
        if candidate.is_file():
            copy_file(candidate)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    copy_file(ROOT / 'index.html')
    copy_file(ROOT / 'pages-manifest.json')
    copy_file(ROOT / '.nojekyll')

    for item in manifest['files']:
        page = ROOT / item['path']
        copy_file(page)
        copy_local_refs(page)

    files = [p for p in SITE.rglob('*') if p.is_file()]
    total = sum(p.stat().st_size for p in files)
    print(f'Built {SITE} with {len(files)} files ({total / 1024 / 1024:.2f} MiB).')


if __name__ == '__main__':
    main()
