import json
from rss_collector.proxy import fetch_feed_content_with_proxy
from rss_collector.utils import get_proxy_settings
from bs4 import BeautifulSoup

# Load proxy settings
proxy_settings = get_proxy_settings()

# Load a STIX JSON file
with open("stix_bundle_example.json", "r") as file:
    stix_data = json.load(file)

# Extract article content
extracted_data = []

for obj in stix_data["objects"]:
    if obj["type"] == "intrusion-set":
        title = obj.get("name", "No title")
        description = obj.get("description", "No description")
        article_url = obj.get("external_references", [{}])[0].get("url")
        article_text = ""
        
        if article_url:
            # Use the proxy-enabled fetch function
            response = fetch_feed_content_with_proxy(article_url, **proxy_settings)
            if response:
                soup = BeautifulSoup(response, "html.parser")
                article_text = soup.get_text()

        extracted_data.append({
            "title": title,
            "description": description,
            "url": article_url,
            "content": article_text
        })

# Save extracted data to a file (optional)
with open("extracted_articles.json", "w") as json_file:
    json.dump(extracted_data, json_file, indent=4)
