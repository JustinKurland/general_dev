import pytest
from unittest.mock import patch, MagicMock
from src.user_agent import UserAgentAnalysis
import aiohttp

@pytest.fixture
def mock_bigquery():
    with patch('PA.user_agent.bigquery.Client', return_value=MagicMock()):
        yield

@patch('PA.user_agent.aiohttp.ClientSession.get')
@pytest.mark.asyncio
async def test_enrich_with_virus_total_success(mock_get, mock_bigquery):
    ua_instance = UserAgentAnalysis(config_path="config.json")

    mock_response = MagicMock()
    mock_response.status = 200

    async def mock_json():
        return {'example_key': 'example_value'}
    
    mock_response.json = mock_json
    mock_get.return_value.__aenter__.return_value = mock_response

    async with aiohttp.ClientSession() as session:
        result = await ua_instance.enrich_with_virus_total(session, 'Mozilla/5.0')

    assert result == {'example_key': 'example_value'}

@patch('PA.user_agent.aiohttp.ClientSession.get')
@pytest.mark.asyncio
async def test_enrich_with_virus_total_failure(mock_get, mock_bigquery):
    ua_instance = UserAgentAnalysis(config_path="config.json")

    mock_get.return_value.status = 500

    async with aiohttp.ClientSession() as session:
        result = await ua_instance.enrich_with_virus_total(session, 'Mozilla/5.0')

    assert result == {}

def test_parse_user_agent_valid(mock_bigquery):
    ua_instance = UserAgentAnalysis(config_path="config.json")
    user_agent_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    result = ua_instance.parse_user_agent(user_agent_string)
    assert result['status'] == 'valid'
    assert result['browser'] == 'Chrome'
    assert result['os'] == 'Windows'

def test_parse_user_agent_invalid(mock_bigquery):
    ua_instance = UserAgentAnalysis(config_path="config.json")
    user_agent_string = "invalid_user_agent"
    result = ua_instance.parse_user_agent(user_agent_string)
    assert result['status'] == 'invalid'
