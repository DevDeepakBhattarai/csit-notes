from __future__ import annotations

import argparse
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

EXCLUDED_PARTS = {'.git', '.github', 'skills', 'scripts'}
EXCLUDED_NAME_PATTERNS = (
    'Editing DevDeepakBhattarai_README.md at main',
)


def clean_title(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r'[_-]+', ' ', stem)
    stem = re.sub(r'\s+', ' ', stem).strip()
    return stem


def read_title(path: Path) -> str:
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')[:50_000]
    except OSError:
        return clean_title(path.name)

    match = re.search(r'<title[^>]*>(.*?)</title>', text, re.IGNORECASE | re.DOTALL)
    if not match:
        return clean_title(path.name)

    title = html.unescape(re.sub(r'\s+', ' ', match.group(1)).strip())
    return title or clean_title(path.name)


def public_url(relative_path: Path) -> str:
    return '/'.join(quote(part, safe='') for part in relative_path.parts)


def discover(root: Path) -> list[dict[str, str]]:
    files: list[dict[str, str]] = []
    for path in sorted(root.rglob('*.html')):
        rel = path.relative_to(root)
        if rel == Path('index.html'):
            continue
        if any(part in EXCLUDED_PARTS or part.startswith('.') for part in rel.parts[:-1]):
            continue
        if any(pattern in path.name for pattern in EXCLUDED_NAME_PATTERNS):
            continue

        directory = rel.parent.as_posix() if rel.parent != Path('.') else ''
        files.append(
            {
                'path': rel.as_posix(),
                'url': public_url(rel),
                'name': path.name,
                'title': read_title(path),
                'directory': directory,
                'topLevel': rel.parts[0] if len(rel.parts) > 1 else 'Root',
            }
        )
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate the CSIT Notes GitHub Pages HTML manifest.')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, default=None)
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.output or root / 'pages-manifest.json'
    files = discover(root)
    payload = {
        'generatedAt': datetime.now(timezone.utc).isoformat(),
        'count': len(files),
        'files': files,
    }
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Generated {output} with {len(files)} HTML pages.')


if __name__ == '__main__':
    main()
