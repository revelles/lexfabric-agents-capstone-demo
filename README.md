# LexFabric Agents – Capstone Demo (Google AI Agents Intensive 2025)

## 🚀 Overview

This project is a **multi-agent evidence and timeline reasoning system** demonstrating:

* Evidence ingestion (synthetic only)
* Entity/date extraction
* Timeline construction
* Natural-language Q&A
* Reproducible hashing
* Offline CLI demo

All evidence is **fully synthetic**.

## Visual Summary: From Fragmented Evidence to Ordered Chronology
![LexFabric Split-Screen Demo](/assets/lexfabric-demo-split-screen.png)
*Figure 1: Traditional manual review vs. LexFabric's multi-agent chronological reconstruction.*

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
6. A lightweight **Router** coordinates which agent runs when, based on the CLI mode
   (`list-evidence`, `list-timeline`, `ask`).

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
    <strong>Figure 4 — Timeline Reasoning:</strong>
    Diagram showing how raw evidence is converted into normalized events and an ordered timeline, which is then queried by the Q&A Agent.
  </figcaption>
</figure>

### Agents

- **Evidence Agent** – loads evidence records and raw text from the synthetic evidence server.
- **Timeline Agent** – extracts events and dates, then builds an ordered timeline.
- **Q&A Agent** – answers natural-language questions by combining memory + timeline lookups.
- **Memory Bank** – holds normalized fragments (entities, summaries, events) for retrieval.
- **Router** – orchestrates which agent runs based on CLI mode and user query.

### Synthetic Evidence Server

Located under `capstone/synthetic_evidence/`, it supports:

- `list_evidence()`
- `get_evidence_text()`
- `list_cases()`
- `select_case()`
- `get_evidence_hashes()`

## 📁 Repository Layout

```
CHANGELOG.md
LICENSE
README.md
assets/
capstone/synthetic_evidence/
docs/
scripts/
src/capstone/
```

## 💻 CLI Usage

From the repository root:

### Run the demo for a case

```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/src"

python -m capstone.demo \
  --root capstone/synthetic_evidence \
  --case-id CC02
```


### Ask a custom question

```bash
PYTHONPATH="$PWD/src" python -m capstone.demo \
  --root capstone/synthetic_evidence \
  --case-id CC02 \
  --ask "What happened first?"
```

### Run a different synthetic case

```bash
PYTHONPATH="$PWD/src" python -m capstone.demo \
  --root capstone/synthetic_evidence \
  --case-id RH10 \
  --ask "Give me a brief overview of this case."
```


## 🔐 Hashing

```bash
python scripts/generate_manifest.py
```

Ensures reproducibility and integrity.

## 🛡️ Safety & Anti‑Hallucination Design

* Evidence‑bound reasoning
* Deterministic SHA‑256 pipeline
* Offline execution
* Narrow agent roles
* Query‑time guardrails
* Synthetic data only

## 📦 Installation

```bash
git clone https://github.com/revelles/lexfabric-agents-capstone-demo.git
cd lexfabric-agents-capstone-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./setup.sh
```

## 📄 License

MIT License.

## 🏁 Status

Capstone submission build:

* Multi-agent pipeline
* Synthetic evidence server
* CLI demo
* Hashing
* CC02 & RH10 cases
* Diagrams & writeups

Private LexFabric MDLS will extend this foundation with secure multi-docket reasoning.
