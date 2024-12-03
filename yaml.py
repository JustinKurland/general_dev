import yaml
import os
import json
from datetime import datetime
from rss_collector.utils import get_proxy_settings
from rss_collector.proxy import fetch_feed_content_with_proxy
from rss_collector.feed_parser import retry_with_backoff, parse_feed

def load_feeds_from_yaml(file_path="feeds.yaml"):
    """
    Load RSS feed URLs from a YAML file.

    Args:
        file_path (str): Path to the YAML file containing the RSS feed URLs.

    Returns:
        list: A list of RSS feed URLs.
    """
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("feeds", [])

def process_feeds_from_yaml(file_path="feeds.yaml"):
    """
    Process RSS feeds specified in a YAML file.

    Args:
        file_path (str): Path to the YAML file containing RSS feed URLs.

    Returns:
        None
    """
    feed_urls = load_feeds_from_yaml(file_path)
    process_feeds(feed_urls)  # Use the existing process_feeds function

def process_feeds(feed_urls):
    """
    Process multiple RSS feeds and save metadata for all feeds into a single JSON file.

    Args:
        feed_urls (list): List of RSS feed URLs.

    Returns:
        None
    """
    # Get proxy settings
    print("Starting process_feeds...")
    proxy_settings = get_proxy_settings()
    app_proxy = proxy_settings["app_proxy"]
    username = proxy_settings["username"]
    password = proxy_settings["password"]
    print(f"Retrieved proxy settings: {proxy_settings}")

    # Directory for storing metadata
    output_dir = "rss_metadata"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory created: {output_dir}")

    # Timestamp for unique file naming
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    metadata_file = os.path.join(output_dir, f"{timestamp}.json")

    # Collect metadata
    all_metadata = {
        "timestamp": timestamp,
        "articles": []
    }

    for feed_url in feed_urls:
        print(f"Processing feed: {feed_url}")
        feed_content = fetch_feed_content_with_proxy(feed_url, app_proxy, username, password)
        if feed_content:
            print(f"Fetched content for feed: {feed_url}")
            try:
                feed_data = parse_feed(feed_content)
                print(f"Parsed feed: {feed_url}")
                for entry in feed_data.get("entries", []):
                    article_metadata = {
                        "title": getattr(entry, "title", "No Title"),
                        "url": getattr(entry, "link", "No URL"),
                        "published_date": getattr(entry, "published", "No Date")
                    }
                    all_metadata["articles"].append(article_metadata)
                    print(f"Article metadata from {feed_url} added: {article_metadata}")
            except Exception as e:
                print(f"Error parsing feed {feed_url}: {e}")
        else:
            print(f"Failed to fetch feed: {feed_url}")

    # Save all metadata to a single JSON file
    with open(metadata_file, "w") as f:
        json.dump(all_metadata, f, indent=4)
    print(f"All metadata saved to {metadata_file}")
