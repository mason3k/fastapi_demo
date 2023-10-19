from collections import namedtuple
from unittest.mock import patch

import pytest

from fastapi_demo.db import MockDb

TestSauce = namedtuple("TestSauce", "id data")


@pytest.fixture(autouse=True)
def no_delay():
    """Recreate the database for ever test so there are not dependencies between tests"""
    with patch("fastapi_demo.main.DB", MockDb()):
        yield


@pytest.fixture
def existing_sauce():
    return TestSauce(
        1,
        {
            "name": "Frank's RedHot",
            "brand": "Frank's",
            "scoville_scale": 450,
            "ingredients": ["Aged Cayenne Red Peppers", "Distilled Vinegar"],
            "flavor_notes": ["Tangy", "Spicy"],
            "bottle_size": 12.0,
            "price": "3.99",
        },
    )


@pytest.fixture
def existing_sauce_2():
    return TestSauce(
        2,
        {
            "name": "Sriracha",
            "brand": "Huy Fong",
            "scoville_scale": 2200,
            "ingredients": ["Chili", "Sugar", "Garlic", "Salt", "Vinegar"],
            "flavor_notes": ["Sweet", "Tangy", "Spicy"],
            "bottle_size": 17.0,
            "price": "4.49",
        },
    )


@pytest.fixture
def new_sauce():
    return TestSauce(
        99,
        {
            "name": "Test Sauce",
            "brand": "Kirkland Signature",
            "scoville_scale": 1200,
            "bottle_size": 12,
            "flavor_notes": ["zany"],
        },
    )
