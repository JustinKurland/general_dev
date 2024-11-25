import pytest
from unittest.mock import patch
from rss_collector.utils import get_proxy_settings
from rss_collector.proxy import fetch_feed_content_with_proxy

def test_fetch_feed_content_with_proxy_debug(mocker):
    """
    Test fetch_feed_content_with_proxy with a mock subprocess call and mocked proxy settings.
    """

    # Mocked proxy settings
    mock_proxy_settings = {
        "app_proxy": "http://mock_proxy.com:85",
        "username": "mock_user",
        "password": "mock_password",
    }

    # Apply the mock for get_proxy_settings
    mocker.patch("rss_collector.utils.get_proxy_settings", return_value=mock_proxy_settings)

    # Mock subprocess call
    mock_subprocess = mocker.patch("subprocess.check_output", return_value="Mocked Response")

    # Test inputs
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

    # Debugging Outputs
    print("\n--- Debugging Mock Application ---")
    print("Mocked proxy settings:", mock_proxy_settings)

    print("\n--- Debugging Expected Command ---")
    print("Expected Command:", expected_command)

    print("\n--- Debugging Mock Subprocess Call ---")
    try:
        # Capture actual calls for more details
        calls = mock_subprocess.call_args_list
        print("Mock Subprocess Call Args:", calls)

        # Assert subprocess call
        mock_subprocess.assert_called_once_with(expected_command, shell=True, text=True)
        print("Mock subprocess called correctly.")
    except AssertionError as e:
        print("Error in subprocess call assertion:", e)
        raise

    # Final assertion for function output
    assert response == "Mocked Response", "Function did not return the expected mocked response"
