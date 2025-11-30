from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Memory:
    """
    Simple in-memory scratchpad shared across agents.

    In a real system this might be Redis, a DB, or a vector store.
    """
    slots: Dict[str, Any] = field(default_factory=dict)
    messages: List[str] = field(default_factory=list)

    def set(self, key: str, value: Any) -> None:
        self.slots[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.slots.get(key, default)

    def add_message(self, text: str) -> None:
        self.messages.append(text)

    def history(self) -> List[str]:
        return list(self.messages)
