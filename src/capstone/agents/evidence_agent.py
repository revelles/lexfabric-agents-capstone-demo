from typing import List, Dict, Any

from .memory import Memory


class EvidenceAgent:
    """
    Agent responsible for reasoning over evidence records for a given case.

    For the capstone, you can:
      - Feed it the evidence_records from demo.py
      - Have it call an LLM (Gemini, etc.)
      - Store summaries in Memory under 'evidence_summary'
    """

    def __init__(self, memory: Memory):
        self.memory = memory

    def summarize(self, case_id: str, records: List[Dict[str, Any]]) -> str:
        """
        Stub implementation. Replace with an LLM call.

        For now, just count by category and store that summary.
        """
        counts: Dict[str, int] = {}
        for rec in records:
            cat = rec.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1

        lines = [
            f"[EvidenceAgent] Summary for case {case_id}:",
            f"- Total records: {len(records)}",
        ]
        if counts:
            lines.append("- By category:")
            for cat, n in sorted(counts.items(), key=lambda kv: kv[0]):
                lines.append(f"  • {cat}: {n}")

        summary = "\n".join(lines)
        self.memory.set("evidence_summary", summary)
        self.memory.add_message(summary)
        return summary
