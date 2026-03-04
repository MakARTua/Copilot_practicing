import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture()
def client():
    """Provide a TestClient for the FastAPI app."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Snapshot and restore the in-memory `activities` between tests.

    This ensures tests are isolated and modifications to the module-level
    `activities` dict do not leak between tests.
    """
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
