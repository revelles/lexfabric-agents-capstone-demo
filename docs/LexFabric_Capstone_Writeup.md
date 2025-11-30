# LexFabric Agents – Capstone Writeup

Google AI Agents Intensive (Nov 2025)

## 1. Introduction

Complex analytical domains—such as legal, compliance, security, and operations—depend on timelines assembled from dozens or hundreds of scattered artifacts: emails, notes, PDFs, filings, logs, screenshots, and metadata. Reconstructing these narratives is tedious and error-prone for humans.

This project demonstrates a **multi-agent evidence analysis pipeline** designed specifically to:

- read synthetic case files
- normalize and analyze evidence
- extract key entities and dates
- build a unified chronological timeline
- answer natural-language questions grounded in the timeline

The system is intentionally **synthetic and offline** for the Capstone, while the private LexFabric MDLS integrates similar architecture for real litigation workflows.

---

## 2. Problem Definition

The central challenge: **How can we build agents that transform disorderly evidence into structured knowledge suitable for reasoning?**

Traditional GPT-style models can summarize single documents, but multi-step reasoning requires:

- structured memory
- deterministic ingestion
- merging of partial records
- provenance and integrity
- multi-agent decomposition
- reproducibility across sessions

Legal workflows are a prime example: a filing on March 2 may reference an email from January 26, which contradicts a note written by someone else. Humans perform these joins manually; agents must do it systematically.

---

## 3. System Overview

The solution is a **three-part system**:

### 3.1 Synthetic Evidence Server (MCP)

A minimal, tool-enabled backend providing:

- `list_evidence`
- `get_evidence_text`
- `list_cases`
- `select_case`
- `get_evidence_hashes`

This creates a stable, reproducible environment for agentic workflows.

---

### 3.2 Multi-Agent Pipeline

Four agents collaborate:

1. **Ingest Agent** – reads evidence, fetches content, tags files.
2. **Analysis Agent** – extracts dates, actors, events, relationships.
3. **Timeline Agent** – merges fragments into a complete chronological sequence.
4. **Q&A Agent** – answers natural-language queries using:
   - the timeline  
   - a semantic memory bank of chunks

---

### 3.3 CLI Interface

A lightweight command-line tool to:

- list evidence  
- show timelines  
- submit natural-language questions  

---

## 4. Evidence Normalization & Hashing

Every ingestion pass produces a **SHA-256 manifest** for all evidence files. This ensures:

- determinism  
- chain-of-custody  
- reproducibility  
- safe incremental updates  

This mirrors real-world legal tech requirements.

---

## 5. Synthetic Case Data

The project ships with **multiple synthetic cases** (CC02 → RH10).  
Each contains:

- emails  
- filings  
- notes  
- at least one timeline fragment  

The variation across cases demonstrates that the system generalizes beyond a single template.

---

## 6. Multi-Agent Pipeline Details

### 6.1 Ingest Agent

- Calls MCP server  
- Loads file contents  
- Parses filenames & categories  
- Produces structured evidence metadata  

### 6.2 Analysis Agent

Extracts:

- dates (explicit, implicit, or natural language)  
- actors and roles  
- event summaries  
- causal references  

Outputs structured entries for the semantic memory bank.

### 6.3 Timeline Agent

- Sorts by timestamp  
- Fills missing fields when inferable  
- Marks uncertainty when not  
- Outputs canonical ordered timeline  

### 6.4 Q&A Agent

- Semantic search across memory  
- Interval search across timeline  
- Combined synthesis for grounded, explainable answers  

---

## 7. CLI Demo

Three modes:

### `list-evidence`

Shows files and categories.

### `list-timeline`

Displays the ordered timeline.

### `ask`

Answers grounded questions.

---

## 7.1 Example Queries for `--ask` Mode

### 1. Timeline Reconstruction

**Query:**  
“What is the earliest event in this case, and which evidence file mentions it?”

- Consults merged timeline  
- Returns earliest event + file mapping  
- Includes provenance  

### 2. Cross-Document Contradiction Detection

**Query:**  
“Do any emails contradict the initial filing? Summarize discrepancies.”

- Cross-checks memory + timeline  
- Highlights mismatched dates or claims  

### 3. Actor-Centric Narrative

**Query:**  
“What actions did the claimant take between the first email and the filing?”

- Timeline window search  
- Summarizes claimant activity  
- Links to evidence IDs  

### 4. Missing Information Audit

**Query:**  
“Which timeline entries have incomplete dates or uncertain ordering?”

- Flags uncertainty  
- Reports missing/ambiguous fields  

### 5. Causal or Procedural Reasoning

**Query:**  
“What led to the dispute escalation according to the evidence?”

- Multi-agent causal synthesis  

### 6. Summaries With Provenance

**Query:**  
“Give me a 4-sentence overview of this case grounded only in the evidence.”

- Grounded summary  
- Zero hallucination  

### 7. Day-Level Event Expansion

**Query:**  
“List everything that happened on the date of the initial filing.”

- Filters timeline  
- Includes adjacent uncertain fragments  

### 8. Entity-Focused Cross-Section

**Query:**  
“Which events involve the operations manager, and where are they mentioned?”

- Entity search  
- Evidence-linked output  

### 9. Detect Gaps & Suggest Next Steps

**Query:**  
“Which logical gaps remain after merging all evidence, and what new evidence would help close them?”

- Gap analysis  
- Evidence recommendations  

### 10. Hash-Provenance Demo

**Query:**  
“Show every timeline entry along with the hash of the file that generated it.”

- Fused timeline + hashing manifest  
- Full provenance  

---

## 7.2 Automated Q&A Harness

The repository includes a script that runs all example questions:

```bash
python scripts/test_ask_examples.py   --root capstone/synthetic_evidence   --case-id CC02
```

It exercises all reasoning patterns:

- timeline reconstruction  
- contradiction detection  
- actor-centric windowing  
- uncertainty auditing  
- causal reasoning  
- summaries with provenance  
- day-level expansion  
- entity cross-sections  
- gap detection + next-evidence suggestions  
- hash-provenance pairing  

---
