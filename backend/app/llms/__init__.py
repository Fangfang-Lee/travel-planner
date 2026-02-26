from crewai.llms.providers.openai.completion import OpenAICompletion
from app.config import settings


def create_llm(model: str = None, temperature: float = 0.7):
    """
    创建 LLM 实例。
    优先使用 MiniMax，如果未配置则回退到 OpenAI。
    """
    # 获取模型名称
    model_name = model or settings.MINIMAX_MODEL or "abab6.5s-chat"

    # 如果配置了 MiniMax API Key，使用 MiniMax
    if settings.MINIMAX_API_KEY:
        return OpenAICompletion(
            model=model_name,
            temperature=temperature,
            api_key=settings.MINIMAX_API_KEY,
            base_url="https://api.minimax.chat/v1",
        )
    # 否则使用 OpenAI
    elif settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "dummy":
        return OpenAICompletion(
            model=model or "gpt-4o",
            temperature=temperature,
            api_key=settings.OPENAI_API_KEY,
        )
    else:
        raise ValueError("请配置 OPENAI_API_KEY 或 MINIMAX_API_KEY")
