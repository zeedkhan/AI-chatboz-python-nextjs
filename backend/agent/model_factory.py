from typing import Any

import openai
from langchain.chat_models import ChatOpenAI
from pydantic import Field
from backend.schemas.agent import LLM_Model, ModelSettings

from backend.schemas.user import UserBase
from backend.setting import settings


openai.api_base = settings.openai_api_base


class WrappedChatOpenAI(ChatOpenAI):
    client: Any = Field(
        default=None,
        description="Meta private value but mypy will complain its missing",
    )
    max_tokens: int
    model_name: LLM_Model = Field(alias="model")


def create_model(
    model_settings: ModelSettings,
    user: UserBase,
    streaming: bool = False,
) -> WrappedChatOpenAI:

    return WrappedChatOpenAI(
        openai_api_key=settings.openai_api_key,
        temperature=model_settings.temperature,
        model=model_settings.model,
        max_tokens=model_settings.max_tokens,
        streaming=streaming,
        max_retries=5,
        model_kwargs={"user": user.email},
    )
