# 注意：这个测试需要有效的 API key
# 实际测试时可以 mock 或使用 pytest.mark.skip


def test_trip_planner_crew_init():
    from app.crew.planner_crew import TripPlannerCrew

    crew = TripPlannerCrew(
        destination="东京",
        duration=5,
        budget=10000,
        travelers=2,
        preferences=["美食", "购物"]
    )

    assert crew.destination == "东京"
    assert crew.duration == 5
    assert crew.budget == 10000
    assert crew.travelers == 2
    assert crew.preferences == ["美食", "购物"]
