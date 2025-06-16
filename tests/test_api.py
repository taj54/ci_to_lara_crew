import pytest
from fastapi import status
from fastapi.testclient import TestClient
from routers.api import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


def test_successful_post(monkeypatch, client):
    class DummyValidator:
        def __init__(
            self, migration_direction, source_version, target_version, payload
        ):
            pass

        def run(self):
            return {"success": True, "message": ["ok"]}

    monkeypatch.setattr(
        "validation.migration_validator.MigrationValidator", DummyValidator
    )
    payload = {
        "migration_direction": "ci_to_lara",
        "source_version": "ci2",
        "target_version": "lara_8.x",
        "inputs": {"description": "bar"},
    }
    response = client.post("/ci-lara-ai-converter/run", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert "Lara8XCrew crew executed successfully." in response.json()["message"]


def test_validator_failure(monkeypatch, client):
    class DummyValidator:
        def __init__(
            self, migration_direction, source_version, target_version, payload
        ):
            pass

        def run(self):
            return {
                "success": False,
                "message": [
                    {
                        "loc": ["description"],
                        "msg": "Migrate from CodeIgniter 2 to Laravel 8.x",
                        "type": "value_error",
                    }
                ],
            }

    monkeypatch.setattr(
        "validation.migration_validator.MigrationValidator", DummyValidator
    )
    payload = {
        "migration_direction": "ci_to_lara",
        "source_version": "ci2",
        "target_version": "lara_8.x",
        "inputs": {"description": ""},
    }
    response = client.post("/ci-lara-ai-converter/run", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert (
        response.json()["detail"][0].get("msg") == "Migrate from CodeIgniter 2 to Laravel 8.x"
    )


def test_missing_inputs(monkeypatch, client):
    class DummyValidator:
        def __init__(
            self, migration_direction, source_version, target_version, payload
        ):
            pass

        def run(self):
            return {
                "success": False,
                "message": [
                    {
                        "type": "dict_type",
                        "loc": ["body", "inputs"],
                        "msg": "Input should be a valid dictionary",
                        "input": "none",
                    }
                ],
            }

    monkeypatch.setattr(
        "validation.migration_validator.MigrationValidator", DummyValidator
    )
    payload = {
        "migration_direction": "ci_to_lara",
        "source_version": "ci2",
        "target_version": "lara_8.x",
        "inputs": "None",
    }
    response = client.post("/ci-lara-ai-converter/run", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert (
        response.json()["detail"][0].get("msg") == "Input should be a valid dictionary"
    )


def test_invalid_schema(client):
    # Missing required fields
    payload = {
        "migration_direction": "ci_to_lara",
        "source_version": "ci2",
        # missing target_version and inputs
    }
    response = client.post("/ci-lara-ai-converter/run", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "target_version" in str(response.json())
