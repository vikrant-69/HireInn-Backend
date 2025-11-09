from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo.collection import Collection
from typing import List, Optional
import random

# Assuming get_db is in 'database.py' and your updated Job model is in 'models.py'
from database import get_db 
from models import Job

router = APIRouter(
    prefix="/JOBS_V1",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)

# --- Endpoint Updated ---
@router.get("/", response_model=List[Job])
async def get_all_jobs(
    company: Optional[str] = Query(None, description="Filter by company name (case-insensitive)"),
    location: Optional[str] = Query(None, description="Filter by location (case-insensitive)"),
    db: Collection = Depends(get_db)
):
    """
    Retrieves a list of jobs, with optional filters for company and location.
    The results are randomly shuffled.
    """
    try:
        # The collection name should match where your job data is stored.
        jobs_collection: Collection = db["jobs"] 
        
        # Build the MongoDB query based on provided filters.
        # The $regex operator provides powerful pattern matching.
        query = {}
        if company:
            query["company"] = {"$regex": company, "$options": "i"} 
        if location:
            query["location"] = {"$regex": location, "$options": "i"} 

        # Fetch documents directly from MongoDB. The cursor is converted to a list.
        jobs_cursor = jobs_collection.find(query)
        jobs = list(jobs_cursor)
        
        # Shuffle the list of jobs randomly
        random.shuffle(jobs)

        # ⭐️ Return the list of documents directly. 
        # FastAPI will automatically validate it against List[Job]
        # and handle the conversion, including the '_id' to 'id' alias.
        return jobs[:10]

    except Exception as e:
        # It's good practice to log the actual error for debugging.
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An internal server error occurred while fetching jobs."
        )
    



    