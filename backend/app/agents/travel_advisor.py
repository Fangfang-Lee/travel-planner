from crewai import Agent
from app.llms import create_llm


def create_travel_advisor():
    return Agent(
        role="旅行顾问",
        goal="深入了解用户的旅行需求和偏好",
        backstory="""
        你是一位经验丰富的旅行顾问，已经帮助数千位客户规划了完美的旅行。
        你擅长通过对话挖掘用户真正的需求，包括预算、偏好、旅行风格等。
        """,
        verbose=True,
        allow_delegation=False,
        llm=create_llm(),
    )
