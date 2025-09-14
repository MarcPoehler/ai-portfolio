from dataclasses import dataclass
from pathlib import Path

from .config import Settings

from .infrastructure.repositories.profile_repository import FileProfileRepository
from .infrastructure.services.openai_chat_service import OpenAIChatService
from .infrastructure.services.pii_regex_detector import RegexPIIDetector
from .application.use_cases.answer_questions_use_case import AnswerQuestionUseCase
from .application.use_cases.pii_processing_use_case import PIIProcessingUseCase
from .application.controllers.chat_controller import ChatController

@dataclass
class Container:
    """Simple DI container assembling all components."""
    settings: Settings
    profile_repository: FileProfileRepository
    pii_detector: RegexPIIDetector | None
    pii_processor: PIIProcessingUseCase | None
    llm_service: OpenAIChatService
    answer_use_case: AnswerQuestionUseCase
    chat_controller: ChatController

def build_container() -> Container:
    """Create and wire all implementations following Clean Architecture."""
    settings = Settings()

    # Repository
    background_path = Path(settings.data_dir) / settings.background_file
    profile_json_path = Path(settings.data_dir) / settings.profile_json_file
    profile_repository = FileProfileRepository(path=background_path, profile_json_path=profile_json_path)
    pii_detector = RegexPIIDetector() if settings.pii_enabled else None
    pii_processor = (
        PIIProcessingUseCase(detector=pii_detector, settings=settings)
        if (pii_detector and settings.pii_enabled)
        else None
    )

    # LLM service (OpenAI Chat Completions)
    llm_service = OpenAIChatService(
        model=settings.llm_model,
        api_key=settings.openai_api_key,
    )

    # Use-Case
    answer_use_case = AnswerQuestionUseCase(
        profile_repository=profile_repository,
        llm_service=llm_service,
        settings=settings,
        pii_processor=pii_processor,
    )

    # Controller
    chat_controller = ChatController(use_case=answer_use_case)

    return Container(
        settings=settings,
        profile_repository=profile_repository,
        llm_service=llm_service,
        answer_use_case=answer_use_case,
        chat_controller=chat_controller,
    pii_detector=pii_detector,
    pii_processor=pii_processor,
    )
