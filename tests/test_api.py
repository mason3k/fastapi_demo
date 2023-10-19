import pytest
from fastapi import status
from fastapi.testclient import TestClient

from fastapi_demo import app

client = TestClient(app)


def test_delete(existing_sauce):
    resp = client.delete(f"/sauces/{existing_sauce.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert client.get(f"/sauces/{existing_sauce.id}").status_code == status.HTTP_404_NOT_FOUND


def test_get_all(existing_sauce):
    resp = client.get("/sauces/")
    assert resp.status_code == status.HTTP_200_OK
    content = resp.json()
    assert isinstance(content, list)
    assert existing_sauce.data in content


def test_get_one(existing_sauce):
    resp = client.get(f"/sauces/{existing_sauce.id}")
    assert resp.status_code == status.HTTP_200_OK
    content = resp.json()
    assert existing_sauce.data == content


def test_get_nonexistent():
    bad_id = 2000001
    resp = client.get(f"/sauces/{bad_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    error = resp.json()["detail"]
    assert str(bad_id) in error
    assert "does not exist" in error


def test_create(new_sauce):
    resp = client.post(f"/sauces/{new_sauce.id}", json=new_sauce.data)
    assert resp.status_code == status.HTTP_201_CREATED
    assert new_sauce.data.items() <= resp.json().items()
    assert client.get(f"/sauces/{new_sauce.id}").status_code == status.HTTP_200_OK


def test_create_gen_id(new_sauce):
    resp = client.post("/sauces/", json=new_sauce.data)
    assert resp.status_code == status.HTTP_201_CREATED
    assert new_sauce.data.items() <= resp.json().items()


def test_create_already_exists(existing_sauce, new_sauce):
    resp = client.post(f"/sauces/{existing_sauce.id}", json=new_sauce.data)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    error = resp.json()["detail"]
    assert str(existing_sauce.id) in error
    assert "already exists" in error


def test_create_bad_data():
    resp = client.post(
        "/sauces/",
        json={
            "name": "bad",
            "brand": "bad",
            "scoville_scale": "not a number",
        },
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    content = resp.json()["detail"]
    assert content[0]["type"] == "int_parsing"
    assert content[0]["loc"] == ["body", "scoville_scale"]


def test_create_missing_data():
    resp = client.post(
        "/sauces/",
        json={
            "brand": "incomplete",
        },
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    content = resp.json()["detail"]
    assert content[0]["type"] == "missing"
    assert content[0]["loc"] == ["body", "name"]


def test_update(existing_sauce_2):
    updates = {
        "name": "updated name",
        "brand": "updated brand",
        "scoville_scale": 12,
        "flavor_notes": ["Bright"],
    }
    resp = client.put(f"/sauces/{existing_sauce_2.id}", json=updates)
    resp.status_code == status.HTTP_200_OK
    assert {**existing_sauce_2.data, **updates}.items() <= resp.json().items()
    assert client.get(f"/sauces/{existing_sauce_2.id}").json() == resp.json()


@pytest.mark.xfail
def test_update_incomplete_data(existing_sauce_2):
    updates = {
        "id": existing_sauce_2.id,
        "flavor_notes": ["Bright"],
    }
    resp = client.put(f"/sauces/{existing_sauce_2.id}", json=updates)
    resp.status_code == status.HTTP_200_OK
    assert {**existing_sauce_2, **updates}.items() <= resp.json().items()
    assert client.get(f"/sauces/{existing_sauce_2.id}").json() == resp.json()


def test_bad_update(existing_sauce_2):
    updates = {
        "id": existing_sauce_2.id,
        "name": "updated name",
        "brand": "updated brand",
        "bottle_size": -3,
    }
    resp = client.put(f"/sauces/{existing_sauce_2.id}", json=updates)
    resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    content = resp.json()["detail"]
    assert content[0]["type"] == "greater_than"
    assert content[0]["loc"] == ["body", "bottle_size"]


def test_update_does_not_exist():
    nonexistent_id = 789
    updates = {
        "id": nonexistent_id,
        "name": "updated name",
        "brand": "updated brand",
        "bottle_size": 10,
    }
    resp = client.put(f"/sauces/{nonexistent_id}", json=updates)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    content = resp.json()["detail"]
    assert str(nonexistent_id) in content
    assert "does not exist" in content
