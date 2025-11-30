from typing import Optional

from .memory import Memory


class QnAAgent:
    """
    Agent that answers user questions based on evidence + timeline summaries.

    For the capstone demo, it just interpolates the summaries from Memory.
    """

    def __init__(self, memory: Memory):
        self.memory = memory

    def answer(self, question: str) -> str:
        evidence_summary: Optional[str] = self.memory.get("evidence_summary")
        timeline_summary: Optional[str] = self.memory.get("timeline_summary")

        lines = [
            "[QnAAgent] Answer (stubbed, no external LLM):",
            f"Question: {question}",
        ]

        if evidence_summary:
            lines.append("\n--- Evidence context ---")
            lines.append(evidence_summary)

        if timeline_summary:
            lines.append("\n--- Timeline context ---")
            lines.append(timeline_summary)

        if not (evidence_summary or timeline_summary):
            lines.append("\n(No context available yet; run EvidenceAgent and TimelineAgent first.)")

        answer = "\n".join(lines)
        self.memory.add_message(answer)
        return answer
