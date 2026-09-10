# py-phosphor-icons

[Phosphor Icons](https://phosphoricons.com/) for Python: the SVGs themselves, a
loader, and search over the icon metadata. No framework, no dependencies.

Framework integrations build on this package:

- [djc-phosphor-icons](https://github.com/joeyjurjens/djc-phosphor-icons) for django-components
- [citry-phosphor-icons](https://github.com/joeyjurjens/citry-phosphor-icons) for citry

## Install

```bash
pip install py-phosphor-icons
```

## Use

```python
from py_phosphor_icons import get_svg, get_svg_inner, search_icons

get_svg("house")  # the whole <svg> element
get_svg_inner("house", "bold")  # just its contents
search_icons("home")  # ranked IconEntry results
```

Weights are `thin`, `light`, `regular`, `bold`, `fill` and `duotone`; styles are
`flat` and `stroke`. An unknown name raises `FileNotFoundError` with the closest
matches suggested.

## Ranking

Search scoring is pluggable. Pass one per call, or set it for the process:

```python
from py_phosphor_icons import Ranking, search_icons, set_ranking

search_icons("home", ranking=MyRanking())
set_ranking("myapp.ranking.MyRanking")  # a class or a dotted path
```
