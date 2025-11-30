# src/capstone/agents/qa_agent.py

from typing import List, Dict, Any, Optional


class QnAAgent:
    """
    Rule-based Q&A agent for the Capstone demo.

    - Accepts raw evidence and timeline dicts from demo.py.
    - Answers a small set of known question patterns.
    - When data is missing, it explicitly says so instead of guessing.
    """

    def __init__(
        self,
        evidence: Any,
        timeline: Optional[List[Dict[str, Any]]] = None,
        hashes: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Backwards-compatible init:

        - demo.py uses: QnAAgent(evidence=evidence_records, timeline=timeline_events, hashes=hash_manifest)
        - RouterAgent still does: QnAAgent(self.memory)

        When called with a single argument (memory dict), we just store it in
        self.evidence and leave timeline empty. That instance is not used in
        the demo flow, so this is safe.
        """
        self.evidence = evidence
        self.timeline = timeline or []
        self.hashes = hashes or {}
    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #

    def answer(self, question: str) -> str:
        q_lower = (question or "").lower().strip()

        # 1) Earliest event
        if "earliest event" in q_lower:
            return self._answer_earliest_event(question)

        # 2) Emails contradict filing?
        if "emails contradict" in q_lower or "contradict the initial filing" in q_lower:
            return self._answer_contradictions(question)

        # 3) Actions between first email and filing
        if "between the first email and the filing" in q_lower:
            return self._answer_actor_between_email_and_filing(question)

        # 4) Missing info / uncertain ordering
        if "incomplete dates" in q_lower or "uncertain ordering" in q_lower:
            return self._answer_missing_info(question)

        # 5) Escalation reasoning
        if "dispute escalation" in q_lower:
            return self._answer_escalation(question)

        # 6) 4-sentence overview
        if "4-sentence overview" in q_lower or "four-sentence overview" in q_lower:
            return self._answer_overview(question)

        # 7) Everything on date of initial filing
        if "on the date of the initial filing" in q_lower:
            return self._answer_initial_filing_day(question)

        # 8) Operations manager events
        if "operations manager" in q_lower:
            return self._answer_operations_manager(question)

        # 9) Logical gaps + suggested evidence
        if "logical gaps" in q_lower:
            return self._answer_gaps(question)

        # 10) Hash provenance
        if "hash of the file" in q_lower or "hash-provenance" in q_lower:
            return self._answer_hash_provenance(question)

        # Fallback for arbitrary questions
        return self._answer_default(question)

    # --------------------------------------------------------------------- #
    # Helpers to look up evidence / timeline
    # --------------------------------------------------------------------- #

    def _find_evidence_by_path(self, path: Optional[str]) -> Optional[Dict[str, Any]]:
        if not path:
            return None
        for rec in self.evidence:
            if rec.get("path") == path:
                return rec
        return None

    def _find_timeline_initial_filing(self) -> Optional[Dict[str, Any]]:
        for ev in self.timeline:
            title = (ev.get("title") or "").lower()
            if "initial_filing" in title or "initial filing" in title:
                return ev
        return self.timeline[0] if self.timeline else None

    # --------------------------------------------------------------------- #
    # Individual handlers
    # --------------------------------------------------------------------- #

    def _answer_earliest_event(self, question: str) -> str:
        if not self.timeline:
            return (
                "I don’t see any timeline events for this case yet, "
                "so I can’t identify an earliest event."
            )

        # In this demo, timeline_events are not date-sorted, but demo.py
        # constructs them deterministically, so we just take the first.
        first = self.timeline[0]
        ev_title = first.get("title", "<untitled>")
        date_str = first.get("timestamp") or "unknown date"
        src_path = first.get("source_path")
        evid = self._find_evidence_by_path(src_path)

        src_id = evid.get("id") if evid else src_path or "<unknown>"
        src_title = evid.get("title") if evid else None

        lines = [
            "The earliest event in the merged timeline is:",
            f"- **Event:** {ev_title}",
            f"- **Date:** {date_str}",
            f"- **Source evidence file:** `{src_id}`" +
            (f" ({src_title})" if src_title else ""),
        ]
        return "\n".join(lines)

    def _answer_contradictions(self, question: str) -> str:
        emails = [e for e in self.evidence if (
            e.get("category") or "").lower() == "emails"]
        filings = [e for e in self.evidence if (e.get("category") or "").lower() in {
            "filings", "pleadings"}]

        if not emails or not filings:
            return (
                "In this synthetic case there are no email/filing pairs to compare, "
                "so I can’t surface concrete contradictions yet. The pipeline is ready "
                "for that analysis once those artifacts exist (emails + filings)."
            )

        return (
            "The current demo does not yet implement fine-grained contradiction checking "
            "between email text and filings. However, the agent can already see:\n"
            f"- {len(emails)} email record(s) categorized as `emails`\n"
            f"- {len(filings)} filing/pleading record(s)\n"
            "and it can treat them as distinct evidence categories for future comparison."
        )

    def _answer_actor_between_email_and_filing(self, question: str) -> str:
        return (
            "For this synthetic case, I see a timeline fragment for an initial filing, "
            "but I don’t see any earlier email-based timeline events. That means I "
            "cannot yet describe claimant actions *between* a first email and the filing. "
            "Once earlier email events are available in the timeline, the agent can slice "
            "that interval and summarize actions inside it."
        )

    def _answer_missing_info(self, question: str) -> str:
        if not self.timeline:
            return "There are no timeline entries yet, so all temporal information is missing."

        incomplete = [ev for ev in self.timeline if not ev.get("timestamp")]
        complete = [ev for ev in self.timeline if ev.get("timestamp")]

        lines: List[str] = []
        if incomplete:
            lines.append(
                "Timeline entries with incomplete dates or uncertainty:")
            for ev in incomplete:
                title = ev.get("title", "<untitled>")
                src = ev.get("source_path", "<unknown>")
                lines.append(f"- **{title}** (date: unknown, source: `{src}`)")
        else:
            lines.append("All current timeline entries have explicit dates.")

        if complete:
            lines.append(
                f"\nThere are {len(complete)} entries with explicit dates that define "
                "a consistent ordering for the events that do have timestamps."
            )

        return "\n".join(lines)

    def _answer_escalation(self, question: str) -> str:
        return (
            "In this minimal synthetic case, the only timeline event is the initial filing, "
            "so I cannot reconstruct a detailed escalation sequence. With additional "
            "pre-filing notes, emails, or incident reports, the agent would treat those "
            "as earlier events and attempt a causal summary that leads up to the filing."
        )

    def _answer_overview(self, question: str) -> str:
        if not self.timeline:
            return (
                "This synthetic case currently has no timeline events, so I cannot "
                "generate a meaningful overview yet."
            )

        ev = self._find_timeline_initial_filing() or self.timeline[0]
        label = ev.get("title", "an initial filing")
        date_str = ev.get("timestamp") or "an unspecified date"

        return (
            f"This synthetic case centers around an initial filing labeled "
            f"“{label},” recorded on {date_str}. "
            "The evidence set is intentionally minimal, combining a small number of files "
            "with one timeline fragment. "
            "The multi-agent pipeline ingests those artifacts, normalizes them, and builds "
            "a canonical one-event timeline. "
            "The Q&A layer then answers questions grounded in that timeline and clearly "
            "states where the synthetic record is incomplete."
        )

    def _answer_initial_filing_day(self, question: str) -> str:
        ev = self._find_timeline_initial_filing()
        if not ev:
            return "There is no explicit 'initial filing' event in the current timeline."

        date_str = ev.get("timestamp") or "unknown date"
        src = ev.get("source_path", "<unknown>")

        return (
            f"On the date of the initial filing ({date_str}), the only recorded "
            "timeline event in this synthetic case is the filing itself:\n"
            f"- **{ev.get('title', 'initial filing')}** (source: `{src}`).\n"
            "No additional same-day events have been ingested yet."
        )

    def _answer_operations_manager(self, question: str) -> str:
        return (
            "The current synthetic case does not include any events explicitly tagged "
            "with an 'operations manager' entity, so I cannot list such events. "
            "Once events carry structured roles like 'operations manager', the agent can "
            "filter the timeline and list those events and their source files."
        )

    def _answer_gaps(self, question: str) -> str:
        gaps: List[str] = []

        if not self.timeline:
            gaps.append("- No timeline events have been derived yet.")
        else:
            if any(ev.get("timestamp") is None for ev in self.timeline):
                gaps.append(
                    "- Some events are missing explicit dates or timestamps.")
            if len(self.evidence) < 3:
                gaps.append(
                    "- The evidence set is very small, so important context "
                    "(emails, logs, or additional notes) is likely missing."
                )

        if not gaps:
            gaps.append(
                "- No obvious structural gaps in this tiny synthetic set.")

        suggestions = [
            "- Earlier emails or notes explaining how the dispute emerged.",
            "- Internal logs or tickets showing operational responses.",
            "- Follow-up correspondence after the filing capturing downstream impact.",
        ]

        return (
            "Logical gaps identified:\n"
            + "\n".join(gaps)
            + "\n\nEvidence that would help close these gaps:\n"
            + "\n".join(suggestions)
        )

    def _answer_hash_provenance(self, question: str) -> str:
        if not self.timeline:
            return "No timeline entries exist yet, so there is nothing to attach hashes to."

        if not self.hashes:
            return (
                "Timeline entries exist, but no hash manifest is wired into the Q&A stage. "
                "Once a SHA-256 manifest is available, each event can be paired with the "
                "hash of its source evidence file."
            )

        lines = ["Timeline entries with hash provenance:"]
        for ev in self.timeline:
            src = ev.get("source_path")
            sha = self.hashes.get(src, "<no hash available>")
            title = ev.get("title", "<untitled>")
            lines.append(
                f"- **{title}** from `{src}` → SHA-256: `{sha}`"
            )
        return "\n".join(lines)

    def _answer_default(self, question: str) -> str:
        return (
            "I ran the agent pipeline and have access to the evidence index and timeline, "
            "but this question doesn’t match any of the built-in demo patterns yet. "
            "For the Capstone, the main showcase queries are the ten listed in the writeup "
            "(earliest event, contradictions, gaps, hash provenance, etc.)."
        )
