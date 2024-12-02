import json
from datetime import datetime, timezone
import pandas as pd


def parse_date(date_str):
    """
    Parse a date string into a timezone-aware datetime object, handling multiple formats.

    Args:
        date_str (str): The date string to parse.

    Returns:
        datetime: A timezone-aware datetime object if parsing is successful; None otherwise.
    """
    date_formats = [
        "%Y-%m-%dT%H:%M:%SZ",  # ISO 8601 format
        "%a, %d %b %Y %H:%M:%S %z",  # RSS format
    ]
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, date_format)
            if parsed_date.tzinfo is None:
                # If the parsed date is naive, set it to UTC
                parsed_date = parsed_date.replace(tzinfo=timezone.utc)
            return parsed_date
        except ValueError:
            continue
    return None  # Return None if no formats match


def get_recent_articles(json_file, top_n=100):
    """
    Extract the most recent articles from a JSON metadata file and organize them into a table.

    Args:
        json_file (str): Path to the JSON file containing RSS feed metadata.
        top_n (int): Number of most recent articles to retrieve.

    Returns:
        pd.DataFrame: A DataFrame containing the title, URL, and published date of the most recent articles.
    """
    try:
        # Load the JSON file
        with open(json_file, "r") as f:
            metadata = json.load(f)

        # Extract articles and their publication dates
        articles = []
        for article in metadata.get("articles", []):
            title = article.get("title", "No Title")
            url = article.get("url", "No URL")
            published_date_str = article.get("published_date", "No Date")
            published_date = parse_date(published_date_str)
            if published_date:
                articles.append({"title": title, "url": url, "published_date": published_date})

        if not articles:
            print("No articles found or all dates were invalid.")
            return None

        # Sort articles by published_date in descending order
        articles.sort(key=lambda x: x["published_date"], reverse=True)

        # Take the top N articles
        recent_articles = articles[:top_n]

        # Convert to a DataFrame for display
        df = pd.DataFrame(recent_articles)
        df["published_date"] = df["published_date"].dt.strftime("%Y-%m-%d %H:%M:%S %Z")
        return df

    except Exception as e:
        print(f"Error: {e}")
        return None


# Example usage:
json_file = "rss_metadata/2024-11-30T20:41:23Z.json"  # Replace with the actual path to your JSON file
top_n = 100  # Number of most recent articles to retrieve

recent_articles_df = get_recent_articles(json_file, top_n)
if recent_articles_df is not None:
    print(recent_articles_df)
else:
    print("No articles found or an error occurred.")
