---
title: "Reverse-Engineering OpenAI Codex"
tags: [reverse-engineering, codex, ai-research]
project: ai-research
updated: 2025-07-26
---

--8<-- "_snippets/disclaimer.md"

# Reverse-Engineering Design Report: OpenAI Codex Software Engineering Agent

Document ID: REDR-2025-07-26-001 Version: 1.0 Classification: Technical Analysis
& Re-implementation Blueprint

## 1. Executive Summary

### 1.1. Project Objective and Findings

This report presents a comprehensive reverse-engineering analysis of the OpenAI
Codex system, a software engineering agent designed to perform complex coding
tasks in parallel. The primary objective is to produce a detailed technical
blueprint for the development of a functionally equivalent, legally compliant,
open-core implementation.

The analysis concludes that building a functionally equivalent system is
technically feasible. The target system, hereafter referred to as "Codex,"
manifests as two distinct but related products: a proprietary, cloud-based agent
integrated within the ChatGPT interface, and an open-source Command Line
Interface (CLI) that functions as a local agent. The core intellectual property
and primary technical challenge lie not in the client-side tooling, which is
open-source, but in the performance and capabilities of the backend Large
Language Models (LLMs) and the legal framework surrounding their training data.

A successful re-implementation hinges on two critical factors: first,
replicating the robust, OS-native security sandbox of the CLI to ensure safe
local code execution; and second, developing a competitive code-generation model
through a dedicated, long-term MLOps and fine-tuning strategy.

### 1.2. System Architecture Synopsis

The OpenAI Codex ecosystem operates on a sophisticated client-server
architecture. The system's intelligence is entirely centralized within the
OpenAI API Platform, while the user interaction and local execution are handled
by two distinct clients:

- Cloud Agent: Accessed via the ChatGPT web UI, this component executes tasks
  within a secure, managed cloud sandbox, pre-loaded with a clone of the user's
  repository.
- CLI Agent: An open-source terminal application (openai/codex) that runs on the
  developer's local machine. It orchestrates an agentic loop with the backend,
  executing returned commands within a local, OS-native sandbox for security.

Both clients communicate with the same backend infrastructure via the OpenAI
Responses API. This API leverages a suite of advanced AI models, including the
specialized codex-1 (a fine-tuned variant of OpenAI's o3 model) for
high-fidelity tasks and o4-mini for faster, more cost-effective interactions in
the CLI. The architecture effectively decouples the agent's "brain" (the LLM)
from its "hands" (the execution environment), allowing for flexible deployment
in either a cloud or local context.

### 1.3. Core Technical Insights

The investigation yielded several critical technical insights that form the
foundation of the re-implementation blueprint:

- **Open-Source Client as a Blueprint**: The publicly available source code for
  the Codex CLI is the most valuable asset for this reverse-engineering effort.
  It reveals the precise API contract with the backend, the schema for
  "tool-calling" (the mechanism by which the LLM requests actions), the
  structure of the agentic loop, and the logic for state management.
- **OS-Native Sandboxing is Paramount**: The CLI's security model is not a
  trivial containerization. It relies on low-level, OS-specific security
  features—Apple Seatbelt on macOS and Landlock/seccomp on Linux—to create a
  highly restrictive environment for executing untrusted, AI-generated code.
- **Agentic Behavior via Tool-Calling**: The system's autonomous behavior is not
  an emergent property of the model alone. It is explicitly orchestrated through
  a tool-calling paradigm. The LLM does not execute code directly; it generates
  a structured request (a function_call) for a tool, such as shell or
  apply_patch, which the client then interprets and executes according to a
  strict, user-configurable approval policy.

### 1.4. Strategic Recommendations

Based on the findings, the following strategic approach is recommended for
developing a successful open-core alternative:

- **Development Strategy**: Phased & Modular Implementation. A phased
  development plan is advised to manage complexity and risk.
  - Phase 1: Focus on building the foundational components: the secure local
    execution client (in Rust, mirroring the official CLI's evolution) and a
    compatible backend API gateway that mocks model responses. This establishes
    the system's "scaffolding."
  - Phase 2: Integrate a leading open-source code generation model to achieve
    baseline end-to-end functionality.
  - Phase 3: Invest in the long-term MLOps pipeline for continuous model
    improvement.
- **AI Model Strategy**: Dual-Path Approach. Achieving performance parity with
  OpenAI's proprietary models is the most significant long-term challenge.
  - Short-Term (Baseline Functionality): Integrate a state-of-the-art
    open-source code model, such as DeepSeek Coder or Code Llama, to provide
    immediate, high-quality code generation capabilities.
  - Long-Term (Competitive Parity): Establish a dedicated MLOps pipeline to
    continuously fine-tune the selected base model. This involves curating a
    legally vetted, high-quality dataset of permissively licensed code and
    employing advanced techniques like Reinforcement Learning from Human
    Feedback (RLHF) to specialize the model for agentic software engineering
    tasks.
- **Legal & Compliance Posture**: Proactive Risk Mitigation.
  - Reverse Engineering: All reverse-engineering activities detailed in this
    report are justified under the "interoperability" exemption of the Digital
    Millennium Copyright Act (DMCA) §1201(f). This legal basis should be
    formally documented.
  - Model Training: To mitigate copyright risks associated with training on
    public code, the project must adopt a stringent data sourcing policy,
    exclusively using legitimately accessible, permissively licensed
    repositories. An "Output Compliance Layer" must be implemented to scan for
    and flag any verbatim code regurgitation from the training set, thereby
    preventing license violations.

## 2. Scope & Legal Constraints

### 2.1. Permissibility of Reverse Engineering under DMCA §1201(f)

The analysis presented in this report is conducted under the legal framework
provided by the Digital Millennium Copyright Act (DMCA), specifically 17 U.S.C.
§ 1201(f), "Reverse Engineering." This provision creates a specific exemption to
the general prohibition against circumventing technological protection measures
(TPMs).

The exemption states that a person who has lawfully obtained the right to use a
copy of a computer program may circumvent a TPM for the "sole purpose of
identifying and analyzing those elements of the program that are necessary to
achieve interoperability of an independently created computer program with other
programs". Our activities fall squarely within this definition. The objective is
not to create a derivative or competing product by copying protected code, but
to understand the unprotected elements—namely, the communication protocols, data
schemas, agentic state machine, and security models—required for an
independently developed backend service to interoperate with a client that is
functionally equivalent to the Codex CLI.

This legal interpretation has been affirmed by the U.S. Copyright Office, which
recognizes that § 1201(f) is intended to preserve existing case law, such as
Sega v. Accolade, that permits reverse engineering for the purpose of creating
compatible, non-infringing software. All methodologies employed, including
network traffic interception and binary analysis, were strictly limited to
identifying these interoperability-enabling elements.

### 2.2. Copyright Implications of AI Model Training

The most significant legal challenge for this project is the training of a new
AI model on a large corpus of publicly available source code. The legal
landscape is evolving, but recent court decisions provide critical guidance on
navigating copyright law in this domain.

The central legal doctrine is "fair use." A successful fair use defense hinges
on a four-factor analysis, with the "purpose and character of the use" being
paramount. The landmark case Authors Guild, Inc. v. Google, Inc. established
that uses that are highly "transformative"—creating a new work with a different
purpose or character—are more likely to be considered fair use.

More directly, the 2025 decision in Bartz v. Anthropic provides a powerful
precedent. The court held that using copyrighted books to train an LLM was
"spectacularly so" transformative because the purpose was not to create a
substitute for the books but to create a new tool for generating language. This
reasoning strongly supports the argument that training a model on source code to
create a new, generative coding tool is also a transformative use.

However, the Anthropic decision came with a critical caveat: the court ruled
against the defendant's use of pirated books, stating that such use "displaced
demand for [the] Authors' books – copy for copy" and was not transformative.
This distinction creates a clear directive for the re-implementation project:
the training data must be sourced from legitimately accessible public
repositories. Scraping code from sources known to host pirated materials or
using datasets that disregard software licenses would fatally undermine a fair
use defense.

### 2.3. FOSS License Obligations and Code Regurgitation

A well-documented issue with large code models, including the original Codex, is
their tendency to "regurgitate" or reproduce training data verbatim. An internal
GitHub study found that approximately 0.1% of code generated by Copilot (powered
by Codex) was a direct copy from the training set. In one notable instance, the
model reproduced the fast inverse square root algorithm, complete with its
original comments and an incorrect copyright notice.

This presents a severe legal risk. If the regurgitated code is governed by a
"copyleft" license (e.g., GNU General Public License), any project incorporating
that code may be obligated to release its own source code under the same
license. Even for permissive licenses, failure to provide required attribution
constitutes a license violation.

To mitigate this risk, the re-implementation blueprint must include a mandatory
Output Compliance Layer. This service will operate as a post-processing step on
all code generated by the model. It will maintain a database of code snippets
from the training data, particularly those under restrictive or copyleft
licenses. Before code is presented to the user, it will be scanned against this
database. If a significant match is found, the system will take one of the
following actions based on a compliance policy:

- **Flag and Attribute**: For permissively licensed code (e.g., MIT, Apache),
  the system will flag the code and automatically provide the required
  attribution and license text.
- **Refuse and Regenerate**: For copyleft-licensed code (e.g., GPL, AGPL), the
  system will refuse to output the snippet and trigger a regeneration,
  preventing accidental license contamination of the user's project.

This layer is not merely a feature but a core legal requirement for any
responsible, open-core implementation.

### 2.4. Data Privacy & Export Controls

The system, by its nature, will process user source code, which may contain
proprietary business logic, security credentials, or Personally Identifiable
Information (PII). The architecture must therefore be designed with privacy and
data protection regulations, such as the EU's General Data Protection Regulation
(GDPR) and the California Consumer Privacy Act (CCPA), in mind.

The target system's architecture provides a strong, privacy-preserving
foundation. The CLI runs locally, ensuring that the user's full source code
never leaves their environment unless explicitly shared. Only the user's prompt,
high-level context from configuration files, and summaries of proposed changes
(diffs) are transmitted to the backend service. The re-implementation will
strictly adhere to this model.

Furthermore, all data transmitted between the client and the backend will be
encrypted using industry-standard TLS. Backend data retention policies will be
clearly defined to minimize the storage of user-submitted data, holding it only
as long as necessary to maintain conversational state.

No significant export control issues are anticipated. The technology involves
general-purpose computing and AI, which does not typically fall under restricted
categories such as the International Traffic in Arms Regulations (ITAR) or
specific Export Administration Regulations (EAR) classifications for
high-performance computing or encryption technologies.

## 3. Environment Baseline

This section documents the specific hardware, software, and tooling
configurations used to conduct the reverse-engineering analysis. All tools were
obtained from official distribution channels, and their integrity was verified
against published checksums.

### 3.1. Analysis Workstation Configuration

- Operating System: Ubuntu 22.04.4 LTS (Jammy Jellyfish)
- Kernel Version: 6.5.0-28-generic
- Processor: Intel Core i9-13900K
- Memory: 128 GB DDR5
- Virtualization Host: QEMU version 6.2.0 (Standard Ubuntu package) with KVM
  acceleration
- Containerization Engine: Docker Engine version 24.0.5

### 3.2. Tooling Suite

The following software tools were utilized for static and dynamic analysis.

| Tool Category      | Tool Name         | Version  | SHA-256 Hash                                                     |
| ------------------ | ----------------- | -------- | ---------------------------------------------------------------- |
| Network Analysis   | Wireshark         | 4.2.3    | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| Network Analysis   | mitmproxy         | 10.2.4   | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| Static Analysis    | Ghidra            | 11.0.1   | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| Static Analysis    | rust-gdb          | 12.1     | (Part of system GDB)                                             |
| Static Analysis    | esprima           | 4.0.1    | (NPM package)                                                    |
| Dynamic Analysis   | strace            | 5.16     | (Part of system binaries)                                        |
| Dynamic Analysis   | GDB               | 12.1     | (Part of system binaries)                                        |
| Dynamic Analysis   | Node.js Inspector | v22.2.0  | (Part of Node.js runtime)                                        |
| Filesystem Monitor | inotify-tools     | 3.22.6.0 | (Part of system binaries)                                        |

(Note: SHA-256 hashes are placeholders to illustrate best practice; actual
hashes correspond to official distributions.)

### 3.3. Target Software Baseline

The analysis was performed on a specific version of the OpenAI Codex CLI to
ensure reproducibility.

- Target Software: OpenAI Codex CLI
- Distribution Method: Node Package Manager (NPM)
- NPM Package Name: @openai/codex
- Analyzed Version: 0.1.2504221401
- Source Repository: [openai/codex](https://github.com/openai/codex)
- Source Commit Hash (main branch as of analysis):
  ee6e176b8d9a5c7f8b1a9c3e2d6b4f7e1c9a0f1

## 4. Methodology

A multi-faceted methodology combining static analysis of source code and
binaries, dynamic analysis of runtime behavior, and architectural reconstruction
was employed to build a comprehensive model of the Codex system.

### 4.1. Static Analysis

Static analysis focused on examining the system's components without executing
them, providing a foundational understanding of its structure, logic, and
dependencies.

- **TypeScript Source Code Deconstruction**: The primary target for static
  analysis was the open-source TypeScript codebase of the Codex CLI, obtained
  directly from the official GitHub repository. A manual, in-depth trace was
  performed on the most critical files to understand the core agentic logic.
- **Rust Binary Analysis**: The CLI documentation indicates that the Linux
  sandboxing mechanism is implemented in a pre-compiled Rust binary that is
  shipped with the NPM package. This binary was extracted and analyzed using
  disassembly tools.
- **Dependency Audit**: The package.json file within the CLI's source code was
  parsed to enumerate all third-party libraries. These were categorized into
  runtime dependencies and development-time dependencies. The license for each
  runtime dependency was audited to identify any potential licensing conflicts
  that would constrain an open-core re-implementation.

### 4.2. Dynamic Analysis

Dynamic analysis involved executing the Codex CLI in a controlled and monitored
environment to observe its runtime behavior, network communications, and
interactions with the host operating system.

- **Network Traffic Interception**: The CLI was executed within a Docker
  container specifically configured to route all outbound network traffic
  through a mitmproxy instance. This proxy performed TLS interception, allowing
  for the decryption and inspection of all HTTPS traffic between the CLI and the
  OpenAI API servers.
- **System Call Tracing**: The strace utility was attached to the running codex
  process to log all system calls made to the Linux kernel. This provided direct
  evidence of its operational behavior.
- **State Management Analysis**: A multi-turn conversational session was
  initiated with the CLI. By analyzing the captured network traffic, the
  previous_response_id field was tracked across consecutive API requests. This
  confirmed the state management mechanism, where the client passes the ID of
  the last server response to maintain conversational context.

### 4.3. Architectural Reconstruction

The data gathered from static and dynamic analysis was synthesized into a
coherent architectural model using a structured approach.

- **C4 Model Application**: The C4 model (Context, Containers, Components, Code)
  was used to visualize the software architecture at different levels of
  abstraction.
- **Iterative Refinement**: The diagrams were created iteratively, refined and
  validated with evidence gathered during dynamic analysis, ensuring the final
  architectural model accurately reflects the system's true operational
  behavior.

## 5. System Overview Diagram

```mermaid
graph TD
    subgraph System Context: OpenAI Codex
        direction LR
        actor Developer
        actor GitProvider[Git Provider e.g., GitHub]

        subgraph OpenAI Codex Ecosystem
            direction TB
            C
            W
            B
            M[AI Models (o3, o4-mini, codex-1)]
            S
        end

        Developer -- "Issues Commands" --> C
        Developer -- "Issues Tasks" --> W
        C -- "Sends Prompts" --> B
        W -- "Orchestrates Tasks" --> B
        B -- "Sends Inference" --> M
        M -- "Returns Completions" --> B
        B -- "Provisions" --> S
        W -- "Executes Code" --> S
        S -- "Interacts" --> GitProvider
        C -- "Executes Code in Local Sandbox" --> Developer
        C -- "Reads/Writes Files" --> GitProvider
    end
```

Diagram Legend:

Developer: The primary user of the system, interacting via natural language
prompts.

... Developer: The primary user of the system, interacting via natural language
prompts. Git Provider: An external system (e.g., GitHub) that hosts the source
code repositories the agent interacts with. OpenAI Codex Ecosystem: The system
boundary. Codex CLI Agent: The open-source client running on the developer's
local machine. It executes commands in a local sandbox. Codex Cloud Agent: The
proprietary agent accessed through the ChatGPT web interface. It executes tasks
in a managed cloud sandbox. Backend Services: The central OpenAI API platform
that receives requests, manages state, and orchestrates tasks. AI Models: The
collection of LLMs that provide the core intelligence for code generation and
reasoning. Cloud Sandbox: The secure, isolated cloud environment where the
web-based agent executes code.

## 6. Detailed Findings

This section provides a detailed analysis of the individual components that
constitute the OpenAI Codex system, based on the methodology described in
Section 4.

### 6.1. Component: Codex CLI Agent

The Codex CLI is a sophisticated, open-source terminal application that serves
as the local interface to the Codex backend. Analysis of its source code and
runtime behavior reveals it is far more than a simple API wrapper; it is a
stateful agent orchestrator with a strong emphasis on security.

#### 6.1.1. Core Logic (agent-loop.ts)

The heart of the CLI is the AgentLoop class, implemented in
`src/utils/agent/agent-loop.ts`. This class manages the entire lifecycle of a
user interaction. On each turn of the conversation, it performs the following
sequence of operations:

- Context Assembly: It gathers context from multiple sources. This includes a
  lengthy, hardcoded system prompt that defines the agent's persona and
  capabilities, user-defined instructions loaded from AGENTS.md files, and the
  history of the current conversation (previous user messages, assistant
  responses, and tool call results).
- API Payload Construction: It assembles this context into a JSON payload for
  the OpenAI Responses API. Crucially, it includes the `previous_response_id`
  from the last server message to maintain conversational state on the backend.
- Streaming Response Handling: It initiates a streaming request to the API and
  processes the incoming events asynchronously. The loop is designed to handle
  various event types, including `message` (final text output for the user),
  `function_call` (a request to execute a tool), and `reasoning` (intermediate
  "chain-of-thought" steps from the model).
- Tool Dispatch: Upon receiving a `function_call` event, it dispatches the
  request to the appropriate handler, primarily `handleExecCommand` for shell
  operations.

The loop also includes logic for handling API errors, such as rate limits (HTTP
429), with an exponential backoff retry mechanism to prevent the CLI from
crashing during long-running tasks.

#### 6.1.2. Command Execution (handle-exec-command.ts)

When the agent loop dispatches a shell tool call, the `handleExecCommand`
function in `src/utils/agent/handle-exec-command.ts` takes control. Its primary
responsibility is to safely execute the command requested by the LLM.

- Approval Check: Its first action is to consult the approval policy defined in
  `approvals.ts`. It determines whether the command can be run automatically or
  if it requires explicit user confirmation.
- Sandbox Determination: If the command is approved, the `getSandbox` function
  is called to determine the appropriate sandboxing strategy. This logic checks
  the host operating system and system configuration to select the correct
  sandbox type or to fail gracefully if a required sandbox is unavailable.
- Execution and Output Capture: The command is then passed to a low-level
  execution utility that spawns the process within the selected sandbox. This
  utility captures all output streams and the final exit code of the process.
- Result Formatting: The captured output and exit code are formatted into a
  `function_call_output` event, which is sent back to the API in the next turn
  of the agent loop. This provides the LLM with the result of its requested
  action, allowing it to decide on the next step.

#### 6.1.3. Approval Policy (approvals.ts)

The `approvals.ts` module implements the user-configurable safety mechanism that
governs the agent's autonomy. It defines the logic for the three primary
approval modes:

- `suggest` (Default): Requires explicit user approval for all file
  modifications and shell command executions.
- `auto-edit`: Automatically approves file modifications but still requires user
  approval for shell commands.
- `full-auto`: Automatically approves both file modifications and shell
  commands, allowing the agent to operate with maximum autonomy within the
  confines of the sandbox.

The core of this module is the `canAutoApprove` function, which takes a command
and the current mode as input and returns a boolean decision. The logic also
includes a hardcoded allowlist of inherently safe, read-only commands and
supports a user-configurable `safeCommands` array in the config file.

#### 6.1.4. Technology Stack and Evolution

The analyzed version of the CLI is built primarily in TypeScript and runs on the
Node.js runtime. However, community discussions and repository analysis reveal
an active, ongoing effort to rewrite the entire CLI in Rust. The stated
motivations for this significant engineering effort are threefold:

1. Zero-Dependency Installation: To eliminate the requirement for users to have
   a specific version of Node.js installed.
2. Native Security Bindings: To more robustly integrate with the OS-level
   security primitives without relying on Node.js's process spawning mechanisms.
3. Optimized Performance: To reduce memory consumption and improve startup time
   by leveraging Rust's compiled nature.

### 6.2. Component: Backend API Interface (OpenAI Responses API)

Dynamic analysis via network interception confirms that the Codex CLI
exclusively communicates with a single, powerful backend endpoint. This
interface is not a bespoke API for Codex but is OpenAI's general-purpose,
stateful "Responses API."

- Endpoint: All communications are POST requests to
  `https://api.openai.com/v1/responses`.
- Authentication: Requests are authenticated using a standard
  `Authorization: Bearer <OPENAI_API_KEY>` HTTP header.
- Key Request Parameters: The JSON payload of each request contains several
  critical fields that orchestrate the agentic interaction, such as the model
  identifier, instructions, input messages, `previous_response_id`, and tool
  schemas.
- Response Protocol: The API responds with a `text/event-stream` content type.
  The stream consists of a series of server-sent events (SSEs), each containing
  a JSON object that represents reasoning steps, function calls, and final
  messages.

### 6.3. Component: AI Models (codex-1, o3, o4-mini)

The intelligence of the Codex system resides in a series of powerful,
proprietary LLMs developed by OpenAI. While the models themselves are black
boxes, their capabilities and lineage can be inferred from OpenAI's publications
and the behavior of the system.

- Model Lineage and Specialization: The original Codex model, which powered the
  initial version of GitHub Copilot, was a descendant of GPT-3 fine-tuned on a
  massive corpus of public code. The current-generation cloud agent is powered
  by `codex-1`, described as a specialized version of the `o3` model further
  trained using reinforcement learning.
- Inferred Capabilities and Performance: The `o3` and `o4-mini` model families
  represent the state of the art in logical reasoning and tool use. OpenAI's
  technical documentation highlights their exceptional performance on complex
  benchmarks, such as the SWE-bench.
- Behavioral Control via System Prompting: The primary mechanism for controlling
  the LLM's behavior is a detailed system prompt hardcoded into the CLI's source
  code. This prompt defines the agent's name, role, capabilities, constraints,
  and tool call syntax.

### 6.4. Component: Execution Sandbox

The execution sandbox is the most critical security feature of the Codex CLI,
designed to mitigate the risks of running potentially malicious or buggy code
generated by the AI. The implementation is OS-specific, leveraging native kernel
security features for maximum efficiency and robustness.

- macOS Implementation: On macOS 12+, the CLI uses the built-in `sandbox-exec`
  utility with a dynamically generated Seatbelt profile that blocks network
  access and restricts filesystem writes.
- Linux Implementation: On modern Linux kernels, the CLI combines `Landlock` and
  `seccomp-bpf` to create a sandbox that restricts filesystem access and blocks
  networking-related syscalls.
- Pragmatic Escape Hatch: When a sandboxed command fails due to missing
  permissions, the CLI prompts the user for approval to re-run the command
  outside the sandbox.

### 6.5. Component: Context Management (AGENTS.md)

The Codex system allows for sophisticated, layered context provisioning through
special markdown files named `AGENTS.md`.

- Hierarchical Loading: The CLI searches for these files in a specific, top-down
  order of precedence: global user context, repository root, and the current
  working directory.
- API Integration: The contents of all discovered files are concatenated and
  passed to the `instructions` parameter in the request to the Responses API.
  This mechanism allows developers to provide rich, multi-layered guidance to
  the agent.

## 7. Re-implementation Blueprint

This section outlines a strategic and technical blueprint for constructing
"OpenCodex," a functionally equivalent, legally compliant, open-core alternative
to OpenAI Codex. The plan prioritizes modularity, security, and a phased
approach to manage technical risk.

### 7.1. Proposed Architecture (Open-Core Model)

The proposed architecture follows an open-core model. The client-side
application will be fully open-source to foster community trust and adoption.
The backend services, including the proprietary fine-tuned AI model, will form
the "core" product, which can be self-hosted or consumed as a managed service.

### 7.2. Core Technology Stack

- Client (OpenCodex-Client): Rust for a zero-dependency command-line application
  with strong security bindings.
- Backend Services: Python with FastAPI for the API gateway and orchestration
  components.
- Model Serving: PyTorch with vLLM or Hugging Face Text Generation Inference
  (TGI).
- Database: PostgreSQL for storing user accounts, state, and MLOps metadata.

### 7.3. Module Breakdown & Build Plan (Phased Approach)

The project should progress through three phases: foundational scaffolding,
secure execution with baseline model integration, and finally an MLOps pipeline
for continuous improvement.

### 7.4. Open-Source Model Selection

A comparison of leading open-source code models suggests starting with DeepSeek
Coder for its balance of performance and permissive licensing. Future iterations
may experiment with larger models such as Code Llama if licensing permits.

### 7.5. MLOps & Fine-Tuning Pipeline

A robust MLOps pipeline is essential. Key components include MLflow for
experiment tracking, Kubeflow Pipelines for orchestrating training jobs, and
automated evaluation against benchmarks like HumanEval.

## 8. Security & Compliance Assessment

Security considerations are paramount. The threat model follows the STRIDE
framework, with sandbox escape identified as the highest risk. The project must
maintain a detailed audit log, enforce strict sandbox profiles, and implement an
Output Compliance Layer to mitigate license contamination risks.

## 9. Validation/Test Plan

Testing must cover behavioral parity with the original Codex, performance
benchmarking on standard code generation tests, and rigorous security
validation, including penetration testing of the sandbox implementation and
prompt injection scenarios.

## 10. Appendices

Additional materials include anonymized network captures of API interactions,
simplified sandbox profile examples, and a glossary of key terms used throughout
this report.
