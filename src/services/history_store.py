from collections import deque
from typing import Deque, Dict, List, TypedDict

class ChatMessage(TypedDict):
    role: str
    content: str

class HistoryStore:
    """Simple per-session in-memory history (replace with Redis/DB later)."""

    def __init__(self, maxlen: int = 6):
        self._store: Dict[str, Deque[ChatMessage]] = {}
        self._maxlen = maxlen

    def get(self, session_id: str) -> Deque[ChatMessage]:
        if session_id not in self._store:
            self._store[session_id] = deque(maxlen=self._maxlen)
        return self._store[session_id]

    def snapshot(self, session_id: str) -> List[ChatMessage]:
        return list(self.get(session_id))

    def append_turns(self, session_id: str, user_q: str, assistant_a: str) -> None:
        q = self.get(session_id)
        q.append({"role": "user", "content": user_q})
        q.append({"role": "assistant", "content": assistant_a})

    def clear(self, session_id: str) -> None:
        self._store.pop(session_id, None)
