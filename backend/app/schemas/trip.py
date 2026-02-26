from pydantic import BaseModel
from typing import Optional, List


class TripRequest(BaseModel):
    destination: str
    duration: int
    budget: float
    travelers: int
    preferences: List[str]


class TripResponse(BaseModel):
    id: str
    destination: str
    duration: int
    budget: float
    travelers: int
    preferences: List[str]
    plan: Optional[str] = None
    status: str = "pending"


class TripOptimizeRequest(BaseModel):
    optimization_type: str  # "budget", "time", "experience"
