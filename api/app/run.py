from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List


router = APIRouter(prefix="/runs", tags=["run"])

#temporary state in memory
runs_db: List["runCreate"] = []

class runCreate(BaseModel):
    id: int
    user_id: int
    date: date
    distance: float 

# class Run(BaseModel):
#     user_id: int
#     date: date
#     distance: float

@router.post("/", response_model=runCreate)
def runner(run: runCreate):
    runs_db.append(run)
    return run

@router.get("/", response_model=List[runCreate])
def get_run():
    return runs_db

@router.get("/{run_id}", response_model=runCreate)
def run(run_id: int):
    for run in runs_db:
        if run.id == run_id:
            return run
    raise HTTPException(
        status_code=404,
        detail="user not found"
    )