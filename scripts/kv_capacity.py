"""
kv_capacity.py
================

This script computes the approximate GPU memory required to store the key–value (KV)
caches for different transformer models at various sequence lengths.  The KV cache
dominates inference memory for long context windows because it must store the keys
and values for each token in each layer and head.  The formula used is:

    KV_memory_bytes = 2 * n_layers * n_heads * d_head * seq_len * dtype_bytes

The factor of 2 accounts for storing both keys and values.  See the TensorWave
blog on KV cache sizing for further discussion【563653443713035†L150-L171】.

You can run this script directly to print a table of memory usage in MiB and GiB
for several popular model configurations and sequence lengths.  Use the
`--plot` option to generate a bar chart and save it as a PNG.  The default
parameters approximate Llama‑7B and Llama‑70B using fp16 weights.  Adjust the
``models`` list below as needed.

Example:

    python kv_capacity.py
    python kv_capacity.py --plot --output kv_cache_chart.png

Dependencies: pandas, matplotlib (for plotting) and seaborn (optional).  These
packages should already be installed in this environment.  If not, install via
``pip install pandas matplotlib seaborn``.
"""

import argparse
from dataclasses import dataclass
from typing import List

import pandas as pd

try:
    import matplotlib.pyplot as plt
    import seaborn as sns  # type: ignore
    HAVE_MATPLOTLIB = True
except ImportError:
    HAVE_MATPLOTLIB = False


@dataclass
class ModelConfig:
    name: str
    layers: int
    heads: int
    head_dim: int
    dtype_bytes: int

    @property
    def bytes_per_token(self) -> float:
        """Return KV cache size per token in bytes."""
        return 2 * self.layers * self.heads * self.head_dim * self.dtype_bytes

    @property
    def mb_per_token(self) -> float:
        return self.bytes_per_token / 2**20  # MiB

    @property
    def gb_per_token(self) -> float:
        return self.bytes_per_token / 2**30  # GiB


def compute_table(models: List[ModelConfig], lengths: List[int]) -> pd.DataFrame:
    """Return a DataFrame with KV cache memory for each model and sequence length."""
    rows = []
    for model in models:
        for seq in lengths:
            total_bytes = model.bytes_per_token * seq
            rows.append({
                "model": model.name,
                "seq_len": seq,
                "MB": total_bytes / 2**20,
                "GB": total_bytes / 2**30,
            })
    return pd.DataFrame(rows)


def plot_table(df: pd.DataFrame, output: str) -> None:
    """Generate a bar chart of KV cache memory usage and save it to a file."""
    if not HAVE_MATPLOTLIB:
        raise RuntimeError("matplotlib is not installed; cannot plot")
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    # Convert seq_len to thousands for readability
    df_plot = df.copy()
    df_plot["Length"] = df_plot["seq_len"] // 1024
    sns.barplot(
        data=df_plot,
        x="Length",
        y="GB",
        hue="model",
        ax=ax,
    )
    ax.set_title("KV cache memory vs. context length")
    ax.set_xlabel("Sequence length (tokens / 1k)")
    ax.set_ylabel("Memory (GiB)")
    ax.legend(title="Model")
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute KV cache memory usage")
    parser.add_argument("--plot", action="store_true", help="Generate a bar chart")
    parser.add_argument(
        "--output", default="kv_cache_chart.png", help="Plot output file"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Define model configurations.  These are approximate and can be adjusted.
    models = [
        ModelConfig(
            name="Llama-7B (fp16)",
            layers=32,
            heads=32,
            head_dim=128,
            dtype_bytes=2,
        ),
        ModelConfig(
            name="Llama-13B (fp16)",
            layers=40,
            heads=40,
            head_dim=128,
            dtype_bytes=2,
        ),
        ModelConfig(
            name="Llama-70B (fp16)",
            layers=80,
            heads=64,
            head_dim=128,
            dtype_bytes=2,
        ),
        # Add more models as needed
    ]
    # Sequence lengths to evaluate
    lengths = [4096, 8192, 32768, 131072, 524288]  # 4k, 8k, 32k, 128k, 512k

    df = compute_table(models, lengths)
    pd.set_option("display.max_rows", None)
    print(
        df.to_string(
            index=False,
            formatters={"MB": "{:,.2f}".format, "GB": "{:,.2f}".format},
        )
    )

    if args.plot:
        plot_table(df, args.output)
        print(f"Plot saved to {args.output}")


if __name__ == "__main__":
    main()
