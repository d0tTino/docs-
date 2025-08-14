---
title: Context Windows Deep Dive
tags: [research, long-context]
series: context-windows
project: ai-research
updated: 2025-08-09
---

# Context Windows in Large Language Models: A Deep Dive

## Executive summary

Language models have undergone a rapid expansion in **context window** sizes over the past few years. While early models like GPT‑3 processed only 2 k–4 k tokens, state‑of‑the‑art models in mid‑2025 claim to handle hundreds of thousands or even millions of tokens【477669928722032†L226-L297】【480357281697940†L79-L83】. Larger contexts unlock new capabilities: summarising entire codebases, analysing multiple documents, preserving conversational state over long dialogues and performing multi‑step reasoning across disparate passages. However, the path from nominal context length to *effective* context is fraught with practical constraints.

This deep dive explains **why models have different context sizes**, explores the **limitations** imposed by memory, compute and positional encodings, and surveys the **techniques** that push LLMs toward effectively infinite context. We provide formulas and capacity planners, summarise model context sizes, outline evaluation benchmarks and propose a multi‑tier architecture for exploiting long contexts responsibly. This document complements the existing *Context Windows Field Guide*, offering additional depth, background and actionable guidance.

## 1. Introduction: context windows and their significance

The **context window** is the maximum number of tokens a model consumes per inference request. A token is roughly ~¾ of a word in English; a 32 k token input corresponds to ~49 pages of text【477669928722032†L226-L297】. Context length matters because it determines how much information can be considered at once. With a larger window, an LLM can ingest more supporting documents, maintain dialogue across long conversations and perform reasoning that spans multiple pages or code files.

The expansion from 2 k tokens to 32 k, 128 k and beyond means that models can summarise books, entire code repositories and cross‑reference long legal documents【477669928722032†L226-L297】【480357281697940†L79-L83】. Researchers have even demonstrated context windows up to 10 million tokens for code analysis【480357281697940†L79-L83】. Despite these advances, *context is expensive*: memory and compute scale at least linearly (and for standard attention, quadratically) with sequence length, and the model’s advertised context does not always reflect what it uses effectively.

### 1.1 Nominal vs. effective context

The **nominal context length** is the advertised maximum sequence length (e.g., 128 k tokens). The **effective context** is the portion of the input that the model actually attends to and utilises during inference. Empirical studies show that models often prioritise the beginning and end of long sequences, ignoring middle sections—a phenomenon known as the *lost‑in‑the‑middle* effect【812281553901334†L65-L76】. Even models trained with 32 k–128 k context lengths attend less to information placed in the middle, highlighting that effective context is usually shorter than the nominal maximum.

Factors influencing effective context include the distribution of positions seen during training, the choice of positional encoding, memory bandwidth and architecture‑specific biases. Meaningful evaluation requires tasks like retrieval, aggregation and reasoning across different positions, such as the **RULER** benchmark and **LongBench**【812281553901334†L65-L76】.

### 1.2 Memory and compute scaling

For a transformer with **L** layers, **H** heads and head dimension **d**, storing the **key–value (KV) cache** for each token requires approximately

\[
\text{KV\_memory\_bytes} = 2 \times L \times H \times d \times \text{seq\_length} \times \text{dtypeBytes},
\]

where the factor 2 accounts for keys and values. For example, a 70 B parameter model with around L≈80, H≈64 and d≈128 uses about 2.6 MiB per thousand tokens in FP16【563653443713035†L150-L171】. A **16 k** request thus consumes over **40 GiB** of GPU memory for the KV cache alone【563653443713035†L150-L171】. Activation memory (for back‑prop during training) and OS overhead push memory requirements even higher. Techniques like gradient accumulation, gradient checkpointing, reversible layers and memory‑efficient optimisers are used to train long contexts【477669928722032†L344-L360】, but at inference time the KV cache usually dominates memory usage.

Compute also grows quadratically with sequence length in standard self‑attention, because every token attends to every other token. FlashAttention and other IO‑aware kernels reduce overhead by fusing operations and optimising memory accesses, but do not change the asymptotic cost. Linear and sparse attention schemes aim to reduce complexity (see section 5).

## 2. Landscape of context sizes (2025)

The last two years have seen a proliferation of LLMs boasting large contexts. Table 1 summarises representative context windows and common use cases based on publicly reported figures.

| Model / system | Nominal context window | Notes |
|---|---|---|
| **GPT‑3** | 2 k | Early large model; limited context restricts reasoning to short prompts【477669928722032†L226-L297】. |
| **Mistral 7B** | 8 k | Mid‑sized open‑source model; typical for 2023–24. |
| **GPT‑4o** | 60 k–128 k | Multi‑modal model; high‑quality context for code and chat【477669928722032†L226-L297】. |
| **Claude 3.5** | 100 k | Good summarisation; widely used for legal and technical docs. |
| **Llama 3.1 (Meta)** | 128 k | Extended using position scaling; used in retrieval‑augmented tasks. |
| **Gemini 1.5 Pro** | up to 1 M | Google claims 1M tokens; experiments with 10 M tokens on code bases【480357281697940†L79-L83】. |
| **Magic.dev LTM‑2‑Mini** | 100 M | For code repository analysis; uses retrieval and compression【480357281697940†L79-L83】. |
| **Llama 4 Scout** | 10 M | Experimental; used for continuous memory in embodied agents【480357281697940†L79-L83】. |
| **GPT‑4.1, Gemini 2.5 Flash / Pro, Llama 4 Maverick** | 1 M | Commercial models with million‑token context【480357281697940†L79-L83】. |
| **Claude 4 (Opus/Sonnet)** | 200 k | Balanced context size for chat and summarisation【480357281697940†L82-L89】. |
| **DeepSeek R1 /V3** | 128 k | Chinese open‑source models for code and text【480357281697940†L90-L93】. |

These nominal lengths reflect training setups and marketing claims. Effective context can be much smaller, and many tasks do not benefit beyond 32 k–64 k. Instead of chasing ever‑larger windows, practitioners should evaluate whether longer contexts deliver meaningful gains relative to cost and complexity.

## 3. Why context sizes differ

### 3.1 Training context length and positional encodings

Most transformer‑based LLMs are trained on fixed‑length segments, typically 1 k–4 k tokens. Extending the context requires either training on longer sequences or **extrapolating** existing positional encodings. Rotary Position Embedding (RoPE) is widely used; it encodes positions as rotations in complex space. However, RoPE extrapolates poorly beyond its trained window. 

Several techniques have emerged to extend RoPE:

1. **Position Interpolation (PI)** rescales input positions to fit within the original window, preventing large rotation angles. PI extends 4 k models to 32 k or more with minimal fine‑tuning and preserves in‑window quality【989342212075024†L50-L60】.
2. **YaRN (Yet another RoPE extension)** fine‑tunes using a truncated normal schedule that covers a wide range of positions while requiring fewer tokens than PI. YaRN enables Llama models to extrapolate to 128 k with 10× less data and 2.5× fewer steps than previous methods【556094126408083†L50-L60】.
3. **StRing** (Shifted Rotary Position Embedding) shifts positions so that queries and keys attend using positive phase differences. StRing improves long‑context performance and enables up to 128 k effective context on Llama 3.1 70B, outperforming GPT‑4‑128k and Claude 2 on retrieval tasks【199134859253240†L78-L94】.
4. **ALiBi** (Attention with Linear Bias) adds a position‑dependent bias term; it naturally extrapolates to longer contexts but may degrade quality at shorter lengths. It is used in models like BLOOM and EleutherAI GPT‑NeoX.
5. **NTK scaling** (a relative attention scaling method) adjusts frequencies to match Neural Tangent Kernel properties; combined with RoPE it improves extrapolation.

Relative positional encodings and learned positions (e.g., T5) can also generalise beyond training but often require training on long sequences for best performance.

### 3.2 Memory and compute ceilings

As illustrated earlier, the KV cache scales linearly with sequence length and model size【563653443713035†L150-L171】. Memory fragmentation, limited GPU memory and scheduler constraints can reduce usable context. Systems like **FlashAttention** fuse operations to reduce IO and memory overhead, enabling efficient exact attention. **PagedAttention** (vLLM) implements a multi‑paged KV cache that evicts least‑used blocks and reduces fragmentation, allowing 128 k contexts on consumer GPUs.

#### KV‑cache capacity planning

To better understand how sequence length and model size impact memory usage, we provide a simple **capacity planner** script (`kv_capacity.py`) and a generated chart.  The script computes the KV cache memory for different models and sequence lengths using the formula above:

\[\text{KV\_memory\_bytes} = 2 \times L \times H \times d \times \text{seq\_len} \times \text{dtypeBytes}.\]

The accompanying chart (Figure 1) shows memory requirements (GiB) for Llama‑7B, Llama‑13B and Llama‑70B models at 4 k, 8 k, 32 k, 128 k and 512 k token windows when using fp16 precision.  As sequence length increases, memory consumption grows rapidly, particularly for large models.  For example, a single 128 k request on Llama‑70B requires about 320 GiB just for the KV cache.  Such calculations illustrate why scaling beyond 32 k–64 k tokens demands careful resource planning.

![KV cache memory requirements for different models and sequence lengths](kv-cache-chart.png)

You can run `kv_capacity.py` (provided in this repository) to compute custom tables or generate updated plots for your hardware and models.  Use `python kv_capacity.py --plot --output <filename>` to save a PNG.

### 3.3 Serving stack constraints

Inference frameworks significantly influence effective context. **vLLM** uses a paged KV cache and asynchronous scheduling to support long contexts and high throughput. **FasterTransformer** and **DeepSpeed** provide optimised kernels but have different memory footprints. When the KV cache saturates GPU memory, some frameworks offload to CPU or disc, incurring latency. Data centre hardware (PCIe vs NVLink) and memory bandwidth thus determine practical context windows.

### 3.4 Model architecture and inductive bias

Beyond the transformer, alternative architectures exhibit different context properties:

- **Efficient attention** uses local or sparse patterns; examples include **Longformer** (sliding window + global attention)【222591077498926†L48-L60】, **BigBird** (random + global + block attention) and **Performer** (linear attention via kernel approximations). These reduce cost but may lose global dependencies.
- **State‑space models** like **Mamba** and the **Legendre Memory Unit (LMU)** treat sequences as continuous dynamical systems, offering linear memory but potentially limited long‑range modelling.
- **Compressive transformers** append a second memory to store compressed summaries of past tokens and enable arbitrarily long sequences.【100878192473897†L50-L60】. **Transformer‑XL** uses segment‑level recurrence and relative position encodings to extend context and speed up evaluation【626234754762794†L260-L315】.
- **Ring Attention** distributes long sequences across multiple devices, performing blockwise attention with overlapping communications. It achieves sequences millions of tokens long without approximations【138967914803289†L71-L85】.

### 3.5 Data distribution and training curriculum

Long context models require training on long sequences. However, natural language corpora rarely contain contiguous passages of 32 k+ tokens. Data must be concatenated or artificially generated, and curriculum schedules (increasing context gradually) help models generalise. Strategies like **gradient accumulation** and **curriculum learning** are used【477669928722032†L344-L360】. Without proper training, models with long windows may overfit to local patterns and fail to utilise the full context.

## 4. Effective context and failure modes

### 4.1 Lost-in-the-middle and position sensitivity

The *lost‑in‑the‑middle* effect arises when relevant information placed in the middle of a long context is ignored. Studies reveal that retrieval accuracy peaks when the key passage is near the beginning or end of the context, degrading when placed mid‑sequence【812281553901334†L65-L76】. This occurs even in long‑context models, indicating that attention weights are not uniformly distributed. Effective context is thus limited by inductive biases and training distribution. Benchmarks such as **RULER** (Retrieval, Multi‑step Reasoning and Evidence), **Lost‑in‑the‑Middle** and **InfiniteBench** evaluate position sensitivity by inserting “passkeys” at different positions and measuring retrieval success.

### 4.2 Long-range dependency and forgetting

Long contexts can lead to **vanishing gradients** during training, causing the model to forget earlier content. Attending over hundreds of thousands of tokens dilutes attention weights, especially with softmax normalisation. Streaming and compressive architectures mitigate this by summarising past segments, but they can lose fine‑grained information. Retrieval‑augmented models may over‑rely on retrieved documents, ignoring remote parts of the current context.

### 4.3 Cost and latency trade‑offs

Doubling sequence length roughly doubles prefill time (loading tokens into the model) and memory usage. Multi‑turn interactive sessions may pay this cost repeatedly. Serving a 128 k input on a 70 B model can take tens of seconds and consume >40 GiB of VRAM【563653443713035†L150-L171】. Developers must weigh context length against throughput, latency and cost. Batching and KV sharing across requests improve efficiency but complicate scheduling.

## 5. Techniques for extending context windows

### 5.1 Positional scaling and interpolation

As described in section 3.1, **Position Interpolation** and **YaRN** enable RoPE models to extrapolate to 32 k–128 k tokens with limited fine‑tuning【989342212075024†L50-L60】【556094126408083†L50-L60】. PI rescales positions while YaRN samples from a truncated normal distribution; both maintain in‑window accuracy. **StRing** further shifts positions to mitigate phase drift and improves effective context【199134859253240†L78-L94】. More recent methods (e.g., **NTK‑scaled RoPE**, **CARoPE**) adjust frequencies to match kernel eigenvalues.

**ALiBi** uses linear biases relative to position differences; it naturally extends to long contexts but may trade off accuracy at shorter lengths.

### 5.2 Efficient, sparse and linear attention

**Longformer** introduces a sliding window attention pattern with optional global tokens, achieving linear complexity and performing well on long document tasks【222591077498926†L48-L60】. **BigBird** and **LED** (Longformer Encoder–Decoder) extend these ideas to the encoder–decoder setting. **Performer** uses kernel tricks (FAVOR+) to approximate softmax attention in linear time, enabling very long contexts but sometimes at the cost of lower accuracy. **Reformer**, **Linear Transformer** and **Retentive Networks** provide alternative linear attention mechanisms. These methods drastically reduce compute and memory, but the restricted receptive field can harm tasks requiring global cross‑attention.

### 5.3 Streaming and compressive attention

**Transformer‑XL** caches hidden states from previous segments and uses relative positional encodings, effectively extending context across segments and reducing computation【626234754762794†L260-L315】. **Compressive Transformers** compress past memories into smaller representations with learned convolution kernels. **StreamingLLM** uses *attention sinks*—special tokens that summarise past context and maintain state. **Infini‑attention** adds a compressive memory inside each transformer block, combining masked local attention with long‑term linear attention to handle extremely long sequences【100878192473897†L50-L60】. These models support streaming input and require bounded memory per time step, making them suitable for real‑time, long‑running conversations.

### 5.4 Distributed full attention

When high accuracy across the entire context is required, approximate methods may be insufficient. **Ring Attention** distributes the sequence across multiple GPUs or TPUs and performs blockwise full attention, overlapping communication with computation【138967914803289†L71-L85】. This approach enables sequences millions of tokens long without approximations, but requires high‑bandwidth interconnects and careful scheduling. It is used in training extremely long context models and for certain “hero run” analyses.

### 5.5 External memory and retrieval augmentation

Long contexts are not always the best way to capture long‑term knowledge. **Retrieval‑augmented models** like **kNN‑LM** and **RETRO** attach an external memory of billions of tokens. At inference time, the model retrieves relevant chunks based on the current query and cross‑attends to them【605812693674672†L49-L63】【897139308669472†L78-L95】. This decouples knowledge storage from the context window: a small model with a short context can outperform a much larger model by looking up relevant information. kNN‑LM uses a nearest neighbour search over the model’s own embeddings, while RETRO employs a BERT‑based retriever and chunked cross‑attention. Retrieval augmentation requires building and maintaining a large vector store but avoids the quadratic cost of long context attention.

### 5.6 System‑level optimisations

Implementing long contexts also requires system‑level improvements. **FlashAttention** (FA‑1, FA‑2, FA‑3) fuses attention operations to maximise memory bandwidth and reduce activation recomputation; FA‑2 and FA‑3 further accelerate multi‑query and group‑query attention. **PagedAttention** (vLLM) manages KV cache pages and evicts blocks when they become inactive, enabling long contexts on commodity GPUs. **ZeRO** and **DeepSpeed** partition parameters and optimiser states across devices, reducing memory usage during training. Combined with memory quantisation and mixed precision (e.g., fp8), these improvements allow models to handle longer contexts without sacrificing throughput.

## 6. Evaluating long contexts

Proper evaluation of long‑context models requires tasks that test retrieval, reasoning and aggregation across the entire sequence. Some guidelines:

1. **Needle‑in‑a‑haystack (NIAH):** Place a key sentence (needle) at different positions in a long sequence filled with distractors. Ask the model to answer a question requiring that sentence. Measure accuracy by position.
2. **Multi‑step retrieval and aggregation:** Provide multiple short facts scattered across the context and ask the model to compute an aggregate (sum, average, logical AND). Evaluate correctness and error patterns.
3. **Long document summarisation:** Provide a long article or book chapter; evaluate whether the summary captures salient points from across the document. Use metrics like ROUGE and human judgments.
4. **Multi‑document reasoning:** Concatenate several documents and require reasoning across them (e.g., cross‑document question answering). Benchmarks like **RULER**, **LongBench** and **InfiniteBench** include such tasks.
5. **Latency and throughput measurement:** Report prefill rate (tokens processed per second), decode rate and memory usage for different sequence lengths and hardware.

These evaluations help determine not just whether a model *can* accept a long context but whether it *uses* it effectively.

## 7. Multi‑tier architecture for effectively infinite context

Given the limitations of monolithic windows, a **multi‑tier architecture** can provide near‑infinite context by combining complementary methods:

1. **Tier 1 – Working set:** Use a moderately sized context (e.g., 32 k) with full attention and an efficient kernel like FlashAttention. Employ paged KV caches to maintain conversation state. This tier handles recent discourse and local reasoning.
2. **Tier 2 – Streaming or compressive memory:** Keep a compressed summary or hidden states of the longer history using streaming attention (Transformer‑XL, Infini‑attention). This provides long‑range continuity without storing all tokens.
3. **Tier 3 – External memory / retrieval:** Store entire documents or previous conversation segments in an external vector database. Retrieve relevant chunks using semantic search and cross‑attend to them. This tier supplies knowledge and remote context beyond the attention window.
4. **Optional Tier 4 – Distributed full attention:** For tasks requiring exact reasoning across the entire sequence (e.g., verifying code bases), run a full attention pass using Ring Attention on specialised hardware.

This layered design ensures that the system scales gracefully: local operations remain efficient, long‑range dependencies are retained, and knowledge is retrieved on demand.

## 8. Future directions

**Transformer alternatives:** Research into **state‑space models** (Mamba, RWKV), **hybrid recurrence‑attention architectures** and **neural Turing machines** aims to overcome quadratic scaling. Combining SSMs with attention may offer dynamic memory without explicit windows.

**Context compression and summarisation:** Automatic summarisation of chat history or code segments can reduce input length while preserving salient information. Learning which tokens to keep and which to compress remains a challenge.

**Data distribution and curricula:** Training models on natural long‑form data (books, audio transcripts) and synthetic long‑range tasks will improve effective context. Curriculum schedules that interleave short and long sequences help models generalise.

**Evaluation benchmarks:** As models exceed million‑token contexts, new benchmarks must stress reasoning, retrieval, and long‑term dependencies. Datasets like **InfiniteBench** and tasks like **Arcee** (long story comprehension) aim to fill this gap. Community efforts to share open source datasets and evaluation harnesses will standardise comparisons.

**Responsible use:** Long contexts can inadvertently capture sensitive or private information. Developers must design retrieval and summarisation pipelines that respect data privacy and implement safe content filters. There is also the risk of recency bias, where models over‑weight the most recent tokens; training methods to balance long and short dependencies are essential.

## 9. Conclusion

Context windows have evolved from thousands to millions of tokens, opening new frontiers for LLM applications. Yet, bigger is not always better: memory and compute requirements scale steeply, and effective context often lags far behind nominal capacity. By understanding the reasons behind context size differences—training length, positional encodings, memory ceilings, serving stack—and by leveraging a toolbox of techniques—positional scaling, efficient attention, streaming, distributed attention and retrieval augmentation—practitioners can design systems that use context judiciously.

Approaching *effectively infinite context* is less about training a single model with an arbitrarily long window and more about combining complementary methods into a layered architecture. Future research into state‑space models, compression and better curricula will continue to expand our ability to model long sequences efficiently and safely.

## See also

- [Context Windows Field Guide](context-windows-field-guide.md)
- [Context Windows Field Guide — Appendix](context-windows-appendix.md)
