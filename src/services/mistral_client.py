import requests
from typing import Dict, List, Tuple, Any
from src.config.settings import settings
class MistralClient:
    """Minimal sync wrapper around Mistral's chat completions.
    Timeouts are set; retries can be added later.
    """

    def __init__(self, timeout_seconds: int = 30):
        self.base = str(settings.MISTRAL_API_BASE)
        self.key = settings.MISTRAL_API_KEY
        self.timeout = settings.REQUEST_TIMEOUT_SECONDS

    def chat(self, model: str, messages: List[Dict[str, str]]) -> Tuple[str, Dict[str, Any]]:
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }
        payload = {"model": model, "messages": messages}
        r = requests.post(
            f"{self.base}/chat/completions",
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )
        r.raise_for_status()
        data = r.json()
        # Keep it simple; bubble up raw failure if structure is unexpected
        reply = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        return reply, usage
