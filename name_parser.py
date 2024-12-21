from nameparser import HumanName
import re

def remove_names_with_nameparser(text):
    if not isinstance(text, str):
        return text  # Return non-string values unchanged

    # Split the text into words and check for potential names
    words = text.split()
    cleaned_words = []

    for word in words:
        # Try to parse the word as a name
        name = HumanName(word)

        # If the word is not a name (e.g., no first or last name), keep it
        if not name.first and not name.last:
            cleaned_words.append(word)

    # Rejoin the cleaned words
    cleaned_text = ' '.join(cleaned_words)

    # Clean up redundant spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text
