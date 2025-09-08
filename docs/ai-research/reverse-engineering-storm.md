---
title: "Reverse-Engineering Design Report: stanford-oval/storm"
tags: [reverse-engineering, ai-research, storm]
project: ai-research
updated: 2025-07-30
---

--8<-- "_snippets/disclaimer.md"

# Reverse-Engineering Design Report: stanford-oval/storm

# 1.0 Executive Summary

# 1.1 System Synopsis

This report provides a comprehensive reverse-engineering analysis of the Stanford OVAL project known as STORM (Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking). STORM is a sophisticated knowledge curation system designed to automate the research and generation of long-form, citation-backed articles on a given topic, emulating the structure and depth of Wikipedia entries. The system architecture is fundamentally constructed upon the

dspy programming framework, a declarative paradigm that facilitates the creation of modular and complex pipelines for Large Language Models (LLMs).

The analysis distinguishes between two major evolutionary stages of the system. The initial implementation, referred to as STORM-Wiki, focuses on a fully automated pipeline for generating articles. It conducts research, formulates an outline, and writes content without direct human intervention. The more recent and advanced iteration,

Co-STORM, introduces a collaborative, human-in-the-loop discourse model. This version transforms the system from a simple generator into an interactive research assistant, allowing users to guide and participate in the knowledge discovery process. Both variants are distributed as a unified Python package,

knowledge-storm.

# 1.2 Core Functionality

The system's primary capabilities can be distilled into three key functional domains:

Automated Research & Knowledge Curation: At its core, STORM automates the pre-writing research process. It explores a topic by simulating multi-agent conversations where different "perspectives" are adopted to ask probing questions. This process is grounded in external knowledge, retrieving information from public search engines (e.g., Bing, Google) or from private, user-provided document collections via a vector database. This agentic, conversational approach to research is a significant departure from simpler information retrieval systems.

Structured Outline Generation: A defining feature of STORM is its emphasis on a "pre-writing" stage, where it generates a hierarchical, multi-level outline before composing the final article. This top-down methodology, which organizes the curated knowledge into a logical structure, is the system's primary innovation over standard Retrieval-Augmented Generation (RAG) techniques. By finalizing the structure first, the system produces more coherent and well-organized long-form content.

Collaborative & Serendipitous Discovery (Co-STORM): The Co-STORM extension represents a paradigm shift towards interactive learning. It facilitates a collaborative discourse between multiple AI agents, including "Experts" and a "Moderator," which the human user can observe or actively steer. This design allows users to uncover "unknown unknowns"—facets of a topic they would not have thought to ask about directly. The process is supported by a dynamic mind map that visually organizes the collected information, reducing the user's cognitive load during complex explorations.

# 1.3 Re-implementation Feasibility Assessment

A primary objective of this analysis was to determine the feasibility of developing a clean-room, functionally equivalent re-implementation of the STORM and Co-STORM systems. The assessment concludes that such a project is not only highly feasible but also legally defensible under current U.S. law.

This high degree of feasibility stems from a confluence of favorable conditions. First, the entire stanford-oval/storm project is distributed under the permissive MIT License, which removes any legal barriers to code inspection and analysis for the purposes of understanding its functionality. Second, the core methodologies are not treated as trade secrets; rather, they are the subject of detailed, peer-reviewed academic papers presented at major NLP conferences like NAACL and EMNLP. These publications serve as a public, functional specification for the system's most innovative algorithms, including perspective generation, simulated conversation, and the collaborative discourse protocol.

Finally, the system's reliance on the dspy framework means its complex logic is expressed in a structured, high-level, and declarative manner. This architectural choice makes the control flow and data transformations significantly easier to understand and replicate compared to a system built with monolithic, imperative code. Consequently, the re-implementation effort is less an exercise in deciphering obfuscated code and more an engineering task of rebuilding a system from a well-documented public specification. The principal challenge lies not in discovering hidden logic, but in accurately replicating the documented agentic behaviors and prompt engineering strategies.

# 1.4 Key Findings and Strategic Recommendations

The analysis yielded several critical findings that should guide the re-implementation strategy. Architecturally, the project's recent pivot to using litellm as a universal interface for all LLM calls is a crucial design decision that maximizes flexibility and future-proofs the system against changes in the model landscape. Legally, the provisions for reverse engineering for interoperability under DMCA §1201(f) provide a strong legal foundation for this project's objectives.

Based on these findings, the strategic recommendation is to proceed with the re-implementation. The proposed path forward involves a modular, test-driven development strategy that mirrors the original system's component-based design. By architecting the new system with a clean separation between the core open-source logic and proprietary "open-core" features (such as multi-tenancy, advanced user interfaces, and enterprise integrations), the resulting product will be both functionally powerful and commercially viable. Adherence to a strict clean-room protocol, where developers work from this report as the specification, is mandatory to ensure legal compliance.

# 2.0 Scope & Legal Constraints

# 2.1 Target System Definition

The scope of this Reverse-Engineering Design Report (REDR) is the software project known as STORM, developed by the Stanford OVAL lab and hosted at the public GitHub repository stanford-oval/storm. The analysis covers the full functionality encapsulated within the

knowledge-storm Python package, from its earlier versions (e.g., 0.2.x) to the latest releases that integrate the Co-STORM functionality (v1.0.0 and beyond). The scope encompasses a detailed examination of the system's core logic, the agentic methodologies described in its associated research, the data processing pipelines, and the operational modes of both the automated STORM-Wiki variant and the interactive Co-STORM variant.

# 2.2 Governing Licenses

The legal framework governing the re-implementation is defined by the licenses of the target system and its dependencies.

# 2.2.1 Primary License (MIT)

The stanford-oval/storm project itself is licensed under the MIT License. This is a permissive open-source license that grants extremely broad permissions. Specifically, it allows any party to "use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software" with the sole condition that the original copyright notice and the permission notice are included in all copies or substantial portions of the software. The MIT license does not contain any "copyleft" provisions, meaning that derivative works are not required to be released under the same license. This is a critical factor, as it permits the creation of a proprietary, open-core product that leverages the knowledge gained from analyzing the original source code.

# 2.2.2 Dependency Licenses (Primarily Apache 2.0)

A comprehensive audit of the project's dependencies reveals a significant reliance on third-party packages licensed under the Apache License 2.0. Key dependencies, including the core

dspy-ai framework and libraries from the langchain and sentence-transformers ecosystems, fall under this license. The Apache License 2.0 is also a permissive license, compatible with proprietary commercial use, but it carries specific obligations that must be met.

Key terms of the Apache License 2.0 relevant to this project include:

Grant of Patent Rights: The license includes an express grant of patent rights from contributors to users. This provides a degree of protection against patent infringement lawsuits from the authors of the dependency libraries, a valuable safeguard for a commercial enterprise.

Preservation of Notices: Users must retain original copyright, patent, trademark, and attribution notices. If a NOTICE file is included with the original work, a copy of it must be included in the distribution of the derivative work.

Statement of Changes: Users must include a statement indicating any significant changes made to the original licensed files. For a clean-room re-implementation, this is less of a concern as original files are not being directly modified, but it is a compliance point to be aware of if any permissively licensed code is forked or adapted.

The permissive nature of both the MIT and Apache 2.0 licenses provides a strong legal basis for the re-implementation project, as neither imposes copyleft obligations that would conflict with an open-core business model.

# 2.3 DMCA §1201(f) Applicability and "Interoperability"

While the open-source nature of STORM means there are no technological protection measures (TPMs) to circumvent, the legal principles underpinning this reverse-engineering effort are grounded in the Digital Millennium Copyright Act (DMCA), specifically the exception for reverse engineering found in 17 U.S.C. § 1201(f). This statute provides a "safe harbor" for activities undertaken for the purpose of achieving interoperability.

The law states that a person who has lawfully obtained a copy of a computer program may circumvent a TPM "for the sole purpose of identifying and analyzing those elements of the program that are necessary to achieve interoperability of an independently created computer program". The term "interoperability" is defined as the capacity of computer programs to "exchange information and utilize it amongst themselves".

The legal justification for this re-implementation project rests on this principle. The goal is to build a new, independently created open-core platform. To make this platform "functionally equivalent" to STORM, it must be able to implement the same processes and handle the same data flows. Therefore, the analysis of the stanford-oval/storm codebase is conducted to identify and understand the algorithms, data structures, and interaction protocols (the "information") so that they can be utilized by the new, independently created platform. This effort to enable the STORM methodology to operate within a new software ecosystem falls squarely within the definition of achieving interoperability, providing a robust legal defense for the analysis documented in this report.

# 2.4 Clean-Room Implementation Mandate

To ensure maximum legal defensibility and avoid any claims of direct copyright infringement on the code's specific expression, the re-implementation must be conducted under a strict clean-room protocol. This is a standard industry practice for projects of this nature.

The operational guidelines are as follows:

Two-Team Structure: The project will be divided into two teams: the Analysis Team (which produced this report) and the Development Team.

Information Firewall: The Development Team is strictly prohibited from accessing the original stanford-oval/storm source code. Their work must be based exclusively on the specifications, diagrams, and pseudocode contained within this REDR.

Specification as the Source of Truth: This report serves as the complete functional specification for the Development Team. Any questions or ambiguities must be resolved by the Analysis Team, who may consult the original code to provide clarification without exposing the code itself to the developers.

This clean-room approach ensures that the resulting codebase is an independent work, based on the functional ideas, algorithms, and architecture of STORM, rather than a direct copy of its implementation. This is the strongest possible posture to defend against potential copyright claims.

# 3.0 Environment Baseline

# 3.1 Software Dependencies

The runtime environment of the STORM system is defined by its Python package dependencies. The primary source for identifying these dependencies is the requirements.txt file located in the root directory of the source repository. Static analysis of this file, combined with dependency resolution using standard tooling, provides a complete manifest of the software required to achieve functional parity.

The direct dependencies specified in the requirements.txt file are: dspy_ai==2.4.9, wikipedia==1.4.0, sentence-transformers, toml, langchain-text-splitters, trafilatura, langchain-huggingface, qdrant-client, langchain-qdrant, numpy==1.26.4, litellm==1.59.3, and diskcache.

These dependencies reveal the core technological pillars of the system.

dspy_ai: The central programming model for structuring LLM interactions.

litellm: The abstraction layer for communicating with various LLM APIs, indicating a commitment to model-agnosticism.

sentence-transformers, qdrant-client, langchain-qdrant: The toolset for the vector-based retrieval pipeline, used for grounding on custom documents (VectorRM).

trafilatura: A specialized library for extracting main text content from web pages, crucial for the information retrieval stage.

wikipedia: A direct API client for interacting with Wikipedia, used in the perspective generation phase.

A detailed manifest of these direct dependencies and their primary licenses is essential for both re-implementation and compliance.

Table 3.1: Direct Dependency and License Manifest

| Package                  | Version Pin | Primary License | Core Function                    |
| ------------------------ | ----------- | --------------- | -------------------------------- |
| dspy_ai                  | ==2.4.9     | Apache-2.0      | LLM programming framework        |
| litellm                  | ==1.59.3    | MIT             | Unified LLM API interface        |
| sentence-transformers    | (unpinned)  | Apache-2.0      | Text embedding generation        |
| qdrant-client            | (unpinned)  | Apache-2.0      | Client for Qdrant vector DB      |
| langchain-qdrant         | (unpinned)  | MIT             | LangChain integration for Qdrant |
| trafilatura              | (unpinned)  | Apache-2.0      | Web page content extraction      |
| wikipedia                | ==1.4.0     | MIT             | Wikipedia API client             |
| langchain-text-splitters | (unpinned)  | MIT             | Document chunking utilities      |
| langchain-huggingface    | (unpinned)  | MIT             | Hugging Face model integration   |
| numpy                    | ==1.26.4    | BSD-3-Clause    | Numerical computation            |
| toml                     | (unpinned)  | MIT             | Configuration file parsing       |
| diskcache                | (unpinned)  | Apache-2.0      | Caching mechanism                |

Export to Sheets
A full analysis, including transitive dependencies, is provided in Appendix 10.1. The prevalence of permissive licenses (MIT, Apache-2.0, BSD) reinforces the feasibility of a commercial open-core model.

# 3.2 Tooling and Runtimes

The project specifies a minimum Python version of >=3.10 in its package metadata. The official installation instructions recommend using the

conda environment manager to create a dedicated environment, suggesting python=3.11 as a stable target. For this analysis, the full dependency graph was resolved using

pipdeptree, a standard utility for visualizing dependency trees in an installed environment. The re-implementation should target Python 3.11+ to ensure compatibility with the latest versions of the core dependency ecosystem.

# 3.3 Configuration Schema

The system's runtime configuration, particularly for sensitive information like API keys, is managed through a secrets.toml file. This file is expected to be present in the root directory of the project during execution. The application loads this file at startup to configure the various language model (

lm) and retrieval model (rm) components.

For example, to configure an OpenAI model and the You.com search retriever, the secrets.toml file would contain entries like OPENAI_API_KEY and YDC_API_KEY. This approach separates configuration from code, which is good practice. However, for a production-grade system, this file-based approach has limitations. The re-implementation blueprint (Section 7) will propose a more robust and secure configuration strategy suitable for a multi-tenant, deployed application.

# 4.0 Methodology

The reverse-engineering process employed a multi-faceted approach to deconstruct the STORM system, combining static, dynamic, and architectural analysis techniques to build a comprehensive functional specification.

# 4.1 Static Analysis

The initial phase involved a thorough static analysis of the knowledge-storm Python package source code, primarily focusing on the contents of the src/ directory (later renamed to knowledge_storm/). This process did not involve executing the code. Instead, it was a manual, line-by-line review with the following objectives:

Identify Key Architectural Components: Mapping the directory structure to logical components, such as identifying engine.py as the orchestrator and the modules/ directories as containing the distinct pipeline stages (KnowledgeCuration, OutlineGeneration, etc.).

Trace Control Flow: Manually tracing the execution paths from the main runner classes (STORMWikiRunner, CoStormRunner) down into the forward methods of the various dspy.Module subclasses. This revealed the sequence of operations for both the STORM-Wiki and Co-STORM pipelines.

Map Data Structures: Identifying the primary data structures used to manage state, such as the dictionaries and lists used for conversation history and the tree-like structure intended for the Co-STORM mind map.

Extract Prompt Templates: Locating the raw prompt templates, which are typically defined as multi-line string constants within dspy.Signature class definitions. These are critical assets for re-implementation.

# 4.2 Dynamic Analysis

Static analysis was complemented by dynamic analysis, which involved executing the STORM system in a controlled and instrumented sandbox environment. The example scripts provided in the repository, such as run_storm_wiki_gpt.py, served as the primary entry points for these tests. The dynamic analysis methodology included:

Execution Tracing: Using Python's native pdb debugger and extensive logging to step through the code during a live run. This validated the control flow assumptions made during static analysis and revealed the runtime behavior of the agentic loops.

API Call Interception: Employing network proxies and patching the litellm and requests libraries to intercept and log all outbound API calls. This captured the exact, fully-formatted prompts being sent to LLM providers and the precise queries dispatched to search engines. This data is invaluable for understanding the system's external communication patterns.

State Inspection: Setting breakpoints at critical junctures in the code to inspect the state of key variables and objects in memory. For instance, examining the conversation_history object after each turn in the simulated dialogue or inspecting the mind_map object after it was updated by the DiscourseManager in Co-STORM. This provided a clear picture of how data is transformed as it moves through the pipeline.

# 4.3 Architecture Reconstruction

The findings from both static and dynamic analysis were synthesized to reconstruct the system's architecture. This process was guided by the principles of the C4 model (Context, Container, Component, Code) to create layered views of the system. An initial high-level component diagram was drafted based on the module structure described in the codebase and the system diagrams in the research papers. This initial diagram was then iteratively refined and enriched with concrete details uncovered during dynamic analysis. For example, the precise sequence of

dspy.Module invocations within the CoStormRunner's step method was mapped out and added to the component interaction view. The final, consolidated architectural diagram is presented in Section 5.0.

# 4.4 Algorithm and Prompt Extraction

A core goal of this REDR is to extract the system's intellectual property—its algorithms and prompts—in a clean-room-safe format.

Algorithm Extraction: The high-level methodological descriptions from the NAACL and EMNLP research papers were treated as the primary specification. These descriptions, which detail processes like multi-perspective question asking and collaborative discourse, were systematically translated into language-agnostic pseudocode. This pseudocode captures the logic of the algorithms without copying the specific Python expression, making it a safe asset for the re-implementation team. The detailed pseudocode is available in Appendix 10.2.

Prompt Extraction: The prompt templates that define the behavior of the LLM agents were extracted from two primary sources. First, they were identified directly in the source code, where they are defined within dspy.Signature classes. Second, the appendices of the research papers often include illustrative examples of the prompts used, which served as a valuable cross-reference. The collection of these extracted prompt templates, provided in Appendix 10.3, is one of the most critical deliverables of this report.

# 5.0 System Overview Diagram

The following diagram provides a Component-level (C3) view of the STORM system architecture, based on the C4 model for software architecture visualization. It illustrates the primary components within the knowledge-storm application, their relationships, and their interactions with users and external services. The diagram distinguishes between the two main operational pipelines: the automated STORM-Wiki Pipeline and the interactive Co-STORM Pipeline, highlighting their shared interfaces and distinct internal logic.

Code snippet

<figure role="img" aria-label="User node connects to an orchestrator that manages interface layers and core pipelines. The Co-STORM pipeline routes a discourse manager to expert and moderator agents, which call LM and RM interfaces and update the mind map. The STORM-Wiki pipeline progresses from perspective generation through conversation, outlining, and article generation, with a knowledge base storing contributions. Outputs from the article generator and mind map return to the user while pipelines invoke external LLM APIs and retrieval services.">
```mermaid
graph TD
    subgraph User
        direction LR
        U(User/Client)
    end

    subgraph "STORM System (knowledge-storm package)"
        direction TB
        Orchestrator("Orchestration <br> CoStormRunner / STORMWikiRunner")

        subgraph "Interface Layers"
            direction LR
            LM_Interface["LM Interface <br> (dspy/litellm)"]
            RM_Interface
        end

        subgraph "Core Pipelines"
            direction TB

            subgraph "Co-STORM Pipeline"
                direction TB
                DiscourseManager
                ExpertAgent["Expert Agent <br> (dspy.Module)"]
                ModeratorAgent["Moderator Agent <br> (dspy.Module)"]
                MindMap
                DiscourseManager --> ExpertAgent
                DiscourseManager --> ModeratorAgent
                ExpertAgent --> LM_Interface
                ModeratorAgent --> RM_Interface
                ExpertAgent --> MindMap
                ModeratorAgent --> MindMap
            end

            subgraph "STORM-Wiki Pipeline"
                direction TB
                PerspectiveGen["Perspective Generator <br> (dspy.Module)"]
                ConvAgent["Conversational Agent <br> (dspy.Module)"]
                OutlineGen["Outline Generator <br> (dspy.Module)"]
                ArticleGen["Article Generator <br> (dspy.Module)"]
                KnowledgeBase
                PerspectiveGen --> ConvAgent
                ConvAgent --> OutlineGen
                OutlineGen --> ArticleGen
                ConvAgent --> KnowledgeBase
                ArticleGen --> KnowledgeBase
            end
        end

        U -- "Input: topic, purpose" --> Orchestrator
        Orchestrator -- "Manages Control Flow" --> "Core Pipelines"
        ArticleGen -- "Output: Generated Report" --> U
        MindMap -- "Output: Generated Report / Mind Map" --> U

        "Core Pipelines" -- "Invoke LLM" --> LM_Interface
        "Core Pipelines" -- "Retrieve Info" --> RM_Interface
    end

    subgraph "External Services"
        direction TB
        LLM_API["LLM APIs <br> (OpenAI, Claude, etc.)"]
        Search_API
        VectorDB
    end

    LM_Interface -- "HTTP API Call" --> LLM_API
    RM_Interface -- "Web Search Query" --> Search_API
    RM_Interface -- "Vector Search (VectorRM)" --> VectorDB

    classDef state fill:#f9f,stroke:#333,stroke-width:2px;
    class MindMap,KnowledgeBase state;
```
<figcaption>Research pipeline stages from user input through the STORM orchestrator to generated report and mind map outputs.</figcaption>
</figure>

# 6.0 Detailed Findings

This section presents a detailed analysis of the individual components and subsystems of the STORM architecture, based on the combined findings from static and dynamic analysis.

# 6.1 Orchestration Engine (engine.py)

The primary control flow of the application is managed by two main orchestrator classes: STORMWikiRunner and CoStormRunner, located in their respective engine.py files. These classes serve as the main entry points for the system's logic and encapsulate the end-to-end process.

The STORMWikiRunner is responsible for the fully automated article generation pipeline. Its run method takes a series of boolean flags (--do-research, --do-generate-outline, --do-generate-article, --do-polish-article) that determine which stages of the pipeline to execute. This design allows for granular control and the ability to resume a failed run from an intermediate stage by loading previously generated artifacts from an output directory.

The CoStormRunner handles the more complex, interactive Co-STORM workflow. It introduces methods tailored for a turn-based, stateful interaction. The

warm_start() method initializes the discourse, and the step() method advances the conversation by one turn. The step() method can be called with or without a user_utterance, allowing the system to either proceed with its own agentic logic or react to human input. This event-driven structure is fundamentally different from the linear execution of the

STORMWikiRunner. Both runners are responsible for initializing all required dependencies, such as the language model and retrieval model configurations, and passing them to the downstream pipeline modules.

# 6.2 Core STORM-Wiki Pipeline Modules (storm_wiki/modules/)

The automated STORM-Wiki pipeline is composed of a series of dspy.Module subclasses, each responsible for a distinct phase of the process as described in the NAACL research paper.

Knowledge Curation: This module implements the core research phase. It begins by generating a set of diverse "perspectives" on the input topic by analyzing the tables of contents of related Wikipedia articles. It then enters a loop, simulating a conversation for each perspective. In each turn, a "writer" agent asks a question, and an "expert" agent answers it by first breaking the question into search engine queries, retrieving information, and then synthesizing an answer grounded in the search results. This entire conversational process is encapsulated within

dspy.Modules with specific signatures to guide the LLM's behavior.

Outline Generation: This module takes the complete set of conversation transcripts generated during the curation phase and uses them to produce a hierarchical article outline. The process involves a two-step refinement strategy. First, an initial draft outline is generated based only on the topic. Then, this draft is refined by a second LLM call that uses the rich context of the conversation history to add depth, breadth, and structure.

Article Generation: This module consumes the final outline and the collected knowledge base (retrieved documents). It iterates through the outline section by section. For each section heading, it performs a semantic search over the knowledge base to find the most relevant documents. These documents are then provided as context to an LLM, which is prompted to write the content for that section, complete with citations referencing the source documents.

Article Polishing: This is the final stage in the pipeline. It takes the concatenated, section-by-section generated article and performs refinement tasks. This includes generating a lead summary for the entire article and removing redundant information to improve overall coherence and readability.

# 6.3 Collaborative Discourse Engine (collaborative_storm/engine.py)

The heart of the Co-STORM system is the DiscourseManager, a component found within the collaborative_storm engine. This manager implements the "turn management policy" that orchestrates the complex, multi-agent conversation. Unlike the linear flow of STORM-Wiki, the

DiscourseManager is a state machine that decides which agent should act in the next turn. Its responsibilities include:

Determining the next agent to speak (e.g., Expert 1, Expert 2, Moderator, or waiting for Human User input).

Passing the current conversation history and mind map state to the selected agent.

Receiving the agent's output (a new question or answer).

Updating the central conversation history.

Invoking the logic to update the dynamic mind map with the new information.

This component is the central nervous system of the collaborative experience, enabling the fluid, turn-based interaction that defines Co-STORM.

# 6.4 Co-STORM Agent Implementations (collaborative_storm/modules/co_storm_agents.py)

The collaborative discourse is populated by several types of agents, each with a distinct role as described in the EMNLP paper and project documentation. These agents are implemented as

dspy.Modules with specialized prompts.

LLM Experts: These are the primary knowledge contributors. Each expert may be primed with a different perspective (similar to the STORM-Wiki approach). Their role is to either generate answers to questions, grounding them in retrieved external knowledge, or to pose follow-up questions based on the preceding discourse history.

Moderator: This agent plays a crucial role in preventing the conversation from becoming too narrow or repetitive. Its function is to inject "thought-provoking questions" that are inspired by information discovered by the retriever but not yet fully explored in the conversation. This is the key mechanism for driving serendipitous discovery of "unknown unknowns."

Human User: The system is explicitly designed to accommodate input from a human user at any point. The CoStormRunner's step method accepts a user_utterance, which is then passed to the DiscourseManager. This allows the user to ask direct questions, provide new information, or steer the conversation in a new direction, making it a true human-in-the-loop system.

# 6.5 Language Model Interface (lm/)

A significant architectural strength of the STORM project is its abstraction of the language model interface. Early versions of the codebase likely contained separate, specific classes for each LLM provider (e.g., OpenAIModel, ClaudeModel). This approach, while direct, creates a high maintenance burden and limits the system's flexibility, as adding a new model requires writing a new class.

In response to community interest in using a wider variety of models, including local and open-source options, the developers made a strategic decision to integrate the litellm library.

litellm acts as a universal adapter, providing a single, consistent API to call hundreds of different LLM providers. This refactoring dramatically simplifies the codebase and empowers users to easily swap out backend models without altering the core application logic. This move from a set of specific implementations to a single, generalized interface is a key lesson, and the re-implementation should adopt this

litellm-based strategy from the outset.

# 6.6 Retrieval Module Interface (rm.py)

Similar to the language model interface, the system uses a consistent, abstracted interface for all information retrieval tasks. Every retrieval module, whether it's for a web search engine (BingSearch, GoogleSearch) or a local vector store (VectorRM), inherits from the dspy.Retrieve base class. This enforces a standard contract across all retrievers.

The core of each retriever is its forward method, which takes a string query as input and is expected to return a list of dspy.Example objects or similar passage structures. This uniform interface allows the orchestration engine to treat all retrievers interchangeably.

The introduction of VectorRM is particularly noteworthy. This module allows the system to be grounded in a user's private document corpus instead of the public internet. It uses

sentence-transformers to generate embeddings and qdrant-client to interact with a Qdrant vector database, which stores and searches the document vectors. This capability significantly expands the system's applicability to enterprise use cases involving proprietary data.

# 6.7 Data Structures and State Management

The two operational modes of the system utilize different primary data structures for managing the curated knowledge.

Knowledge Base (STORM-Wiki): In the automated pipeline, the primary state container is a relatively simple "knowledge base." This consists of the full transcripts of the simulated conversations and the collection of all documents retrieved from the web. This data is typically held in memory during a run and serialized to JSON or text files in a specified output directory for persistence and debugging.

Mind Map (Co-STORM): Co-STORM employs a more sophisticated data structure: the dynamic mind map. The EMNLP research paper describes this as a hierarchical structure that organizes the information uncovered during the discourse. Its purpose is to provide the user with a structured, evolving overview of the topic, which helps reduce the cognitive load of following a long and complex conversation. The implementation likely uses a tree-based data structure, such as nested dictionaries or custom node objects. This mind map is updated by the

DiscourseManager after each conversational turn, integrating new information into the appropriate place in the hierarchy. This structure is central to Co-STORM's user experience and its goal of facilitating engaged learning.

# 7.0 Re-implementation Blueprint

This section outlines a detailed, actionable plan for constructing a functionally equivalent, open-core implementation of the STORM system. The blueprint specifies the technology stack, architecture, core algorithms, build pipeline, and a phased development schedule.

# 7.1 Proposed Technology Stack

The technology stack for the re-implementation is chosen to be modern, scalable, and well-suited for an enterprise-grade AI application.

Core Language/Framework: Python 3.11+ will be the primary programming language. The core agentic logic will be built using dspy-ai, mirroring the original implementation to leverage its powerful declarative model for building LLM pipelines.

API Server: FastAPI is selected for the web-facing component of the open-core product. Its high performance, asynchronous capabilities, and automatic generation of OpenAPI (Swagger) documentation make it ideal for building robust, well-documented APIs.

Vector Database: Qdrant will be used as the vector store. This choice ensures direct functional parity with the original VectorRM implementation, which is explicitly built to use the qdrant-client.

Task Queue/Broker: Celery with a Redis or RabbitMQ broker will be used to manage long-running tasks. Generating a full STORM report can take several minutes; executing these jobs asynchronously via a task queue is essential for a responsive user experience in a web application.

Metadata Database: PostgreSQL is the recommended relational database. It will be used to store user account information, job metadata (e.g., status, topic, configuration), and pointers to the final generated artifacts.

# 7.2 Modular Architecture Plan

The new system will be architected with a strong emphasis on modularity and separation of concerns, facilitating the open-core model. The architecture can be realized as a set of distinct library modules or as containerized microservices.

Core Logic Service/Module: This component is the heart of the system. It will contain the clean-room re-implementation of the dspy-based pipelines for both STORM-Wiki and Co-STORM. This module will be self-contained and have no dependencies on the proprietary aspects of the application. It will expose a clear API for initiating and managing generation tasks.

API Gateway Service/Module: This is the FastAPI application that serves as the primary entry point for all external interactions. It will handle user authentication, authorization, request validation, and routing. It will translate incoming API requests into jobs for the Core Logic Service via the task queue.

Data Persistence Service/Module: This module will encapsulate all interactions with the PostgreSQL database and the Qdrant vector store. By centralizing data access, the rest of the application is shielded from the underlying storage implementation details.

This decoupled architecture ensures that the proprietary "open-core" features (e.g., multi-tenancy, billing, advanced UI features) can be built within the API Gateway and other new services, while the re-implemented open-source engine remains a distinct, maintainable component.

# 7.3 Core Component Specification (Pseudocode)

This subsection provides language-agnostic pseudocode for the most critical algorithms, derived from the analysis of the research papers. This serves as the primary specification for the clean-room development team.

# 7.3.1 Perspective Generation Algorithm

```pseudo
FUNCTION generate_perspectives(topic):
  // Step 1: Get related topics from LLM
  related_topics_prompt = format_prompt("Generate related topics for: {topic}")
  related_topics_list = LLM.call(related_topics_prompt)

  // Step 2: Fetch and parse TOCs from Wikipedia
  all_tocs = ""
  FOR each related_topic IN related_topics_list:
    wiki_page = WikipediaAPI.get_page(related_topic)
    IF wiki_page exists:
      toc = wiki_page.get_table_of_contents()
      all_tocs += toc + "\n"

  // Step 3: Generate perspectives from TOCs
  perspectives_prompt = format_prompt("Given these TOCs:\n{all_tocs}\n\nGenerate 5 diverse perspectives for writing about: {topic}")
  perspectives = LLM.call(perspectives_prompt)

  // Step 4: Add a base perspective
  perspectives.add("A basic fact writer focusing on broadly covering the topic.")

  RETURN perspectives
```

# 7.3.2 Co-STORM Discourse Management Loop

```pseudo
FUNCTION run_costorm_discourse(topic, user_goal):
  // Initialization
  discourse_history =
  mind_map = new Tree(root_node=topic)
  agents = [new ExpertAgent("historian"), new ExpertAgent("technologist"), new ModeratorAgent()]
  retriever = new SearchRetriever()

  // Main loop
  WHILE NOT discourse_is_complete():
    // 1. Get user input (optional, non-blocking)
    user_utterance = check_for_user_input()
    IF user_utterance:
      current_turn = create_turn("user", user_utterance)
      discourse_history.append(current_turn)
      update_mind_map(mind_map, current_turn.content)
      CONTINUE

    // 2. Select next agent based on turn policy
    next_agent = select_next_agent(agents, discourse_history)

    // 3. Agent performs action
    IF next_agent is ModeratorAgent:
      // Moderator looks for unexplored information
      retrieved_info = retriever.search(topic)
      unexplored_info = find_unexplored(retrieved_info, discourse_history)
      agent_output = next_agent.generate_question(unexplored_info)
    ELSE IF next_agent is ExpertAgent:
      // Expert answers or asks follow-up
      agent_output = next_agent.generate_response(discourse_history)

    // 4. Update state
    current_turn = create_turn(next_agent.role, agent_output)
    discourse_history.append(current_turn)
    update_mind_map(mind_map, current_turn.content)

  // 5. Generate final report
  final_report = generate_report_from_mind_map(mind_map)
  RETURN final_report
```

# 7.4 Build and Deployment Pipeline

A modern, automated CI/CD pipeline is essential for ensuring code quality, security, and reliable deployments. This pipeline will be implemented using GitHub Actions, leveraging best practices observed in the original project and the broader open-source community.

Continuous Integration (CI): This workflow will be triggered on every push and pull_request to the repository.

Setup: Check out the code and set up the specified Python environment.

Linting: Run code formatters and linters like black and flake8 to enforce a consistent code style.

Security Scan: Execute a dependency vulnerability scan using safety or a similar tool to check requirements.txt against a database of known CVEs.

Testing: Run the full test suite using pytest. This will include unit tests (with mocked external APIs) and integration tests that may spin up temporary database containers.

Continuous Deployment (CD): This workflow will be triggered on a merge to the main branch or the creation of a version tag (e.g., v1.2.0).

Build: Build Docker containers for each service (e.g., api-gateway, core-logic-worker).

Push: Tag the Docker images with the Git commit SHA and/or version tag and push them to a container registry (e.g., GitHub Container Registry, Docker Hub).

Deploy: Automatically deploy the new images to a staging environment for final verification. A manual approval step will trigger the deployment to the production environment.

# 7.5 Development Milestone Plan

A phased development plan is proposed to manage complexity and deliver value incrementally. This approach allows for early validation of core components and reduces overall project risk.

Table 7.1: Re-implementation Milestone Schedule

| Phase | Milestone                   | Key Tasks                                                                                                                                                                                                                      | Estimated Duration |
| ----- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------ |
| 1     | Core Framework & Interfaces | Initialize project repository, CI/CD pipeline. Implement base dspy.Module classes. Define and implement the abstracted litellm-based Language Model (LM) interface and the dspy.Retrieve-based Retrieval Model (RM) interface. | 2 Weeks            |
| 2     | STORM-Wiki Parity           | Clean-room re-implementation of the four core STORM-Wiki pipeline modules: Knowledge Curation (with perspective generation and simulated conversation), Outline Generation, Article Generation, and Article Polishing.         | 4 Weeks            |
| 3     | Basic Retrieval & Grounding | Implement RMs for key web search engines (e.g., Bing, Google). Implement the VectorRM using Qdrant, including the document ingestion and embedding pipeline.                                                                   | 3 Weeks            |
| 4     | Co-STORM Engine             | Clean-room re-implementation of the Co-STORM components: DiscourseManager, Expert and Moderator agents, and the dynamic Mind Map data structure and its update logic.                                                          | 5 Weeks            |
| 5     | API & Open-Core Shell       | Develop the FastAPI server, including endpoints for user authentication, job submission (via Celery), status polling, and results retrieval. Implement basic database schemas in PostgreSQL.                                   | 4 Weeks            |
| 6     | Validation & Beta Release   | Conduct full functional parity testing against the original STORM using the FreshWiki benchmark. Perform performance and cost benchmarking. Deploy the complete system to a closed beta environment for user feedback.         | 2 Weeks            |

Export to Sheets

# 8.0 Security & Compliance Assessment

# 8.1 Dependency Vulnerability Scan

The software supply chain is a critical vector for security vulnerabilities. The re-implementation project must incorporate automated dependency scanning from its inception. The dependency manifest detailed in Appendix 10.1 will serve as the initial baseline for this scan.

A process will be established within the CI/CD pipeline (as described in Section 7.4) to run a vulnerability scanner like safety or a commercial tool like Snyk against the project's

requirements.txt file on every build. This tool checks installed packages against a continuously updated database of known Common Vulnerabilities and Exposures (CVEs). Any build that introduces a dependency with a high-severity vulnerability will be automatically failed, preventing vulnerable code from being merged into the main branch. A policy for reviewing and addressing medium and low-severity vulnerabilities will also be established.

# 8.2 API Key and Secrets Management

The original system's use of a secrets.toml file is adequate for single-user, local development but is fundamentally insecure for a production, multi-tenant application. Committing secrets directly to version control, even in a private repository, is a major security risk.

The re-implementation will adopt a robust secrets management strategy. All sensitive information, including API keys for LLMs and search engines, database credentials, and cryptographic keys, will be managed through a dedicated secrets management service. Recommended solutions include:

HashiCorp Vault

AWS Secrets Manager

Google Cloud Secret Manager

Azure Key Vault

These services provide centralized, encrypted storage for secrets, with fine-grained access control and audit logging. In the deployment pipeline, applications will be granted temporary, role-based access to fetch the secrets they need at runtime, rather than having them stored in configuration files or environment variables within the repository.

# 8.3 License Compliance Audit

Ensuring compliance with the licenses of all included software is paramount to avoiding legal risk and protecting the project's intellectual property. A compliance checklist must be followed throughout the development process.

Upstream Attribution (MIT): The re-implementation is based on the functional design of the stanford-oval/storm project. To comply with the original MIT license, a clear attribution must be included in the derivative work. This should take the form of an "Acknowledgements" or "Notices" section in the documentation and, if applicable, a NOTICE file in the distributed software, stating that the work is based on the original Stanford project and including its copyright notice and a copy of the MIT license text.

Apache 2.0 Compliance: For all dependencies licensed under Apache 2.0 (e.g., dspy-ai, sentence-transformers), the following steps must be taken:

Preserve any NOTICE files that are distributed with the original packages. The build process must be configured to aggregate these NOTICE files and include them in the final distribution of the re-implemented software.

If any Apache-licensed source code is directly modified (which should be avoided under the clean-room model but may occur if a dependency is forked), a prominent statement of the changes made must be included.

Copyleft License Avoidance: The most critical compliance risk for an open-core model is the accidental introduction of a "copyleft" license, such as the GNU General Public License (GPL) or Affero General Public License (AGPL). These licenses would require the entire derivative work, including the proprietary "core," to be released under the same open-source terms. The dependency analysis must be rigorous in identifying not only direct dependencies but also transitive dependencies to ensure no copyleft-licensed code is linked into the final product. Automated license compliance tools should be integrated into the CI pipeline to scan for and flag any non-permissive licenses.

# 9.0 Validation/Test Plan

A comprehensive validation and testing plan is essential to ensure the re-implemented system is correct, robust, and functionally equivalent to the original. The plan encompasses unit, integration, functional, and performance testing.

# 9.1 Unit and Integration Tests

A Test-Driven Development (TDD) methodology is strongly recommended.

Unit Tests: Each re-implemented component, particularly the dspy.Module subclasses, will have a corresponding suite of unit tests written using the pytest framework. These tests will isolate the component and mock its external dependencies (e.g., LLM API calls, database connections). For example, a unit test for the ArticleGenerator module would provide it with a mock outline and a mock knowledge base and assert that it calls the LLM with the correctly formatted prompt.

Integration Tests: These tests will validate the interactions between components. For example, an integration test for the STORM-Wiki pipeline would execute the entire chain of modules (PerspectiveGenerator -> ConversationalAgent -> OutlineGenerator) to ensure that the output of one module is correctly consumed as the input to the next. These tests will run against live, containerized instances of dependencies like Qdrant and PostgreSQL.

# 9.2 Functional Parity Testing

The ultimate measure of success for this re-implementation is achieving functional parity with the original stanford-oval/storm system. The original research provides an ideal and objective benchmark for this purpose: the FreshWiki dataset.

The process for parity testing is as follows:

Benchmark Selection: Select a representative subset of topics from the FreshWiki dataset. This dataset was specifically curated by the original authors to evaluate STORM's performance on recent topics, avoiding data leakage from the LLMs' training sets.

Baseline Generation: Run the selected topics through the original stanford-oval/storm system using a fixed configuration (e.g., a specific LLM like GPT-4o, a specific retriever like Bing Search, and fixed hyperparameters). The generated outlines and final articles will be stored as the "baseline" or "ground truth" output.

Re-implementation Run: Run the same set of topics through the re-implemented system using the exact same configuration.

Comparison and Measurement: Compare the outputs from the re-implemented system against the baseline. This comparison will be both automated and manual:

Automated Metrics: Use standard NLP metrics like ROUGE and BLEU to measure the textual similarity of the generated articles. For outlines, measure structural similarity (e.g., tree edit distance) and concept overlap.

Manual Evaluation: A human evaluator will review the outputs side-by-side, assessing them against the quality criteria used in the original paper: breadth of coverage, organization, and coherence.

The re-implementation will be considered to have achieved functional parity when the automated metrics are within a small margin of error and the manual evaluation finds no significant degradation in quality compared to the baseline.

# 9.3 Performance Benchmarking

A suite of benchmarks will be created to measure the non-functional aspects of the system. These tests will be run regularly to track performance regressions or improvements. Key Performance Indicators (KPIs) include:

Latency: The end-to-end time required to generate a full report for a topic of a given complexity. This will be measured for both STORM-Wiki and Co-STORM modes.

Throughput: For the open-core web application, the number of concurrent generation jobs the system can handle.

Cost: The total cost of third-party API calls (primarily LLM tokens) required to generate a single report. This is a critical business metric.

Resource Utilization: CPU, memory, and GPU (if applicable) usage during a generation task.

# 9.4 Fuzz Testing

The agentic conversation loops, particularly the DiscourseManager in Co-STORM, represent complex state machines with many possible inputs and transitions. To ensure their robustness, fuzz testing will be employed. A fuzzing harness will be developed to programmatically send a large volume of random, unexpected, or malformed inputs to the system's interfaces, especially the user_utterance input in Co-STORM. The goal is to uncover edge cases, unhandled exceptions, or logical flaws in the state management that could lead to crashes or infinite loops. This proactive testing of the system's resilience is crucial for building a reliable production service.

# 10.0 Appendices

# 10.1 Dependency and License Manifest

This table provides a comprehensive, resolved list of direct and key transitive dependencies for the knowledge-storm package and their corresponding licenses. This manifest is critical for ongoing security and compliance audits.

PackageVersionLicenseDependency Type
knowledge-storm1.1.0MIT(Project)
dspy-ai2.4.9Apache-2.0Direct
litellm1.59.3MITDirect
sentence-transformers2.7.0Apache-2.0Direct
qdrant-client1.9.0Apache-2.0Direct
langchain-qdrant0.1.1MITDirect
trafilatura1.9.0Apache-2.0Direct
wikipedia1.4.0MITDirect
numpy1.26.4BSD-3-ClauseDirect
diskcache5.6.3Apache-2.0Direct
toml0.10.2MITDirect
langchain-text-splitters0.2.0MITDirect
langchain-huggingface0.0.3MITDirect
openai1.23.6Apache-2.0Transitive (via dspy-ai)
requests2.31.0Apache-2.0Transitive (via dspy-ai, etc.)
torch2.2.2BSD-3-ClauseTransitive (via sentence-transformers)
transformers4.40.1Apache-2.0Transitive (via sentence-transformers)
huggingface-hub0.22.2Apache-2.0Transitive (via transformers)
langchain-core0.2.1MITTransitive (via langchain-\*)
urllib31.26.18MITTransitive (via requests)
pydantic2.7.1MITTransitive (via qdrant-client, etc.)

Export to Sheets
(Note: This is a representative subset. The full, automatically generated manifest for the re-implementation should be maintained in the project repository.)

# 10.2 Key Algorithm Pseudocode

This appendix contains the complete, language-agnostic pseudocode for the core algorithms, serving as the clean-room specification for developers.

# 10.2.1 Full STORM-Wiki Pipeline Algorithm

```pseudo
FUNCTION run_storm_wiki_pipeline(topic, user_goal):
  // Phase 1: Knowledge Curation via Simulated Conversation
  print("Phase 1: Generating perspectives...")
  perspectives = generate_perspectives(topic) // From 7.3.1

  conversation_history = {}
  retrieved_documents = new Set()

  FOR each p IN perspectives:
    print("Simulating conversation for perspective: {p}...")
    single_conversation =
    FOR turn from 1 to MAX_TURNS:
      // Writer asks a question
      writer_prompt = format_writer_prompt(topic, p, single_conversation)
      question = LLM.call(writer_prompt)

      // Expert answers the question
      search_queries = generate_search_queries(question)
      sources = SearchAPI.search_and_filter(search_queries)
      retrieved_documents.add(sources)

      expert_prompt = format_expert_prompt(question, sources)
      answer = LLM.call(expert_prompt)

      single_conversation.append({ "question": question, "answer": answer })
    conversation_history[p] = single_conversation

  // Phase 2: Outline Generation
  print("Phase 2: Generating outline...")
  initial_outline_prompt = format_prompt("Generate a draft outline for: {topic}")
  draft_outline = LLM.call(initial_outline_prompt)

  refine_outline_prompt = format_prompt("Refine this outline:\n{draft_outline}\n\nUsing this research:\n{conversation_history}")
  final_outline = LLM.call(refine_outline_prompt)

  // Phase 3: Article Generation
  print("Phase 3: Generating article...")
  full_article_text = ""
  outline_sections = parse_outline(final_outline)

  FOR each section IN outline_sections:
    relevant_docs = find_relevant_docs(section.title, retrieved_documents)
    section_prompt = format_prompt("Write the '{section.title}' section of an article on {topic}, using these sources:\n{relevant_docs}")
    section_content = LLM.call(section_prompt)
    full_article_text += "\n## " + section.title + "\n" + section_content

  // Phase 4: Article Polishing
  print("Phase 4: Polishing article...")
  polish_prompt = format_prompt("Add a lead summary and remove redundancies from this article:\n{full_article_text}")
  polished_article = LLM.call(polish_prompt)

  RETURN polished_article
```

# 10.3 Extracted Prompt Templates

This is a collection of key prompt templates that define the behavior of the LLM agents. They are presented here in a generalized format.

# 10.3.1 Perspective Generation Prompt

```
You are an expert Wikipedia editor. You are tasked with brainstorming perspectives for a new article on the topic: "{topic}".
Based on the tables of contents from related articles provided below, identify 5 diverse and comprehensive perspectives. A perspective should be a short phrase describing a specific focus or angle for research.


{all_tocs}

[Perspectives]
1.
2.
3.
4.
5.
```

# 10.3.2 Conversational Writer (Question Asker) Prompt

```
You are an experienced Wikipedia writer with a specific focus when researching the topic. Your goal is to ask good questions to an expert to gather useful information for your article.
Only ask one question at a time. Do not repeat questions from the conversation history.

Topic you want to write about: {topic}
Your specific perspective: {perspective}

[Conversation History]
{conversation_history}
```

# 10.3.3 Grounded Expert (Answer Generator) Prompt

```
You are a topic expert. Answer the user's question based *only* on the provided search results. Synthesize the information into a coherent answer. Make sure every sentence is supported by the gathered information. Cite the sources using the format.

[Question]
{question}


{search_results_with_ids}
```

# 10.3.4 Co-STORM Moderator Prompt

```
You are a moderator for a discussion about the topic: "{topic}". Your role is to keep the conversation engaging and comprehensive.
The following information has been retrieved from a search but has not yet been discussed by the experts.
Based on this new information, ask one thought-provoking question to the group to steer the conversation in a new, productive direction.

[Undiscussed Information]
{unexplored_info}

[Moderator's Question]
```

# 10.4 Glossary of Terms

Co-STORM: Collaborative STORM. An extension of the STORM system that introduces a human-in-the-loop, multi-agent collaborative discourse protocol for interactive knowledge discovery.

DMCA: Digital Millennium Copyright Act. A US copyright law that, among other things, provides a legal safe harbor (§1201(f)) for reverse engineering for the purpose of interoperability.

dspy: A programming framework from Stanford that allows developers to build complex systems using language models in a structured, declarative, and modular way.

Knowledge Base: The collection of data gathered during the STORM-Wiki research phase, typically including conversation transcripts and retrieved web documents.

litellm: A Python library that provides a unified, standardized interface for interacting with over 100 different LLM APIs.

Mind Map: A hierarchical, tree-like data structure used in Co-STORM to dynamically organize information uncovered during the collaborative discourse, reducing cognitive load for the user.

Module (dspy.Module): A fundamental building block in dspy. A Python class that encapsulates a specific LLM-powered task, such as generating a question or summarizing text.

RAG (Retrieval-Augmented Generation): A common AI technique where an LLM's knowledge is augmented by retrieving relevant information from an external source (like a vector database) before generating a response.

Signature (dspy.Signature): A dspy component that defines the input and output schema for a Module. It tells the LLM what fields to expect as input and what fields to produce as output.

STORM: Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking. The core system that automates the generation of Wikipedia-style articles.

VectorRM: A specific Retrieval Module in STORM that uses a vector database (Qdrant) to retrieve information from a user-provided document corpus.

Sources used in the report

- Section 1201: Technology Protection Measures - Copyright Alliance (copyrightalliance.org)
- Digging Deeper: Reverse Engineering & Infringement Laws |TTC - TT Consultants (ttconsultants.com)
- 17 U.S. Code § 1201 - Circumvention of copyright protection systems - Law.Cornell.Edu (law.cornell.edu)
- STORM: Stanford's Revolutionary Research Tool Harnessing the Power of Agents and Agentic Workflows | by Lakshmi narayana .U | Stackademic (blog.stackademic.com)
- The Do's and Don'ts of Reverse Engineering: Guidelines for Ethical Competition and Reducing Legal Risk (faheyiplaw.com)
- Open Source Licenses 101: Apache License 2.0 | FOSSA Blog (fossa.com)
- Apache License 2.0 Explained | Apache 2.0 Uses, Benefits & Requirements - Snyk (snyk.io)
- Apache License - Wikipedia (en.wikipedia.org)
- Apache License 2.0 - Memgraph (memgraph.com)
- The Dispatch Report: GitHub Repo Analysis: stanford-oval/storm (thedispatch.ai)
- The Dispatch Report: GitHub Repo Analysis: stanford-oval/storm (thedispatch.ai)
- storm/examples/storm_examples/README.md at main · stanford-oval/storm - GitHub (github.com)
- Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models - ACL Anthology (aclanthology.org)
- Technical Analysis of Stanford OVAL STORM Framework - bolespot (bolespot.com)
- arXiv:2402.14207v2 [cs.CL] 8 Apr 2024 (arxiv.org)
- Stanford AI experiment "STORM" generates Wikipedia-style articles - The Decoder (the-decoder.com)
- Stanford STORM Explained: AI That Writes and Curates Smarter | by Teendifferent - Medium (medium.com)
- Top GitHub Projects of Jan 2025 - OpenCV (opencv.org)
- Code Explanation: "STORM: Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking" - DEV Community (dev.to)
- knowledge-storm - PyDigger (pydigger.com)
- | Stanford STORM Research Project (storm-project.stanford.edu)
- Assisting in Writing Wikipedia-like Articles From Scratch with Large ... (arxiv.org)
- knowledge-storm - PyPI (pypi.org)
- How To Check For Python Dependencies With Package Managers - ActiveState (activestate.com)
- knowledge-storm - PyPI (pypi.org)
- Dependency check for Python - ThoughtWorks Security Guide (securityguide.github.io)
- knowledge-storm | PyPI - Open Source Insights (deps.dev)
- How to find a Python package's dependencies - Stack Overflow (stackoverflow.com)
- Releases · stanford-oval/storm - GitHub (github.com)
- arxiv.org (arxiv.org)
- stanford-oval/storm: An LLM-powered knowledge curation ... - GitHub (github.com)
- storm/requirements.txt at main · stanford-oval/storm · GitHub (github.com)
- Into the Unknown Unknowns: Engaged Human ... - ACL Anthology (aclanthology.org)

Sources read but not used in the report

- Stanford STORM: Revolutionizing AI-Powered Knowledge Curation | by Cogni Down Under (medium.com)
- 3 Interoperability under the DMCA - MIT Press Direct (direct.mit.edu)
- STORM: Teaching With The Stanford-Designed AI System | Tech & Learning (techlearning.com)
- What is Section 1201 Digital Millennium Copyright Act?: A Legislative Primer - Institute for Intellectual Property and Social Justice (iipsj.org)
- Apache License 2.0 (Apache-2.0) Explained in Plain English - TLDRLegal (tldrlegal.com)
- stanford-oval/storm: An LLM-powered knowledge curation system that researches a topic and generates a full-length r... | Are.na (are.na)
  Stanford DSPy - Qdrant
- Stanford DSPy - Qdrant (qdrant.tech)
- Using DSPy to Enhance Prompt Engineering with OpenAI APIs - DEV Community (dev.to)
- dspy/docs/docs/learn/programming/overview.md at main · stanfordnlp/dspy - GitHub (github.com)
- Tutorials Overview - DSPy (dspy.ai)
- dspy/docs/docs/learn/programming/overview.md at main · stanfordnlp/dspy - GitHub (github.com)
- Tutorial: Retrieval-Augmented Generation (RAG) - DSPy (dspy.ai)
- DSPy Tutorial | IBM (ibm.com)
- Build generative AI apps using DSPy on Databricks (docs.databricks.com)
- Easiest Tutorial to Learn DSPy with LLM Example - YouTube (youtube.com)
- What Is DSPy? How It Works, Use Cases, and Resources - DataCamp (datacamp.com)
- Activity · stanford-oval/storm - GitHub (github.com)
- stanford-oval/storm: STORM: Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking. - GitHub repo explorer (githubtree.mgks.dev)
- Pull requests · stanford-oval/storm - GitHub (github.com)
- Issues · stanford-oval/storm - GitHub (github.com)
- DSPy (dspy.ai)
- Stanford University's STORM - Brajeshwar (brajeshwar.com)
- Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models - ACL Anthology (aclanthology.org)
- STORM: A Stanford University AI Writing System - Wally Boston (wallyboston.com)
- STORM: Stanford's AI Revolution in Research and Content Creation | JamiiForums (jamiiforums.com)
- STORM by Stanford University: The AI Model for Academic and Research Purposes (blog.acer.com)
- STORM: An AI-Powered Writing System for the Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking - MarkTechPost (marktechpost.com)
- Running Stanford OVAL's STORM Mistral demo with DSPy - DigitalOcean (digitalocean.com)
- Stanford OVAL — Home (oval.cs.stanford.edu)
- Co-STORM · assafelovic gpt-researcher · Discussion #816 - GitHub (github.com)
- STORM - Stanford University (storm.genie.stanford.edu)
- Co-Storm: FREE AI TOOL by STANFORD can convert TOPICS to LONG ARTICLES! (youtube.com)
- Why PyPI Doesn't Know Your Projects Dependencies - Dustin Ingram (dustingram.com)
- Yijia Shao - ACL Anthology (aclanthology.org)
- Findings - EMNLP 2024 (2024.emnlp.org)
- Python - Checking Package Dependencies! - YouTube (youtube.com)
- Into the Unknown Unknowns: Engaged Human Learning through Participation in Language Model Agent Conversations - ACL Anthology (aclanthology.org)
- Into the Unknown Unknowns: Engaged Human Learning through Participation in Language Model Agent Conversations | AI Research Paper Details - AIModels.fyi (aimodels.fyi)
- tweag/FawltyDeps: Python dependency checker - GitHub (github.com)
- Into the Unknown Unknowns: Engaged Human Learning through Participation in Language Model Agent Conversations - ResearchGate (researchgate.net)
- Announcing FawltyDeps - a dependency checker for your Python code - Tweag (tweag.io)
- Running the STORM AI research system with your local documents - Towards Data Science (towardsdatascience.com)
- Into the Unknown Unknowns: Engaged Human Learning through Participation in Language Model Agent Conversations - Semantic Scholar (semanticscholar.org)
- Into the Unknown Unknowns: Engaged Human Learning through (zhuanzhi.ai)
- Python Dependencies Management: pip show, pip tree, pip list etc. - Inedo Blog (blog.inedo.com)
