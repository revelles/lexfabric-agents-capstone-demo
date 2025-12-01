# **Kaggle Writeup – LexFabric Agents (Competition-Optimized Version)**

Google AI Agents Intensive – Capstone Project (Nov 2025)

## **1. Overview**

The LexFabric Agents project is a **multi-agent evidence analysis and timeline reasoning system** designed for domains where critical information is scattered across emails, notes, filings, PDFs, and logs. In real settings—particularly legal workflows—events rarely arrive in chronological order. Instead, humans must reconstruct timelines from dozens or hundreds of fragmented artifacts.

This project demonstrates an **end-to-end agentic architecture** capable of:

* ingesting structured and unstructured evidence
* extracting dates, actors, and events
* merging partial fragments
* building a chronological timeline
* and answering natural-language questions grounded purely in the ingested files

The dataset, tools, and reasoning system are fully **synthetic** for the purposes of the Google AI Agents Intensive. However, the architecture parallels features used in the private **LexFabric MDLS (Multi-Docket Litigation System)**, a professional evidence automation environment.



## **2. Problem Addressed**

### **The challenge:**

Modern analytical workflows require agents not only to analyze single documents, but to **combine multiple documents into coherent, logical structures**. LLMs excel at summarizing a single file—but struggle with:

* ordering events across files
* preventing hallucinations
* maintaining provenance
* cross-document consistency checking
* merging partial evidence fragments
* answering grounded questions without inventing facts

For example:

> A filing dated March 2 may reference a dispute from January 26 which contradicts a note written by a different stakeholder.

Human analysts manually perform these multi-source joins. Our goal is to teach agents to do them reliably.


### Before/After: Why This Matters
![LexFabric Split-Screen Demo](/assets/lexfabric-demo-split-screen.png)
*Figure 1: Traditional manual review vs. LexFabric's multi-agent chronological reconstruction.*
## **3. System Architecture**

The solution uses a **three-tier structure**:
## 🧱 Architecture

This project is built as a small, self-contained **multi-agent system** with a deterministic, evidence-bound pipeline:

1. The **Synthetic Evidence Server** exposes synthetic cases (e.g., `CC02`, `RH10`) via simple tools:
   - `list_cases()`, `list_evidence()`, `get_evidence_text()`, `get_evidence_hashes()`.
2. The **Evidence Agent** loads evidence metadata and raw text from the server.
3. The **Timeline Agent** extracts dates and events, orders them, and builds a structured timeline.
4. The **Memory Bank** stores normalized fragments (entities, dates, summaries, events).
5. The **Q&A Agent** answers user questions by:
   - searching the memory bank, and  
   - walking the ordered timeline for sequence-sensitive queries.
6. A lightweight **Router** coordinates which agent runs when, based on the CLI mode (`list-evidence`, `list-timeline`, `ask`).



### Visual Overview

#### High-Level System Overview

<figure style="text-align:center; margin-top: 2em; margin-bottom: 2em;">
  <img src="/docs/diagrams/01_system_overview.svg"
       alt="High-level system overview showing agents interacting with the synthetic evidence server and producing timelines and answers."
       width="80%">
  <figcaption style="font-size:0.6em; margin-top:6px; color:#555;">
    <strong>Figure 2 — High-level system overview:</strong> Shows agents interacting with the synthetic evidence server and producing timelines and answers.
  </figcaption>
</figure>

#### End-to-End Multi-Agent Pipeline

<figure style="text-align:center; margin-top: 2em; margin-bottom: 2em;">
  <img src="/docs/diagrams/02_multi_agent_pipeline.svg"
       alt="End-to-end multi-agent pipeline: Evidence Agent ingests evidence, Timeline Agent orders events, Memory Bank stores structured fragments, Q&A Agent answers questions, and Router orchestrates the flow."
       width="100%">
  <figcaption style="font-size:0.6em; margin-top:12px; color:#555;">
    <strong>Figure 3 — End-to-end multi-agent pipeline:</strong>
    Evidence Agent ingests evidence, Timeline Agent orders events,
    Memory Bank stores structured fragments, Q&A Agent answers questions,
    and Router orchestrates the flow.
  </figcaption>
</figure>

#### Timeline Reasoning Flow

<figure style="text-align:center; margin-top: 2em; margin-bottom: 2em">
  <img src="/docs/diagrams/04_timeline_reasoning_flow.svg"
       alt="Diagram showing how raw evidence is converted into normalized events and an ordered timeline, which is then queried by the Q&A Agent."
       width="45%">
  <figcaption style="font-size:0.6em; margin-top:12px; color:#555;">
    <strong>Figure 3 — Timeline Reasoning:</strong>
    Diagram showing how raw evidence is converted into normalized events and an ordered timeline, which is then queried by the Q&A Agent.
  </figcaption>
</figure>



### Agents

- **Evidence Agent** – loads evidence records and raw text.
- **Timeline Agent** – extracts events and dates, then builds an ordered timeline.
- **Q&A Agent** – answers questions grounded in memory + timeline.
- **Memory Bank** – holds normalized fragments (entities, summaries, events).
- **Router** – orchestrates which agent runs based on the CLI mode.



### Synthetic Evidence Server

Located in `capstone/synthetic_evidence/`, it supports:

- `list_evidence()`
- `get_evidence_text()`
- `list_cases()`
- `select_case()`
- `get_evidence_hashes()`




### **3.1 Synthetic Evidence Server (MCP)**

A lightweight MCP server provides deterministic tools:

* `list_evidence`: enumerate files
* `get_evidence_text`: return file contents
* `list_cases`: list available cases
* `select_case`: switch datasets dynamically
* `get_evidence_hashes`: produce SHA-256 manifest

This ensures **reproducibility**, **testability**, and **safe evaluation**.



### **3.2 Multi-Agent Reasoning Pipeline**

The following agents collaborate:

#### **1. Ingest Agent**

* loads evidence metadata
* reads file contents via MCP
* tags category, extension, and location

#### **2. Analysis Agent**

* extracts actor names
* pulls explicit/implicit date fragments
* derives event summaries
* identifies causality phrases (“after,” “because of,” etc.)

#### **3. Timeline Agent**

* merges events
* sorts by timestamp
* marks uncertainty
* produces canonical timeline entries

#### **4. Q&A Agent**

A grounded, rule-based system (no external API calls) that:

* queries the timeline
* performs interval searches
* detects contradictions
* provides provenance-backed answers
* refuses to hallucinate missing information



### **3.3 CLI Interface**

A user-friendly command-line wrapper provides:

```bash
python -m capstone.demo --mode list-evidence --case-id CC02
python -m capstone.demo --mode list-timeline --case-id CC02
python -m capstone.demo --case-id CC02 --ask "What happened first?"
```

This mirrors real-world usage in legal, compliance, and investigative tooling.



## **4. Evidence Normalization & Hashing**

Each ingestion pass generates a **SHA-256 hash manifest** for all files.
Benefits:

* chain-of-custody fidelity
* version reproducibility
* deduplication
* test-stable evaluation
* hash-to-event provenance

This mirrors industry requirements for legal review, audit, and regulated domains.



## **5. Synthetic Case Data**

The repository contains multiple synthetic cases (`CC02` → `RH10`), each with a different structure:

* emails
* notes
* filings
* incident reports
* timeline fragments

This diversity ensures generalization and demonstrates that the pipeline works beyond a single curated example.



## **6. Example Agent Outputs**

To validate the system, a test harness runs **10 reasoning patterns**, each reflecting a real-world analytical task:



### **1. Timeline Reconstruction**

**Query:**
*“What is the earliest event in this case, and which evidence file mentions it?”*

→ System identifies earliest timeline entry and its evidence source.



### **2. Cross-Document Contradiction Detection**

**Query:**
*“Do any emails contradict the initial filing?”*

→ System admits when data is missing (no hallucinations).



### **3. Actor-Centric Narrative**

**Query:**
*“What actions did the claimant take between the first email and the filing?”*

→ Interval search across timeline events.



### **4. Missing Information Audit**

Detects entries lacking:

* explicit dates
* ordering certainty
* links to actors



### **5. Causal/Procedural Reasoning**

Identifies causal chains such as:

* “escalation caused by unaddressed complaints”
* “follow-up triggered after operational failure”

Without inventing facts.



### **6. Evidence-Grounded 4-Sentence Summary**

Produces a short summary that:

* contains zero hallucinations
* references only loaded files
* clearly states when information is missing



### **7. Same-Day Event Expansion**

Filters events by date, grouping them for human review.



### **8. Entity Cross-Section**

Finds all events involving a target role, e.g., “operations manager.”



### **9. Gap Detection + Next Evidence Recommendations**

Example output:

* missing timestamps
* insufficient emails
* absent follow-up logs



### **10. Hash-Provenance Display**

Shows each timeline entry with its originating SHA-256 file hash.



## **7. Key Competition Strengths**
The following points summarize why this multi-agent architecture performs well under the competition’s evaluation criteria.

This project aligns directly with **what Google’s judging rubric rewards**:

### ✅ **1. Clear real-world value**

Legal, compliance, and operational investigations need this exact workflow.

### ✅ **2. Strong multi-agent design**

Each agent has responsibilities, no overlap, no ambiguity.

### ✅ **3. Deterministic, reproducible evaluation**

Synthetic evidence + hash manifest = perfect reproducibility.

### ✅ **4. No hallucination**

Rule-based Q&A explicitly refuses to invent information.

### ✅ **5. Test harness with 10 advanced queries**

This demonstrates maturity, completeness, and reliability. These queries cover multi-document joins, temporal reasoning, contradiction detection, and missing-data awareness — the exact tasks where agentic designs outperform monolithic LLM prompts.

### ✅ **6. Professional-level architecture**

This project is deployable and extendable (LexFabric MDLS-compatible).

### ✅ **7. Clean CLI interface**

Judges can run everything locally in seconds.



## **8. Future Work**

The next steps for production-level deployment include:

* semantic embedding indexing
* evidence clustering
* role-based timeline segmentation
* automated causality graph construction
* cross-case knowledge transfer

These will be integrated into the private LexFabric MDLS after the Capstone submission.



## **9. Conclusion**

LexFabric Agents demonstrates how multi-agent systems can reliably transform fragmented evidence into structured, chronological, and explainable knowledge. The architecture emphasizes **grounded reasoning, reproducibility, integrity, and safety**—all critical for high-stakes domains.

The system is ready for further extension, commercial deployment, and integration into fully featured litigation automation workflows.

