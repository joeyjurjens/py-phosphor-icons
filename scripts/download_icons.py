#!/usr/bin/env python3
"""Download Phosphor Icons from a GitHub release and extract SVGs into the package."""

import io
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

DEST_DIR = Path(__file__).parent.parent / "src" / "py_phosphor_icons" / "svgs"
VERSION_FILE = Path(__file__).parent.parent / "src" / "py_phosphor_icons" / "phosphor_version.txt"
README = Path(__file__).parent.parent / "README.md"
WEIGHTS = ["thin", "light", "regular", "bold", "fill", "duotone"]
STYLES = {
    "flat": "SVGs Flat",
    "stroke": "SVGs",
}

ISSUES_START = "<!-- known-issues-start -->"
ISSUES_END = "<!-- known-issues-end -->"


def download_icons(version: str) -> None:
    url = (
        f"https://github.com/phosphor-icons/homepage/releases/download/{version}/phosphor-icons.zip"
    )
    print(f"Downloading icons from {url}...")
    with urllib.request.urlopen(url) as response:
        data = response.read()

    print("Extracting SVGs...")
    # Per style, so the package modules living alongside them survive.
    for style in STYLES:
        shutil.rmtree(DEST_DIR / style, ignore_errors=True)

    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for style, zip_folder in STYLES.items():
            for weight in WEIGHTS:
                dest = DEST_DIR / style / weight
                dest.mkdir(parents=True)
                prefix = f"{zip_folder}/{weight}/"
                extracted = 0
                for name in zf.namelist():
                    if name.startswith(prefix) and name.endswith(".svg"):
                        (dest / Path(name).name).write_bytes(zf.read(name))
                        extracted += 1
                print(f"  {style}/{weight}: {extracted} icons")

    VERSION_FILE.write_text(version)
    print(f"\nDone! Icons saved to {DEST_DIR} (Phosphor {version})")

    update_readme_issues(version)


def find_missing_icons() -> dict[str, list[str]]:
    canonical = sorted(p.stem for p in (DEST_DIR / "flat" / "regular").glob("*.svg"))
    missing: dict[str, list[str]] = {}
    for name in canonical:
        gaps = []
        for style in STYLES:
            for weight in WEIGHTS:
                filename = name if weight == "regular" else f"{name}-{weight}"
                if not (DEST_DIR / style / weight / f"{filename}.svg").exists():
                    gaps.append(f"`{style}/{weight}`")
        if gaps:
            missing[name] = gaps
    return missing


def update_readme_issues(version: str) -> None:
    missing = find_missing_icons()

    if missing:
        lines = [
            "## Known Icon Issues\n",
            "The following icons are incomplete in the upstream Phosphor release"
            " and will fail to render in certain combinations:\n",
        ]
        for name, gaps in sorted(missing.items()):
            lines.append(f"- **{name}**: missing from {', '.join(gaps)}")
        section = "\n".join(lines)
        print(f"\nFound {len(missing)} icon(s) with missing weights — updating README.")
    else:
        section = "## Known Icon Issues\n\nNo issues found."
        print("\nNo missing weights found.")

    block = f"{ISSUES_START}\n{section}\n{ISSUES_END}"
    content = README.read_text() if README.exists() else ""

    if ISSUES_START in content:
        start = content.index(ISSUES_START)
        end = content.index(ISSUES_END) + len(ISSUES_END)
        content = content[:start] + block + content[end:]
    else:
        content = content.rstrip("\n") + ("\n\n" if content else "") + block + "\n"

    README.write_text(content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: download_icons.py <version>")
        print("Example: download_icons.py v2.1.0")
        sys.exit(1)
    download_icons(sys.argv[1])
