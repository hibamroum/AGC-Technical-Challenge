from __future__ import annotations

PROMPT_VERSION = "v1.0.0"

class PromptBuilder:
    """Fluent builder for the system prompt."""

    def __init__(self):
        self._role = ""
        self._task = ""
        self._constraints = ""
        self._style = ""
        self._format = ""

    def role(self, text: str):
        self._role = text
        return self

    def task(self, text: str):
        self._task = text
        return self

    def constraints(self, text: str):
        self._constraints = text
        return self

    def style(self, text: str):
        self._style = text
        return self

    def output_format(self, text: str):
        self._format = text
        return self

    def build(self) -> str:
        return (
            f"[PROMPT_VERSION={PROMPT_VERSION}]\n"
            f"{self._role}\n\n"
            f"Task:\n{self._task}\n\n"
            f"Constraints:\n{self._constraints}\n\n"
            f"Style:\n{self._style}\n\n"
            f"Output Format:\n{self._format}"
        )

DEFAULT_MEMORY = [
    "User prefers concise, practical safety guidance.",
    "User is comfortable with short bullet points.",
]

def memory_message() -> dict:
    return {"role": "system", "content": "Conversation Memory:\n- " + "\n- ".join(DEFAULT_MEMORY)}
