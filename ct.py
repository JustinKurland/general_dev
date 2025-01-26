import pytest
import json
import os

@pytest_asyncio.fixture
async def mock_config_file(tmp_path):
    """Creates a mock config.json file for testing."""
    config_data = {
        "threat_metrix": {"api_key": "mock_threat_metrix_key"},
        "virustotal": {"api_key": "mock_virustotal_key"},
        "censys": {"api_id": "mock_censys_id", "api_secret": "mock_censys_secret"},
    }
    # Create a temporary file for config.json
    config_path = tmp_path / "config.json"
    with open(config_path, "w") as file:
        json.dump(config_data, file)
    yield str(config_path)
    os.remove(config_path)
