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
    """Generate index.html landing page."""
    landing_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UniSDK Documentation</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #F5F7FA; color: #333; min-height: 100vh;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .container { max-width: 800px; width: 90%; text-align: center; padding: 2rem; }
    .logo { margin-bottom: 1.5rem; }
    .logo svg { height: 48px; }
    h1 { font-size: 2rem; font-weight: 700; color: #0a2d72; margin-bottom: 0.5rem; }
    .subtitle { font-size: 1.1rem; color: #666; margin-bottom: 2.5rem; }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
    .card { background: #fff; border-radius: 12px; padding: 2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s, box-shadow 0.2s; }
    .card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
    .card h2 { font-size: 1.3rem; color: #0a2d72; margin-bottom: 1rem; }
    .card p { font-size: 0.9rem; color: #666; margin-bottom: 1.2rem; line-height: 1.5; }
    .card .btn { display: inline-block; padding: 0.6rem 1.5rem; background: #0a2d72; color: #fff; text-decoration: none; border-radius: 6px; font-size: 0.9rem; font-weight: 500; transition: background 0.2s; }
    .card .btn:hover { background: #0052A5; }
    .version-section { margin-top: 2rem; padding: 1.5rem; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .version-section h3 { font-size: 1rem; color: #0a2d72; margin-bottom: 1rem; }
    .version-list { display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; }
    .version-list a { display: inline-block; padding: 0.4rem 1rem; background: #e8edf5; color: #0a2d72; text-decoration: none; border-radius: 20px; font-size: 0.85rem; transition: background 0.2s; }
    .version-list a:hover { background: #0a2d72; color: #fff; }
    .footer { margin-top: 3rem; font-size: 0.8rem; color: #999; }
    .footer a { color: #0052A5; text-decoration: none; }
  </style>
</head>
<body>
  <div class="container">
    <div class="logo">
      <svg viewBox="0 0 180 40" width="180" height="40" xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" style="stop-color:#0a2d72"/><stop offset="100%" style="stop-color:#0052A5"/></linearGradient></defs>
        <rect x="0" y="0" width="8" height="36" rx="1" fill="url(#g)"/>
        <rect x="0" y="0" width="32" height="8" rx="1" fill="url(#g)"/>
        <rect x="12" y="14" width="20" height="8" rx="1" fill="url(#g)"/>
        <text x="42" y="28" font-family="Arial,sans-serif" font-size="22" font-weight="700" fill="#0a2d72" letter-spacing="1">Telink</text>
        <text x="42" y="38" font-family="Arial,sans-serif" font-size="7" font-weight="400" fill="#0052A5" letter-spacing="2.5">SEMICONDUCTOR</text>
      </svg>
    </div>
    <h1>UniSDK Documentation</h1>
    <p class="subtitle">Telink Unified Software Development Kit</p>
    <div class="card-grid">
      <div class="card">
        <h2>English</h2>
        <p>Complete documentation including getting started guides, API references, peripheral drivers, and more.</p>
        <a class="btn" href="./en/main/">Browse English Docs</a>
      </div>
    </div>
    <div class="version-section">
      <h3>All Versions</h3>
      <div class="version-list" id="version-list">
        <span style="color:#999;">Loading...</span>
      </div>
    </div>
    <div class="footer">
      &copy; Telink Semiconductor. All rights reserved.
      &middot; <a href="https://www.telink-semi.cn/">Official Website</a>
      &middot; <a href="https://github.com/telink-semi/unisdk-doc">Docs Repository</a>
      &middot; <a href="https://forum.telink-semi.cn/">Technical Forum</a>
    </div>
  </div>
  <script>
    (function() {
      var vl = document.getElementById('version-list');
      fetch('./versions.json').then(function(r) { return r.json(); }).then(function(d) {
        if (!d.versions || !d.versions.length) { vl.innerHTML = '<span style="color:#999;">No other versions.</span>'; return; }
        vl.innerHTML = '';
        var seen = {};
        d.versions.forEach(function(v) {
          if (seen[v.name]) return; seen[v.name] = true;
          var a = document.createElement('a'); a.href = v.url; a.textContent = v.label; vl.appendChild(a);
        });
      }).catch(function() { vl.innerHTML = '<span style="color:#999;">Unable to load versions.</span>'; });
    })();
  </script>
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

    # Scan for language directories
    for lang in ['en']:
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
                'url': f'/{lang}/{version_name}/',
                'label': label,
                'lang': lang,
            })

    # Also add language-specific main versions as top-level entries
    for lang in ['en']:
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