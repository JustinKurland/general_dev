import json
from datetime import datetime
import pandas as pd


def load_and_sort_articles(json_file):
    """
    Load articles from a JSON file, sort by published date, and return the 100 most recent articles.

    Args:
        json_file (str): Path to the JSON file containing metadata.

    Returns:
        pd.DataFrame: A DataFrame containing the 100 most recent articles with title, URL, and published date.
    """
    try:
        # Load metadata from the JSON file
        with open(json_file, "r") as f:
            metadata = json.load(f)

        # Extract articles
        articles = metadata.get("articles", [])

        # Parse and sort articles by published date
        sorted_articles = sorted(
            articles,
            key=lambda x: datetime.strptime(x["published_date"], "%Y-%m-%dT%H:%M:%SZ"),
            reverse=True,
        )

        # Select the 100 most recent articles
        most_recent_articles = sorted_articles[:100]

        # Format the result as a pandas DataFrame
        formatted_table = pd.DataFrame(
            [
                {
                    "Title": article.get("title", "No Title"),
                    "URL": article.get("url", "No URL"),
                    "Published Date": article.get("published_date", "No Date"),
                }
                for article in most_recent_articles
            ]
        )

        return formatted_table

    except FileNotFoundError:
        print(f"Error: The file {json_file} was not found.")
        return pd.DataFrame()
    except KeyError as e:
        print(f"Error: Missing key in JSON data - {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()


# Example usage
if __name__ == "__main__":
    # Specify the path to your JSON file
    json_file_path = "rss_metadata/2024-12-01T20:41:23Z.json"

    # Load and sort articles
    recent_articles_table = load_and_sort_articles(json_file_path)

    # Display the result
    if not recent_articles_table.empty:
        print(recent_articles_table)
    else:
        print("No articles found or an error occurred.")
