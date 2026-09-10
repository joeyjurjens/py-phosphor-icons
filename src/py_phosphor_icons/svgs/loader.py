import re
from functools import cache
from pathlib import Path

from py_phosphor_icons.search import search_icons

SVGS_DIR = Path(__file__).parent

VALID_WEIGHTS = frozenset({"bold", "duotone", "fill", "light", "regular", "thin"})
VALID_STYLES = frozenset({"flat", "stroke"})

DEFAULT_WEIGHT = "regular"
DEFAULT_STYLE = "flat"

SVG_INNER_RE = re.compile(r"<svg[^>]*>(.*)</svg>", re.DOTALL)


def validate(weight: str, style: str) -> None:
    if weight not in VALID_WEIGHTS:
        raise ValueError(
            f"Invalid weight '{weight}'. Choose from: {', '.join(sorted(VALID_WEIGHTS))}"
        )
    if style not in VALID_STYLES:
        raise ValueError(f"Invalid style '{style}'. Choose from: {', '.join(sorted(VALID_STYLES))}")


def svg_path(name: str, weight: str = DEFAULT_WEIGHT, style: str = DEFAULT_STYLE) -> Path:
    validate(weight, style)
    filename = name if weight == DEFAULT_WEIGHT else f"{name}-{weight}"
    return SVGS_DIR / style / weight / f"{filename}.svg"


def exists(name: str, weight: str = DEFAULT_WEIGHT, style: str = DEFAULT_STYLE) -> bool:
    return svg_path(name, weight, style).exists()


def get_svg(name: str, weight: str = DEFAULT_WEIGHT, style: str = DEFAULT_STYLE) -> str:
    path = svg_path(name, weight, style)
    if not path.exists():
        raise FileNotFoundError(not_found_message(name, weight, style))
    return path.read_text().strip()


def get_svg_inner(name: str, weight: str = DEFAULT_WEIGHT, style: str = DEFAULT_STYLE) -> str:
    match = SVG_INNER_RE.search(get_svg(name, weight, style))
    return match.group(1) if match else ""


@cache
def icon_names(style: str = DEFAULT_STYLE, weight: str = DEFAULT_WEIGHT) -> tuple[str, ...]:
    validate(weight, style)
    suffix = "" if weight == DEFAULT_WEIGHT else f"-{weight}"
    return tuple(
        sorted(p.stem.removesuffix(suffix) for p in (SVGS_DIR / style / weight).glob("*.svg"))
    )


def suggest_names(
    name: str, weight: str = DEFAULT_WEIGHT, style: str = DEFAULT_STYLE, limit: int = 3
) -> list[str]:
    """Same search that powers the icon picker, so a wrong name is answered with
    what the user probably meant - by tag too, not just by spelling."""
    available = set(icon_names(style, weight))
    return [icon.name for icon in search_icons(name) if icon.name in available][:limit]


def not_found_message(name: str, weight: str, style: str) -> str:
    suggestions = suggest_names(name, weight, style)
    hint = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
    return f"Icon '{name}' (weight: {weight}, style: {style}) not found.{hint}"
