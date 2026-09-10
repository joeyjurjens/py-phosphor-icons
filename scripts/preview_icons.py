#!/usr/bin/env python3
# ruff: noqa: E501
"""Generate preview.html with all icons rendered in every weight and style."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

import django  # noqa: E402

django.setup()

from py_phosphor_icons.components.icon import Icon  # noqa: E402

from py_phosphor_icons.svgs import icon_names  # noqa: E402

WEIGHTS = ["regular", "thin", "light", "bold", "fill", "duotone"]
STYLES = ["flat", "stroke"]
OUTPUT = ROOT / "docs" / "preview.html"


def render_icon(name, weight, style):
    try:
        return Icon.render(kwargs={"name": name, "weight": weight, "style": style})
    except FileNotFoundError:
        return '<svg viewBox="0 0 256 256" class="missing"><line x1="0" y1="0" x2="256" y2="256" stroke="red" stroke-width="16"/><line x1="256" y1="0" x2="0" y2="256" stroke="red" stroke-width="16"/></svg>'


def main():
    names = icon_names()
    print(f"Rendering {len(names)} icons × {len(WEIGHTS)} weights × {len(STYLES)} styles...")

    header_cells = "".join(
        f"<th>{style}<br><small>{weight}</small></th>" for style in STYLES for weight in WEIGHTS
    )

    rows = []
    for i, name in enumerate(names):
        if i % 100 == 0:
            print(f"  {i}/{len(names)}")
        cells = "".join(
            f'<td title="{name} · {weight} · {style}">{render_icon(name, weight, style)}</td>'
            for style in STYLES
            for weight in WEIGHTS
        )
        rows.append(f"<tr><td class='name'>{name}</td>{cells}</tr>")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>djc-phosphor-icons preview</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}
  body {{ font-family: sans-serif; font-size: 13px; background: #f8f8f8; margin: 0; }}

  .toolbar {{
    position: sticky; top: 0; z-index: 10;
    background: white; border-bottom: 1px solid #e0e0e0;
    padding: 10px 16px; display: flex; align-items: center; gap: 20px; flex-wrap: wrap;
  }}
  .toolbar h2 {{ margin: 0; font-size: 15px; margin-right: 8px; }}
  .toolbar label {{ display: flex; align-items: center; gap: 6px; font-size: 13px; }}
  .toolbar input[type=search] {{
    padding: 5px 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 13px; width: 220px;
  }}
  .toolbar input[type=range] {{ width: 100px; }}
  .toolbar input[type=color] {{ width: 32px; height: 28px; padding: 1px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; }}
  .toolbar input[type=checkbox] {{ width: 15px; height: 15px; cursor: pointer; }}

  .wrap {{ padding: 16px; }}
  table {{ border-collapse: collapse; background: white; }}
  th, td {{ border: 1px solid #e0e0e0; padding: 6px 10px; text-align: center; vertical-align: middle; }}
  th {{ background: #f0f0f0; position: sticky; top: 57px; z-index: 5; white-space: nowrap; }}
  td.name {{ text-align: left; font-family: monospace; font-size: 12px; white-space: nowrap; position: sticky; left: 0; background: white; z-index: 1; }}
  tr:hover td {{ background: #f5f5ff; }}
  tr:hover td.name {{ background: #f5f5ff; }}
  svg {{ display: block; margin: auto; width: var(--icon-size, 32px); height: var(--icon-size, 32px); color: var(--icon-color, currentColor); }}
  svg.missing {{ width: var(--icon-size, 32px); height: var(--icon-size, 32px); }}
  tr.hidden {{ display: none; }}
</style>
</head>
<body>
<div class="toolbar">
  <h2>djc-phosphor-icons</h2>
  <label>
    <input type="search" id="search" placeholder="Filter icons…" oninput="filterIcons(this.value)">
  </label>
  <label>
    Size <span id="size-label">32</span>px
    <input type="range" id="size" min="12" max="80" value="32" oninput="setSize(this.value)">
  </label>
  <label>
    Color
    <input type="color" id="color" value="#000000" oninput="setColor(this.value)">
  </label>
  <label>
    <input type="checkbox" id="mirrored" onchange="setMirrored(this.checked)">
    Mirrored
  </label>
  <label>
    Background
    <input type="color" id="bg" value="#ffffff" oninput="setBg(this.value)">
  </label>
</div>
<div class="wrap">
<table id="table">
  <thead><tr><th>name</th>{header_cells}</tr></thead>
  <tbody id="tbody">{"".join(rows)}</tbody>
</table>
</div>
<script>
  const root = document.documentElement;

  function filterIcons(q) {{
    q = q.toLowerCase();
    document.querySelectorAll('#tbody tr').forEach(row => {{
      row.classList.toggle('hidden', !row.querySelector('.name').textContent.includes(q));
    }});
  }}

  function setSize(v) {{
    root.style.setProperty('--icon-size', v + 'px');
    document.getElementById('size-label').textContent = v;
  }}

  function setColor(v) {{
    root.style.setProperty('--icon-color', v);
  }}

  function setMirrored(on) {{
    document.querySelectorAll('svg:not(.missing)').forEach(svg => {{
      svg.style.transform = on ? 'scaleX(-1)' : '';
    }});
  }}

  function setBg(v) {{
    document.getElementById('table').style.background = v;
    document.querySelectorAll('td').forEach(td => td.style.background = '');
  }}
</script>
</body>
</html>"""

    OUTPUT.write_text(html)
    print(f"\nDone! Open {OUTPUT}")


if __name__ == "__main__":
    main()
