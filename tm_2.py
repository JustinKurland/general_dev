import pytest
from unittest.mock import patch, MagicMock
from src.threat_metrix import ThreatMetrixDataExtraction
import aiohttp
import json
import os

@pytest.fixture
def mock_bigquery():
    with patch('PA.threat_metrix.bigquery.Client', return_value=MagicMock()):
        yield

@pytest.fixture
def mock_config_file(tmp_path):
    """Creates a mock config.json file for testing."""
    config_data = {
        "threat_metrix": {"api_key": "mock_threat_metrix_key"},
        "virustotal": {"api_key": "mock_virustotal_key"},
        "censys": {"api_id": "mock_censys_id", "api_secret": "mock_censys_secret"}
    }
    # Create a temporary file for config.json
    config_path = tmp_path / "config.json"
    with open(config_path, "w") as file:
        json.dump(config_data, file)
    yield str(config_path)
    os.remove(config_path)

@patch('PA.threat_metrix.aiohttp.ClientSession.get')
@pytest.mark.asyncio
async def test_enrich_with_virus_total_success(mock_get, mock_bigquery, mock_config_file):
    """Test successful VirusTotal enrichment."""
    tm_instance = ThreatMetrixDataExtraction(config_path=mock_config_file)

    mock_response = MagicMock()
    mock_response.status = 200

    async def mock_json():
        return {'example_key': 'example_value'}
    
    mock_response.json = mock_json
    mock_get.return_value.__aenter__.return_value = mock_response

    async with aiohttp.ClientSession() as session:
        result = await tm_instance.enrich_with_virus_total(session, '8.8.8.8')

    assert result == {'example_key': 'example_value'}

@patch('PA.threat_metrix.aiohttp.ClientSession.get')
@pytest.mark.asyncio
async def test_enrich_with_virus_total_failure(mock_get, mock_bigquery, mock_config_file):
    """Test VirusTotal enrichment failure."""
    tm_instance = ThreatMetrixDataExtraction(config_path=mock_config_file)

    mock_get.return_value.status = 500

    async with aiohttp.ClientSession() as session:
        result = await tm_instance.enrich_with_virus_total(session, '8.8.8.8')

    assert result == {}

@pytest.mark.asyncio
async def test_enrich_with_virus_total_invalid_input(mock_bigquery, mock_config_file):
    """Test VirusTotal enrichment with invalid IP input."""
    tm_instance = ThreatMetrixDataExtraction(config_path=mock_config_file)

    async with aiohttp.ClientSession() as session:
        result = await tm_instance.enrich_with_virus_total(session, 'invalid_ip')

    assert result == {}
