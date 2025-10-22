---
title: "KV Cache Chart"
tags: [kv-cache, ai-research]
project: ai-research
updated: 2025-08-15
---

!!! note "Disclaimer"
    This document is provided for research purposes only and does not constitute legal advice. It also does not constitute financial advice.
# KV Cache Chart

![Bar chart showing token count on the x-axis and KV cache memory (GiB) on the y-axis; memory usage climbs almost linearly so larger models and longer sequences demand substantially more capacity.](kv-cache-chart.svg)

*Figure: KV cache memory grows nearly linearly with context length across model scales.*


<iframe src="kv-cache-chart.html" width="100%" height="420"></iframe>

*Note:* Regenerate the HTML using [`scripts/kv_capacity.py`](https://github.com/d0tTino/docs-/blob/main/scripts/kv_capacity.py) with the `--plotly` flag if the underlying data changes.

A static rendering of the KV cache visualization originally distributed as an HTML artifact.

The chart highlights a near-linear relationship between sequence length and KV cache memory. As token counts grow, larger models consume proportionally more memory, so scaling up model size or context length quickly drives up the cache footprint.

## Refreshing the chart

The SVG and interactive HTML are generated from model parameters in [`scripts/kv_capacity.py`](https://github.com/d0tTino/docs-/blob/main/scripts/kv_capacity.py). To refresh the artifacts, run:

```
python scripts/kv_capacity.py --plot --output docs/ai-research/kv-cache-chart.svg
python scripts/kv_capacity.py --plotly --output docs/ai-research/kv-cache-chart.html
```
