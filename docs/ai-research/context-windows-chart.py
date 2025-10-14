"""Generate a chart from the context windows design matrix.

This script reads the Markdown table in
``docs/ai-research/context-windows-design-matrix.md`` and produces a bar chart
of the typical maximum effective context length for each method. The chart is
saved as ``context-windows-design-matrix.svg`` in the same folder as the table.

Usage:
    python scripts/context_windows_chart.py

Dependencies: pandas, matplotlib, seaborn.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore

TABLE_PATH = Path("docs/ai-research/context-windows-design-matrix.md")
OUTPUT_PATH = Path("docs/ai-research/context-windows-design-matrix.svg")


def _read_markdown_table(path: Path) -> pd.DataFrame:
    """Parse a Markdown table into a DataFrame."""
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            # Skip alignment lines like | :--- |
            if set(line.replace("|", "").strip()) <= set("-: "):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            rows.append(cells)
    header = rows[0]
    data = rows[1:]
    return pd.DataFrame(data, columns=header)


def _parse_length(value: str) -> float | None:
    """Return the maximum numeric length in ``value``.

    Examples
    --------
    >>> _parse_length("32k–128k")
    128000.0
    >>> _parse_length("100k+")
    100000.0
    >>> _parse_length("Unbounded") is None
    True
    """
    matches = re.findall(r"(\d+(?:\.\d+)?)([kM]?)", value)
    if not matches:
        return None
    number, suffix = matches[-1]
    val = float(number)
    if suffix == "k":
        val *= 1_000
    elif suffix == "M":
        val *= 1_000_000
    return val


def build_chart(output: Path) -> None:
    """Read the design matrix table and write a bar chart to ``output``."""
    df = _read_markdown_table(TABLE_PATH)
    df["max_tokens"] = df["Typical max effective length"].apply(_parse_length)
    df_plot = df.dropna(subset=["max_tokens"])

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_plot, x="Method", y="max_tokens", ax=ax)
    ax.set_ylabel("Typical max effective length (tokens)")
    ax.set_xlabel("Method")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default=str(OUTPUT_PATH),
        help="Output image file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_chart(Path(args.output))
    print(f"Chart saved to {args.output}")


if __name__ == "__main__":
    main()
