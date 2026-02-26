from crewai.tools import tool
from tavily import Tavily
from app.config import settings


class TavilySearchTool:
    @tool("搜索旅行相关信息")
    def search(query: str) -> str:
        """
        搜索旅行相关信息，包括景点、酒店、美食、天气等。
        输入应该是清晰的搜索关键词。
        """
        tavily = Tavily(api_key=settings.TAVILY_API_KEY)
        results = tavily.search(query=query, max_results=5)

        if not results.get("results"):
            return "未找到相关信息"

        formatted = []
        for r in results["results"]:
            formatted.append(f"标题: {r.get('title', '')}\n内容: {r.get('content', '')}\n")

        return "\n\n".join(formatted)
