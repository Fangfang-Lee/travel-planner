from crewai import Agent
from langchain_openai import ChatOpenAI


def create_planner_agent():
    return Agent(
        role="行程规划师",
        goal="整合信息，制定合理的行程安排",
        backstory="""
        你是一位资深的行程规划师，擅长将各种旅行信息整合成完整、合理的行程计划。
        你会考虑时间安排、距离顺序、用户偏好等因素。
        """,
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model="gpt-4"),
    )
