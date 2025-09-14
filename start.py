from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from backend.container import build_container
from backend.presentation.http_chat_router import get_chat_router
from backend.presentation.errors import domain_error_handler, generic_error_handler
from backend.domain.errors import DomainError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_portfolio")


def create_app() -> FastAPI:
    """Application factory using FastAPI lifespan instead of deprecated on_event."""
    container = build_container()

    cors_origins = container.settings.cors_allowed_origins or [
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ]

    @asynccontextmanager
    async def lifespan(app: FastAPI):  # noqa: D401 (simple lifespan)
        # Startup phase
        if not container.settings.openai_api_key:
            logger.warning("OPENAI_API_KEY missing – LLM calls will fail.")
        logger.info(
            "Startup env=%s model=%s cors=%s",
            container.settings.environment,
            container.settings.llm_model,
            cors_origins,
        )
        yield
        # Shutdown phase (currently no cleanup needed)

    app = FastAPI(title="ai-portfolio-backend", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=False,
        allow_methods=["POST"],
        allow_headers=["*"],
    )

    # Exception handlers
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(Exception, generic_error_handler)

    # Routes
    app.include_router(get_chat_router(container), prefix="")
    return app


app = create_app()
