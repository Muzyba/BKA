#!/usr/bin/env python3
"""Build the Kodi-compatible static ZIP listing for GitHub Pages."""
from html import escape
from pathlib import Path
from urllib.parse import quote
import shutil

root = Path(__file__).resolve().parent
site = root / '_site'
if site.exists():
    shutil.rmtree(site)
site.mkdir()
(site / '.nojekyll').touch()

zips = sorted(
    (file for file in root.iterdir() if file.is_file() and file.suffix.lower() == '.zip'),
    key=lambda file: file.name.casefold(),
)
lines = [
    '<!DOCTYPE html>',
    '<html lang="pl">',
    '<head><meta charset="utf-8"><title>BKA - Best Kodi Addons</title></head>',
    '<body>',
]
for file in zips:
    shutil.copy2(file, site / file.name)
    filename = escape(file.name)
    href = quote(file.name, safe='')
    lines.append(f'<a href="{href}">{filename}</a><br>')
lines += ['</body>', '</html>']
(site / 'index.html').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'BKA: generated {len(zips)} ZIP links in _site/index.html')
