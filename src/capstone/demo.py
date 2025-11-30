# src/capstone/demo.py

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from capstone.agents.router import RouterAgent
from capstone.agents.qa_agent import QnAAgent


console = Console()


@dataclass
class CaseChoice:
    """Simple representation of a synthetic case."""
    case_id: str
    path: Path
    description: str = ""


# --- Filesystem-based discovery ---------------------------------------------


def discover_cases(root: Path) -> List[CaseChoice]:
    """
    Discover cases as immediate subdirectories under `root`.

    Example:
        capstone/synthetic_evidence/
          CC02/
          RH10/
    """
    if not root.exists():
        console.print(f"[bold red][ERROR][/bold red] Evidence root does not exist: {root}")
        return []

    subdirs = [p for p in sorted(root.iterdir()) if p.is_dir()]

    # If no subdirs, treat root as a single pseudo-case
    if not subdirs:
        return [CaseChoice(case_id="DEFAULT", path=root)]

    cases: List[CaseChoice] = []
    for p in subdirs:
        cases.append(CaseChoice(case_id=p.name, path=p))
    return cases


def load_evidence_for_case(case: CaseChoice) -> List[Dict[str, Any]]:
    """
    Walk the case directory and build a simple evidence record list.

    Category heuristic:
      - First path component under the case directory (e.g., 'pleadings', 'emails').
      - If files are directly under the case root, category='uncategorized'.
    """
    records: List[Dict[str, Any]] = []

    for file_path in case.path.rglob("*"):
        if not file_path.is_file():
            continue

        rel = file_path.relative_to(case.path)
        parts = rel.parts

        if len(parts) > 1:
            category = parts[0]
        else:
            category = "uncategorized"

        record = {
            "id": str(rel),
            "case_id": case.case_id,
            "category": category,
            "title": file_path.stem,
            "path": str(file_path),
            "ext": file_path.suffix.lower(),
        }
        records.append(record)

    return records


def derive_timeline_events(evidence_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Simple heuristic:

    - Any evidence with category 'timeline' (case/timeline/...) becomes an event.
    - We don't parse actual dates yet; just use filename as 'title'.
    """
    events: List[Dict[str, Any]] = []
    for rec in evidence_records:
        cat = (rec.get("category") or "").lower()
        if cat == "timeline":
            events.append(
                {
                    "title": rec.get("title", "<untitled>"),
                    "timestamp": None,
                    "source_path": rec.get("path"),
                }
            )
    return events


def interactive_choose_case(choices: List[CaseChoice]) -> Optional[CaseChoice]:
    if not choices:
        console.print("[bold yellow]No cases available.[/bold yellow]")
        return None

    console.print("\n[bold cyan]Available cases:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", justify="right", style="dim", width=3)
    table.add_column("Case ID", style="bold")
    table.add_column("Description", style="dim")

    for idx, c in enumerate(choices, start=1):
        desc = c.description or ""
        table.add_row(str(idx), c.case_id, desc)

    console.print(table)

    while True:
        raw = input("\nSelect a case by number (or 'q' to quit): ").strip()
        if raw.lower() in {"q", "quit", "exit"}:
            return None
        if not raw.isdigit():
            console.print("[yellow]Please enter a number.[/yellow]")
            continue
        idx = int(raw)
        if 1 <= idx <= len(choices):
            return choices[idx - 1]
        console.print(f"[yellow]Please enter a number between 1 and {len(choices)}.[/yellow]")


# --- Core demo flow ---------------------------------------------------------


def run_interactive_demo(
    root: Path,
    case_id: Optional[str] = None,
    ask: Optional[str] = None,
) -> None:
    cases = discover_cases(root)
    if not cases:
        console.print("[bold red]No cases discovered. Exiting.[/bold red]")
        return

    if case_id:
        chosen = next((c for c in cases if c.case_id == case_id), None)
        if not chosen:
            console.print(f"[bold red]Case '{case_id}' not found.[/bold red] Available case_ids:")
            for c in cases:
                console.print(f"  - [cyan]{c.case_id}[/cyan]")
            return
    else:
        chosen = interactive_choose_case(cases)

    if not chosen:
        console.print("[bold yellow]No case selected. Exiting.[/bold yellow]")
        return

    console.print(Panel.fit(
        Text(f"CASE: {chosen.case_id}", style="bold white"),
        title="Capstone Agents Demo",
        border_style="cyan",
    ))

    # 1) Load evidence records
    evidence_records = load_evidence_for_case(chosen)
    console.print(f"[bold blue][INFO][/bold blue] Loaded [bold]{len(evidence_records)}[/bold] evidence records for this case.")

    if evidence_records:
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Sample Evidence"
        table.add_column("ID", style="dim", overflow="fold")
        table.add_column("Category", style="cyan")
        table.add_column("Title", style="bold")

        for rec in evidence_records[:5]:
            rid = rec.get("id", "<no-id>")
            cat = rec.get("category", "<no-category>")
            title = rec.get("title") or "<no-title>"
            table.add_row(rid, cat, title)

        console.print(table)
    else:
        console.print(f"[yellow]No evidence files found under {chosen.path}[/yellow]")

    # 2) Derive timeline events
    timeline_events = derive_timeline_events(evidence_records)
    console.print(f"\n[bold blue][INFO][/bold blue] Derived [bold]{len(timeline_events)}[/bold] timeline events.")

    # 3) Run multi-agent pipeline via RouterAgent
    console.print(Panel.fit("Running agent pipeline...", border_style="green"))
    router = RouterAgent()
    router.run_case_pipeline(chosen.case_id, evidence_records, timeline_events)

    # 4) Show EvidenceAgent + TimelineAgent outputs from memory
    console.print(Panel.fit(
        "[bold]Evidence Summary (EvidenceAgent)[/bold]",
        border_style="magenta",
    ))
    evidence_summary = router.memory.get("evidence_summary", "(no evidence summary)")
    console.print(evidence_summary)

    console.print()
    console.print(Panel.fit(
        "[bold]Timeline Summary (TimelineAgent)[/bold]",
        border_style="magenta",
    ))
    timeline_summary = router.memory.get("timeline_summary", "(no timeline summary)")
    console.print(timeline_summary)

    # 5) Ask a demo question via QnAAgent (rule-based, no external LLM)
    console.print()
    console.print(Panel.fit(
        "[bold]Q&A (QnAAgent)[/bold]",
        border_style="magenta",
    ))

    if ask:
        question = ask
    else:
        question = "Give me a short, high-level overview of this case based on the evidence and timeline."

    console.print(f"[bold]Question:[/bold] {question}\n")

    # Optional: try to get a hash manifest from the RouterAgent's memory.
    # If none is present, we fall back to an empty dict.
    hash_manifest = router.memory.get("hash_manifest", {})

    # Construct the rule-based QnAAgent directly from evidence + timeline.
    qna = QnAAgent(
        evidence=evidence_records,
        timeline=timeline_events,
        hashes=hash_manifest,
    )

    answer = qna.answer(question)
    console.print(answer)

    console.print("\n[bold green][OK][/bold green] Demo completed.")


# --- CLI entry-point --------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capstone demo: Choose a case, inspect evidence, summarize timeline, and run agents."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("capstone/synthetic_evidence"),
        help="Root directory where synthetic evidence is stored.",
    )
    parser.add_argument(
        "--case-id",
        type=str,
        default=None,
        help="If provided, run non-interactive mode for this case_id.",
    )
    parser.add_argument(
        "--ask",
        type=str,
        default=None,
        help="Optional question to ask the QnAAgent after running the pipeline.",
    )
    args = parser.parse_args()

    run_interactive_demo(
        root=args.root,
        case_id=args.case_id,
        ask=args.ask,
    )


if __name__ == "__main__":
    main()
