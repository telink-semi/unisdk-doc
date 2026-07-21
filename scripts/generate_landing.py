#!/usr/bin/env python3
"""
Generate landing page (index.html) for the gh-pages root.

Reads version metadata from the build output directory and generates
a landing page that links to each language + version combination.

Usage:
    python scripts/generate_landing.py <build_dir> <output_dir>

Example:
    python scripts/generate_landing.py _build/versions _build/versions
"""

import os
import sys
import json


def generate_landing_page(build_dir, output_dir):
    """Generate a minimal index.html that auto-redirects to English docs."""
    landing_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UniSDK Documentation</title>
  <meta http-equiv="refresh" content="0; url=./en/latest/">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #F5F7FA; color: #333; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
    .container { text-align: center; padding: 2rem; }
    .logo { margin-bottom: 1.5rem; }
    .logo img { height: 48px; }
    h1 { font-size: 1.5rem; color: #0a2d72; }
    a { color: #0052A5; }
  </style>
</head>
<body>
  <div class="container">
    <div class="logo"><img src="_static/logo.svg" alt="Telink Logo"></div>
    <h1>UniSDK Documentation</h1>
    <p>Redirecting to <a href="./en/latest/">English docs</a> or <a href="./zh/latest/">中文文档</a>...</p>
  </div>
</body>
</html>"""

    # Write landing page
    output_path = os.path.join(output_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(landing_html)
    print(f"Landing page generated: {output_path}")


def generate_versions_json(build_dir, output_dir):
    """Scan build directory and generate versions.json."""
    versions = []

    # Scan for language directories (dynamically detect from build output)
    for lang in sorted(os.listdir(build_dir)):
        lang_dir = os.path.join(build_dir, lang)
        if not os.path.isdir(lang_dir):
            continue

        # Scan for version directories
        for version_name in sorted(os.listdir(lang_dir), reverse=True):
            version_dir = os.path.join(lang_dir, version_name)
            if not os.path.isdir(version_dir):
                continue

            # Determine label
            if version_name == 'main':
                label = f'latest ({lang})'
            else:
                label = f'{version_name} ({lang})'

            versions.append({
                'name': version_name,
                'url': f'{lang}/{version_name}/',
                'label': label,
                'lang': lang,
            })

    # Also add language-specific main versions as top-level entries
    for lang in sorted(os.listdir(build_dir)):
        main_dir = os.path.join(build_dir, lang, 'main')
        if os.path.isdir(main_dir):
            # Add a clean latest entry
            pass

    data = {'versions': versions}

    output_path = os.path.join(output_dir, 'versions.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Versions JSON generated: {output_path} ({len(versions)} entries)")


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <build_dir> <output_dir>")
        sys.exit(1)

    build_dir = sys.argv[1]
    output_dir = sys.argv[2]

    os.makedirs(output_dir, exist_ok=True)

    generate_versions_json(build_dir, output_dir)
    generate_landing_page(build_dir, output_dir)


if __name__ == '__main__':
    main()