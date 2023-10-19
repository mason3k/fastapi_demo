import pytest
from fastapi import status
from fastapi.testclient import TestClient

from fastapi_demo import app

client = TestClient(app)

existing_sauce = {
    "id": 1,
    "name": "Frank's RedHot",
    "brand": "Frank's",
    "scoville_scale": 450,
    "ingredients": ["Aged Cayenne Red Peppers", "Distilled Vinegar"],
    "flavor_notes": ["Tangy", "Spicy"],
    "bottle_size": 12.0,
    "price": "3.99",
}

existing_sauce_2 = {
    "id": 2,
    "name": "Sriracha",
    "brand": "Huy Fong",
    "scoville_scale": 2200,
    "ingredients": ["Chili", "Sugar", "Garlic", "Salt", "Vinegar"],
    "flavor_notes": ["Sweet", "Tangy", "Spicy"],
    "bottle_size": 17.0,
    "price": "4.49",
}


new_sauce = {
    "id": 99,
    "name": "Test Sauce",
    "brand": "Kirkland Signature",
    "scoville_scale": 1200,
    "bottle_size": 12,
    "flavor_notes": ["zany"],
}


def test_get_all():
    resp = client.get("/sauces/")
    assert resp.status_code == status.HTTP_200_OK
    content = resp.json()
    assert isinstance(content, list)
    assert existing_sauce in content


def test_get_one():
    resp = client.get("/sauces/1")
    assert resp.status_code == status.HTTP_200_OK
    content = resp.json()
    assert existing_sauce == content


def test_get_nonexistent():
    bad_id = 2000001
    resp = client.get(f"/sauces/{bad_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    error = resp.json()["detail"]
    assert str(bad_id) in error
    assert "does not exist" in error


def test_create():
    # id: int
    # name: str
    # brand: str
    # scoville_scale: NonNegativeInt | None = None
    # ingredients: list[str] | None = None
    # flavor_notes: list[str] | None = None
    # bottle_size: PositiveFloat | None = None
    # price: Decimal | None = None
    resp = client.post("/sauces/", json=new_sauce)
    assert resp.status_code == status.HTTP_201_CREATED
    assert new_sauce.items() <= resp.json().items()


def test_create_already_exists():
    existing_id = existing_sauce["id"]
    resp = client.post("/sauces/", json=new_sauce | {"id": existing_id})
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    error = resp.json()["detail"]
    assert str(existing_id) in error
    assert "already exists" in error


def test_create_bad_data():
    resp = client.post(
        "/sauces/",
        json={
            "id": 57,
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
            "id": 57,
            "brand": "incomplete",
        },
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    content = resp.json()["detail"]
    assert content[0]["type"] == "missing"
    assert content[0]["loc"] == ["body", "name"]


def test_update():
    existing_id = existing_sauce_2["id"]
    updates = {
        "id": existing_id,
        "name": "updated name",
        "brand": "updated brand",
        "scoville_scale": 12,
        "flavor_notes": ["Bright"],
    }
    resp = client.put(f"/sauces/{existing_id}", json=updates)
    resp.status_code == status.HTTP_200_OK
    assert {**existing_sauce_2, **updates}.items() <= resp.json().items()


@pytest.mark.xfail
def test_update_incomplete_data():
    existing_id = existing_sauce_2["id"]
    updates = {
        "id": existing_id,
        "flavor_notes": ["Bright"],
    }
    resp = client.put(f"/sauces/{existing_id}", json=updates)
    resp.status_code == status.HTTP_200_OK
    assert {**existing_sauce_2, **updates}.items() <= resp.json().items()


def test_bad_update():
    ...


def test_update_default_merging():
    ...


def test_delete():
    ...
