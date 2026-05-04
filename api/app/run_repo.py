from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List
from db import base
import sqlite3

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

def initialize_db():
    try:
        get_new_conn = base.get_db("user.db")
        get_new_conn.row_factory = sqlite3.Row
        new_cursor = get_new_conn.cursor()
    except Exception as e:
        print(e)
        raise e
    return new_cursor

#update
def update_run(run_id: int, run: runCreate):
    to_update = None
    try:
        new_cursor = initialize_db()
        selected_id = new_cursor.execute(
            """
            SELECT * FROM run_db WHERE id = ?
            """, (run_id,)
        )
        print("selected", selected_id)
        curr_id = dict(selected_id.fetchone())["id"]
        print("curr_id", curr_id)
        print("run_id", run_id)
        if curr_id != None and run_id == curr_id:
            new_cursor.execute(
                """
                UPDATE run_db
                SET user_id = ?, date = ?, distance = ?
                WHERE id = ?
                """, (run.user_id, run.date, run.distance, run_id,)
            )
            # print("new updated run", update_new_run)
            print("to update", to_update)
            print("the run", run)
            new_run = runId(id=run_id, **dict(run))
            to_update = new_run
            new_cursor.connection.commit()

            return new_run

    except Exception as e:
        print("An error has occured", e)
        raise e
    finally:
        new_cursor.connection.close()
        if to_update == None:
            raise HTTPException(
                status_code=404,
                detail="cannot update run that doesn't exist"
            )
#delete
def delete_run(run_id: int):
    to_delete = None
    try:
        new_cursor = initialize_db()
        new_cursor.execute(
            """
            SELECT * FROM run_db WHERE id = ?
            """, (run_id,)
        )
        selected_id = new_cursor.fetchone()
        if dict(selected_id) == None:
            return to_delete
        to_delete = dict(selected_id)
        new_cursor.execute(
            """
            DELETE FROM run_db WHERE id = ?
            """, (to_delete["id"],)
        )
        new_cursor.connection.commit()
        return to_delete
    

    except Exception as e:
        print(e)
        raise e
    finally:
        new_cursor.connection.close()
        if to_delete == None:
            raise HTTPException(
                status_code=404,
                detail="cannot delete run that doesn't exist"
            )
#post
def create_run(run: runCreate):
    # use the new model and set the id, the dump the existing run as a dictionary inside
    print("run", run)
    print("run dict", dict(run))
    run = runCreate(**dict(run))
    try: 
        get_new_cursor = initialize_db()
        get_new_cursor.execute(
            """
            INSERT INTO run_db (user_id, date, distance) VALUES (?, ?, ?)
            """, (run.user_id, run.date, run.distance)
        )
        # new_row = get_new_cursor.execute(
        #     """
        #     SELECT LAST_INSERT_ROWID();
        #     """
        # )
        new_row = get_new_cursor.execute("SELECT LAST_INSERT_ROWID()")
        new_run_id = new_row.fetchone()[0]
        get_new_cursor.connection.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        get_new_cursor.connection.close()
    new_run = runId(id=new_run_id, **dict(run))

    return new_run

#get
def get_run(run_id: int):
    run = None
    try:
        get_new_cursor = initialize_db()
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
        get_new_cursor.connection.close()
    return run

#simple get
def simple_get_run():
    result = []
    try:
        #ensure data that's passed back to pydantic model is acceptable
        get_all_cursor = initialize_db()
        get_all_cursor.execute(
            """
            SELECT * FROM run_db
            """
        )
        all_users = get_all_cursor.fetchall()
        result = [dict(row) for row in all_users]
        
    except Exception as e:
        print(e)
        raise e
    finally: 
        get_all_cursor.connection.close()
    return result
    
    