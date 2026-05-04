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



# def test_get_all_runs():
#     response = client.get("/runs")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#     data = response.json()
#     if data:
#         assert "user_id" in data[0]
#         assert "date" in data[0]
#         assert "distance" in data[0]
#         assert "id" in data[0]


# def test_create_run():
#     payload = {"user_id": 1, "date": "2026-04-23", "distance": 5.5}
#     response_post = client.post("/runs", json=payload)
#     assert response_post.status_code == 200
#     post_data = response_post.json()
#     response_get = client.get("/runs")
#     data = response_get.json()
#     assert response_get.status_code == 200
#     assert isinstance(data, list)
#     assert post_data["date"] == "2026-04-23"
#     assert post_data["user_id"] == 1
#     assert post_data["id"] in [item["id"] for item in data]
#     exists_in_db = [item["date"] for item in data if item["id"] == post_data["id"]]
#     assert len(exists_in_db) == 1
#     client.delete(f"/runs/{post_data['id']}")

# def test_get_one_run():
#     payload = {"user_id": 1, "date": "2026-04-23", "distance": 5.5}
#     response_post = client.post("/runs", json=payload)
#     assert response_post.status_code == 200
#     post_data = response_post.json()

#     one_run = post_data
#     print(one_run['id'])
#     response = client.get(f"/runs/{one_run['id']}")
#     assert response.status_code == 200
#     data = response.json()
#     assert one_run['id'] == data['id']
#     client.delete(f"/runs/{one_run['id']}")

# def test_delete_run():
#     payload = {"user_id": 1, "date": "2026-04-23", "distance": 5.5}
#     response_post = client.post("/runs", json=payload)
#     assert response_post.status_code == 200
#     created = response_post.json()
#     response_delete = client.delete(f"/runs/{created['id']}")
#     delete_json = response_delete.json()
#     assert response_delete.status_code == 200
#     assert delete_json["id"] == created["id"]
#     assert delete_json == created
#     last_get_check = client.get("/runs")
#     new_data = last_get_check.json()
#     assert created["id"] not in [item["id"] for item in new_data]

def test_update_run():
    payload = {"user_id": 1, "date": "2026-05-04", "distance": 5.5}
    response_post = client.post("/runs", json=payload)
    assert response_post.status_code == 200
    post_data = response_post.json()
    print("post_data", post_data)
    new_payload = {"user_id": 2, "date": "2026-05-04", "distance": 7.5}
    response_update = client.put(f"/runs/{post_data['id']}", json=new_payload)
    assert response_update.status_code == 200
    update_data = response_update.json()
    print("update_data", update_data)
    assert update_data["user_id"] != post_data["user_id"]
    assert update_data["distance"] != post_data["distance"]
    bad_payload = {"user_id": 7, "date": "2026-05-04", "distance": 12, "id": 999}
    bad_update_resp = client.put(f"/runs/{post_data['id']}", json=bad_payload)
    assert bad_update_resp.status_code == 200
    bad_data = bad_update_resp.json()
    assert bad_data["id"] == post_data["id"]
    assert bad_data["id"] != 999
    ghost_update = client.put(f"/runs/9999999", json=new_payload)
    assert ghost_update.status_code == 404
    bad_date_payload = {"user_id": 2, "date": "2026-05-4", "distance": 19.5}
    validation_resp = client.put(f"/runs/{post_data['id']}", json=bad_date_payload)
    assert validation_resp.status_code == 422

    

