#!/usr/bin/env python3
import argparse
import os
import subprocess
from pathlib import Path
import textwrap
from typing import List, Tuple

EXAMPLE_QUERIES: List[Tuple[str, str]] = [
    (
        "1. Timeline Reconstruction",
        "What is the earliest event in this case, and which evidence file mentions it?",
    ),
    (
        "2. Cross-Document Contradiction Detection",
        "Do any emails contradict the initial filing? Summarize discrepancies.",
    ),
    (
        "3. Actor-Centric Narrative",
        "What actions did the claimant take between the first email and the filing?",
    ),
    (
        "4. Missing Information Audit",
        "Which timeline entries have incomplete dates or uncertain ordering?",
    ),
    (
        "5. Causal or Procedural Reasoning",
        "What led to the dispute escalation according to the evidence?",
    ),
    (
        "6. Summaries With Provenance",
        "Give me a 4-sentence overview of this case grounded only in the evidence.",
    ),
    (
        "7. Day-Level Event Expansion",
        "List everything that happened on the date of the initial filing.",
    ),
    (
        "8. Entity-Focused Cross-Section",
        "Which events involve the operations manager, and where are they mentioned?",
    ),
    (
        "9. Detect Gaps & Suggest Next Steps",
        "Which logical gaps remain after merging all evidence, and what new evidence would help close them?",
    ),
    (
        "10. Hash-Provenance Demo",
        "Show every timeline entry along with the hash of the file that generated it.",
    ),
]


def run_query(
    python_bin: str,
    module: str,
    root: str,
    case_id: str,
    label: str,
    query: str,
    env: dict,
) -> None:
    header = f"\n{'=' * 80}\n{label}\n{'=' * 80}\n"
    print(header)
    print(f"Query: {query}\n")

    cmd = [
        python_bin,
        "-m",
        module,
        "--root",
        root,
        "--case-id",
        case_id,
        "--ask",
        query,
    ]

    print(f"[CMD] {' '.join(cmd)}\n")

    completed = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    if completed.stdout:
        print("[STDOUT]")
        print(completed.stdout.strip())
        print()

    if completed.stderr:
        print("[STDERR]")
        print(completed.stderr.strip())
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run all example `--ask` queries against capstone.demo."
    )
    parser.add_argument(
        "--python-bin",
        default="python",
        help="Python executable to use (default: python)",
    )
    parser.add_argument(
        "--module",
        default="capstone.demo",
        help="Module to run with -m (default: capstone.demo)",
    )
    parser.add_argument(
        "--root",
        required=True,
        help="Root directory for synthetic evidence (e.g. capstone/synthetic_evidence)",
    )
    parser.add_argument(
        "--case-id",
        required=True,
        help="Case ID to test (e.g. CC02 or RH10)",
    )

    args = parser.parse_args()

    # Determine repo root = parent of this scripts/ folder
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[1]  # .../lexfabric-agents-capstone-demo
    src_path = repo_root / "src"

    # Build env with PYTHONPATH including src/
    env = os.environ.copy()
    existing_pp = env.get("PYTHONPATH", "")
    if existing_pp:
        env["PYTHONPATH"] = f"{src_path}:{existing_pp}"
    else:
        env["PYTHONPATH"] = str(src_path)

    intro = textwrap.dedent(
        f"""
        Running example `--ask` queries against {args.module}
        Evidence root: {args.root}
        Case ID: {args.case_id}
        Python: {args.python_bin}
        PYTHONPATH: {env['PYTHONPATH']}
        """
    ).strip()
    print(intro)
    print("-" * 80)

    for label, query in EXAMPLE_QUERIES:
        run_query(
            python_bin=args.python_bin,
            module=args.module,
            root=args.root,
            case_id=args.case_id,
            label=label,
            query=query,
            env=env,
        )


if __name__ == "__main__":
    main()
