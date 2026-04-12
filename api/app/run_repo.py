from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List

router = APIRouter(prefix="/runs", tags=["run"])

#temporary state in memory
runs_db: List["runCreate"] = []
next_run_id = 1

class runCreate(BaseModel):
    user_id: int
    date: date
    distance: float

# plug in runCreate model to avoid repeatition and valid users input without cleaning it
class runId(runCreate):
    id: int

#update
def update_run(run: runId):
    target_index = 0
    for runs in runs_db:
        if runs.id == run.id:
            new_run = runId(**run.dict())
            target_index = runs_db.index(runs)
            runs_db[target_index] = new_run
            return runs_db[target_index]
    raise HTTPException(
        status_code=404,
        detail="user not found"
    ) 

#delete
def delete_run(run_id: int):
    for run in runs_db:
        if run_id == run.id:
            rm_val = runs_db.index(run)
            runs_db.pop(rm_val)
            return run
    raise HTTPException(
        status_code=404,
        detail="user not found"
    )
#post
def create_run(run: runCreate):
    global next_run_id
    # use the new model and set the id, the dump the existing run as a dictionary inside
    run = runId(id=next_run_id, **run.dict())
    runs_db.append(run)
    next_run_id += 1

    return run

#get
def get_run(run_id: int):
    for run in runs_db:
        if run.id == run_id:
            return run
    raise HTTPException(
        status_code=404,
        detail="user not found"
    )
#simple get
def simple_get_run():
    return runs_db
    