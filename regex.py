import re
from bs4 import BeautifulSoup

def clean_work_notes_comprehensive(text):
    if not isinstance(text, str):
        return text  # Return non-string values unchanged

    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()

    # General timestamp formats to be removed
    timestamp_patterns = [
        r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2} -',  # Format: 10-02-2024 14:39:21 -
        r'(Sent:|On) [A-Za-z]+,? [A-Za-z]+ \d{1,2},? \d{4}( at \d{1,2}:\d{2}(AM|PM)?)?',  # Sent: Thu, Feb 1, 2024 at 1:24PM
        r'Sent: \d{2} [A-Za-z]+ \d{4} \d{1,2}:\d{2}',  # Format: Sent: 03 January 2024 13:39
        r'On [A-Za-z]{3}, [A-Za-z]+ \d{1,2}, \d{4} at \d{1,2}:\d{2}(AM|PM)'  # On Fri, Jan 5, 2024 at 12:14PM
    ]

    # Remove all timestamp patterns
    for pattern in timestamp_patterns:
        text = re.sub(pattern, '', text)

    # Remove "To: LastName, FirstName; LastName, FirstName"
    text = re.sub(r'To: .*?(?=Subject:|$)', '', text)

    # Remove "Subject:" specifically
    text = re.sub(r'Subject:', '', text)

    # Remove email addresses
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w{2,}\b', '', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    # Strip leading and trailing whitespace
    text = text.strip()

    return text
