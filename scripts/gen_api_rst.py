#!/usr/bin/env python3
"""
API Reference RST generation script using Doxygen + Breathe.

Generates per-group Doxygen XML output, then creates RST files with
``.. doxygenfile::`` directives organized into the correct directory
structure under en/api_reference/.

Usage:
    python scripts/gen_api_rst.py

Prerequisites:
    - doxygen installed on the system
    - sphinx-build + breathe available in the Python environment
    - SDK headers checked out at _sdk_src/ (or symlinked)
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT                         # conf.py is at project root
API_REF_DIR = PROJECT_ROOT / "en" / "api_reference"
DOXYGEN_TEMPLATE = PROJECT_ROOT / "Doxyfile.in.template"
SDK_DIR = PROJECT_ROOT / "_sdk_src"             # SDK checkout path
TEMPLATE_TEXT = DOXYGEN_TEMPLATE.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Source groups — mirrors gen_api_docs.py
# Each group maps to a separate Doxygen run.
# ---------------------------------------------------------------------------
SOURCE_GROUPS = [
    # -- Public API (single source dir) --
    {
        "name": "public_api",
        "breathe_project": "public_api",
        "output_subdir": "public_api",
        "source_dirs": [SDK_DIR / "api" / "include"],
        "recursive": False,
        "full_path_names": "NO",
        # per_subdir=False means flat output under output_subdir
        "per_subdir": False,
    },
    # -- Core Driver API (two source dirs) --
    {
        "name": "core_drivers",
        "breathe_project": "core_drivers",
        "output_subdir": "core_drivers",
        "source_dirs": [
            SDK_DIR / "core" / "include",
            SDK_DIR / "core" / "common" / "include",
        ],
        "recursive": False,
        "full_path_names": "NO",
        "per_subdir": False,
    },
]

# SoC groups — dynamically discovered
soc_root = SDK_DIR / "soc"
if soc_root.exists():
    for soc_dir in sorted(soc_root.iterdir()):
        if not soc_dir.is_dir():
            continue
        drv_inc = soc_dir / "drivers" / "include"
        if not drv_inc.exists():
            continue
        soc_name = soc_dir.name  # e.g. "TL321X"
        SOURCE_GROUPS.append({
            "name": f"soc_{soc_name}",
            "breathe_project": soc_name,
            "output_subdir": f"soc_drivers/{soc_name}",
            "source_dirs": [drv_inc],
            "recursive": False,
            "full_path_names": "NO",
            "per_subdir": False,
        })


def log(msg: str):
    """Print to stderr so stdout stays clean."""
    print(msg, file=sys.stderr)


def find_header_files(source_dirs: list[Path]) -> list[Path]:
    """Collect all .h files from the given source directories (non-recursive)."""
    files: list[Path] = []
    for sd in source_dirs:
        if not sd.exists():
            log(f"  [SKIP] Source directory does not exist: {sd}")
            continue
        for f in sorted(sd.iterdir()):
            if f.suffix == ".h" and "_internal.h" not in f.name:
                files.append(f)
    return files


def doxygen_input_dirs(source_dirs: list[Path]) -> str:
    """Convert source dir paths to relative paths (from project root) for Doxygen INPUT."""
    return " ".join(
        os.path.relpath(str(d), str(DOCS_DIR)) for d in source_dirs if d.exists()
    )


def run_doxygen(group: dict) -> Path:
    """
    Generate a temporary Doxyfile from the template and run Doxygen.
    Returns the path to the generated XML directory.
    """
    # Determine paths
    group_slug = group["name"]
    xml_output = f"_doxygen/{group_slug}/xml"
    xml_dir = DOCS_DIR / xml_output

    # Ensure clean output directory
    xml_parent = xml_dir.parent
    if xml_parent.exists():
        shutil.rmtree(xml_parent)
    # Doxygen cannot create intermediate directories; ensure parent exists
    xml_parent.mkdir(parents=True, exist_ok=True)

    # Render template
    doxyfile_content = (
        TEMPLATE_TEXT
        .replace("@@INPUT_DIRS@@", doxygen_input_dirs(group["source_dirs"]))
        .replace("@@XML_OUTPUT@@", xml_output)
        .replace("@@RECURSIVE@@", "YES" if group.get("recursive", False) else "NO")
        .replace("@@FULL_PATH_NAMES@@", group.get("full_path_names", "NO"))
    )

    # Write temporary Doxyfile
    temp_doxyfile = DOCS_DIR / f"_doxyfile_{group_slug}"
    temp_doxyfile.write_text(doxyfile_content, encoding="utf-8")

    # Run Doxygen
    log(f"  Generating XML for group '{group['name']}' ...")
    result = subprocess.run(
        ["doxygen", temp_doxyfile.name],
        cwd=str(DOCS_DIR),
        capture_output=True,
        text=True,
    )

    # Print Doxygen stderr (warnings, errors)
    if result.stderr.strip():
        for line in result.stderr.strip().split("\n"):
            log(f"    {line}")

    # Print Doxygen warnings/errors from stderr only
    # (verbose progress output on stdout is intentionally suppressed)

    if result.returncode != 0:
        log(f"  [ERROR] Doxygen failed for group '{group['name']}'")
        # Keep temp file for debugging
        log(f"  Temp Doxyfile kept at: {temp_doxyfile}")
        result.check_returncode()

    # Clean up temp file
    temp_doxyfile.unlink()

    # Capture Doxygen log file
    doxy_log = DOCS_DIR / "doxygen.log"
    if doxy_log.exists():
        doxy_log.rename(DOCS_DIR / f"_doxygen/{group_slug}/doxygen.log")

    return xml_dir


def generate_rst_files(group: dict, header_files: list[Path]):
    """Generate RST files with .. doxygenfile:: directives."""
    out_base = API_REF_DIR / group["output_subdir"]
    out_base.mkdir(parents=True, exist_ok=True)
    project_name = group["breathe_project"]

    for hf in header_files:
        rst_content = (
            f"{hf.name}\n"
            f"{'=' * len(hf.name)}\n"
            f"\n"
            f".. doxygenfile:: {hf.name}\n"
            f"   :project: {project_name}\n"
        )

        rst_path = out_base / (hf.stem + ".rst")
        rst_path.write_text(rst_content, encoding="utf-8")
        log(f"  -> {rst_path.relative_to(PROJECT_ROOT)}")


def main():
    API_REF_DIR.mkdir(parents=True, exist_ok=True)

    total_headers = 0
    for group in SOURCE_GROUPS:
        log(f"\n[{group['name']}]")

        # Find input header files
        header_files = find_header_files(group["source_dirs"])
        if not header_files:
            log("  No header files found, skipping Doxygen run.")
            continue

        # Run Doxygen
        xml_dir = run_doxygen(group)

        # Generate RST files
        generate_rst_files(group, header_files)
        total_headers += len(header_files)

    log(f"\nDone! Processed {total_headers} header files across {len(SOURCE_GROUPS)} groups.")
    log(f"RST output: {API_REF_DIR}")
    log("\nNext step: sphinx-build -b html . _build")


if __name__ == "__main__":
    main()
