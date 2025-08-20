from typing import Optional, Literal, Dict, Any
from pydantic import BaseModel, constr

ModelName = Literal["mistral-tiny", "mistral-small", "mistral-large-latest"]

class ChatRequest(BaseModel):
    question: constr(strip_whitespace=True, min_length=1, max_length=1000)
    model: ModelName = "mistral-tiny"

class ChatResponse(BaseModel):
    response: str
    usage: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None

class ErrorResponse(BaseModel):
    error_code: str
    message: str

class HistoryItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class HistoryResponse(BaseModel):
    count: int
    items: list[HistoryItem]
