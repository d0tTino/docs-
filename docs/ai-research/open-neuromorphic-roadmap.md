---
title: "Democratizing Brain-Inspired AI: A Strategic Analysis and 5-Year Roadmap for an Open Neuromorphic Ecosystem"
tags: [neuromorphic, roadmap, ai-research]
project: ai-research
updated: 2025-08-01
---

--8<-- "_snippets/disclaimer.md"

# Democratizing Brain-Inspired AI: A Strategic Analysis and 5-Year Roadmap for an Open Neuromorphic Ecosystem

[[toc]]

!!! info "Roadmap at a glance"
    This five-year report surveys the open neuromorphic computing ecosystem, contrasting large-scale research platforms with
    ultra-efficient edge accelerators to highlight the field's performance dichotomy and persistent software/tooling gaps. It
    outlines strategic investments needed to unify tooling, democratize hardware access, and stimulate application discovery so
    the ecosystem can scale beyond early adopters.

    - **Time horizon:** 2025–2030 roadmap aligned to upcoming funding cycles
    - **Scope:** Open and academically accessible neuromorphic hardware, software stacks, and supporting benchmarks
    - **Top findings:** Performance dichotomy between research-scale simulators and edge accelerators; ecosystem/tooling gaps;
      talent and access constraints throttling adoption
    - **Primary audience:** Research program officers, public-interest funders, and ecosystem-builders evaluating investment
      strategies
    - **Required tooling:** Familiarity with Lava, PyNN, NeuroBench, and mainstream ML frameworks (PyTorch, TensorFlow) for
      integration assessments

## 1 Executive Summary
Neuromorphic computing has evolved from a specialized academic discipline into a credible, though still developing, paradigm for ultra-low-power artificial intelligence. The current landscape is defined by a handful of pioneering platforms, notably Intel's Loihi 2, the European Union-backed SpiNNaker 2 and BrainScaleS-2 systems, and nascent commercial ventures such as BrainChip's Akida. These systems have demonstrated the potential for orders-of-magnitude improvements in energy efficiency for specific, event-driven workloads. However, the field's progression toward widespread adoption and democratization is critically constrained by a lack of software standardization, fragmented and immature development ecosystems, and highly restricted access to state-of-the-art hardware.

This report presents a comprehensive analysis of the open and academically accessible neuromorphic landscape, culminating in a strategic five-year roadmap intended to guide investment toward overcoming these critical barriers. The principal findings are as follows:

- **Performance Dichotomy**: The field is bifurcated into two distinct classes of systems. On one side are large-scale, highly flexible platforms designed for neuroscience simulation, such as SpiNNaker 2 and the Deep South project. On the other are smaller, application-specific, and exceptionally efficient inference accelerators for edge computing, like Akida and ODIN. At present, no single architecture provides a unified solution for both large-scale, flexible model exploration and ultra-low-power deployment.
- **Economic Realities**: While individual neuromorphic chips offer profound reductions in operational expenditure (OpEx) through minimal power consumption—with figures around 1 W for Loihi 2 and as low as 30 mW for Akida—their overall economic advantage is not yet established. The high capital expenditure (CapEx) associated with advanced semiconductor fabrication, coupled with the significant "hidden costs" of specialized software development and the scarcity of expert talent, currently prevents a favorable Total Cost of Ownership (TCO) compared to the mature and highly optimized GPU/TPU ecosystem for general-purpose AI tasks.
- **Critical Ecosystem Gaps**: The primary impediment to the democratization of neuromorphic AI is not the potential of the hardware but the immaturity of the surrounding ecosystem—a "software chasm." The lack of mature and user-friendly toolchains, significant friction in integrating with mainstream machine learning (ML) frameworks like PyTorch and TensorFlow, and the absence of a universally adopted benchmark suite analogous to MLPerf represent the most formidable barriers to broader adoption.

Based on this analysis, the proposed five-year roadmap recommends a strategic pivot in funding priorities. Instead of focusing on bespoke, single-investigator hardware projects, investments should be directed toward building foundational, shared ecosystem infrastructure. Key recommendations include:

- **Unifying the Ecosystem**: Funding the collaborative development and adoption of a universal Neuromorphic Intermediate Representation (NIR) to decouple software from hardware, and establishing a standardized benchmark suite, with NeuroBench as a leading candidate, to enable fair and rigorous performance comparisons.
- **Democratizing Access**: Creating federated cloud access programs to primary research hardware (Loihi 2, SpiNNaker 2, BrainScaleS-2) and sponsoring the development of open-source hardware reference designs on accessible, mature semiconductor process nodes.
- **Solving the Algorithm Deficit**: Launching targeted research initiatives to develop novel, non-gradient-based on-chip learning algorithms that natively exploit the unique temporal and sparse computational capabilities of neuromorphic substrates.

A concerted, strategic investment in this foundational infrastructure is poised to catalyze a virtuous cycle. Improved and standardized tools will attract a larger community of developers. This expanded community will create the "killer applications" that demonstrate undeniable value. In turn, these applications will drive commercial investment and further hardware innovation, ultimately realizing the transformative promise of a scalable, open, and profoundly energy-efficient paradigm for artificial intelligence.

## 2 The Open Neuromorphic Landscape: A Comparative Analysis
The current landscape of open and academically accessible neuromorphic computing is characterized by a rich diversity of architectural philosophies, each representing a different set of trade-offs between biological fidelity, computational efficiency, and programmability. This section provides a detailed comparative analysis of the most prominent platforms, moving beyond a simple catalog of specifications to dissect the strategic intent and technological compromises inherent in each design. The analysis is anchored by a comprehensive matrix that normalizes key metrics to facilitate direct comparison.

### 2.1 Comparative Landscape Matrix
The following table synthesizes quantitative specifications and qualitative assessments for the leading neuromorphic platforms.

| Feature | Intel Loihi 2 | Heidelberg BrainScaleS-2 | Manchester SpiNNaker 2 | BrainChip Akida | ODIN | Stanford Neurogrid | IBM NorthPole | Deep South |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Lead Organization | Intel Labs | Heidelberg University | TU Dresden / U. Manchester | BrainChip Inc. | UCLouvain | Stanford University | IBM Research | Western Sydney Univ. |
| Type | Digital, Asynchronous | Mixed-Signal, Accelerated | Digital, Many-Core | Digital, Event-Based | Digital, Asynchronous | Mixed-Signal, Real-Time | Digital, Inference Accelerator | Digital, FPGA-Based |
| Release Year | 2021 | 2022 | 2021 | 2022 | 2019 | ~2009 | 2023 | 2024 |
| Process Node | Intel 4 (~7nm) | 65nm | 22nm FDSOI | ~28nm (est.) | 28nm FDSOI | >180nm | 12nm | N/A (FPGA) |
| Die Area (mm²) | 31 | 32 | 43.79 | N/A | 0.086 | Board-level | 795 | System-level |
| Neurons | 1,048,576 | 512 | 152,000 | Configurable | 256 | 1,048,576 | 256 Cores | Simulates 100B+ |
| Synapses | 120 Million | 131,072 | 152 Million | Configurable (8MB SRAM) | 65,536 | 6 Billion | 224MB SRAM | Simulates 228T ops/s |
| On-Chip Learning | Yes (Programmable) | Yes (PPU-driven) | Yes | Yes (Limited) | Yes (SDSP) | No | No (Inference only) | N/A |
| Typical Power | ~1 W | ~1 W | ~2-5 W | ~30 mW | 30µW - 1mW | < 2 W (board) | ~74 W | Low (unspecified) |
| Dev-kit Cost / Access | INRC (Free loan/cloud) | EBRAINS (Free cloud) | EBRAINS / SpiNNcloud | PCIe: $289+ | Open-source (FPGA) | Academic Project | Proprietary | Remote access |
| License (HW/SW) | Proprietary / BSD-3 & LGPL | Proprietary / LGPL & PyNN | Proprietary / CeCILL & PyNN | Proprietary / Proprietary | Open (Verilog) / Open | N/A | Proprietary | Proprietary |
| Energy (pJ/SOP) | Not Reported | ~10 | Not Reported | ~3 (vendor claim) | 12.7 | Very Low | N/A (Non-SOP) | Very Low |
| Synaptic Density (M-synapses/mm²) | 3.87 | 0.004 | 3.47 | N/A | 0.76 | N/A | N/A | N/A |
| Throughput (G-SOPs/s/W) | >15,000 (8-bit ops) | High (accelerated) | High (parallel) | Very High | Low (single core) | High (real-time) | N/A (Non-SOP) | Very High |
| Dev-Tool Maturity (0-5) | 4 | 3 | 4 | 3 | 2 | 1 | N/A | 2 |
| Community Health (0-5) | 4 | 4 | 5 | 2 | 3 | 1 | N/A | 2 |
| Documentation Depth (0-5) | 4 | 3 | 4 | 2 | 3 | 1 | N/A | 2 |
| ML Workflow Integration (0-5) | 3 | 3 | 2 | 4 | 1 | 0 | N/A | 2 |

### 2.2 Digital, Asynchronous Processors: The Path to Determinism and Scale
This class of neuromorphic hardware leverages standard digital CMOS technology to create massively parallel architectures that communicate asynchronously. This approach prioritizes scalability, programmability, and deterministic behavior, making it a strong candidate for complex AI applications.

#### 2.2.1 Intel Loihi 2
Intel's Loihi 2 represents a significant investment by a major semiconductor manufacturer into brain-inspired computing. Fabricated on a pre-production version of the "Intel 4" process node, the 31 mm² chip integrates 128 programmable neuromorphic cores alongside six x86 Lakemont cores for system management and complex instruction execution. Each chip supports up to 1 million leaky integrate-and-fire (LIF) neurons and 120 million synapses. Key architectural advancements over its predecessor include support for "graded spikes," which carry a configurable 32-bit integer payload, fully programmable neuron models via microcode, and hardware support for advanced three-factor learning rules. This programmability allows researchers to move beyond simple neuron models and explore more complex, biologically plausible dynamics. The chip's typical power consumption is under 1 W, making it highly efficient for its computational capacity.

The Loihi 2 ecosystem is curated through the Intel Neuromorphic Research Community (INRC), which provides qualified academic and industry researchers with free access to hardware and software. Access is primarily facilitated through a cloud platform, though hardware systems like the single-chip Oheo Gulch and eight-chip Kapoho Point boards can be loaned for projects with specific on-site requirements. The primary software interface is Lava, an open-source Python framework developed by Intel. Lava is designed to be platform-agnostic, enabling development on conventional CPUs before deployment to Loihi hardware. Its dual-license model—permissive BSD-3 for high-level libraries and more restrictive LGPL-2.1 for low-level hardware mapping components—is designed to encourage community contribution while preventing proprietary forks of the core compiler technology.

From a performance perspective, Loihi 2's synaptic density of 3.87 M-synapses/mm² is among the highest for digital neuromorphic chips. While a direct energy-per-synaptic-operation (pJ/SOP) metric is not consistently reported in academic literature, system-level benchmarks provide strong indicators of its efficiency. The large-scale Hala Point system, comprising 1,152 Loihi 2 chips, can achieve over 15 trillion 8-bit operations per second per watt (TOPS/W) on conventional deep neural networks. Recent application studies in sensor fusion have demonstrated energy efficiency gains of over 100-fold compared to a CPU and nearly 30-fold compared to a GPU for the same task.

#### 2.2.2 Manchester SpiNNaker 2
The SpiNNaker (Spiking Neural Network Architecture) project, now in its second generation, represents a different philosophy focused on creating a massively parallel platform for real-time, large-scale brain simulation. Developed at the Technische Universität Dresden in collaboration with the University of Manchester, the SpiNNaker 2 chip is a many-core system built on a 22nm FDSOI process. Each chip contains 152 ARM Cortex-M4F application cores and one management core, with each application core modeling a population of neurons in software. This software-based approach provides immense flexibility in defining neuron and synapse models. A single chip can support approximately 152,000 neurons and 152 million synapses within a power envelope of 2-5 W. The architecture is explicitly designed for scale; the full "SpiNNcloud" system under construction aims to integrate up to 10 million ARM cores, enabling simulations that approach the scale of the human brain. In a nod to the growing convergence of neuroscience and AI, SpiNNaker 2 also includes dedicated hardware accelerators for common machine learning operations, such as matrix multiplication (MACs).

The SpiNNaker 2 ecosystem leverages well-established tools from the computational neuroscience community, primarily PyNN and NEST. This allows a large existing user base to port their models to the hardware with minimal changes. Hardware access is provided through the European Union's EBRAINS research infrastructure, a legacy of the Human Brain Project, offering free remote access to academic researchers. Commercialization efforts are being led by SpiNNcloud Systems GmbH.

With a reported die area of 43.79 mm², SpiNNaker 2 has a synaptic density of 3.47 M-synapses/mm², comparable to Loihi 2. Direct energy-per-operation figures are not readily available, but performance is often characterized by its real-time simulation capabilities and relative efficiency gains. The architecture is designed to deliver a 10-fold increase in neural simulation capacity per watt over the first-generation SpiNNaker. In specific reinforcement learning tasks, a SpiNNaker 2 implementation achieved up to a 32-fold reduction in energy consumption compared to a GPU baseline.

#### 2.2.3 BrainChip Akida
BrainChip's Akida processor is a commercially-driven digital neuromorphic system explicitly designed for ultra-low-power AI inference at the edge. Rather than focusing on biological simulation, Akida's architecture is optimized to accelerate mainstream machine learning models, including Convolutional Neural Networks (CNNs), Recurrent Neural Networks (RNNs), and Vision Transformers. It operates on an event-based principle, converting conventional sensor data (like image pixels) into a sparse, spike-like representation for processing. The AKD1000 chip supports configurable network topologies with low-precision weights and activations (1, 2, 4, or 8 bits), a key technique for reducing memory footprint and computational cost. While it supports on-chip learning, this capability is limited on the first-generation AKD1000 device to the final fully-connected layer and requires binary weights, constraining its use to specific adaptation tasks. Its most compelling feature is its extremely low power consumption, rated at approximately 30 mW during active operation.

The Akida ecosystem is geared toward commercial developers and engineers. Development kits are available for purchase, including a standalone PCIe board ($289-$499) and integrated systems with a Raspberry Pi or a Shuttle PC. This direct commercial availability stands in contrast to the gated, research-focused access models of Loihi 2 and SpiNNaker 2. The software stack, MetaTF, is built upon TensorFlow and Keras, signaling a clear strategy to integrate with established ML development workflows and lower the barrier to entry for AI practitioners.

BrainChip has published a standout energy efficiency metric of approximately 3 pJ/SOP. It is important to note that this is a vendor-reported figure and refers to an implementation in 28nm technology, which may differ from the process used for the current AKD1000 product. Nonetheless, it serves as a strong indicator of the architecture's potential for extreme energy efficiency in targeted inference tasks.

#### 2.2.4 ODIN
ODIN, developed at UCLouvain, is a landmark project as the first fully open-source digital spiking neuromorphic processor. Fabricated in a 28nm FDSOI process, the chip is remarkably small (0.086 mm²) and efficient, housing 256 neurons and 65,536 synapses with on-chip spike-driven synaptic plasticity (SDSP). Its primary significance lies not in its scale but in its accessibility. By making the complete Verilog hardware description language (HDL) source code available on GitHub, the ODIN project provides an invaluable resource for education, research, and as a foundation for future open-source designs. While the physical ASIC is not commercially available, the design can be synthesized and deployed on small FPGAs, making it one of the most democratized neuromorphic hardware platforms in existence. At the time of its publication, ODIN achieved a highly competitive energy efficiency of 12.7 pJ/SOP.

### 2.3 Mixed-Signal and Analog Systems: The Quest for Ultimate Efficiency
Mixed-signal architectures represent a fundamentally different approach, seeking to emulate the physics of neural computation directly in silicon. They use analog circuits to model neuron and synapse dynamics, which can be thousands of times more energy-efficient than digital simulation. However, this efficiency comes at the cost of precision, flexibility, and scalability.

#### 2.3.1 Heidelberg BrainScaleS-2
BrainScaleS-2 is a state-of-the-art mixed-signal neuromorphic system developed at Heidelberg University as part of the Human Brain Project. The ASIC combines an analog core, where 512 Adaptive Exponential Integrate-and-Fire (AdEx) neuron circuits and 131,072 synapses evolve in continuous time, with a digital periphery that handles event communication and on-chip learning. Its most distinctive feature is an acceleration factor of 1,000 compared to biological real-time; neural dynamics that occur in milliseconds in the brain are emulated in microseconds on the chip. This makes it uniquely suited for studying long-term plasticity and developmental processes that would be computationally intractable on other systems. On-chip learning is managed by embedded digital "Plasticity Processing Units" (PPUs), which can be programmed to implement a wide variety of plasticity rules, including those inspired by gradient-based optimization from machine learning.

The BrainScaleS-2 ecosystem, like that of SpiNNaker 2, is integrated into the EBRAINS platform, providing free remote access to the international research community. Its software stack is notably diverse, supporting the neuroscience-standard PyNN API while also embracing modern ML frameworks through hxtorch (a PyTorch-based library) and jaxsnn (a JAX-based library), indicating a strategic effort to bridge the gap between neuroscience and AI research.

The trade-offs of the analog approach are starkly illustrated by the system's physical characteristics. The 32 mm² die yields a synaptic density of just 0.004 M-synapses/mm², nearly three orders of magnitude lower than its digital counterparts. This is a direct consequence of the large silicon area required for analog components like capacitors and current sources. Furthermore, analog circuits are susceptible to manufacturing variations (device mismatch), which necessitates complex calibration procedures to ensure consistent behavior across the chip. Despite these challenges, the system's synapse drivers can process up to 125 million events per second, and its energy efficiency is estimated to be on the order of 10 pJ per synaptic event.

#### 2.3.2 Stanford Neurogrid
Though an older system (first operational around 2009), Stanford's Neurogrid remains a highly influential design that pioneered the hybrid analog-computation/digital-communication approach. It is a board-level system composed of 16 custom "Neurocore" chips, capable of simulating one million neurons and six billion synapses in real-time. Its core principle—using power-efficient analog circuits to emulate ion channel dynamics and robust digital routers to communicate spikes—laid the groundwork for many subsequent mixed-signal designs. Neurogrid demonstrated that this hybrid approach could achieve staggering efficiency, consuming less than 2 W for the entire board while performing a simulation that would have required a supercomputer consuming hundreds of kilowatts at the time. While primarily an academic research platform with no broad accessibility, its architectural legacy is a testament to the enduring appeal of analog efficiency.

### 2.4 Large-Scale and Non-Spiking Architectures
A final category includes systems that push the boundaries of scale or deviate from the traditional spiking neuron model, offering insights into alternative paths for brain-inspired computing.

#### 2.4.1 Deep South
The Deep South project at Western Sydney University is a neuromorphic supercomputer built not from custom ASICs but from commercially available Field-Programmable Gate Arrays (FPGAs). Its ambitious goal is to simulate brain-scale networks by achieving a throughput of 228 trillion synaptic operations per second, a rate comparable to that estimated for the human brain. The strategic use of FPGAs provides complete reconfigurability, allowing researchers to implement and test novel neuron models and network architectures without the prohibitive cost and time of fabricating new silicon. This flexibility is a key differentiator from ASIC-based systems. The project aims to make the system remotely accessible via a Python-based front-end, lowering the barrier for computational neuroscientists to conduct large-scale experiments. While specific power consumption figures are not yet published, the project's core motivation is to provide a massively parallel simulation platform that is significantly more power-efficient than conventional GPU-based supercomputers.

#### 2.4.2 IBM NorthPole
IBM's NorthPole is an AI inference accelerator that, while not a spiking neuromorphic processor, is profoundly brain-inspired in its architecture. Its design philosophy directly attacks the von Neumann bottleneck by eliminating off-chip memory access during inference. The 12nm chip integrates a massive 224 MB of SRAM distributed across 256 processing cores, effectively making the entire chip an "active memory". This memory-near-compute approach drastically reduces data movement, the primary source of energy consumption in conventional systems. NorthPole is specialized for low-precision (2, 4, and 8-bit) inference, a technique widely used to optimize deep learning models. It is a proprietary IBM research project and not open-source, but its design principles are highly influential. Its performance demonstrates the power of its architectural choices: on the ResNet-50 benchmark, it achieves 25 times higher frames-per-second-per-watt than a comparable 12nm GPU, showcasing the immense efficiency gains possible with specialized, brain-inspired dataflow and memory organization. A version of the technology is being developed for the U.S. Air Force, indicating a clear path toward real-world deployment.

The current landscape reveals a critical divergence between systems designed for neuroscience simulation and those designed for AI acceleration. Platforms like SpiNNaker 2 and BrainScaleS-2, with roots in the Human Brain Project, prioritize biological fidelity and simulation speed-up, supporting established neuroscience software like PyNN and NEST. In contrast, platforms like Intel's Loihi 2 and BrainChip's Akida are explicitly positioned as energy-efficient AI processors, with software stacks (Lava, MetaTF) designed to solve optimization problems and integrate with mainstream machine learning workflows. This split creates a rift in the ecosystem; tools and algorithms optimized for one domain are often ill-suited for the other. A successful democratization strategy must recognize this divide and either choose a focus or deliberately fund initiatives that bridge the two communities.

Furthermore, the model of hardware access is a crucial determinant of a platform's potential for democratization. The spectrum ranges from fully open-source hardware designs like ODIN, which offer maximum freedom but require significant user expertise for FPGA synthesis, to commercially available off-the-shelf products like Akida, which lower the barrier for funded teams. In between are the free-for-research cloud access models of EBRAINS (for SpiNNaker 2 and BrainScaleS-2) and the curated community model of Intel's INRC. Each model serves a different segment of the community. A comprehensive strategy should not favor one model but seek to lower the barriers within each: for example, by funding fabrication runs for open-source designs, providing hardware vouchers for commercial platforms, and expanding capacity on free cloud services.

Finally, the analysis reveals the severe and persistent trade-offs of analog computing. While mixed-signal systems like BrainScaleS-2 promise unparalleled energy efficiency by computing in the analog domain, they pay a steep price in silicon area. The synaptic density of BrainScaleS-2 is nearly three orders of magnitude lower than its digital counterparts, a direct result of the physical space required for analog circuits. This, combined with challenges like device mismatch and the need for extensive calibration, suggests that for scalable, general-purpose AI, the most viable near-term path lies in highly optimized digital architectures that adopt brain-inspired principles like asynchronicity and sparsity, rather than attempting a direct physical emulation of biological processes.

## 3 Economic Viability: A Total Cost of Ownership Perspective
To move beyond purely technical metrics and assess the real-world feasibility of neuromorphic computing, a robust economic analysis is essential. This section presents a Total Cost of Ownership (TCO) model that compares the projected lifecycle costs of deploying a large-scale neuromorphic computing cluster against a baseline system built with today's leading GPU technology. This analysis is critical for understanding the economic tipping points at which brain-inspired architectures may offer not just a performance advantage, but a compelling financial one.

### 3.1 The TCO Framework: Beyond Chip Price
A simplistic comparison of individual component costs is insufficient for strategic decision-making. A comprehensive TCO model must account for the full spectrum of expenses incurred over a system's operational lifespan, typically 3-5 years for high-performance computing (HPC) infrastructure. For this analysis, a 4-year TCO model is used, encompassing two primary categories of cost:

- **Capital Expenditure (CapEx)**: The upfront, one-time costs associated with acquiring and deploying the system. This includes not only the primary compute hardware (GPUs or neuromorphic chips) but also ancillary components like servers, high-speed networking fabrics (e.g., InfiniBand), storage systems, and the necessary data center infrastructure such as racks, power distribution units (PDUs), and cooling systems. It also includes initial software licensing and the significant, often underestimated, cost of system integration and initial application development.
- **Operational Expenditure (OpEx)**: The recurring costs required to run and maintain the system. The most significant of these are electricity for powering the hardware and for cooling the facility (accounted for by the Power Usage Effectiveness, or PUE, metric). OpEx also includes hardware and software maintenance contracts, and the salaries of the personnel required to operate, manage, and develop for the platform.

### 3.2 Baseline: TCO of a 1 PFLOPS GPU Cluster
To establish a baseline, we model the 4-year TCO for an HPC cluster capable of delivering 1 PetaFLOP of performance for typical AI workloads (e.g., 16-bit floating-point, or FP16). The NVIDIA H100 GPU is used as the reference component.

**CapEx Calculation**

An NVIDIA H100 PCIe (80GB) accelerator has a peak FP16 performance of approximately 2 PFLOPS (with sparsity). For a sustained 1 PFLOPS on real-world workloads, a conservative estimate requires approximately 500 H100 units. The market price for a single H100 card is approximately $31,000.

- **GPU Cost**: 500 units \* $31,000/unit = $15,500,000.
- **Ancillary Hardware**: Industry estimates suggest that servers, networking, storage, and other infrastructure typically add 50% to 100% of the accelerator cost to the total hardware bill. Using a conservative 75% multiplier, this adds approximately $11,625,000.
- **Total Estimated CapEx**: $15,500,000 + $11,625,000 = ~$27,125,000.

**OpEx Calculation**

- **Power Consumption**: An NVIDIA H100 GPU has a Thermal Design Power (TDP) of up to 700 W. A high-density server containing eight H100s, along with CPUs and other components, can consume 10-12 kW. A 500-GPU cluster would require approximately 63 such servers, leading to a total power draw of roughly 63 \* 12 kW = 756 kW.
- **Electricity Cost**: Using a U.S. average data center electricity rate of $0.1063 per kWh and a typical PUE of 1.6 (representing the overhead for cooling and power delivery), the annual power cost is calculated as:

```text
756 kW × 8760 hours/year × $0.1063/kWh × 1.6 PUE ≈ $1,126,000 per year
```

- **Maintenance and Personnel**: Annual hardware/software maintenance is often estimated at 10-15% of CapEx. Personnel costs for a team of engineers to manage and operate the cluster can easily exceed $1,000,000 annually. A conservative combined estimate is ~$2,000,000 per year.
- **Total 4-Year OpEx**: ($1,126,000 + $2,000,000) \* 4 = ~$12,504,000.

**Total 4-Year TCO (GPU Baseline)**: $27,125,000 (CapEx) + $12,504,000 (OpEx) = ~$39,629,000.

### 3.3 TCO Model for a 1 PFLOPS-Equivalent Neuromorphic Cluster
Modeling the TCO for a neuromorphic cluster is more speculative due to the lack of a commercial market for large-scale systems. However, by using publicly available data on chip fabrication and system prototypes, a plausible estimate can be constructed. We use Intel's Loihi 2 as the reference component.

**CapEx Calculation**

- **Chip Cost**: The cost of a neuromorphic chip is derived from the underlying wafer cost. Loihi 2 is fabricated on the "Intel 4" process, which is a 7nm-class technology. A 300mm wafer on a 7nm node is estimated to cost approximately $9,346. The Loihi 2 die is 31 mm². A 300mm wafer yields approximately 1,800 gross dies of this size. Assuming an aggressive but plausible 70% yield for a mature process, this results in ~1,260 good dies per wafer.
- **Cost per Good Die**: $9,346 / 1,260 ≈ $7.50.
- **After accounting for packaging, testing, and a commercial margin, a reasonable volume cost per chip is estimated to be between $50 and $150. We use $100 for this model.**
- **System Scale**: The performance equivalence between FLOPs and Synaptic Operations (SOPs) is not direct. However, we can use Intel's Hala Point system as a reference. Hala Point uses 1,152 Loihi 2 chips to achieve a peak performance of 20 PetaOps/second (8-bit). To achieve a sustained 1 Peta-equivalent-OP/second (assuming 1 FLOP ≈ 1 SOP for this high-level model), we would need approximately 1/20th of the Hala Point's peak performance, or roughly 58 Loihi 2 chips. To build a full system with redundancy and communication overhead, a cluster of 100 Loihi 2 chips is a conservative starting point. This highlights a potential ambiguity: if we scale to 1 PFLOPS, we would need ~50 Hala Point systems, or ~57,600 chips. This discrepancy reveals the difficulty in comparing performance metrics. For this TCO, we will model a system with ~50,000 chips to achieve a comparable raw operation count.
- **Chip Cost**: 50,000 chips \* $100/chip = $5,000,000.
- **Ancillary Hardware**: Assuming a similar 75% overhead for system integration.
- **Total Estimated CapEx**: $5,000,000 + $3,750,000 = ~$8,750,000.
- **Initial Development Cost ("Talent Tax")**: The scarcity of engineers with deep expertise in neuromorphic software and hardware necessitates a significant upfront investment in talent acquisition and training, adding an estimated $2,000,000 to the initial project cost.

**OpEx Calculation**

- **Power Consumption**: The 1,152-chip Hala Point system consumes a maximum of 2.6 kW. A 50,000-chip cluster would therefore consume approximately (50,000 / 1,152) \* 2.6 kW ≈ 113 kW.
- **Electricity Cost**: Using the same model as the GPU cluster:

```text
113 kW × 8760 hours/year × $0.1063/kWh × 1.6 PUE ≈ $168,000 per year
```

This represents a nearly 7-fold reduction in power and cooling costs.
- **Maintenance and Personnel**: While maintenance costs may be lower due to simpler hardware, the cost for specialized personnel would be significantly higher than for a standard HPC cluster. We estimate a combined cost of ~$2,500,000 per year, reflecting the premium for rare expertise.

**Total 4-Year TCO (Neuromorphic Projection)**: ($8,750,000 + $2,000,000) (CapEx) + ($168,000 + $2,500,000) \* 4 (OpEx) = ~$21,422,000.

### 3.4 TCO Summary and Analysis

| Cost Component | NVIDIA H100 Cluster (Baseline) | Projected Neuromorphic Cluster | Delta (Neuromorphic Advantage) |
| --- | --- | --- | --- |
| CapEx (Hardware) | $27,125,000 | $8,750,000 | -$18,375,000 |
| CapEx (Initial Development) | Included in Personnel | $2,000,000 | +$2,000,000 |
| OpEx (Power & Cooling) | $4,504,000 | $672,000 | -$3,832,000 |
| OpEx (Maintenance & Personnel) | $8,000,000 | $10,000,000 | +$2,000,000 |
| **Total 4-Year TCO** | **$39,629,000** | **$21,422,000** | **-$18,207,000 (46% Reduction)** |

The economic analysis reveals that the strategic advantage of neuromorphic computing is not merely in the potential for cheaper individual chips, but in a fundamental restructuring of the cost profile for large-scale AI. While the upfront capital expenditure for a neuromorphic cluster is projected to be substantially lower due to smaller, simpler chip designs, the most profound and durable advantage lies in the dramatic reduction of operational expenditure. The model shows a nearly 7-fold decrease in power and cooling costs, a direct consequence of the architecture's inherent energy efficiency. This is the central economic argument for the technology: in a future where data center power is a constrained and increasingly expensive resource, the low-OpEx nature of neuromorphic computing becomes a decisive strategic asset, offering a path to sustainable scaling of AI capabilities.

However, this potential is tempered by a significant, non-obvious cost: the "talent tax." The ecosystem for conventional AI is mature, with millions of developers proficient in CUDA, PyTorch, and TensorFlow. In contrast, the pool of engineers with deep expertise in neuromorphic frameworks like Lava or the intricacies of SNNs is orders of magnitude smaller. This scarcity inflates salaries, extends development timelines, and increases project risk. As modeled, the higher personnel costs can offset a significant portion of the operational savings in the near term. This underscores a critical point: a successful democratization strategy cannot focus on hardware alone. It must aggressively invest in education, documentation, and the simplification of software tools to lower this "talent tax." Without a concerted effort to grow the developer community, even free and highly efficient hardware will face a prohibitive TCO due to the high cost and low availability of human capital.

## 4 Bridging the Chasm: Opportunity and Gap Analysis
Despite significant advances in hardware, the open neuromorphic ecosystem is confronted by critical gaps in fabrication, software, and standardization that collectively impede its transition from research novelty to mainstream technology. This section provides a systematic analysis of these deficiencies, identifying high-impact opportunities for strategic intervention.

### 4.1 Hardware and Fabrication Gaps
While neuromorphic ASICs demonstrate impressive performance, fundamental limitations in their design and accessibility constrain the pace of innovation.

- **Limited On-Chip Learning Flexibility**: A key promise of neuromorphic computing is continuous, online learning at the edge. However, current hardware implementations fall short of this goal. For instance, the commercially available BrainChip Akida AKD1000 restricts on-chip learning to the final fully-connected layer and requires binary weights, which is suitable for simple adaptation but not for complex, deep learning tasks. Intel's Loihi 2 offers highly programmable learning rules via microcode, but this flexibility comes with significant implementation complexity, requiring specialized, low-level expertise. The mixed-signal BrainScaleS-2 platform supports flexible plasticity rules through its embedded digital processors, but these operations are constrained by the physical properties of the analog substrate. This contrasts sharply with the universal and highly optimized backpropagation algorithm that runs on any GPU, representing a major gap in functional capability.
- **Architectural Inflexibility of ASICs**: Application-Specific Integrated Circuits (ASICs) like Loihi 2 and Akida achieve their efficiency through specialization. Their neuron models, connectivity schemes, and data pathways are physically baked into the silicon. While this provides immense speed and efficiency for intended workloads, it inherently limits architectural exploration. Researchers cannot fundamentally alter the neuron dynamics or network topology beyond the provided programmable parameters. This rigidity is a barrier to testing novel brain-inspired theories that may not map well to existing hardware. This is a primary motivation for FPGA-based systems like Deep South, which trade the raw efficiency of an ASIC for the complete reconfigurability needed for foundational research.
- **The Fabrication Accessibility Barrier**: The most advanced neuromorphic chips are fabricated on cutting-edge or specialized semiconductor process nodes, such as Intel 4 for Loihi 2 and 22nm FDSOI for SpiNNaker 2. The cost of designing and fabricating a chip on these nodes runs into the tens of millions of dollars, placing it far beyond the reach of academic research groups, startups, or the open-source community. While fully open-source hardware designs like ODIN (fabricated on a more accessible 28nm process) are a crucial first step, they remain largely academic artifacts without viable and affordable pathways to fabrication, such as subsidized multi-project wafer (MPW) shuttle programs.

### 4.2 Software and Algorithmic Gaps: The Core Bottleneck
The single greatest impediment to the adoption of neuromorphic computing is the state of its software. The hardware's potential is currently locked behind immature, fragmented, and difficult-to-use toolchains.

- **Toolchain Immaturity and Usability**: While frameworks like Intel's Lava and the community-driven Nengo are powerful, they lack the maturity, polish, and extensive library support of their mainstream counterparts, TensorFlow and PyTorch. The learning curve is steep, and documentation, while improving, often assumes a high level of domain expertise. An examination of the public GitHub issue trackers for core libraries like Lava reveals a community actively working to build out fundamental features, fix bugs, and improve usability, which is indicative of a project in a state of rapid development rather than mature stability. This state of flux creates a high barrier to entry for developers from outside the core neuromorphic community.
- **Friction with Mainstream ML Workflows**: For neuromorphic computing to be adopted by the broader AI community, it must integrate seamlessly into existing development and deployment (MLOps) pipelines. Current solutions create significant friction. Frameworks like BrainChip's MetaTF and Nengo's NengoDL require a multi-step process to convert a standard Artificial Neural Network (ANN) into a Spiking Neural Network (SNN) that can run on the hardware. This process often involves quantization-aware retraining and careful hyperparameter tuning to recover accuracy lost during conversion, adding complexity and time to the development cycle. This is a stark contrast to the one-click deployment that AI developers have come to expect from the GPU ecosystem.
- **The Training Algorithm Deficit**: The field has yet to produce a broadly applicable, efficient, and purely event-based training algorithm that can rival the power of backpropagation. The dominant methods for training SNNs remain indirect: either converting a pre-trained ANN or using "surrogate gradients," where the non-differentiable spiking function is replaced with a smooth approximation during training. While effective, these methods do not fully leverage the temporal dynamics and event-driven nature of the hardware. The search for truly novel, on-chip learning paradigms that can learn from sparse, temporal data online is a primary focus of advanced research, as evidenced by the goals of DARPA programs like µBRAIN, which seeks inspiration from the extreme efficiency of insect brains.
- **Lack of a Universal Intermediate Representation (IR)**: The neuromorphic ecosystem critically lacks a standard, compiler-friendly intermediate representation analogous to ONNX in the conventional AI world. Currently, each hardware platform has its own proprietary backend and programming model. This forces high-level frameworks like PyNN and Nengo to develop and maintain separate, complex compiler pathways for each hardware target they wish to support. This duplicates effort across the community and makes it difficult to port applications from one hardware platform to another. The community-led Neuromorphic Intermediate Representation (NIR) initiative is a promising step toward solving this problem, but it requires significant investment and broad adoption to become a true standard.

### 4.3 Ecosystem and Standardization Gaps
Beyond the specific hardware and software challenges, the broader ecosystem suffers from a lack of the connective tissue that enables mature technology fields to thrive.

- **The Benchmarking Vacuum**: The field cannot systematically measure progress or validate performance claims without a standardized, widely accepted benchmark suite. There is no neuromorphic equivalent of MLPerf, which has been instrumental in driving competition and innovation in the conventional AI hardware space. This makes it exceedingly difficult for users to perform fair, apples-to-apples comparisons of different hardware and software solutions. Emerging efforts like NeuroBench are a direct response to this critical gap, but they are still in their infancy and require community-wide support to become authoritative. Standard benchmarks like MLPerf Tiny are not designed to capture the unique advantages of event-based computation and temporal dynamics, making them unsuitable for evaluating neuromorphic systems.
- **A Fragmented Community**: The neuromorphic world is largely split into two distinct communities with different goals, vocabularies, and values. The first is rooted in computational neuroscience, using platforms like SpiNNaker and BrainScaleS to simulate and understand the brain. The second is rooted in computer engineering and AI, using platforms like Loihi and Akida to build efficient accelerators for machine learning tasks. While there is overlap, the communities often operate in parallel, slowing the cross-pollination of ideas. Organizations like Open Neuromorphic (ONM) are actively working to create a unified community, but this remains a significant cultural challenge.
- **Inconsistent and Gated Access Models**: As previously discussed, the pathway for a researcher or developer to gain access to hardware is inconsistent and often opaque. The process can involve joining a corporate research community (Intel's INRC), applying for access on a European research infrastructure (EBRAINS), purchasing a commercial development kit, or attempting to synthesize an open-source design onto an FPGA. This lack of a simple, unified access model is a major barrier to democratization and open, reproducible research.

The state of the field reflects a classic technology-pushed dynamic, where the hardware capabilities have outpaced the software required to effectively utilize them. A director at Intel Labs has noted that "the state of neuromorphic hardware currently leads the state of neuromorphic computing software". This creates a dangerous cycle: without compelling and easy-to-use software, there is no market pull to drive hardware adoption and investment; but without stable and accessible hardware, the software community lacks a platform upon which to build. The most effective strategy to break this cycle is to shift investment focus from developing ever-more-advanced hardware to building the software and ecosystem infrastructure that can unlock the potential of the hardware that already exists.

The most critical piece of this missing infrastructure is a common compiler framework, analogous to LLVM in the world of conventional computing. The current paradigm, where each software framework builds a bespoke compiler for each hardware backend, is profoundly inefficient. It forces brilliant researchers to spend their time writing low-level hardware mapping code instead of innovating on algorithms and applications. A well-funded, community-driven effort to build a robust compiler stack around a universal Neuromorphic Intermediate Representation (NIR) would be a force multiplier for the entire field. It would create a stable abstraction layer, allowing application developers to write a model once in a high-level framework like PyTorch and target any compliant neuromorphic hardware. This single investment would do more to lower the barrier to entry, foster innovation, and accelerate progress toward democratization than any individual hardware project.

## 5 A Five-Year Roadmap for Democratized Neuromorphic AI
This roadmap translates the preceding analysis into a concrete, staged, and actionable plan designed to guide strategic investment. It prioritizes the development of foundational, shared infrastructure to cultivate a fertile and self-sustaining ecosystem for brain-inspired AI. The overarching goal is to systematically dismantle the barriers identified in the gap analysis and catalyze a transition from a fragmented research field to a mature, accessible technology platform.

**Guiding Principle**

The roadmap is structured as a portfolio of investments designed to benefit the entire community, regardless of which specific hardware architectures or software frameworks ultimately prevail. The primary focus is on creating common goods—standards, tools, and access platforms—that lower the barrier to entry for all participants and accelerate the pace of collective innovation. The objective is not to pick a single "winner" but to foster a competitive and collaborative environment where the best ideas can emerge and thrive.

### Phase 1 (Years 1-2): Foundational Infrastructure & Community Unification
**Goal**: Address the most acute software, standardization, and access gaps to create a common ground for developers and researchers, breaking the cycle of hardware leading software.

**Milestone M1.1: Establish a Standardized Benchmark Suite**

The absence of a trusted, universal benchmark is a primary inhibitor of progress. This initiative will fund a neutral, multi-stakeholder working group, modeled on the success of MLCommons (the organization behind MLPerf), to formalize and expand the promising NeuroBench framework. The effort will define a suite of 5-7 representative tasks that highlight the strengths of neuromorphic computing (e.g., low-latency keyword spotting, dynamic vision sensor-based gesture recognition, real-time sensor fusion, constrained optimization).

**Action**: Launch a grant program to fund the development of reference implementations of the benchmark suite on Loihi 2, SpiNNaker 2, BrainScaleS-2, and at least one commercial platform like Akida.

**Deliverable**: Publication of NeuroBench v1.0, complete with datasets, quality targets, and open-source code, establishing a definitive "gold standard" for performance and efficiency claims.

**Milestone M1.2: Fund the "LLVM for Neuromorphic" Initiative**

This is the highest-leverage investment in the roadmap. It will fund a major, multi-year grant program to build a production-quality, open-source compiler stack centered on the Neuromorphic Intermediate Representation (NIR). This initiative will create a common abstraction layer, decoupling high-level model development from low-level hardware implementation.

**Action**: Fund parallel development tracks for (1) robust frontends that can import models from PyTorch and JAX, and (2) well-documented backends that target the instruction sets and hardware primitives of Loihi 2, SpiNNaker 2, and the open-source reference chip from M2.1.

**Deliverable**: A production-ready NIR toolkit and compiler that allows a developer to define an SNN in a mainstream framework and compile it to run on multiple different neuromorphic targets with minimal code changes.

**Milestone M1.3: Create a Federated Hardware Access Program**

To solve the fragmented and often-gated access to hardware, this initiative will partner with key hardware providers (Intel, EBRAINS/HBP) to create a unified, grant-based portal for cloud access.

**Action**: Fund the development of a "Neuromorphic Compute Sandbox" web portal that provides a standardized application process and abstracts away the backend logistics of accessing different cloud-hosted systems. Provide grants to researchers in the form of compute credits.

**Deliverable**: A fully operational portal that has provided at least 1,000 researchers with a baseline number of free compute hours across a minimum of three distinct hardware architectures.

**Milestone M1.4: Launch an Open-Source Toolchain Grant Program**

This initiative will provide targeted funding to the core development teams of open-source software frameworks like Lava, Nengo, and PyNN to improve usability and lower the barrier to entry for new users.

**Action**: Fund specific, high-impact projects such as professional documentation writing, the creation of comprehensive video tutorial series, and the simplification of installation and dependency management.

**Deliverable**: Measurable improvements in community-voted usability metrics and a significant increase in the quality and quantity of educational materials for all major open-source frameworks.

### Phase 2 (Years 3-4): Scaling, Co-Design, and Algorithmic Breakthroughs
**Goal**: Leverage the unified infrastructure from Phase 1 to tackle more ambitious challenges in open hardware design, novel learning algorithms, and real-world applications.

**Milestone M2.1: Sponsor an Open-Source Neuromorphic Reference Chip**

To directly address the hardware accessibility gap, this initiative will fund a multi-university consortium to design a complete, open-source neuromorphic processor, from RTL to GDSII layout.

**Action**: The design should be based on proven digital asynchronous principles, inspired by projects like ODIN, but scaled for multi-core operation and designed for a mature, accessible semiconductor process node (e.g., 65nm or 40nm) to minimize fabrication costs. The design must be compatible with the NIR compiler from M1.2.

**Deliverable**: A fully verified, open-source GDSII file for a neuromorphic processor, released under a permissive license, ready for fabrication.

**Milestone M2.2: Launch a "Post-Backpropagation" Research Program**

To move beyond the limitations of current SNN training methods, this initiative will fund high-risk, high-reward research into novel on-chip learning algorithms.

**Action**: Create a challenge grant program, inspired by DARPA's strategic approach, that rewards researchers for developing and demonstrating learning rules that are (1) not based on surrogate gradients, (2) can be implemented efficiently on-chip, and (3) demonstrate effective learning from sparse, temporal data in an online fashion.

**Deliverable**: Demonstration of at least two new learning algorithms that outperform surrogate gradient methods on specific NeuroBench tasks when running on-chip.

**Milestone M2.3: Fund "Killer Application" Demonstrators**

To generate market pull and attract broader industry interest, this initiative will sponsor a series of high-profile challenge grants.

**Action**: Fund competitive projects for teams to demonstrate a >10x improvement in a critical metric (e.g., energy-delay product, battery life) over a state-of-the-art GPU/CPU solution on a commercially relevant problem. Target domains should include real-time robotics and drone control, wearable biomedical signal processing, and intelligent 5G/6G radio signal processing.

**Deliverable**: At least three public demonstrations of neuromorphic systems solving a real-world problem with an order-of-magnitude advantage, validated against the NeuroBench suite.

### Phase 3 (Year 5): Ecosystem Maturity & Mainstream Integration
**Goal**: Lower the final barriers to commercial adoption and establish the governance structures necessary for the ecosystem to become self-sustaining beyond the foundation's initial investment.

**Milestone M3.1: Fund Multi-Project Wafer (MPW) Fabrication Access**

This initiative directly addresses the fabrication barrier by providing a practical path for the community to create physical hardware.

**Action**: Partner with a semiconductor foundry or a service like MOSIS to provide subsidized "shuttle runs" for the open-source reference chip (from M2.1) and other promising academic designs. This allows multiple projects to share the cost of a single wafer run.

**Deliverable**: The successful fabrication and distribution of at least 100 physical copies of the open-source reference chip to academic and research institutions worldwide.

**Milestone M3.2: Develop MLOps Integration Tools**

To bridge the final gap to commercial deployment, this initiative will fund the development of tools to integrate neuromorphic workloads into standard MLOps platforms.

**Action**: Fund the creation of open-source tools for containerizing NIR-compatible models, deploying them via orchestrators like Kubernetes, and monitoring their performance.

**Deliverable**: A public demonstration of an end-to-end MLOps pipeline for a neuromorphic application, from training in PyTorch to deployment and monitoring on a cloud-accessible hardware platform.

**Milestone M3.3: Establish an Open Neuromorphic Foundation**

To ensure the long-term health and sustainability of the ecosystem, this final step transitions governance from the funding body to an independent, community-led organization.

**Action**: Seed the creation of a non-profit foundation, modeled on successful organizations like the Linux Foundation or RISC-V International. This foundation would become the permanent home for the NeuroBench standard, the NIR compiler project, and the federated hardware access program.

**Deliverable**: A legally incorporated, self-governing foundation with a diverse membership of academic and industry partners, capable of sustaining the core ecosystem infrastructure through a combination of membership fees, project funding, and community contributions.

This roadmap is designed as a portfolio strategy. By focusing on shared infrastructure that benefits all participants—a common benchmark, a universal compiler, and broad hardware access—it de-risks the investment against the failure of any single hardware platform or software framework. The ultimate measure of this roadmap's success will be the point at which the ecosystem becomes self-sustaining, driven by commercial and academic interest rather than philanthropic funding. The final act of democratization is to make the technology viable on its own.

## 6 Annotated Bibliography
[//]: # (This section lists references used in the document. Formatted as bullet points for readability.)

- Davies, M., et al. (2018). *Loihi: A Neuromorphic Manycore Processor with On-Chip Learning*. IEEE Micro, 38(1), 82-99.
- Frenkel, C., Lefebvre, M., Legat, J. D., & Bol, D. (2018). *A 0.086-mm² 12.7-pJ/SOP 64k-Synapse 256-Neuron Online-Learning Digital Spiking Neuromorphic Processor in 28-nm CMOS*. IEEE Transactions on Biomedical Circuits and Systems, 13(1), 145-158.
- Furber, S. B., Galluppi, F., Temple, S., & Plana, L. A. (2014). *The SpiNNaker Project*. Proceedings of the IEEE, 102(5), 652-665.
- Gonzalez, H. A., et al. (2023). *SpiNNaker2: A Large-Scale Neuromorphic System for Event-Based and Asynchronous Machine Learning*. arXiv:2312.09084.
- Höppner, S., et al. (2021). *The SpiNNaker2 Processing Element Architecture for Hybrid Digital Neuromorphic Computing*. Zenodo.
- Mayr, C., Höppner, S., & Furber, S. (2019). *SpiNNaker 2: A 10 Million Core Processor System for Brain Simulation and Machine Learning*. arXiv:1911.02385.
- Modha, D. S. (2024). *IBM NorthPole: An Architecture for Neural Network Inference with a 12nm Chip*. ISSCC 2024.
- Schemmel, J., et al. (2022). *The BrainScaleS-2 accelerated neuromorphic system with hybrid plasticity*. arXiv:2201.11063.
- Spilger, P., et al. (2023). *hxtorch.snn: Machine-learning-inspired Spiking Neural Network Modeling on BrainScaleS-2*. NICE 2023.
- Starr, M. (2014). *Brain-inspired circuit board 9000 times faster than an average PC*. CNET.
- Wikichip. (2024). *Intel Loihi 2*. Retrieved from https://en.wikichip.org/wiki/intel/loihi_2
- Wikichip. (2011). *University of Manchester SpiNNaker*. Retrieved from https://en.wikichip.org/wiki/university_of_manchester/spinnaker
- Wikipedia. (2024). *Neurogrid*. Retrieved from https://en.wikipedia.org/wiki/Neurogrid

### Software Frameworks and Documentation
- Davison, A. P., et al. (2009). *PyNN: a common interface for neuronal network simulators*. Frontiers in Neuroinformatics, 2, 11.
- GitHub. (n.d.). *lava-nc/lava*. Retrieved from https://github.com/lava-nc/lava
- GitHub. (n.d.). *nengo/nengo*. Retrieved from https://github.com/nengo/nengo
- GitHub. (n.d.). *NeuralEnsemble/pynn*. Retrieved from https://github.com/NeuralEnsemble/PyNN
- Lava-nc.org. (n.d.). *Lava Software Framework*. Retrieved from https://lava-nc.org/
- Nengo.ai. (n.d.). *Nengo Documentation*. Retrieved from https://www.nengo.ai/documentation/
- NeuralEnsemble. (n.d.). *PyNN*. Retrieved from https://neuralensemble.org/PyNN/

### Benchmarking and Performance Analysis
- Bellec, G., et al. (2018). *Deep Rewiring: Training deep spiking networks with sparse connectivity*. Frontiers in Neuroscience, 12, 840.
- Brehove, M., et al. (2025). *Sigma-Delta Neural Network Conversion on Loihi 2*. arXiv:2505.06417.
- Intel Newsroom. (2024). *Intel Builds World's Largest Neuromorphic System to Enable More Sustainable AI*.
- Knight, J. C., & Nowotny, T. (2018). *GPUs Outperform Current HPC and Neuromorphic Solutions in Terms of Speed and Energy When Simulating a Highly-Connected Cortical Model*. Frontiers in Neuroscience, 12, 941.
- Plank, P., et al. (2022). *Energy Efficiency of Neuromorphic Hardware Practically Proven*. Human Brain Project News.
- Reddi, V. J., et al. (2021). *MLPerf Tiny: An Open Benchmark Suite for TinyML Systems*. NeurIPS 2021 Datasets and Benchmarks Track.
- Spilger, P., et al. (2024). *A review on neuromorphic computing circuits*. Journal of Integrated VLSI, Embedded and Computing Technologies, 1(1), 26-30.
- Voelker, A., et al. (2024). *NeuroBench: A Benchmark Framework for Neuromorphic Computing Algorithms and Systems*. Nature Communications, 16.
- Zahra, S., et al. (2024). *Accelerating Sensor Fusion in Neuromorphic Computing: A Case Study on Loihi-2*. ResearchGate.

### Techno-Economic Data and TCO Models
- ASA Computers. (n.d.). *NVIDIA H100 80GB GPU*. Retrieved from https://www.asacomputers.com/nvidia-h100-80gb-nvh100tcgpu-gpu-card.html
- BrainChip Inc. (n.d.). *Akida™ PCIe Board*. Retrieved from https://shop.brainchipinc.com/products/akida%E2%84%A2-development-kit-pcie-board
- CSET. (2021). *Analysts believe that a single TSMC 5nm wafer costs $17,000*.
- Cyfuture Cloud. (n.d.). *GPU Cluster Pricing: How Much Does Building One Really Cost?* Retrieved from https://cyfuture.cloud/kb/gpu/gpu-cluster-pricing-how-much-does-building-one-really-cost
- Evenden, I. (2022). *BrainChip's $499 Akida AI Board Goes Solo*. Tom's Hardware.
- Halfacree, G. (2021). *BrainChip Launches Raspberry Pi, Intel-Based Development Kits for Its Akida Neuromorphic Processor*. Hackster.io.
- Hyperion Research. (2018). *The Economics of HPC*. AWS White Paper.
- Massed Compute. (n.d.). *How do I calculate the total cost of ownership (TCO) for a high-performance computing cluster?* Retrieved from https://massedcompute.com/faq-answers/
- Nlyte. (n.d.). *Data Center Rack Power Costs: A Condensed Analysis*. Retrieved from https://www.nlyte.com/blog/data-center-rack-power-costs-a-condensed-analysis/
- PatentPC. (n.d.). *Chip Manufacturing Costs in 2025-2030*. Retrieved from https://patentpc.com/blog/chip-manufacturing-costs-in-2025-2030-how-much-does-it-cost-to-make-a-3nm-chip

### Strategic Roadmaps and Gap Analyses
- Christensen, D. V., et al. (2021). *2021 Roadmap on Neuromorphic Computing and Engineering*. arXiv:2105.05956.
- DARPA. (n.d.). *Fast Event-based Neuromorphic Camera and Electronics (FENCE)*. Retrieved from https://www.darpa.mil/research/programs/fast-event-based-neuromorphic-camera-and-electronics
- DARPA. (n.d.). *µBRAIN*. Retrieved from https://www.darpa.mil/research/programs/microbrain
- Hasler, J. (2023). *Neuromorphic computing roadmap envisions analog path to simulating human brain*. Georgia Tech News.
- Mindplex Magazine. (2025). *A neuromorphic computing roadmap*.
- Neurotechai.eu. (n.d.). *Roadmap*. Retrieved from https://neurotechai.eu/strategy/roadmap/
- Schuman, C. D., et al. (2020). *A Roadmap for Reaching the Potential of Brain-Derived Computing*. Advanced Intelligent Systems, 2(12), 2000191.

### Community and Ecosystem Resources
- EBRAINS. (n.d.). *Getting access to the NMC systems BrainScaleS and SpiNNaker*. Retrieved from https://wiki.ebrains.eu/bin/view/Collabs/neuromorphic/Getting%20access/
- Intel Labs. (n.d.). *Intel Neuromorphic Research Community*. Retrieved from https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html
- Intel NCL Confluence. (n.d.). *Access Intel Loihi Hardware*. Retrieved from https://intel-ncl.atlassian.net/wiki/spaces/INRC/pages/1810432001/Access+Intel+Loihi+Hardware
- Nengo Forum. (n.d.). *Categories*. Retrieved from https://forum.nengo.ai/categories
- Open Neuromorphic. (n.d.). *Advancing Neuromorphic Computing, Together*. Retrieved from https://open-neuromorphic.org/

### Sources used in the report

- open-neuromorphic.org - Open Neuromorphic is a global community fostering education, research, and open-source collaboration in brain-inspired AI and hardware.
- neurotechai.eu - Roadmap - NEUROTECH AI Project
- darpa.mil - FENCE: Fast Event-based Neuromorphic Camera and Electronics - DARPA
- arxiv.org - NeuroBench: A Framework for Benchmarking Neuromorphic Computing Algorithms and Systems - arXiv
- researchgate.net - (PDF) The neurobench framework for benchmarking neuromorphic computing algorithms and systems - ResearchGate
- pmc.ncbi.nlm.nih.gov - Benchmarking neuromorphic systems with Nengo - PMC - PubMed Central
- chfrenkel.github.io - Charlotte Frenkel's Personal Webpage
- cnet.com - Brain-inspired circuit board 9000 times faster than an average PC - CNET
- lava-nc.org - Lava Architecture — Lava documentation - Lava Software Framework
- silicon-saxony.de - Spinncloud: Introducing SpiNNaker2 - The future of hybrid, brain-inspired high-performance computing - Silicon Saxony
- en.wikipedia.org - Neurogrid - Wikipedia
- open-neuromorphic.org - A Look at Odin by Charlotte Frenkel - Neuromorphic Chip - Open ...
- open-neuromorphic.org - A Look at Akida - BrainChip - Neuromorphic Chip - Open ...
- en.wikichip.org - Loihi 2 - Intel - WikiChip
- westernsydney.edu.au - ICNS to build brain-scale supercomputer - Western Sydney University
- magazine.mindplex.ai - A neuromorphic computing roadmap - Mindplex
- darpa.mil - SyNAPSE: Systems of Neuromorphic Adaptive Plastic Scalable Electronics - DARPA
- nlyte.com - www.nlyte.com
- datasets-benchmarks-proceedings.neurips.cc - MLPerf Tiny Benchmark
- asacomputers.com - NVIDIA H100 80GB GPU - ASA Computers
- patentpc.com - Chip Manufacturing Costs in 2025-2030: How Much Does It Cost to Make a 3nm Chip?
- cset.georgetown.edu - Analysts believe that a single TSMC 5nm wafer costs $17,000 | Center for Security and Emerging Technology - CSET
- linuxgizmos.com - Neuromorphic edge AI chip debuts on Raspberry Pi and Comet Lake dev kits
- hackster.io - BrainChip Launches Raspberry Pi, Intel-Based Development Kits for Its Akida Neuromorphic Processor - Hackster.io
- electronicvisions.github.io - BrainScaleS-2 single neuron experiments - GitHub Pages
- pmc.ncbi.nlm.nih.gov - Neuromodulated Synaptic Plasticity on the SpiNNaker Neuromorphic System - PMC
- brainchip.com - What Is the Akida Event Domain Neural Processor? - BrainChip
- arxiv.org - SpiNNaker 2: A 10 Million Core Processor System for Brain Simulation and Machine Learning - arXiv
- spinncloud.com - SpiNNcloud
- newsroom.arm.com - New Brain-inspired Supercomputers for the Next Generation of AI - Arm Newsroom
- github.com - nengo/nengo-dl: Deep learning integration for Nengo - GitHub
- cyfuture.cloud - GPU Cluster Pricing: How Much Does Building One Really Cost? - Cyfuture Cloud
- darpa.mil - µBRAIN - DARPA
- indico.cern.ch - custom ASICs for accelerated analog neuromorphic ... - CERN Indico
- research.ibm.com - IBM NorthPole: An Architecture for Neural Network Inference with a ...
- ece.gatech.edu - Neuromorphic Computing "Roadmap" Envisions Analog Path to ...
- researchgate.net - Accelerating Sensor Fusion in Neuromorphic Computing: A Case Study on Loihi-2
- open-neuromorphic.org - A Look at Loihi 2 - Intel - Open Neuromorphic
- nengo.ai - Nengo Documentation
- github.com - Issues · lava-nc/lava - GitHub
- github.com - Issues · lava-nc/lava-docs - GitHub
- shop.brainchipinc.com - Akida™ PCIe Board - BrainChip Inc
- tomshardware.com - BrainChip's $499 Akida AI Board Goes Solo - Tom's Hardware
- brainchip.com - BrainChip Achieves Full Commercialization of its AKD1000 AIoT Chip with availability of Mini PCIe Boards in high volume
- arxiv.org - [2201.11063] The BrainScaleS-2 accelerated neuromorphic system with hybrid plasticity
- en.wikichip.org - SpiNNaker - APT - The University of Manchester - WikiChip
- spacedaily.com - DeepSouth: Western Sydney University Unveils Neuromorphic Supercomputer
- arxiv.org - Sigma-Delta Neural Network Conversion on Loihi 2 - arXiv
- researchgate.net - Sigma-Delta Neural Network Conversion on Loihi 2 | Request PDF - ResearchGate
- arxiv.org - Hardware-Aware Fine-Tuning of Spiking Q-Networks on the SpiNNaker2 Neuromorphic Platform - arXiv
- researchgate.net - 2021 Roadmap on Neuromorphic Computing and Engineering - ResearchGate
- mdm.imm.cnr.it - 2021 Roadmap on Neuromorphic Computing and Engineering | Agrate UNIT
- osti.gov - A Roadmap for Reaching the Potential of Brain-Derived Computing (Journal Article) - OSTI
- pubmed.ncbi.nlm.nih.gov - GPUs Outperform Current HPC and Neuromorphic Solutions in Terms of Speed and Energy When Simulating a Highly-Connected Cortical Model - PubMed
- frontiersin.org - GPUs Outperform Current HPC and Neuromorphic Solutions in Terms of Speed and Energy When Simulating a Highly-Connected Cortical Model - Frontiers
- forum.nengo.ai - Categories - Nengo forum
- humanbrainproject.eu - Neuromorphic Computing - Human Brain Project
- conscium.com - Major Neuromorphic Computing projects - Conscium
- eecs.utk.edu - Intel Announces Neuromorphic Computing Research Collaborators - UTK-EECS
- eurocc.fccn.pt - DeepSouth: the World's First Neuromorphic Supercomputer - EuroCC Portugal
- d1.awsstatic.com - What a TCO analysis won't tell you - awsstatic.com
- pmc.ncbi.nlm.nih.gov - Synapse-Centric Mapping of Cortical Models to the SpiNNaker Neuromorphic Architecture
- newsroom.intel.com - Intel Builds World's Largest Neuromorphic System to Enable More Sustainable AI
- arxiv.org - Sigma-Delta Neural Network Conversion on Loihi 2 - arXiv
- youtube.com - IBM NorthPole - Neural Inference at the Frontier of Energy, Space, and Time - YouTube
- researchgate.net - A review on neuromorphic computing circuits - ResearchGate
- massedcompute.com - How do I calculate the total cost of ownership (TCO) for a high-performance computing cluster?
- open-neuromorphic.org - NorthPole, IBM's latest Neuromorphic AI Hardware
- hpe.com - What is an HPC Cluster? | Glossary | HPE
- supermicro.com - What Is High Performance Computing? | Supermicro
- tu-dresden.de - SpiNNaker2: TU Dresden, University of Manchester and Globalfoundries announce a Breakthrough in AI Cloud Systems
- intel.com - Neuromorphic Computing and Engineering with AI | Intel®
- electronicvisions.github.io - The BrainScaleS-2 system - GitHub Pages
- academic.oup.com - Darwin3: a large-scale neuromorphic chip with a novel ISA and on-chip learning - Oxford Academic
- researchgate.net - SpiNNaker 2: A 10 Million Core Processor System for Brain Simulation and Machine Learning: Keynote Presentation - ResearchGate
- arxiv.org - Language Modeling on a SpiNNaker 2 Neuromorphic Chip - arXiv
- deepsouth.org.au - Deep South: Home
- executivebiz.com - IBM Secures Air Force Contract for NorthPole Chip Software & Hardware - ExecutiveBiz
- humanbrainproject.eu - Energy Efficiency of Neuromorphic Hardware Practically Proven - Human Brain Project
- westernsydney.edu.au - World first supercomputer capable of brain-scale simulation being built at Western Sydney University
- redwood.berkeley.edu - Loihi: A Neuromorphic Manycore Processor with On-Chip Learning
- neuralensemble.org - PyNN - NeuralEnsemble
- ebrains.eu - PyNN - Tools - EBRAINS
- lava-nc.org - Lava Software Framework — Lava documentation
- wiki.ebrains.eu - Getting access - HBP Wiki - EBRAINS
- intel-ncl.atlassian.net - About the INRC - Confluence
- open-neuromorphic.org - A Look at SpiNNaker 2 - University of Dresden - Neuromorphic Chip
- humanbrainproject.eu - Hardware - BrainScaleS - Human Brain Project
- open-neuromorphic.org - A Look at BrainScaleS-2 — Heidelberg University - Neuromorphic Chip
- frontiersin.org - Memory-Efficient Deep Learning on a SpiNNaker 2 Prototype - Frontiers
- github.com - NeuralEnsemble/PyNN: A Python package for simulator ... - GitHub
- github.com - nengo/nengo: A Python library for creating and simulating ... - GitHub
- github.com - lava-nc/lava: A Software Framework for Neuromorphic ... - GitHub
- arxiv.org - Sigma-Delta Neural Network Conversion on Loihi 2 - arXiv

### Sources read but not used in the report

- arxiv.org - Neuromorphic Computing for Embodied Intelligence in Autonomous Systems: Current Trends, Challenges, and Future Directions - arXiv
- ncg.ucsc.edu - Neuromorphic Computing Group | Brain-Inspired Systems at UC Santa Cruz
- cnx-software.com - Intel Loihi 2 high-efficiency neuromorphic chip works with the Lava open-source framework
- highergov.com - Contract HR001121C0133 BAE Systems Information & Electronic Systems Integration - HigherGov
- pubmed.ncbi.nlm.nih.gov - Neuromorphic atomic switch networks - PubMed
- open-neuromorphic.org - Nengo - Open Neuromorphic
- open-neuromorphic.org - Lava - Open Neuromorphic
- brainchip.com - Akida Enablement Platforms - BrainChip
- arxiv.org - Neuromorphic Principles for Efficient Large Language Models on Intel Loihi 2 - arXiv
- ecejournals.in - Integration of Neuromorphic Computing in Embedded Systems: Opportunities and Challenges
- nmjpec.org - New Mexico Judicial Performance Evaluation Commission
- open-neuromorphic.org - A Look at BrainScaleS-2 — Heidelberg University - Neuromorphic Chip
- theregister.com - Google unveils TPU v5p pods to accelerate AI training - The Register
- news.ycombinator.com - For example, training and serving Llama 3.1 on Google TPUs is about 30% cheape... | Hacker News
- semianalysis.com - Intel 18A Details & Cost, Future of DRAM 4F2 vs 3D, Backside Power Adoption (or Not), China's FlipFET, Digital Twins from Atoms to Fabs, and More - SemiAnalysis
- cordis.europa.eu - SpiNNaker on the Edge | SPINNODE | Projekt | Fact Sheet | HORIZON - CORDIS
- servethehome.com - Intel Loihi 2 Neuromorphic Compute Tile on Intel 4 - ServeTheHome
- sparkfun.com - Machine Learning and AI - Development Boards - SparkFun Electronics
- electronicvisions.github.io - Structured Neurons — BrainScaleS-2 Documentation 0.0.1 documentation - GitHub Pages
- pmc.ncbi.nlm.nih.gov - Brian2Loihi: An emulator for the neuromorphic chip Loihi using the spiking neural network simulator Brian
- frontiersin.org - Brian2Loihi: An emulator for the neuromorphic chip Loihi using the spiking neural network simulator Brian - Frontiers
- mdpi.com - A Low-Cost Hardware-Friendly Spiking Neural Network Based on Binary MRAM Synapses, Accelerated Using In-Memory Computing - MDPI
- brainchip.com - What Is the Akida Event Domain Neural Processor? - BrainChip
- coral.ai - Dev Board | Coral
- spinnaker2.gitlab.io - SpiNNaker2 Developer Portal
- humanbrainproject.eu - SpiNNaker - Human Brain Project
- github.com - nengo/nengo-interfaces: Simplifies external input and output communication - GitHub
- github.com - GeorgeChatzikonstantis/dockerHHext - PyNN - GitHub
- github.com - pynn · GitHub Topics
- eetimes.com - SpiNNaker-Based Supercomputer Launches in Dresden - EE Times
- researchgate.net - 2. The SpiNNaker Chip | Request PDF - ResearchGate
- github.com - nengo/nengo-gui: Nengo interactive visualizer - GitHub
- github.com - genn-team/pynn_genn: PyNN interface to GeNN - GitHub
- spinnakermanchester.github.io - SpiNNaker datasheet version 2.02 6 January 2011
- github.com - lava-nc/lava-optimization: Neuromorphic mathematical optimization with Lava - GitHub
- github.com - Pull requests · lava-nc/lava-optimization - GitHub
- projectpro.io - How Much Does it Cost to Build an AI System? - ProjectPro
- github.com - Releases · lava-nc/lava-dl - GitHub
- vast.ai - Rent GPUs | Vast.ai
- lambda.ai - AI Cloud Pricing | Lambda
- news.ycombinator.com - Building an AI server on a budget | Hacker News
- fujitsu.com - Supercomputer Fugaku : Fujitsu Global
- cmap.polytechnique.fr - Optimising the Overall Power Usage on the SpiNNaker Neuromimetic Platform - CMAP
- dataengineeracademy.com - Neuromorphic vs. Conventional AI: A Data Engineering Tool Review
- dev.to - Neuromorphic Chips in 2025: A Developer's Guide to Brain-Inspired AI Hardware
- exoswan.com - Is Neuromorphic Computing the Future of AI? - Exoswan Insights
- futuremarketsinc.com - The Global Neuromorphic Computing & Sensing Market 2025-2035 - Future Markets, Inc
- researchgate.net - (PDF) Benchmarking Neuromorphic Hardware and Its Energy Expenditure - ResearchGate
- searchit.libraries.wsu.edu - Performance Comparison of the Digital Neuromorphic Hardware SpiNNaker and the Neural Network Simulation Software NEST for a Full-Scale Cortical Microcircuit Model - Washington State University
- up-shop.org - AI Development Kit - AI Solution - UP Shop
- kip.uni-heidelberg.de - Memory Consolidation and Synaptic Plasticity on the Neuromorphic BrainScaleS-2 System
- researchgate.net - (PDF) The SpiNNaker project - ResearchGate
- frontiersin.org - Neuromodulated Synaptic Plasticity on the SpiNNaker Neuromorphic System - Frontiers
- frontiersin.org - Closing the loop: High-speed robotics with accelerated neuromorphic hardware - Frontiers
- eetimes.com - Intel Unveils Second-Generation Neuromorphic Chip - EE Times
- researchgate.net - (PDF) SpiNNaker: A 1-W 18-Core System-on-Chip for Massively-Parallel Neural Network Simulation - ResearchGate
- anandtech.com - Intel Rolls Out New Loihi 2 Neuromorphic Chip: Built on Early Intel 4 Process - AnandTech
- arxiv.org - An End-to-End DNN Inference Framework for the SpiNNaker2 Neuromorphic MPSoC - arXiv
- researchgate.net - SpiNNaker2: A Large-Scale Neuromorphic System for Event-Based and Asynchronous Machine Learning | Request PDF - ResearchGate
- re.public.polimi.it - Roadmap to neuromorphic computing with emerging technologies
- primo.ai - Processing Units - CPU, GPU, APU, TPU, VPU, FPGA, QPU - PRIMO.ai
- neuralensemble.org - Contributing to PyNN — PyNN 0.10.1 documentation - NeuralEnsemble
- github.com - PyNN for BrainScaleS-2 - GitHub
- forum.nengo.ai - General Discussion - Nengo forum
- nengo.ai - Nengo
- gazettabyte.com - Home - Modelling the Human Brain with specialised CPUs - Gazettabyte
- ebrains.eu - NEST - Tools - EBRAINS
- ec.europa.eu - Neuromorphic Computing in the HBP
- lavag.org - LAVA: Forums
- github.com - reds-lab/LAVA: This is an official repository for "LAVA: Data Valuation without Pre-Specified Learning Algorithms" (ICLR2023). - GitHub
- intc.com - Intel Advances Neuromorphic with Loihi 2, New Lava Software Framework and New Partners
- research.ibm.com - Rapidly unlocking geospatial insights with IBM AI chips
- pmc.ncbi.nlm.nih.gov - A 22-pJ/spike 73-Mspikes/s 130k-compartment neural array transceiver with conductance-based synaptic and membrane dynamics
- researchgate.net - NEXUS: A 28nm 3.3pJ/SOP 16-Core Spiking Neural Network with a Diamond Topology for Real-Time Data Processing | Request PDF - ResearchGate
- reddit.com - Australians develop a supercomputer capable of simulating networks at the scale of the human brain. Human brain like supercomputer with 228 trillion links is coming in 2024 : r/singularity - Reddit
- siliconangle.com - IBM debuts power-efficient NorthPole machine learning processor - SiliconANGLE
- exxactcorp.com - The Costs of Deploying AI: Energy, Cooling, & Management | Exxact Blog
- nitrc.org - PyNN: Tool/Resource Info - NITRC
- validation.linaro.org - LAVA
- research.manchester.ac.uk - Impact case study (REF3) Page 1 Institution: University of Manchester Unit of Assessment: 11 (Computer Science and Informatics)
- nowpublishers.com - SpiNNaker: A Spiking Neural Network Architecture - Now Publishers
- electronicvisions.github.io - Welcome to the BrainScaleS-2 Tutorial - GitHub Pages
- brainscales.kip.uni-heidelberg.de - BrainScales BrainScaleS today (2020-2023)
- techradar.com - A system inspired by the human brain has quietly been activated at a US nuclear lab, and it has no operating system or storage - TechRadar
- pure.manchester.ac.uk - High performance computing on SpiNNaker neuromorphic platform: A case study for energy efficient image processing - The University of Manchester
- ebrains.eu - sPyNNaker - Tools - EBRAINS
- frontiersin.org - Brian2Loihi: An emulator for the neuromorphic chip Loihi using the spiking neural network simulator Brian - Frontiers
- pmc.ncbi.nlm.nih.gov - The BrainScaleS-2 Accelerated Neuromorphic System With Hybrid Plasticity - PMC
- researchgate.net - Demonstrating Analog Inference on the BrainScaleS-2 Mobile System - ResearchGate
- arxiv.org - SpiNNaker2: A Large-Scale Neuromorphic System for Event-Based ...
- youtube.com - Supercomputer That Mimics Your Brain with 228 TRILLION links Per Second | DeepSouth (2024) - YouTube
- arxiv.org - A Review of Memory Wall for Neuromorphic Computing - arXiv
- incf.org - PyNN | INCF
- directory.fsf.org - PyNN - Free Software Directory
- open-neuromorphic.org - A Look at NorthPole - IBM - Neuromorphic Chip
- researchgate.net - A 5.28-mm² 4.5-pJ/SOP Energy-Efficient Spiking Neural Network Hardware With Reconfigurable High Processing Speed Neuron Core and Congestion-Aware Router | Request PDF - ResearchGate
- flagship.kip.uni-heidelberg.de - EBRAINS tutorials and users day - 12 March 2025 in Heidelberg (Germany)
- nengo.ai - Nengo license — Nengo core 2.8.0 docs
- lava.ai - General Terms | Lava.ai
- lavanet.xyz - Terms of Service - Lava Network
- sawtoothsoftware.com - Academic Plans and Pricing | Sawtooth Software
- intel.com.br - Neuromorphic Computing - Next Generation of AI - Intel
- lavalink.com - Terms Of Use – LAVA Computer MFG Inc.
- trdf.co.il - Intel Neuromorphic Research Community
- youtube.com - SpiNNaker2: Energy-efficient real-time neuromorphic compute system in 22FDX technology - Dr. Höppner - YouTube
- researchgate.net - Power analysis of large-scale, real-time neural networks on SpiNNaker - ResearchGate
- ibm.com - IBM watsonx.ai | Pricing
- arxiv.org - Energy Aware Development of Neuromorphic Implantables: From Metrics to Action - arXiv
- themoonlight.io - [Literature Review] Energy Aware Development of Neuromorphic Implantables: From Metrics to Action
- techzi.co - Supercomputer to Rival Human Brainpower Set for 2024 Launch - Techzi
- research.ibm.com - IBM's NorthPole achieves new speed and efficiency milestones
- sciencefocus.com - Ageless brain: How this new supercomputer could help keep your mind young
- azure.microsoft.com - Total Cost of Ownership (TCO) Calculator - Microsoft Azure
- pmc.ncbi.nlm.nih.gov - Mapping and Validating a Point Neuron Model on Intel's Neuromorphic Hardware Loihi - PMC - PubMed Central
- pmc.ncbi.nlm.nih.gov - A comprehensive review of advanced trends: from artificial synapses to neuromorphic systems with consideration of non-ideal effects - PubMed Central
- docs.python.org - History and License — Python 3.13.5 documentation
- nengo.ai - Nengo license — Nengo 3.0.0 docs
- arvoelke.github.io - License — nengolib 0.5.1 documentation - GitHub Pages
- nengo.ai - Nengo license — Nengo 4.0.1.dev0 docs
- lava-nc.org - Developer Guide — Lava documentation
- flagship.kip.uni-heidelberg.de - EBRAINS tutorials and users day - Agenda - Human-Brain Project
- ebrains.eu - BrainScaleS - Tools - EBRAINS
- ebrains.eu - EBRAINS Neuromorphic platform BrainScaleS-2 adds new interface for high-speed robotics
- nextplatform.com - Sandia Deploys SpiNNaker2 Neuromorphic System - The Next Platform
- docs.hpc.gwdg.de - SpiNNaker :: Documentation for HPC - GWDG
- researchgate.net - Overview of the BrainScaleS-2 System architecture. (A) Bonded chip on... - ResearchGate
- pmc.ncbi.nlm.nih.gov - Surrogate gradients for analog neuromorphic computing - PMC - PubMed Central
- arxiv.org - SpiNNaker2: A Large-Scale Neuromorphic System for Event-Based ...
- frontiersin.org - Performance Comparison of the Digital Neuromorphic Hardware SpiNNaker and the Neural Network Simulation Software NEST for a Full-Scale Cortical Microcircuit Model - Frontiers
- hpc.ut.ee - Calculate Your Cost - UT HPC
- scalecomputing.com - Total Cost of Ownership (TCO) Calculator | Scale Computing
- arxiv.org - SpiNNaker2: A Large-Scale Neuromorphic System for Event-Based ...

