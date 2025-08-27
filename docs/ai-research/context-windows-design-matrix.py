#!/usr/bin/env python3
"""Generate Plotly table for context-windows design matrix."""
from pathlib import Path

import plotly.graph_objects as go


def _read_markdown_table(path: Path) -> tuple[list[str], list[list[str]]]:
    rows: list[list[str]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            if set(line.replace("|", "").strip()) <= set("-: "):
                continue
            rows.append([cell.strip() for cell in line.strip("|").split("|")])
    header = rows[0]
    data_rows = rows[1:]
    return header, data_rows


def main() -> None:
    base_path = Path(__file__).resolve().parent
    md_path = base_path / "context-windows-design-matrix.md"
    html_path = base_path / "context-windows-design-matrix.html"

    header, rows = _read_markdown_table(md_path)
    columns = list(zip(*rows)) if rows else [[] for _ in header]

    table = go.Figure(
        data=[
            go.Table(
                header=dict(values=header, align="left"),
                cells=dict(values=columns, align="left"),
            )
        ]
    )

    table.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    table.write_html(str(html_path), include_plotlyjs="cdn", full_html=True)


if __name__ == "__main__":
    main()
