from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List


router = APIRouter(prefix="/runs", tags=["run"])

#temporary state in memory
runs_db: List["runCreate"] = []
next_run_id = 1

class runCreate(BaseModel):
    # id: int
    user_id: int
    date: date
    distance: float

# plug in runCreate model to avoid repeatition and valid users input without cleaning it
class runId(runCreate):
    id: int

@router.post("/", response_model=runId)
def runner(run: runCreate):
    # run id needs to be referenced as a global variable
    global next_run_id
    if len(runs_db) >= 0:
        # use the new model and set the id, the dump the existing run as a dictionary inside
        run = runId(id=next_run_id, **run.dict())
        runs_db.append(run)
        next_run_id += 1

    else:
        run = runId(id=next_run_id, **run.dict())
        runs_db.append(run)
        next_run_id += 1

    return run

@router.get("/", response_model=List[runId])
def get_run():
    return runs_db

@router.get("/{run_id}", response_model=runId)
def run(run_id: int):
    for run in runs_db:
        if run.id == run_id:
            return run
    raise HTTPException(
        status_code=404,
        detail="user not found"
    )