"""Activities API endpoints"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/trip/{trip_id}")
async def get_trip_activities(trip_id: int):
    """Get all activities for a specific trip

    TODO: Implement activities listing
    - Validate user has access to trip
    - Query activities for trip
    - Return list of activities
    """
    return {"message": f"Get activities for trip {trip_id} - TODO: Implement", "activities": []}


@router.get("/{activity_id}")
async def get_activity(activity_id: int):
    """Get a specific activity by ID

    TODO: Implement activity retrieval
    - Validate user has access to activity
    - Query activity from database
    - Return activity details
    """
    return {"message": f"Get activity {activity_id} endpoint - TODO: Implement"}


@router.post("/trip/{trip_id}")
async def create_activity(trip_id: int):
    """Create a new activity for a trip

    TODO: Implement activity creation
    - Validate trip exists and user owns it
    - Validate activity data
    - Create activity in database
    - Return created activity
    """
    return {"message": f"Create activity for trip {trip_id} - TODO: Implement"}


@router.put("/{activity_id}")
async def update_activity(activity_id: int):
    """Update an existing activity

    TODO: Implement activity update
    - Validate user owns activity (through trip)
    - Update activity in database
    - Return updated activity
    """
    return {"message": f"Update activity {activity_id} endpoint - TODO: Implement"}


@router.delete("/{activity_id}")
async def delete_activity(activity_id: int):
    """Delete an activity

    TODO: Implement activity deletion
    - Validate user owns activity (through trip)
    - Delete activity from database
    - Return success message
    """
    return {"message": f"Delete activity {activity_id} endpoint - TODO: Implement"}
