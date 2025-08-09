title | tags | project | updated
---|---|---|---
Context Windows Field Guide — Appendix | research, long‑context | ai‑research | 2025‑08‑09

# Appendix: Context Windows Field Guide

This appendix provides supporting material for the **Context Windows Field Guide**.

## A. Key formulas and capacity planner

### A.1 Key–value cache memory

For a transformer with **L** layers, **H** heads and head dimension **d**, and using a data type requiring **dtypeBytes** bytes (e.g. 2 bytes for FP16), the memory used by the key–value cache is

```
KV_memory_bytes ≈ 2 × L × H × d × seq_length × dtypeBytes.
```

The factor of 2 accounts for keys and values.  For example, a 70 B‑parameter model with **L ≈ 80**, **H ≈ 64**, **d ≈ 128** and **dtypeBytes = 2** uses approximately 2.6 MiB per thousand tokens【563653443713035†L150-L171】.  A 7 B model with half as many layers and heads uses ~0.7 MiB per thousand tokens.  Multiply the per‑token cost by the sequence length to estimate VRAM requirements.  Remember to leave room for model parameters, activations and overhead.

### A.2 Throughput and latency

Inference speed depends on the **prefill phase** (computing attention over the entire context) and the **decode phase** (one token at a time).  Prefill cost scales roughly linearly with sequence length for linear/sparse attention and quadratically for full attention; decode cost is constant per token.  To estimate total time, measure tokens per second on your hardware for a given model and window length.  Divide the desired input length by prefill throughput to estimate latency.

### A.3 Memory per request in multi‑tenant systems

When serving multiple requests concurrently, total KV memory is:

```
Total_KV_memory ≈ KV_memory_per_token × seq_length × num_concurrent_requests.
```

PagedAttention can evict unused pages and share memory across requests; vLLM provides an API to estimate memory usage and automatically schedule requests.

## B. Evaluation templates

The following test patterns can be adapted for benchmarking long‑context models.

### B.1 Needle in a haystack

1. Generate a long filler text of **L** tokens from a corpus (e.g., Wikipedia paragraphs).
2. Insert a unique key–value pair (e.g., “**ID42: blue**”) at position *p* (beginning, middle or end).
3. Prompt the model with the entire sequence followed by: “What is the colour associated with ID42?”.
4. Record whether the model outputs “blue.”  Vary **L** and *p* to trace effective context.

### B.2 Aggregation and arithmetic

1. Create **N** numeric statements spaced evenly across a sequence of length **L**, e.g., “Number i is v_i.”  Ensure the numbers are small enough to sum without overflow.
2. Ask the model: “What is the sum of the numbers?” and “What is the mean of the numbers?”.
3. Compare the response with the ground truth.
4. For multi‑step reasoning, interleave distracting sentences to increase task difficulty.

### B.3 Multi‑hop reasoning

1. Prepare pairs of related facts located far apart (e.g., “Alice was born in Paris.” ... “People born in Paris speak French.”).
2. Ask the model to deduce a conclusion (“What language does Alice speak?”).
3. Evaluate accuracy as **L** increases.  For robust testing, randomise positions and include distractors.

### B.4 Long document summarisation

1. Select a long article or book section.
2. Provide the full text to the model and ask for a summary or a specific analysis (e.g., “Summarise the main arguments” or “List the characters and their relationships”).
3. Compare the output to a human‑written summary or reference answer.  Evaluate how performance degrades with length and whether the model captures information from the middle sections.

### B.5 Position sensitivity heatmap

For each position *p* in {1 k, 4 k, 16 k, 64 k, …}, embed a retrieval query and measure the model’s success rate.  Plot the results to visualise where the model focuses its attention.

## C. Glossary

**Context window:** The maximum number of tokens that an LLM can process in a single forward pass.

**Nominal context:** The advertised maximum context length (e.g., 128 k tokens).  It is the upper bound on input length supported by the model and serving stack.

**Effective context:** The portion of the context window that the model actually uses.  Effective context may be much smaller than nominal due to positional biases and training distribution【812281553901334†L65-L76】.

**Key–value (KV) cache:** The memory used to store key and value vectors for each token in each layer during inference.  It scales linearly with sequence length and model depth【563653443713035†L150-L171】.

**Prefill vs decode:** The prefill phase processes the entire context at once; decode generates tokens one by one.  Prefill complexity is O(N²) for full attention and O(N) for linear/sparse attention; decode is O(N) per token.

**FlashAttention:** A kernel that reorganises the attention computation to reduce memory bandwidth, enabling longer contexts at high throughput【563653443713035†L150-L171】.

**PagedAttention/vLLM:** A serving mechanism that stores KV tensors in a paged format and evicts unused pages to support large windows and concurrent requests.

**Position Interpolation (PI):** A method to extend rotary position embeddings (RoPE) by downscaling positions, enabling models trained on short sequences to extrapolate to longer ones【989342212075024†L50-L60】.

**YaRN:** A refinement of PI that reduces the amount of data needed during fine‑tuning and reaches 128 k tokens with fewer steps【556094126408083†L50-L60】.

**StRing:** A technique that shifts position indices during fine‑tuning to improve long‑context performance【199134859253240†L78-L94】.

**Infini‑attention:** A transformer variant that combines masked local attention with long‑term linear attention and a compressive memory to handle sequences of hundreds of thousands of tokens【100878192473897†L50-L60】.

## D. Design matrix summary

The CSV file `context-windows-design-matrix.csv` (see repository) lists the main families of methods (positional scaling, efficient attention, streaming/compressive, distributed full attention, external memory, system‑level optimisations) along with their complexity, typical effective length, advantages and caveats.  Use this matrix to compare techniques and decide which to apply in your project.