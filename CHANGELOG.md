# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)  
and uses [Semantic Versioning](https://semver.org/).

---

## [1.1.0] – 2025-12-02
### Added
- Introduced **FastAPI microservice layer** (`src/api.py`) exposing:
  - `POST /v1/agent/analyze`
  - `GET /health`
  - Optional `GET /` landing route
- Added **Pydantic v2 data contracts**:
  - `AnalysisRequest`
  - `AnalysisResponse`
  - `TimelineEvent`
- Added **Dockerfile** enabling containerized deployment via Uvicorn.
- Added `src/__init__.py` to formalize the `src` namespace package.
- Added new architecture asset placeholder: `assets/api_schema.png`.
- Added `.gitignore` rules for `*.pdf` and `docs/scratch.md`.

### Changed
- Refactored `src/capstone/demo.py` to expose a clean, programmatic entrypoint:
  - `analyze_case(case_id, query)`
  - Supports both Router-based and deterministic fallback execution paths.
- Updated `requirements.txt` with service-level dependencies (`fastapi`, `uvicorn`, `pydantic`).
- Updated `README.md` to include:
  - API usage documentation
  - Swagger/ReDoc instructions
  - Example payloads/responses
  - Docker build + run instructions
  - Updated repository layout diagram

### Fixed
- Corrected absolute/relative imports inside `src/capstone/*` for consistent module loading.
- Ensured VS Code + Pylance resolve modules inside `.venv`.

### Notes
- This release elevates LexFabric Agents from a CLI-only demo to a fully deployable **typed HTTP microservice**.
- Backwards-compatible with the Kaggle Capstone submission (`v1.0.3`).
- Private MDLS work will extend the Router, Q&A integration, and authenticated multi-docket workflows.

---

## [1.0.3] – 2025-12-01
### Added
- Added **Capstone Demo Video (2:58)** to the README.
- Added new assets:
  - `assets/lexfabric-demo-split-screen.png`
  - Updated CLI demo screenshot
  - Kaggle PDF writeup (`LexFabric Agents – Multi-Agent Evidence & Timeline Reasoning _ Kaggle.pdf`)
- Added final documentation polish ahead of Kaggle submission.

### Changed
- Updated `README.md` with a dedicated video section placed after the Overview.
- Verified diagram references and adjusted paths under `docs/diagrams/`.
- Strengthened claims around synthetic-only evidence and reproducibility.

### Removed
- Removed outdated video assets:
  - `LexFabric_Agents.mp4`
  - `LexFabric_Agents_2min.mp4`
  - `The_AI_Detectives.mp4`

### Notes
- This is the **official Kaggle submission build**, tagged `v1.0.3`.

---

## [1.0.1] – 2025-12-01
### Added
- Split-screen demo image (`assets/lexfabric-demo-split-screen.png`).

### Changed
- Updated `README.md` with a visual summary of the agent pipeline.
- Updated `docs/kaggle_writeup.md` with visuals.
- Updated `docs/whitepaper.md` with inline diagrams.

---

## [1.0.0] – 2025-11-29
### Added
- Initial public release of the **LexFabric Agents – Capstone Demo**.
- Multi-agent system:
  - Evidence Agent
  - Timeline Agent
  - Q&A Agent
  - Memory Bank
  - Router
- Synthetic Evidence Server (MCP tools):
  - `list_evidence`
  - `get_evidence_text`
  - `list_cases`
  - `select_case`
  - `get_evidence_hashes`
- Evidence hashing (SHA-256 manifests).
- CLI interface (`capstone.demo`) with:
  - `list-evidence`
  - `list-timeline`
  - `ask`
- Documentation: README, Kaggle writeup, video script.
- Environment bootstrap (`setup.sh`).

### Notes
- Uses **synthetic evidence only**.
- Private MDLS extensions to follow.

---

# Version Links

[1.1.0]: https://github.com/revelles/lexfabric-agents-capstone-demo/compare/v1.0.3...v1.1.0  
[1.0.3]: https://github.com/revelles/lexfabric-agents-capstone-demo/compare/v1.0.1...v1.0.3  
[1.0.1]: https://github.com/revelles/lexfabric-agents-capstone-demo/compare/v1.0.0...v1.0.1  
[1.0.0]: https://github.com/revelles/lexfabric-agents-capstone-demo/releases/tag/v1.0.0
