from fastapi import FastAPI
from routers import jobs
from database import get_db
import uvicorn 

app = FastAPI(
    title="Job API",
    description="API for fetching job postings from MongoDB",
    version="1.0.0",
)

app.include_router(jobs.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Job API"}

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )       