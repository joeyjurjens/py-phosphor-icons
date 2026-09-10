from py_phosphor_icons.search.metadata import IconEntry, all_icons
from py_phosphor_icons.search.ranking import Ranking, get_ranking


def matches_categories(icon: IconEntry, categories: list[str] | tuple[str, ...]) -> bool:
    wanted = {category.lower() for category in categories}
    return wanted.issubset({category.lower() for category in icon.categories})


def search_icons(
    query: str | None = None,
    categories: str | list[str] | tuple[str, ...] | None = None,
    ranking: Ranking | None = None,
) -> tuple[IconEntry, ...]:
    icons = all_icons()

    if categories:
        if isinstance(categories, str):
            categories = [categories]
        icons = tuple(icon for icon in icons if matches_categories(icon, categories))

    if not query or not query.strip():
        return icons

    ranking = ranking or get_ranking()
    matches = [(ranking.score(query, icon), icon) for icon in icons]
    matches = [match for match in matches if match[0] > 0]
    matches.sort(key=lambda match: (-match[0], match[1].name))
    return tuple(icon for _, icon in matches)
