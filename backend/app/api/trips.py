from fastapi import APIRouter, HTTPException
from app.schemas.trip import TripRequest, TripResponse, TripOptimizeRequest
from app.crew.planner_crew import TripPlannerCrew
import uuid
from datetime import datetime

router = APIRouter()

# In-memory storage (use database in production)
trips_db = {}


@router.post("/trips/plan", response_model=TripResponse)
async def create_trip_plan(request: TripRequest):
    trip_id = str(uuid.uuid4())

    trip = TripResponse(
        id=trip_id,
        destination=request.destination,
        duration=request.duration,
        budget=request.budget,
        travelers=request.travelers,
        preferences=request.preferences,
        status="processing"
    )

    trips_db[trip_id] = trip

    try:
        crew = TripPlannerCrew(
            destination=request.destination,
            duration=request.duration,
            budget=request.budget,
            travelers=request.travelers,
            preferences=request.preferences
        )
        result = crew.plan()

        trip.plan = str(result)
        trip.status = "completed"
        trips_db[trip_id] = trip

        return trip
    except Exception as e:
        trip.status = "failed"
        trips_db[trip_id] = trip
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trips/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: str):
    if trip_id not in trips_db:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trips_db[trip_id]


@router.get("/trips")
async def list_trips():
    return list(trips_db.values())


@router.post("/trips/{trip_id}/optimize")
async def optimize_trip(trip_id: str, request: TripOptimizeRequest):
    if trip_id not in trips_db:
        raise HTTPException(status_code=404, detail="Trip not found")

    trip = trips_db[trip_id]
    return {
        "trip_id": trip_id,
        "message": f"优化类型: {request.optimization_type}",
        "status": "optimized"
    }
