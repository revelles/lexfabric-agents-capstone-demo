# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and uses [Semantic Versioning](https://semver.org/).



## [1.0.3] – 2025-12-01
### Added
- Added **Capstone Demo Video (2:58)** to the README.
- Added new assets:
  - `assets/lexfabric-demo-split-screen.png`
  - Updated CLI demo screenshot
  - Kaggle PDF writeup (`LexFabric Agents – Multi-Agent Evidence & Timeline Reasoning _ Kaggle.pdf`)
- Added final documentation polish ahead of Kaggle submission.

### Changed
- Updated `README.md` with a dedicated video section placed immediately after the Overview.
- Verified architecture diagram references and adjusted paths under `docs/diagrams/`.
- Strengthened claims around synthetic-only evidence and reproducibility.

### Removed
- Removed outdated video assets:
  - `LexFabric_Agents.mp4`
  - `LexFabric_Agents_2min.mp4`
  - `The_AI_Detectives.mp4`

### Notes
- This is the **official Kaggle submission build**, tagged `v1.0.3`.
- Future development continues privately in the LexFabric MDLS framework.



## [1.0.1] – 2025-12-01
### Added
- Split-screen demo image `assets/lexfabric-demo-split-screen.png` illustrating fragmented evidence vs. ordered LexFabric chronology.

### Changed
- Updated `README.md` with a visual summary of the end-to-end pipeline.
- Updated `docs/kaggle_writeup.md` to include the split-screen graphic.
- Updated `docs/whitepaper.md` with inline architecture diagrams.



## [1.0.0] – 2025-11-29
### Added
- Initial public release of the **LexFabric Agents – Capstone Demo**.
- Multi-agent pipeline:
  - Ingest Agent
  - Analysis Agent
  - Timeline Agent
  - Q&A Agent
  - Memory Bank
- Synthetic Evidence Server (MCP tools):
  - `list_evidence`
  - `get_evidence_text`
  - `list_cases`
  - `select_case`
  - `get_evidence_hashes`
- Evidence hashing & manifest generation (SHA-256).
- CLI interface (`capstone.demo`) supporting:
  - `list-evidence`
  - `list-timeline`
  - `ask`
- Case selector supporting CC02 & RH10 datasets.
- Documentation:
  - README.md
  - Kaggle writeup
  - Video script
- Environment bootstrap (`setup.sh`).

### Notes
- Uses **synthetic evidence only**.
- Private LexFabric MDLS extensions will ship in future tags.
