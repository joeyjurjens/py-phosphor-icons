"""Phosphor Icons for Python: the SVGs, a loader, and search over them."""

from py_phosphor_icons.search import (
    IconEntry,
    Ranking,
    all_icons,
    categories,
    get_icon,
    get_ranking,
    search_icons,
    set_ranking,
    using_ranking,
)
from py_phosphor_icons.svgs import (
    DEFAULT_STYLE,
    DEFAULT_WEIGHT,
    VALID_STYLES,
    VALID_WEIGHTS,
    exists,
    get_svg,
    get_svg_inner,
    icon_names,
    suggest_names,
    svg_path,
    validate,
)

__all__ = [
    "DEFAULT_STYLE",
    "DEFAULT_WEIGHT",
    "VALID_STYLES",
    "VALID_WEIGHTS",
    "IconEntry",
    "Ranking",
    "all_icons",
    "categories",
    "exists",
    "get_icon",
    "get_ranking",
    "get_svg",
    "get_svg_inner",
    "icon_names",
    "search_icons",
    "set_ranking",
    "suggest_names",
    "using_ranking",
    "svg_path",
    "validate",
]
