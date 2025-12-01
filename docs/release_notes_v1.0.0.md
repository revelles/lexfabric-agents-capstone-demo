# Release Notes — v1.0.0  
LexFabric Agents – Capstone Demo  
Released: 2025-11-29

This is the first public release of the multi-agent evidence and timeline analysis system built for the Google AI Agents Intensive (Nov 2025). It demonstrates how agentic workflows can ingest synthetic legal evidence, build chronological timelines, and answer questions through a structured memory system.



## 🚀 Key Features

### Multi-Agent Architecture
- **Evidence Agent** – loads evidence records and raw text.
- **Timeline Agent** – extracts events and dates, then builds an ordered timeline.
- **Q&A Agent** – answers questions grounded in memory + timeline.
- **Memory Bank** – holds normalized fragments (entities, summaries, events).
- **Router** – orchestrates which agent runs based on the CLI mode.


### Synthetic Evidence Server (MCP)
Provides:
- `list_evidence`
- `get_evidence_text`
- `list_cases`
- `select_case`
- `get_evidence_hashes`

Supports clean tool-driven workflows and reproducible testing.

### Evidence Hashing
- Full SHA-256 hashing pipeline  
- Manifest generator (`hash_all`)  
- Deterministic runs for reproducibility  

### CLI Demo
Use:
```bash
python -m capstone.demo --mode list-evidence --case-id CC02
python -m capstone.demo --mode list-timeline --case-id CC02
python -m capstone.demo --mode ask --query "What happened after the email?"
```

## Visuals Update – 1.0.1 (2025-12-01)

- Added `assets/lexfabric-demo-split-screen.png`, a split-screen visual showing fragmented evidence on the left and the ordered LexFabric timeline on the right.
- Updated README, Kaggle writeup, and whitepaper to reference this visual and clarify the before/after impact of the multi-agent pipeline.
