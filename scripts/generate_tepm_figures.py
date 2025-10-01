"""Generate datasets and figures for the DNA archival storage TEPM article."""
from __future__ import annotations

import io
import math
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

BASE_DIR = Path(__file__).resolve().parents[1] / "docs" / "non-ai-research"
FIG_DIR = BASE_DIR / "fig"
DATA_DIR = BASE_DIR / "data"

BITS_PER_BASE = 1.8  # Effective information density per base
BYTES_PER_BASE = BITS_PER_BASE / 8
SECONDS_PER_DAY = 86_400

def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def save_svg(fig: plt.Figure, output_path: Path, *, title: str, description: str) -> None:
    """Save figure to SVG ensuring <title> and <desc> metadata are embedded."""
    buffer = io.StringIO()
    fig.savefig(buffer, format="svg", metadata={
        "Title": title,
        "Description": description,
    })
    svg = buffer.getvalue()
    buffer.close()
    if "<desc>" not in svg:
        svg = svg.replace(f"<title>{title}</title>", f"<title>{title}</title>\n <desc>{description}</desc>", 1)
    output_path.write_text(svg, encoding="utf-8")


def compute_cumulative_cost(years: np.ndarray, *, initial: float, energy_per_year: float,
                             migration_interval: int | None = None, migration_cost: float = 0.0) -> np.ndarray:
    """Return cumulative cost for each year given recurring energy and migration events."""
    cumulative = np.zeros_like(years, dtype=float)
    for idx, year in enumerate(years):
        cost = initial
        cost += energy_per_year * year
        if migration_interval and migration_cost:
            migrations = math.floor(max(year, 0) / migration_interval)
            cost += migrations * migration_cost
        cumulative[idx] = cost
    return cumulative


def generate_tco_dataset() -> pd.DataFrame:
    years = np.arange(0, 101, 10)
    dna = compute_cumulative_cost(years, initial=3_000, energy_per_year=0.5)
    tape = compute_cumulative_cost(years, initial=200, energy_per_year=15,
                                   migration_interval=12, migration_cost=200)
    hdd = compute_cumulative_cost(years, initial=350, energy_per_year=20,
                                  migration_interval=5, migration_cost=250)
    df = pd.DataFrame({
        "Year": years,
        "DNA (Silica)": dna,
        "Tape (LTO-9 Class)": tape,
        "HDD (Archival)": hdd,
    })
    df.to_csv(DATA_DIR / "TEPM_Fig1_TCO_Comparison.csv", index=False)
    return df


def generate_write_cost_dataset() -> pd.DataFrame:
    records = []
    scenarios = [
        ("Chemical", 2025, 1.0e-7, 1_000),
        ("Chemical", 2028, 0.5e-7, 5_000),
        ("Chemical", 2030, 0.3e-7, 10_000),
        ("Enzymatic", 2025, 5.0e-7, 500),
        ("Enzymatic", 2028, 1.0e-7, 10_000),
        ("Enzymatic", 2030, 5.0e-9, 1_000_000),
    ]
    for platform, year, cost_per_base, throughput_bases in scenarios:
        cost_per_tb = cost_per_base * ((1_000_000_000_000 * 8) / BITS_PER_BASE)
        throughput_tb_day = throughput_bases * BYTES_PER_BASE * SECONDS_PER_DAY / 1_000_000_000_000
        records.append({
            "Platform": platform,
            "Year": year,
            "Cost_per_base": cost_per_base,
            "Cost_per_TB": cost_per_tb,
            "Throughput_bases_per_s": throughput_bases,
            "Throughput_TB_per_day": throughput_tb_day,
        })
    df = pd.DataFrame(records)
    df.to_csv(DATA_DIR / "TEPM_Fig2_Write_Cost_Comparison.csv", index=False)
    return df


def generate_reliability_dataset() -> pd.DataFrame:
    records = []
    illumina_points = [
        (5, 0.18),
        (6, 0.16),
        (8, 0.14),
        (10, 0.12),
        (12, 0.10),
    ]
    nanopore_points = [
        (20, 0.28),
        (25, 0.25),
        (30, 0.22),
        (35, 0.20),
        (40, 0.18),
        (45, 0.16),
    ]
    for coverage, ecc in illumina_points:
        records.append({"Platform": "Illumina-class", "Coverage": coverage, "ECC_rate": ecc})
    for coverage, ecc in nanopore_points:
        records.append({"Platform": "Nanopore-class", "Coverage": coverage, "ECC_rate": ecc})
    df = pd.DataFrame(records)
    df.to_csv(DATA_DIR / "TEPM_Fig3_Reliability_Pareto.csv", index=False)
    return df


def generate_lifecycle_dataset(tco: pd.DataFrame) -> pd.DataFrame:
    horizon_years = 100
    dna_cost = float(tco.loc[tco["Year"] == horizon_years, "DNA (Silica)"].iloc[0])
    tape_cost = float(tco.loc[tco["Year"] == horizon_years, "Tape (LTO-9 Class)"].iloc[0])
    hdd_cost = float(tco.loc[tco["Year"] == horizon_years, "HDD (Archival)"].iloc[0])

    records = [
        {
            "Medium": "DNA (Silica Encapsulated)",
            "Lifecycle_cost_per_TB_year": dna_cost / horizon_years,
            "Refresh_cadence_years": None,
            "Energy_kWh_per_TB_year": 0.01,
        },
        {
            "Medium": "DNA (Dehydrated)",
            "Lifecycle_cost_per_TB_year": (dna_cost * 1.25) / horizon_years,
            "Refresh_cadence_years": 250,
            "Energy_kWh_per_TB_year": 0.05,
        },
        {
            "Medium": "Tape (LTO-9 Class)",
            "Lifecycle_cost_per_TB_year": tape_cost / horizon_years,
            "Refresh_cadence_years": 12,
            "Energy_kWh_per_TB_year": 0.12,
        },
        {
            "Medium": "Archival HDD",
            "Lifecycle_cost_per_TB_year": hdd_cost / horizon_years,
            "Refresh_cadence_years": 5,
            "Energy_kWh_per_TB_year": 12.0,
        },
    ]
    df = pd.DataFrame(records)
    df.to_csv(DATA_DIR / "TEPM_Fig4_Lifecycle_Cost.csv", index=False)
    return df


def plot_tco(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for column, color in [
        ("DNA (Silica)", "#1f78b4"),
        ("Tape (LTO-9 Class)", "#33a02c"),
        ("HDD (Archival)", "#e31a1c"),
    ]:
        ax.plot(df["Year"], df[column], marker="o", label=column, color=color)
    ax.set_xlabel("Archive lifespan (years)")
    ax.set_ylabel("Cumulative TCO ($/TB)")
    ax.set_title("Century-scale TCO favors low-refresh media")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
    ax.legend()
    fig.tight_layout()
    save_svg(
        fig,
        FIG_DIR / "TEPM_Fig1_TCO_Comparison.svg",
        title="TEPM Figure 1 - TCO Comparison",
        description="Cumulative total cost of ownership for DNA, tape, and HDD archival media across a 100-year horizon.",
    )
    plt.close(fig)


def plot_write_cost(df: pd.DataFrame) -> None:
    fig, (ax_cost, ax_throughput) = plt.subplots(nrows=2, sharex=True, figsize=(7, 6))

    for platform, style in [("Chemical", "o-"), ("Enzymatic", "s-")]:
        subset = df[df["Platform"] == platform]
        ax_cost.plot(subset["Year"], subset["Cost_per_TB"], style, label=platform)
        ax_throughput.plot(subset["Year"], subset["Throughput_TB_per_day"], style, label=platform)

    ax_cost.set_yscale("log")
    ax_throughput.set_yscale("log")
    ax_cost.set_ylabel("Write cost ($/TB)")
    ax_cost.set_title("Projected DNA write cost and throughput trajectories")
    ax_cost.grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
    ax_throughput.grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
    ax_throughput.set_ylabel("Write throughput (TB/day)")
    ax_throughput.set_xlabel("Roadmap year")
    ax_cost.legend()

    def currency_formatter(value, _pos):
        if value == 0:
            return "$0"
        magnitude = int(math.floor(math.log10(value))) if value > 0 else 0
        if magnitude >= 6:
            return f"${value/1e6:.0f}M"
        if magnitude >= 3:
            return f"${value/1e3:.0f}K"
        return f"${value:.0f}"

    ax_cost.yaxis.set_major_formatter(FuncFormatter(currency_formatter))

    def throughput_formatter(value, _pos):
        if value == 0:
            return "0"
        if value >= 1:
            return f"{value:.1f}"
        return f"{value:.2f}"

    ax_throughput.yaxis.set_major_formatter(FuncFormatter(throughput_formatter))

    fig.tight_layout()
    save_svg(
        fig,
        FIG_DIR / "TEPM_Fig2_Write_Cost_Comparison.svg",
        title="TEPM Figure 2 - Write Cost and Throughput",
        description="Roadmap comparison of chemical and enzymatic DNA synthesis cost per TB and throughput in TB per day.",
    )
    plt.close(fig)


def plot_reliability(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for platform, marker, color in [
        ("Illumina-class", "o", "#1f78b4"),
        ("Nanopore-class", "s", "#ff7f00"),
    ]:
        subset = df[df["Platform"] == platform]
        ax.plot(subset["Coverage"], subset["ECC_rate"] * 100, marker=marker, label=platform, color=color)
    ax.set_xlabel("Sequencing coverage (×)")
    ax.set_ylabel("Logical redundancy (ECC rate, %)")
    ax.set_title("Reliability frontier couples ECC and physical coverage")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
    ax.legend()
    fig.tight_layout()
    save_svg(
        fig,
        FIG_DIR / "TEPM_Fig3_Reliability_Pareto.svg",
        title="TEPM Figure 3 - Reliability Pareto Frontier",
        description="Pareto frontier showing ECC rate versus sequencing coverage for Illumina-class and Nanopore-class DNA storage pipelines.",
    )
    plt.close(fig)


def plot_lifecycle(df: pd.DataFrame) -> None:
    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    mediums = df["Medium"]
    x = np.arange(len(mediums))
    bar = ax1.bar(x, df["Lifecycle_cost_per_TB_year"], color="#6a3d9a", alpha=0.8)
    ax1.set_ylabel("Lifecycle cost ($/TB-year)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(mediums, rotation=20, ha="right")
    ax1.set_title("Lifecycle cost and energy demand of archival media")
    ax1.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.6)

    ax2 = ax1.twinx()
    ax2.plot(x, df["Energy_kWh_per_TB_year"], color="#e31a1c", marker="o", linewidth=2, label="Energy")
    ax2.set_ylabel("Energy (kWh/TB-year)")

    ax1.legend([bar], ["Lifecycle cost"], loc="upper left")
    ax2.legend(loc="upper right")
    fig.tight_layout()
    save_svg(
        fig,
        FIG_DIR / "TEPM_Fig4_Lifecycle_Cost.svg",
        title="TEPM Figure 4 - Lifecycle Cost and Energy",
        description="Comparison of lifecycle cost per TB-year and energy requirements for DNA, tape, and HDD archival media.",
    )
    plt.close(fig)


def main() -> None:
    ensure_dirs()
    tco_df = generate_tco_dataset()
    write_df = generate_write_cost_dataset()
    reliability_df = generate_reliability_dataset()
    lifecycle_df = generate_lifecycle_dataset(tco_df)

    plot_tco(tco_df)
    plot_write_cost(write_df)
    plot_reliability(reliability_df)
    plot_lifecycle(lifecycle_df)


if __name__ == "__main__":
    main()
