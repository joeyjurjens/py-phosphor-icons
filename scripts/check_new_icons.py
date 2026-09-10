#!/usr/bin/env python3
"""Check whether a new Phosphor Icons release is available on GitHub."""

import json
import os
import urllib.request
from pathlib import Path

GITHUB_API_URL = "https://api.github.com/repos/phosphor-icons/homepage/releases/latest"
VERSION_FILE = Path(__file__).parent.parent / "src" / "py_phosphor_icons" / "phosphor_version.txt"


def main() -> None:
    current = VERSION_FILE.read_text().strip() if VERSION_FILE.exists() else None
    print(f"Current Phosphor version: {current or 'unknown'}")

    print("Checking latest release...")
    with urllib.request.urlopen(GITHUB_API_URL) as response:
        data = json.loads(response.read())

    latest = data["tag_name"]
    print(f"Latest Phosphor version: {latest}")

    if current == latest:
        print("Already up to date.")
        set_output("has_new", "false")
        return

    print(f"New version available: {latest}")
    set_output("has_new", "true")
    set_output("new_version", latest)


def set_output(key: str, value: str) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"{key}={value}\n")
    else:
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
