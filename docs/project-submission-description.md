
# LexFabric Agents – A Multi-Agent System for Evidence & Timeline Reasoning

**Track:** Freestyle  
**All evidence used in this project is synthetic.**

LexFabric Agents is a deterministic multi-agent reasoning system that transforms fragmented evidence into a structured chronological timeline and answers natural-language questions strictly grounded in that evidence. The project addresses a major bottleneck in analytical domains such as law, compliance, audits, and investigations, where information is scattered across emails, notes, logs, and filings, often described with inconsistent or incomplete timestamps. Analysts must reconstruct what happened and when it happened—something traditional monolithic LLMs fail at because they struggle with ordering, reconciliation, and provenance.

This project demonstrates how a carefully engineered multi-agent architecture can perform these tasks with reproducibility, transparency, and zero hallucination. The system runs entirely offline, uses only synthetic data, and mirrors workflows used by legal analysts and forensic investigators.



## 1. Problem Context

Real-world evidence is rarely chronological. Key events may be buried in side notes, logs may use relative time expressions (“later that morning”), and different authors may use different labels for the same person. Manual reconstruction is slow and error-prone. LLMs, when asked to synthesize multiple documents, often hallucinate missing details or produce inconsistent timelines. LexFabric Agents replaces this with a deterministic pipeline optimized for safety and clarity.



## 2. Architecture Overview

The system consists of five components orchestrated through a Router:

### 2.1. Evidence Agent
- Retrieves evidence files from the Synthetic Evidence Server via deterministic functions (`list_evidence()`, `get_evidence_text()`, `list_cases()`, `select_case()`, `get_evidence_hashes()`).
- Records each file’s SHA-256 fingerprint to guarantee integrity and reproducibility.

### 2.2. Timeline Agent
Extracts events, actors, and timestamps.  
Date handling combines:

- deterministic parsing for explicit dates  
- controlled, normalization-only LLM assistance for relative expressions (“the next morning”, “two days later”)

The LLM never infers or invents facts—it converts relative expressions into explicit timestamps based on known context. All downstream ordering uses deterministic Python sorting.

### 2.3. Memory Bank
- Stores normalized entities, event fragments, summaries, timestamps, and provenance.
- Includes lightweight **Entity Resolution** to unify synonyms and references (e.g., “Bob,” “Robert,” “Mr. Smith”).
- Ensures narrative coherence and avoids fragmentation during retrieval.

### 2.4. Q&A Agent
- Performs evidence-bounded reasoning by searching the Memory Bank and walking the unified timeline.
- Every answer includes provenance citations with filenames and SHA-256 hashes.
- If a question cannot be answered strictly from evidence, it returns a safe fallback rather than guessing.
- Enforces true zero-hallucination behavior.

### 2.5. Router
- Determines the sequence of agent calls required to satisfy the user’s intent.
- Avoids redundant execution by reusing cached results when possible.
- Reflects real investigative toolchains.



## 3. Synthetic Evidence Server

Located under `capstone/synthetic_evidence/`, it provides deterministic case files through a simple MCP-style interface. Running entirely offline, it ensures:

- reproducible evaluation  
- controlled evidence access  
- no API drift  
- safe experimentation for judges  

This isolates the pipeline from environmental variability. The system performs no network calls and uses no external APIs, ensuring fully offline and reproducible operation.




## 4. Execution & Reproducibility
The system is demonstrated using two synthetic cases included in the repository: CC02 and RH10.

Run the system with:

```bash
export PYTHONPATH="$PWD/src"
python -m capstone.demo --root capstone/synthetic_evidence --case-id CC02
```

This command:

* loads evidence through the Evidence Agent
* extracts documents into structured fragments
* normalizes timestamps
* builds the ordered timeline
* initializes the Memory Bank
* performs grounded Q&A with source citations

Because the pipeline uses hashing, deterministic sorting, and constrained LLM behavior, repeated runs always produce identical results.



## 5. CLI Experience

The `capstone.demo` entrypoint reflects real workflows used by legal and investigative analysts. It produces:

* full evidence manifests
* extracted events
* a unified chronological timeline
* grounded Q&A results with SHA-256 provenance

The CLI avoids unnecessary complexity while enabling judges to reproduce the results with a single command.



## 6. Determinism, Safety, and Integrity

The system enforces strict guarantees:

### **6.1. Zero hallucination**

The Q&A Agent refuses to answer beyond the available evidence.

### **6.2. Chain of custody**

Every file is hashed using SHA-256; every Q&A answer includes citations.

### **6.3. Deterministic timeline ordering**

No randomness or probabilistic sampling is used.

### **6.4. Controlled LLM boundary**

LLMs are used only for extraction and date normalization—never reasoning.

### **6.5.Offline execution**

No API variability or external model dependencies.

These constraints align with high-stakes domains where reliability is critical.



## 7. Reasoning Capabilities

The system was evaluated using a synthetic suite of realistic tasks:

### **7.1. Contradiction Detection**

Identifies conflicting claims (e.g., email vs. filing) and cites evidence.

### **7.2. Causal Reconstruction**

Builds multistep causal chains strictly from extracted timestamps.

### **7.3. Gap Detection**

Highlights missing periods, incomplete metadata, or absent document categories.

These tasks demonstrate robust multi-document reasoning that monolithic LLMs routinely mishandle.



## 8. Why This Architecture Works

LexFabric Agents succeeds because it respects the strengths and limits of LLMs:

* LLMs extract information well → extraction is LLM-assisted.
* Ordering, provenance, and reasoning require determinism → handled programmatically.
* Entity resolution preserves narrative coherence.
* Provenance is mandatory for every answer.
* The Router enforces predictable behavior.

The architecture reflects real-world constraints in legal engineering and achieves system-level rigor beyond typical prompt engineering.



## 9. Extensibility

Future enhancements may include:

* semantic embedding retrieval
* automated causality graphing
* cross-docket or cross-case timeline fusion
* deeper entity resolution
* role-based timeline segmentation
* integrated explainability reports

The modular multi-agent design makes these upgrades natural extensions.



## 10. Conclusion

LexFabric Agents demonstrates how a deterministic, evidence-bounded multi-agent architecture can solve complex cross-document reasoning tasks that monolithic LLMs routinely mishandle. By combining the Evidence Agent, Timeline Agent, Q&A Agent, Memory Bank with entity resolution, Router orchestration, and a deterministic Synthetic Evidence Server, the system produces structured, explainable, citation-backed knowledge without hallucination and without external dependencies. It offers a reproducible, high-integrity analytical workflow suitable for professional and high-stakes environments, making it a strong submission for the Google AI Agents Intensive Capstone.



