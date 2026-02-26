import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # OpenAI (可选)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # MiniMax API
    MINIMAX_API_KEY: str = os.getenv("MINIMAX_API_KEY", "")
    MINIMAX_MODEL: str = os.getenv("MINIMAX_MODEL", "MiniMax-M2.5")

    # Tavily Search
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # App Settings
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))


settings = Settings()
