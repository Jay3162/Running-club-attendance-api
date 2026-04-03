from fastapi import APIRouter
from typing import List
from api.app.run_repo import runCreate, runId
from api.app import run_repo

router = APIRouter(prefix="/runs", tags=["run"])

@router.put("/", response_model=runId)
def update_run(run: runId):
    print("run", run)
    print("runner", run.dict())
    # match the user id
    # get the fields
    print("id", run.id)
    print("date", run.date)
    # update the fields
    updated_run = runId(**run.dict())
    print("updated_run", updated_run)
    # return the updated fields
    return run

@router.delete("/", response_model=runId)
def remove_run(run_id: int):
    return run_repo.delete_run(run_id)

@router.post("/", response_model=runId)
def runner(run: runCreate):
    return run_repo.create_run(run)
    

@router.get("/{run_id}", response_model=runId)
def run(run_id: int):
    return run_repo.get_run(run_id)

@router.get("/", response_model=List[runId])
def get_run():
    return run_repo.simple_get_run(run_repo.runs_db)