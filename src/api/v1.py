from typing import Optional
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from src.schemas import (
    ChatRequest,
    ChatResponse,
    ErrorResponse,
    HistoryResponse,
    HistoryItem,
)
from src.services.history_store import HistoryStore
from src.services.mistral_client import MistralClient
from src.services.chat_service import ChatService
from src.config.settings import settings
router = APIRouter(prefix="/api/v1")

# Minimal "manual DI"
_history_store = HistoryStore(maxlen=settings.HISTORY_MAXLEN)
_mistral_client = MistralClient()
_chat_service = ChatService(_mistral_client, _history_store)

@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def chat(
    body: ChatRequest,
    session_id: Optional[str] = Header(default=None, alias="X-Session-Id"),
):
    try:
        reply, usage = _chat_service.respond(
            question=body.question,
            model=body.model,
            session_id=session_id,
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error_code="UPSTREAM_ERROR", message=str(e)
            ).model_dump(),
        )

    # If guardrail blocked, we returned a plain string message with empty usage
    if usage == {} and "only answers" in reply:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(error_code="DOMAIN_BLOCK", message=reply).model_dump(),
        )

    return ChatResponse(response=reply, usage=usage, session_id=session_id)

@router.get("/history", response_model=HistoryResponse)
def get_history(
    session_id: Optional[str] = Header(default=None, alias="X-Session-Id")
):
    items_raw = _history_store.snapshot(session_id or "default")
    items = [HistoryItem(role=i["role"], content=i["content"]) for i in items_raw]
    return HistoryResponse(count=len(items), items=items)

@router.delete("/history")
def clear_history(
    session_id: Optional[str] = Header(default=None, alias="X-Session-Id")
):
    _history_store.clear(session_id or "default")
    return {"ok": True}
