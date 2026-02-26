from crewai import Crew, Task, Process
from app.agents import (
    create_travel_advisor,
    create_search_agent,
    create_planner_agent,
    create_budget_analyst,
    create_weather_agent,
)


class TripPlannerCrew:
    def __init__(self, destination: str, duration: int, budget: float,
                 travelers: int, preferences: list):
        self.destination = destination
        self.duration = duration
        self.budget = budget
        self.travelers = travelers
        self.preferences = preferences

        self.travel_advisor = create_travel_advisor()
        self.search_agent = create_search_agent()
        self.planner = create_planner_agent()
        self.budget_analyst = create_budget_analyst()
        self.weather_agent = create_weather_agent()

    def plan(self):
        # Define tasks
        clarify_task = Task(
            description=f"Clarify travel requirements for {self.destination}, "
                        f"{self.duration} days, budget {self.budget} yuan, "
                        f"{self.travelers} travelers, preferences: {self.preferences}",
            agent=self.travel_advisor,
            expected_output="清晰的需求清单，包括必去景点、住宿偏好、餐饮要求等",
        )

        search_task = Task(
            description=f"Search for travel information about {self.destination}, "
                        f"including attractions, hotels, restaurants, weather",
            agent=self.search_agent,
            expected_output="搜索结果摘要，包含景点、酒店、美食、天气信息",
            context=[clarify_task],
        )

        plan_task = Task(
            description=f"Create a detailed travel plan for {self.destination}, "
                        f"{self.duration} days based on search results",
            agent=self.planner,
            expected_output="详细的每日行程安排",
            context=[clarify_task, search_task],
        )

        budget_task = Task(
            description=f"Calculate estimated cost for the trip to {self.destination}, "
                        f"budget: {self.budget} yuan for {self.travelers} people",
            agent=self.budget_analyst,
            expected_output="费用明细表和优化建议",
            context=[plan_task],
        )

        weather_task = Task(
            description=f"Check weather forecast for {self.destination} "
                        f"for the next {self.duration} days and provide tips",
            agent=self.weather_agent,
            expected_output="天气预报和旅行建议",
            context=[plan_task],
        )

        # Create crew
        crew = Crew(
            agents=[
                self.travel_advisor,
                self.search_agent,
                self.planner,
                self.budget_analyst,
                self.weather_agent,
            ],
            tasks=[clarify_task, search_task, plan_task, budget_task, weather_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return result
