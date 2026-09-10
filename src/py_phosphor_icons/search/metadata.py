import json
from dataclasses import dataclass
from functools import cache
from pathlib import Path

METADATA_FILE = Path(__file__).parent / "metadata.json"


@dataclass(frozen=True)
class IconEntry:
    name: str
    alias: str | None
    codepoint: int | None
    categories: tuple[str, ...]
    figma_category: str | None
    tags: tuple[str, ...]
    released_at: float | None
    updated_at: float | None

    def __str__(self) -> str:
        return self.name


@cache
def all_icons() -> tuple[IconEntry, ...]:
    return tuple(
        IconEntry(
            name=entry["name"],
            alias=entry["alias"],
            codepoint=entry["codepoint"],
            categories=tuple(entry["categories"]),
            figma_category=entry["figma_category"],
            tags=tuple(entry["tags"]),
            released_at=entry["released_at"],
            updated_at=entry["updated_at"],
        )
        for entry in json.loads(METADATA_FILE.read_text())
    )


@cache
def icons_by_name() -> dict[str, IconEntry]:
    lookup = {icon.name: icon for icon in all_icons()}
    for icon in all_icons():
        if icon.alias:
            lookup.setdefault(icon.alias, icon)
    return lookup


def get_icon(name: str) -> IconEntry | None:
    return icons_by_name().get(name)


@cache
def categories() -> tuple[str, ...]:
    return tuple(sorted({category for icon in all_icons() for category in icon.categories}))
