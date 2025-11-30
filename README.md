# LexFabric Agents Capstone Demo

This repository contains a standalone, synthetic-only capstone project for the **Google + Kaggle 5-Day AI Agents Intensive (Nov 2025)**.

It demonstrates how to build a small **multi-agent system** that:

- Discovers **synthetic legal cases** from the filesystem
- Loads and inspects **evidence files** per case
- Derives a toy **timeline** from files
- Uses a modular **agent architecture** to:
  - Summarize evidence
  - Summarize timelines
  - Answer user questions with shared memory
- Exposes everything through a simple **CLI demo**:

```bash
python -m capstone.demo
