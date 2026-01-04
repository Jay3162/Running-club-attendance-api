from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/runs", tags=["run"])

class runCreate(BaseModel):
    user_id: int
    date: date
    distance: float 

# class Run(BaseModel):
#     user_id: int
#     date: date
#     distance: float

@router.post("/")
def runner(run: runCreate):
    return {"message": "run created", "run": run}

@router.get("/")
def run():
    return {"runs": []}