from main import app
import pytest
from fastapi.testclient import TestClient
from db import base
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS test_db (user_id INTEGER, date TEXT, distance INTEGER, id INTEGER PRIMARY KEY AUTOINCREMENT)
    """
)

def get_test_db():

    return conn
app.dependency_overrides[base.get_db] = get_test_db
#sqlite:///:memory:

client = TestClient(app)



def test_get_all_runs():
    response = client.get("/runs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    data = response.json()
    if data:
        assert "user_id" in data[0]
        assert "date" in data[0]
        assert "distance" in data[0]
        assert "id" in data[0]

def test_create_run():
    payload = {"user_id": 1, "date": "2026-04-23", "distance": 5.5}
    response_post = client.post("/runs", json=payload)
    assert response_post.status_code == 200
    post_data = response_post.json()
    response_get = client.get("/runs")
    data = response_get.json()
    assert response_get.status_code == 200
    assert isinstance(data, list)
    assert post_data["date"] == "2026-04-23"
    assert post_data["user_id"] == 1
    assert post_data["id"] in [item["id"] for item in data]
    exists_in_db = [item["date"] for item in data if item["id"] == post_data["id"]]
    assert len(exists_in_db) == 1
    # assert exists_in_db[0] == post_data["date"]

def test_delete_run():
    payload = {"user_id": 1, "date": "2026-04-23", "distance": 5.5}
    response_post = client.post("/runs", json=payload)
    assert response_post.status_code == 200
    created = response_post.json()
    response_delete = client.delete(f"/runs/{created['id']}")
    delete_json = response_delete.json()
    assert response_delete.status_code == 200
    assert delete_json["id"] == created["id"]
    assert delete_json == created
    last_get_check = client.get("/runs")
    new_data = last_get_check.json()
    assert created["id"] not in [item["id"] for item in new_data]
