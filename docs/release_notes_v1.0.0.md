# Release Notes — v1.0.0  
LexFabric Agents – Capstone Demo  
Released: 2025-11-29

This is the first public release of the multi-agent evidence and timeline analysis system built for the Google AI Agents Intensive (Nov 2025). It demonstrates how agentic workflows can ingest synthetic legal evidence, build chronological timelines, and answer questions through a structured memory system.

---

## 🚀 Key Features

### Multi-Agent Architecture
- **Ingest Agent** for loading evidence and metadata  
- **Analysis Agent** for extracting actors, dates, events  
- **Timeline Agent** for merging fragments into ordered records  
- **Q&A Agent** for hybrid timeline + memory search  

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
