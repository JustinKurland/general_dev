import pytest
import yaml
from rss_collector.orchestration import load_feeds_from_yaml, process_feeds_from_yaml

def test_load_feeds_from_yaml(tmp_path):
    """
    Test the load_feeds_from_yaml function to ensure it loads RSS feeds from a YAML file.
    """
    # Mock YAML file content
    yaml_content = """
    feeds:
      - https://example.com/feed1.rss
      - https://example.com/feed2.rss
    """
    yaml_file = tmp_path / "feeds.yaml"
    yaml_file.write_text(yaml_content)

    # Load feeds from the YAML file
    feeds = load_feeds_from_yaml(str(yaml_file))

    # Assertions
    assert len(feeds) == 2
    assert feeds == ["https://example.com/feed1.rss", "https://example.com/feed2.rss"]

def test_process_feeds_from_yaml(mocker, tmp_path):
    """
    Test the process_feeds_from_yaml function to ensure it correctly integrates YAML loading and feed processing.
    """
    # Mock YAML file content
    yaml_content = """
    feeds:
      - https://example.com/feed1.rss
      - https://example.com/feed2.rss
    """
    yaml_file = tmp_path / "feeds.yaml"
    yaml_file.write_text(yaml_content)

    # Mock process_feeds to prevent actual RSS fetching
    mock_process_feeds = mocker.patch("rss_collector.orchestration.process_feeds")

    # Call the function to process feeds from the YAML file
    process_feeds_from_yaml(str(yaml_file))

    # Assert that process_feeds was called with the correct feed URLs
    mock_process_feeds.assert_called_once_with([
        "https://example.com/feed1.rss",
        "https://example.com/feed2.rss"
    ])
