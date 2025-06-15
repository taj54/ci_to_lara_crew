import pytest
from validation.migration_validator import MigrationValidator


def test_missing_payload():
    validator = MigrationValidator("ci_to_lara", "ci2", "lara_8.x", None)
    result = validator.run()
    assert not result["success"]
    assert "Input payload is missing" in result["message"][0]["msg"]