import pytest
from unittest.mock import patch
from rss_collector.proxy import fetch_feed_content_with_proxy

def test_fetch_feed_content_with_proxy_debug(mocker):
    """
    Test fetch_feed_content_with_proxy with detailed debugging to capture mismatches.
    """

    # Mocked proxy settings
    mock_proxy_settings = {
        "app_proxy": "http://mock_proxy.com:85",
        "username": "mock_user",
        "password": "mock_password",
    }

    # Mock get_proxy_settings function
    mocker.patch("rss_collector.utils.get_proxy_settings", return_value=mock_proxy_settings)

    # Mock subprocess.check_output
    mock_subprocess = mocker.patch("subprocess.check_output", return_value="Mocked Response")

    # Test input
    feed_url = "https://example.com/rss"

    # Call the function
    response = fetch_feed_content_with_proxy(feed_url)

    # Construct expected command
    expected_command = (
        f"echo '{mock_proxy_settings['password']}' | "
        f"curl -s -x '{mock_proxy_settings['app_proxy']}' "
        f"-U '{mock_proxy_settings['username']}' "
        f"'{feed_url}' --proxy-ntlm"
    )

    # Debugging: Print actual vs. expected command
    print("\n--- Debugging Subprocess Call ---")
    print(f"Expected Command: {expected_command}")
    print(f"Actual Call Arguments: {mock_subprocess.call_args}")

    # Assert subprocess.call arguments
    mock_subprocess.assert_called_once_with(expected_command, shell=True, text=True)

    # Assert response
    assert response == "Mocked Response"
