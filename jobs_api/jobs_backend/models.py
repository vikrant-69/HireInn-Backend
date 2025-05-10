from typing import Optional, List
from pydantic import BaseModel, Field

class Job(BaseModel):
    id: Optional[str] = Field(alias="_id")  # or use str if you don't handle ObjectId directly
    company: str
    job_id: str
    job_title: str
    job_description: str
    qualifications: str
    location: str
    employment_type: Optional[str] = None
    compensation_details: Optional[str] = None
    other: Optional[str] = None

    class Config:
        validate_by_name = True
