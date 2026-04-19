from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List
from db import base
import sqlite3

router = APIRouter(prefix="/runs", tags=["run"])

# print("db", base.get_db("user.db"))

# new_runs_db = base.get_db("user.db")

# print("new db", new_runs_db)

# cursor = new_runs_db.cursor()

# cursor.execute(
#     """
#     SELECT * FROM run_db
#     """
# )

# print("all data", cursor.fetchall())

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
    # use the new model and set the id, the dump the existing run as a dictionary inside
    run = runCreate(**run.dict())
    try: 
        get_new_conn = base.get_db("user.db")
        get_new_cursor = get_new_conn.cursor()
        get_new_cursor.execute(
            """
            INSERT INTO run_db (user_id, date, distance) VALUES (?, ?, ?)
            """, (run.user_id, run.date, run.distance)
        )
        print("my run", run)
        # new_row = get_new_cursor.execute(
        #     """
        #     SELECT LAST_INSERT_ROWID();
        #     """
        # )
        new_row = get_new_cursor.execute("SELECT LAST_INSERT_ROWID()")
        new_run_id = new_row.fetchone()[0]
    except Exception as e:
        print(e)
        raise e
    finally:
        get_new_conn.commit()
        get_new_conn.close()
    print("new_run_id", new_run_id)
    new_run = runId(id=new_run_id, **run.dict())

    return new_run

#get
def get_run(run_id: int):
    run = None
    try:
        get_new_conn = base.get_db("user.db")
        get_new_conn.row_factory = sqlite3.Row
        get_new_cursor = get_new_conn.cursor()
        get_new_cursor.execute(
            """
            SELECT * FROM run_db WHERE id = ?
            """, (run_id,)
        )
        new_id = get_new_cursor.fetchone()
        if new_id:
            run = dict(new_id)
        else:
            raise HTTPException(
                status_code=404,
                detail="user not found"
            )
    except Exception as e:
        print(e)
        raise e
    finally:
        get_new_conn.close()
    return run

#simple get
def simple_get_run():
    result = []
    try:
        get_new_conn = base.get_db("user.db")
        #ensure data that's passed back to pydantic model is acceptable
        get_new_conn.row_factory = sqlite3.Row
        get_all_cursor = get_new_conn.cursor()
        get_all_cursor.execute(
            """
            SELECT * FROM run_db
            """
        )
        all_users = get_all_cursor.fetchall()
        print("all_users", all_users)
        result = [dict(row) for row in all_users]
        print("result", result)
        
    except Exception as e:
        print(e)
        raise e
    finally: 
        get_new_conn.close()
    return result
    
    