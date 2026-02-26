from langchain_openai import ChatOpenAI
from app.config import settings


def create_llm(model: str = None, temperature: float = 0.7):
    """
    创建 LLM 实例。
    优先使用 MiniMax，如果未配置则回退到 OpenAI。
    """
    # 如果配置了 MiniMax API Key，使用 MiniMax
    if settings.MINIMAX_API_KEY:
        return ChatOpenAI(
            model=model or settings.MINIMAX_MODEL,
            temperature=temperature,
            openai_api_key=settings.MINIMAX_API_KEY,
            openai_api_base="https://api.minimax.chat/v1",
        )
    # 否则使用 OpenAI
    elif settings.OPENAI_API_KEY:
        return ChatOpenAI(
            model=model or "gpt-4",
            temperature=temperature,
            openai_api_key=settings.OPENAI_API_KEY,
        )
    else:
        raise ValueError("请配置 OPENAI_API_KEY 或 MINIMAX_API_KEY")
