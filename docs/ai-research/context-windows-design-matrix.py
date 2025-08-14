#!/usr/bin/env python3
"""Generate Plotly table for context-windows design matrix."""
from pathlib import Path
import csv
import plotly.graph_objects as go


def main() -> None:
    base_path = Path(__file__).resolve().parent
    csv_path = base_path / "context-windows-design-matrix.csv"
    html_path = base_path / "context-windows-design-matrix.html"

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

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
