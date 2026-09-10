#!/usr/bin/env python3
"""Download icon metadata from the Phosphor API. The release zip the SVGs come
from carries no tags or categories; the API serves the data phosphoricons.com
searches with."""

import json
import sys
import urllib.request
from pathlib import Path

API_URL = "https://api.phosphoricons.com/v1/icons"
ROOT = Path(__file__).parent.parent
SVGS_DIR = ROOT / "src" / "py_phosphor_icons" / "svgs"
DEST = ROOT / "src" / "py_phosphor_icons" / "search" / "metadata.json"


def fetch() -> list[dict]:
    print(f"Downloading metadata from {API_URL}...")
    with urllib.request.urlopen(API_URL) as response:
        data = json.loads(response.read())
    return [icon for icon in data["icons"] if icon.get("published")]


def normalize(icon: dict) -> dict:
    return {
        "name": icon["name"],
        "alias": icon.get("alias"),
        "codepoint": icon.get("code"),
        "categories": sorted(icon.get("search_categories") or []),
        "figma_category": icon.get("category"),
        "tags": list(icon.get("tags") or []),
        "released_at": icon.get("released_at"),
        "updated_at": icon.get("last_updated_at"),
    }


def bare(name: str) -> dict:
    return {
        "name": name,
        "alias": None,
        "codepoint": None,
        "categories": [],
        "figma_category": None,
        "tags": [],
        "released_at": None,
        "updated_at": None,
    }


def download_metadata() -> None:
    if not SVGS_DIR.is_dir():
        sys.exit(f"No SVGs found at {SVGS_DIR}. Run download_icons.py first.")

    shipped = {p.stem for p in (SVGS_DIR / "flat" / "regular").glob("*.svg")}
    entries = {icon["name"]: normalize(icon) for icon in fetch()}
    # A release zip cut before a rename still ships the old name.
    by_alias = {entry["alias"]: entry for entry in entries.values() if entry["alias"]}

    # The API and the zip are published separately, so the SVGs decide what exists.
    metadata = []
    missing = []
    for name in sorted(shipped):
        entry = entries.get(name) or by_alias.get(name)
        if entry is None:
            missing.append(name)
            entry = bare(name)
        elif entry["name"] != name:
            entry = {**entry, "name": name, "alias": entry["name"]}
        metadata.append(entry)

    extra = sorted(set(entries) - shipped)
    if extra:
        print(f"Ignoring {len(extra)} icon(s) with metadata but no SVG: {', '.join(extra)}")
    if missing:
        print(f"No metadata for {len(missing)} shipped icon(s): {', '.join(missing)}")

    DEST.write_text(json.dumps(metadata, separators=(",", ":"), sort_keys=True))
    print(f"\nDone! {len(metadata)} entries saved to {DEST}")


if __name__ == "__main__":
    download_metadata()
