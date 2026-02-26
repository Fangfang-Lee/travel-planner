from crewai import Agent
from app.llms import create_llm
from app.tools.tavily_search import TavilySearchTool


def create_weather_agent():
    return Agent(
        role="天气与应急代理",
        goal="提供天气信息和应急处理方案",
        backstory="""
        你是一位旅行安全专家，擅长预测天气风险并提供应急方案。
        你会关注目的地在旅行期间可能遇到的天气问题并给出建议。
        """,
        verbose=True,
        allow_delegation=False,
        llm=create_llm(),
        tools=[TavilySearchTool()],
    )
