# ✅ **2. Polished 2m55s NotebookLM Video Script**

This script is optimized to produce a **2 minute 55 second** narrated video inside NotebookLM.

---

## **🎬 VIDEO SCRIPT — 2m55s**

**Title Card (0:00–0:05)**  
**LexFabric Agents – Multi-Agent Evidence & Timeline Reasoning System**  
Freestyle Track · Google AI Agents Intensive (2025)

---

### **Hook (0:05–0:20)**  
In legal analysis, compliance reviews, and investigations, one of the most time-consuming tasks is reconstructing what actually happened. Evidence arrives scattered across emails, notes, logs, and documents. Events are out of order, timestamps are inconsistent, and key details are buried. Analysts spend hours trying to stitch everything together.

---

### **Problem (0:20–0:40)**  
Traditional LLMs can summarize individual files, but the moment you ask them to synthesize across documents—identify contradictions, reconstruct timelines, or answer grounded questions—they hallucinate or produce inconsistent results. They’re powerful, but not built for deterministic, multi-document reasoning.

---

### **Solution Overview (0:40–1:00)**  
LexFabric Agents solves this with a fully offline, deterministic multi-agent architecture. It transforms fragmented evidence into a coherent chronological timeline and answers natural-language questions strictly based on what the evidence can prove. All data is synthetic. All reasoning is grounded. And every output is reproducible.

---

### **Agents (1:00–1:35)**  
The system is built around five specialized components.

**The Evidence Agent** loads records from the Synthetic Evidence Server, extracts raw text, and verifies each file’s SHA-256 fingerprint.

**The Timeline Agent** identifies actors, events, and timestamps. It uses deterministic parsing for explicit dates, and controlled LLM-assisted normalization to convert relative expressions like “two days later” into explicit ISO dates.

**The Memory Bank** stores normalized entities and events and includes lightweight entity resolution so “Bob,” “Robert,” and “Mr. Smith” map to the same person.

**The Q&A Agent** answers natural-language questions by traversing the timeline and memory structures. Every answer includes provenance citations, and if evidence is insufficient, it returns a safe fallback.

And finally, **the Router** orchestrates which agents run depending on the user’s query.

---

### **Demo Narrative (1:35–2:15)**  
The system runs from a single command:

```

export PYTHONPATH="$PWD/src"
python -m capstone.demo --root capstone/synthetic_evidence --case-id CC02

```

First, the Evidence Agent loads and hashes each file.  
Then the Timeline Agent extracts events and normalizes timestamps.  
The Memory Bank organizes everything into canonical entities and fragments.  
Finally, the Q&A Agent answers grounded questions.

You see a deterministic timeline, clear event ordering, and evidence-bounded reasoning with no hallucinations.

---

### **Impact (2:15–2:40)**  
This architecture directly addresses one of the hardest problems in legal and investigative work: timeline reconstruction. With deterministic logic, strict provenance, and offline execution, LexFabric Agents delivers a reliable, reproducible pipeline. It’s not just summarization—it’s structured reasoning at scale.

---

### **Closing (2:40–2:55)**  
LexFabric Agents demonstrates how multi-agent design can safely extend LLM capabilities for real analytical workflows. By combining deterministic processing with controlled LLM assistance, it transforms fragmented evidence into explainable knowledge.  
Thank you.

---

If you'd like:

✅ A shorter 30-second judge version  
✅ Captions for your uploaded images  
✅ Or a media kit for LinkedIn / GitHub  

Just tell me.
```
