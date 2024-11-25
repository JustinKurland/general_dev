import re

def extract_urls_from_description(description):
    """
    Extract all URLs from the given description text.

    Args:
        description (str): The description field from a STIX JSON object.

    Returns:
        list: A list of URLs found in the description.
    """
    if not description:
        return []
    
    # Regular expression to match URLs
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, description)
    return urls


import json

def extract_urls_from_stix(stix_json):
    """
    Extract all URLs from the descriptions in a STIX JSON bundle.

    Args:
        stix_json (str): The STIX JSON bundle as a string.

    Returns:
        dict: A dictionary with STIX object IDs as keys and extracted URLs as values.
    """
    stix_data = json.loads(stix_json)
    url_mapping = {}

    for obj in stix_data.get("objects", []):
        if obj.get("type") == "intrusion-set":
            description = obj.get("description", "")
            urls = extract_urls_from_description(description)
            if urls:
                url_mapping[obj["id"]] = urls

    return url_mapping

# Example usage
stix_json = '...'  # Replace with your STIX JSON string
url_mapping = extract_urls_from_stix(stix_json)

# Print the results
for intrusion_id, urls in url_mapping.items():
    print(f"Intrusion Set ID: {intrusion_id}")
    for url in urls:
        print(f" - {url}")

# Save to a file
with open("extracted_urls.json", "w") as f:
    json.dump(url_mapping, f, indent=4)
