from crewai import Agent
from langchain_openai import ChatOpenAI
from app.tools.tavily_search import TavilySearchTool


def create_search_agent():
    return Agent(
        role="搜索代理",
        goal="获取准确、及时的旅行信息",
        backstory="""
        你是一位专业的旅行信息搜索专家，擅长从各种来源获取最新的旅行信息。
        你能快速找到景点、酒店、餐厅、天气等用户需要的信息。
        """,
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model="gpt-4"),
        tools=[TavilySearchTool()],
    )
