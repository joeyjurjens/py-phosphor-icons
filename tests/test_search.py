import pytest

from py_phosphor_icons.search import Ranking, all_icons, categories, get_icon, search_icons
from py_phosphor_icons.search.ranking import get_ranking, set_ranking, using_ranking
from py_phosphor_icons.svgs import icon_names, suggest_names


def names(icons):
    return [icon.name for icon in icons]


def test_metadata_covers_every_shipped_icon():
    assert {icon.name for icon in all_icons()} == set(icon_names())


def test_metadata_is_sorted():
    assert names(all_icons()) == sorted(names(all_icons()))


def test_get_icon_resolves_aliases():
    assert get_icon("asclepius").name == "asclepius"
    assert get_icon("caduceus").name == "asclepius"
    assert get_icon("no-such-icon") is None


def test_categories_are_unique_and_sorted():
    assert list(categories()) == sorted(set(categories()))
    assert "Brand" in categories()


def test_empty_query_returns_everything_alphabetically():
    assert names(search_icons()) == sorted(icon_names())
    assert names(search_icons("   ")) == sorted(icon_names())


@pytest.mark.parametrize(
    "query,expected",
    [
        ("house", "house"),
        ("arrow left", "arrow-left"),
        ("magnifying glass", "magnifying-glass"),
        ("shopping cart", "shopping-cart"),
    ],
)
def test_exact_name_ranks_first(query, expected):
    assert names(search_icons(query))[0] == expected


def test_matches_on_tags_only():
    # "roledex" is a tag of address-book, and appears in no icon name.
    assert "address-book" in names(search_icons("roledex"))


def test_matches_on_alias():
    assert names(search_icons("caduceus"))[0] == "asclepius"


def test_matches_on_codepoint():
    house = get_icon("house")
    assert "house" in names(search_icons(str(house.codepoint)))


def test_tolerates_a_typo():
    assert "house" in names(search_icons("hous"))


def test_all_tokens_must_match():
    assert search_icons("house definitelynotatag") == ()


def test_category_filter():
    results = search_icons(categories="Brand")
    assert results
    assert all("Brand" in icon.categories for icon in results)


def test_category_filter_combines_with_query():
    assert names(search_icons("github", categories="Brand")) == ["github-logo"]
    assert search_icons("github", categories="Weather") == ()


def test_multiple_categories_must_all_apply():
    both = search_icons(categories=["Map", "System"])
    assert all({"Map", "System"} <= set(icon.categories) for icon in both)
    assert "house" in names(both)


def test_results_are_deterministic():
    assert search_icons("arrow") == search_icons("arrow")


class TagsOnlyRanking(Ranking):
    def token_score(self, token, icon):
        return max(
            (self.match(token, tag.lower()) for tag in icon.tags),
            default=0.0,
        )


def test_ranking_can_be_passed_in():
    assert "house" not in names(search_icons("house", ranking=TagsOnlyRanking()))
    assert "house" in names(search_icons("homes", ranking=TagsOnlyRanking()))


def test_ranking_can_be_configured():
    try:
        set_ranking(f"{__name__}.TagsOnlyRanking")
        assert isinstance(get_ranking(), TagsOnlyRanking)
        assert "house" not in names(search_icons("house"))
    finally:
        set_ranking(Ranking)


def test_ranking_accepts_a_class_or_an_instance():
    with using_ranking(TagsOnlyRanking):
        assert isinstance(get_ranking(), TagsOnlyRanking)
    tuned = TagsOnlyRanking()
    with using_ranking(tuned):
        assert get_ranking() is tuned


def test_using_ranking_restores_the_previous_one():
    with using_ranking(TagsOnlyRanking):
        assert isinstance(get_ranking(), TagsOnlyRanking)
    assert type(get_ranking()) is Ranking


def test_a_bad_dotted_path_fails_where_it_is_configured():
    with pytest.raises(ModuleNotFoundError):
        set_ranking("nope.NotARanking")
    assert type(get_ranking()) is Ranking

    with pytest.raises(ValueError, match="dotted path"):
        set_ranking("NotAPath")


def test_ranking_defaults_to_the_bundled_one():
    assert type(get_ranking()) is Ranking


def test_suggestions_use_search_not_just_spelling():
    assert "house" in suggest_names("hous")
    assert "shopping-cart" in suggest_names("cart")
    assert suggest_names("zzzzzzzz") == []


def test_suggestions_only_offer_what_that_weight_ships():
    for name in suggest_names("book", weight="light", style="stroke"):
        assert name in icon_names("stroke", "light")
