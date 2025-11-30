from typing import List, Dict, Any

from .memory import Memory
from .evidence_agent import EvidenceAgent
from .timeline_agent import TimelineAgent
from .qa_agent import QnAAgent


class RouterAgent:
    """
    High-level orchestrator that wires:
      - EvidenceAgent
      - TimelineAgent
      - QnAAgent

    For CLI integration, you'll do something like:

        router = RouterAgent()
        router.run_case_pipeline(case_id, evidence_records, timeline_events)
        print(router.answer("What is this case about?"))
    """

    def __init__(self):
        self.memory = Memory()
        self.evidence_agent = EvidenceAgent(self.memory)
        self.timeline_agent = TimelineAgent(self.memory)
        self.qa_agent = QnAAgent(self.memory)

    def run_case_pipeline(
        self,
        case_id: str,
        evidence_records: List[Dict[str, Any]],
        timeline_events: List[Dict[str, Any]],
    ) -> None:
        self.evidence_agent.summarize(case_id, evidence_records)
        self.timeline_agent.summarize(case_id, timeline_events)

    def answer(self, question: str) -> str:
        return self.qa_agent.answer(question)
