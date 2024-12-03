import os
from rss_collector.orchestration import process_feeds_from_yaml

def main():
    """
    Entry point to test process_feeds_from_yaml functionality.
    It uses a default feeds.yaml file in the same directory.
    """
    # Determine the default path to feeds.yaml
    default_yaml_path = os.path.join(os.path.dirname(__file__), "feeds.yaml")
    
    # Check if the feeds.yaml file exists
    if not os.path.exists(default_yaml_path):
        raise FileNotFoundError(f"YAML file not found at {default_yaml_path}")

    # Call the process_feeds_from_yaml function with the default YAML file path
    process_feeds_from_yaml(default_yaml_path)
    print("Processing completed successfully.")

if __name__ == "__main__":
    main()
