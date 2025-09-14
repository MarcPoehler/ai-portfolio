from fastapi import APIRouter, Depends, Body, HTTPException

from ..application.controllers.chat_controller import (
    ChatController, ChatRequest, ChatResponse
)
from ..container import Container
from ..domain.errors import PIIBlockedError

def get_chat_router(container: "Container") -> APIRouter:
    api_router = APIRouter()


    @api_router.post("/v1/chat", response_model=ChatResponse)
    def chat(
        req: ChatRequest = Body(...),
        chat_controller: ChatController = Depends(lambda: container.chat_controller),
    ) -> ChatResponse:
        try:
            return chat_controller.handle(req)
        except PIIBlockedError as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "PII_BLOCKED",
                    "message": str(e),
                    "findings": getattr(e, "findings", []),
                },
            )

    return api_router
