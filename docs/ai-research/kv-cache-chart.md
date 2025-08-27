---
title: "KV Cache Chart"
tags: [kv-cache, ai-research]
project: ai-research
updated: 2025-08-15
---

--8<-- "_snippets/disclaimer.md"

# KV Cache Chart

![Line chart showing KV cache memory rising roughly linearly with token count; larger models require far more memory per token.](kv-cache-chart.svg)

A static rendering of the KV cache visualization originally distributed as an HTML artifact.

The chart highlights a near-linear relationship between sequence length and KV cache memory. As token counts grow, larger models consume proportionally more memory, so scaling up model size or context length quickly drives up the cache footprint.
