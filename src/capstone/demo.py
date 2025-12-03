# src/capstone/demo.py

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console

# Try to import the real multi-agent Router; fall back gracefully if not available
try:
    from .agents.router import RouterAgent  # adjust to your actual class name
    HAS_ROUTER = True
except Exception:
    RouterAgent = None  # type: ignore
    HAS_ROUTER = False

# Try to import QnAAgent; fall back if not needed yet
try:
    from .agents.qa_agent import QnAAgent  # relative import
    HAS_QA = True
except Exception:
    QnAAgent = None  # type: ignore
    HAS_QA = False

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
    
from pathlib import Path
from typing import Any, Dict, List, Optional

# If you have a Router or similar orchestrator, import it here.
# Adjust this import to match your actual code if needed.
try:
    from .agents.router import Router  # type: ignore
    HAS_ROUTER = True
except ImportError:
    HAS_ROUTER = False


def _get_project_root() -> Path:
    """
    Resolve the project root from this file.

    demo.py is at:   src/capstone/demo.py
    project root is: repo root (two levels up from src)
    """
    return Path(__file__).resolve().parents[2]


def _get_evidence_root() -> Path:
    """
    Points to: <repo-root>/capstone/synthetic_evidence
    """
    return _get_project_root() / "capstone" / "synthetic_evidence"


def _build_naive_timeline(case_id: str) -> List[Dict[str, str]]:
    """
    Minimal deterministic timeline from the synthetic text files,
    used as a fallback if we don't (yet) wire the real agents.
    """
    evidence_root = _get_evidence_root()
    case_dir = evidence_root / case_id / "timeline"

    if not case_dir.exists():
        raise FileNotFoundError(f"Timeline folder not found for case {case_id}: {case_dir}")

    events: List[Dict[str, str]] = []

    for txt_file in sorted(case_dir.glob("*.txt")):
        content = txt_file.read_text(encoding="utf-8").strip()
        events.append({
            "date": txt_file.stem,   # e.g. "01_initial_filing"
            "event": content,
        })

    return events


def analyze_case(case_id: str, user_query: Optional[str] = None) -> Dict[str, Any]:
    """
    Refactored entry point for API usage.
    Returns a structured dictionary; NO prints, only data.

    It tries to use your Router (if present), otherwise falls back to
    a deterministic filesystem-based timeline using the synthetic evidence.
    """
    evidence_root = _get_evidence_root()
    case_dir = evidence_root / case_id

    if not case_dir.exists():
        raise FileNotFoundError(f"Case {case_id} not found in synthetic store: {case_dir}")

    results: Dict[str, Any] = {
        "case_id": case_id,
        "status": "success",
        "steps": [],
        "timeline": [],
        "final_answer": None,
    }

    results["steps"].append(f"Resolved project root at: {_get_project_root()}")
    results["steps"].append(f"Using evidence root: {evidence_root}")
    results["steps"].append(f"Found case directory: {case_dir}")

    # --- Preferred path: use your real multi-agent Router if available ---
    if HAS_ROUTER:
        # ⚠️ Adjust this block to match your actual Router API.
        # This is a placeholder pattern – you’ll plug in the true call signature.
        router = Router(evidence_root=str(evidence_root))

        # Example signatures you might adapt:
        #   router_result = router.run(case_id=case_id, query=user_query)
        # or router_result = router.process(case_id, user_query)
        #
        # For now, we just call a hypothetical method and expect a dict-like result.
        router_result = router.run(case_id=case_id, query=user_query)  # <-- adjust to your real method

        # You can shape this however your Router returns data.
        # Here we just assume it already returns a dictionary in the right format.
        return router_result

    # --- Fallback path: no Router wired yet, build a simple timeline from files ---
    timeline = _build_naive_timeline(case_id)
    results["timeline"] = timeline
    results["steps"].append(f"Timeline built from {len(timeline)} event file(s)")

    if user_query:
        # Placeholder: you can later hook this into qa_agent.ask(...)
        results["steps"].append(f"Query received but QA agent not yet wired: {user_query}")
        results["final_answer"] = None

    return results



if __name__ == "__main__":
    main()
