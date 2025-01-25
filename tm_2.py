import pytest
from unittest.mock import patch, MagicMock
from src.threat_metrix import ThreatMetrixDataExtraction
import aiohttp

@pytest.fixture
def mock_bigquery():
    with patch('PA.threat_metrix.bigquery.Client', return_value=MagicMock()):
        yield

@patch('PA.threat_metrix.aiohttp.ClientSession.get')
@pytest.mark.asyncio
async def test_enrich_with_virus_total_success(mock_get, mock_bigquery):
    
    tm_instance = ThreatMetrixDataExtraction(config_path="config.json")

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
async def test_enrich_with_virus_total_failure(mock_get, mock_bigquery):

    tm_instance = ThreatMetrixDataExtraction(config_path="config.json")

    mock_get.return_value.status = 500

    async with aiohttp.ClientSession() as session:
        result = await tm_instance.enrich_with_virus_total(session, '8.8.8.8')

    assert result == {}

@pytest.mark.asyncio
async def test_enrich_with_virus_total_invalid_input(mock_bigquery):
    
    tm_instance = ThreatMetrixDataExtraction(config_path="config.json")

    async with aiohttp.ClientSession() as session:
        result = await tm_instance.enrich_with_virus_total(session, 'invalid_ip')

    assert result == {}
