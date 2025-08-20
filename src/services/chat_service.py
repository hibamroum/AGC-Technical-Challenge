from typing import List, Dict, Optional, Tuple

from src.core.prompt_builder import PromptBuilder, memory_message
from src.core.guardrails import enforce_public_safety_only, sanitize
from src.services.history_store import HistoryStore
from src.services.mistral_client import MistralClient

class ChatService:
    def __init__(self, client: MistralClient, history: HistoryStore):
        self.client = client
        self.history = history

    def build_system_prompt(self) -> str:
        return (
            PromptBuilder()
            .role("You are a supportive, pragmatic assistant focused on women’s safety in public spaces.")
            .task(
                "Provide accurate, practical guidance for streets, transit, workplaces, and events. "
                "Define terms when helpful and add one tactical tip tailored to the question."
            )
            .constraints(
                "Do not give legal or medical advice. Do not victim-blame. If unsure, say so briefly. "
                "Prefer region-agnostic advice unless the user provides location."
            )
            .style("Tone: warm, clear, non-judgmental. Use simple sentences.")
            .output_format(
                "Answer using this structure:\n"
                "1) Direct answer (2–4 sentences)\n"
                "2) Optional bullets (max 3)\n"
                "3) One follow-up question"
            )
            .build()
        )

    def respond(
        self,
        question: str,
        model: str = "mistral-tiny",
        session_id: Optional[str] = None,
    ) -> Tuple[str, dict]:
        # Guardrails
        violation = enforce_public_safety_only(question)
        if violation:
            return violation, {}

        question = sanitize(question)

        # Assemble messages
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.build_system_prompt()},
            memory_message(),
        ]
        if session_id:
            messages.extend(self.history.snapshot(session_id))
        messages.append({"role": "user", "content": question})

        # Call LLM
        reply, usage = self.client.chat(model=model, messages=messages)

        # Save to history
        if session_id:
            self.history.append_turns(session_id, question, reply)

        return reply, usage
