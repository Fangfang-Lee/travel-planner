from crewai import Agent
from langchain_openai import ChatOpenAI


def create_budget_analyst():
    return Agent(
        role="预算分析师",
        goal="计算旅行费用并提供优化建议",
        backstory="""
        你是一位精明的预算分析师，擅长计算各种旅行费用并提供节省建议。
        你会根据行程给出详细的费用 breakdown。
        """,
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model="gpt-4"),
    )
