from crewai.tools import BaseTool
from pydantic import Field
from tavily import TavilyClient
from app.config import settings


class TavilySearchTool(BaseTool):
    name: str = Field(default="search_travel_info", description="搜索旅行相关信息")
    description: str = Field(
        default="搜索旅行相关信息，包括景点、酒店、美食、天气等。输入应该是清晰的搜索关键词。",
        description="搜索旅行相关信息"
    )

    def _run(self, query: str) -> str:
        tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)
        results = tavily.search(query=query, max_results=5)

        if not results.get("results"):
            return "未找到相关信息"

        formatted = []
        for r in results["results"]:
            formatted.append(f"标题: {r.get('title', '')}\n内容: {r.get('content', '')}\n")

        return "\n\n".join(formatted)
