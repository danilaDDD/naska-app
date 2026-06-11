import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import logging
import pytest
import db
from main import app  # noqa: E402


@pytest.fixture(autouse=True)
def disable_logging():
    logging.getLogger("naska").setLevel(logging.CRITICAL)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def users_db():
    db._users.clear()
    db._next_id = 1
    yield db._users
    db._users.clear()
    db._next_id = 1