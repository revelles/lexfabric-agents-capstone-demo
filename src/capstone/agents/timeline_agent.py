from typing import List, Dict, Any

from .memory import Memory


class TimelineAgent:
    """
    Agent responsible for deriving and summarizing a timeline for a case.

    In the demo, it receives simple 'events' derived from files.
    """

    def __init__(self, memory: Memory):
        self.memory = memory

    def summarize(self, case_id: str, events: List[Dict[str, Any]]) -> str:
        if not events:
            summary = f"[TimelineAgent] No timeline events for case {case_id}."
            self.memory.set("timeline_summary", summary)
            self.memory.add_message(summary)
            return summary

        lines = [
            f"[TimelineAgent] Timeline summary for case {case_id}:",
            f"- Total events: {len(events)}",
        ]

        preview = events[:5]
        lines.append("- First events:")
        for ev in preview:
            ts = ev.get("timestamp") or ev.get("date") or "unknown-date"
            title = ev.get("title") or "Untitled event"
            lines.append(f"  • {ts}: {title}")

        summary = "\n".join(lines)
        self.memory.set("timeline_summary", summary)
        self.memory.add_message(summary)
        return summary
