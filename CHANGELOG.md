# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and uses [Semantic Versioning](https://semver.org/).

---

## [1.0.0] – 2025-11-29
### Added
- Initial public release of the **LexFabric Agents – Capstone Demo**.
- Multi-agent pipeline (Ingest Agent, Analysis Agent, Timeline Agent, Q&A Agent).
- Synthetic Evidence Server (MCP) with:
  - `list_evidence`
  - `get_evidence_text`
  - `list_cases`
  - `select_case`
  - `get_evidence_hashes`
- Evidence hashing & manifest generation using SHA-256.
- Case selector supporting CC02 → RH10 synthetic datasets.
- CLI interface (`capstone.demo`) with modes:
  - `list-evidence`
  - `list-timeline`
  - `ask`
- Timeline construction algorithm with merge logic.
- Local memory bank integration for hybrid question answering.
- Documentation:
  - README.md (submission version)
  - Kaggle writeup
  - Video script
- Setup script (`setup.sh`) for environment bootstrap.

### Notes
- This release uses **synthetic evidence only**.
- Private LexFabric MDLS features will ship in later tagged versions.
