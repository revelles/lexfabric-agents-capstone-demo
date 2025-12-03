# LexFabric Agents – Capstone Demo (Google AI Agents Intensive 2025)

## 🚀 Overview

This project is a **multi-agent evidence and timeline reasoning system** demonstrating:

* Evidence ingestion (synthetic only)
* Entity/date extraction
* Timeline construction
* Natural-language Q&A
* Reproducible hashing
* Offline CLI demo
* Typed microservice API (FastAPI)

All evidence is **fully synthetic**.

## Visual Summary: From Fragmented Evidence to Ordered Chronology
![LexFabric Split-Screen Demo](/assets/lexfabric-demo-split-screen.png)
*Figure 1: Traditional manual review vs. LexFabric's multi-agent chronological reconstruction.*

## 🎥 Capstone Demo Video (2:58)

Watch the official Kaggle demo video on YouTube:  
👉 https://youtu.be/c4q6CFecvu4



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



## 🔌 Production-Ready Microservice

LexFabric is not just a CLI script; it can run as a **stateless FastAPI microservice**.

* The core reasoning entry point is exposed via `analyze_case(case_id, query)` in `src/capstone/demo.py`.
* `src/api.py` wraps this as a FastAPI app with **Pydantic** models enforcing strict data contracts:
  - `AnalysisRequest` – input payload (`case_id`, optional `query`)
  - `AnalysisResponse` – normalized JSON (`steps`, `timeline[]`, `final_answer`)
* This turns the probabilistic Agentic layer into **deterministic, typed JSON** suitable for downstream systems, dashboards, or other services.

> Note: If you want a diagram for the API (mentioned in the text), place it at `assets/api_schema.png` and update the alt text/caption accordingly.



## 📊 Visual Overview

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
Dockerfile
LICENSE
README.md
assets/
capstone/
  synthetic_evidence/
docs/
scripts/
src/
  api.py
  capstone/
    agents/
    demo.py
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



## 🌐 API Usage (FastAPI Microservice)

### 1. Run the API locally

From the repository root, with your virtualenv activated:

```bash
uvicorn src.api:app --reload
```

This starts the service on `http://127.0.0.1:8000`.

### 2. Explore the interactive docs

Open:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc:      `http://127.0.0.1:8000/redoc`
* Health:     `http://127.0.0.1:8000/health`

### 3. Endpoints

| Method | Path                | Description                                |
|  | - |  |
| GET    | `/`                 | Simple JSON landing page (optional)        |
| GET    | `/health`           | Liveness probe                             |
| POST   | `/v1/agent/analyze` | Run the evidence → timeline → Q&A pipeline |

### 4. Request / Response Schema

**Request** – `POST /v1/agent/analyze`

```json
{
  "case_id": "CC02",
  "query": "What happened first?"
}
```

* `case_id` (string, required) – synthetic case ID (`CC02`, `RH10`, etc.)
* `query` (string, optional) – natural language question (can be omitted).

**Response** – `200 OK`

```json
{
  "case_id": "CC02",
  "status": "success",
  "steps": [
    "Resolved project root at: /.../lexfabric-agents-capstone-demo",
    "Using evidence root: /.../capstone/synthetic_evidence",
    "Found case directory: /.../capstone/synthetic_evidence/CC02",
    "Timeline built from 1 event file(s)"
  ],
  "timeline": [
    {
      "date": "01_initial_filing",
      "event": "..."  // contents of 01_initial_filing.txt
    }
  ],
  "final_answer": null
}
```

If the case is missing:

```json
{
  "detail": "Case XYZ not found in synthetic store: /.../capstone/synthetic_evidence/XYZ"
}
```

with status `404`.



## 🐳 Docker Usage (Optional)

A minimal Dockerfile is included.

Build the image:

```bash
docker build -t lexfabric-api .
```

Run the container:

```bash
docker run -p 8000:8000 lexfabric-api
```

Then use the same URLs:

* `http://127.0.0.1:8000/health`
* `http://127.0.0.1:8000/docs`



## 🔐 Hashing

```bash
python scripts/generate_manifest.py
```

This regenerates the SHA-256 manifest under `capstone/synthetic_evidence/manifest.json`, ensuring reproducibility and integrity.



## 🛡️ Safety & Anti-Hallucination Design

* Evidence-bound reasoning
* Deterministic SHA-256 pipeline
* Offline execution
* Narrow agent roles
* Query-time guardrails
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
* FastAPI microservice + typed API

Private LexFabric MDLS will extend this foundation with secure multi-docket reasoning.
