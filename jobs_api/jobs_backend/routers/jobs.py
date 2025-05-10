from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_db
from models import Job
from typing import List, Optional
from bson import ObjectId
import json
from pymongo.collection import Collection

router = APIRouter(
    prefix="/test_jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

# @router.get("/", response_model=List[Job])
# async def get_all_jobs(db=Depends(get_db)):
#     jobs_collection = db["test_jobs"]
#     jobs = list(jobs_collection.find({}))
#     return json.loads(json.dumps(jobs, cls=JSONEncoder))


@router.get("/", response_model=List[Job])
async def get_all_jobs(
    company: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    db=Depends(get_db)
):
    jobs_collection: Collection = db["test_jobs"]

    # Build MongoDB query based on provided filters
    query = {}
    if company:
        query["company"] = {"$regex": company, "$options": "i"} 
    if location:
        query["location"] = {"$regex": location, "$options": "i"} 

    jobs = list(jobs_collection.find(query))
    return json.loads(json.dumps(jobs, cls=JSONEncoder))
