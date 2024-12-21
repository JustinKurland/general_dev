from bs4 import BeautifulSoup
import re

def clean_work_notes(text):
    # Remove HTML tags using BeautifulSoup
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text(separator=" ")

    # Remove special characters and extra whitespace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'```[^\```]*```', '', cleaned_text)  # Remove ``` tags
    cleaned_text = re.sub(r'[\r\n]+', ' ', cleaned_text)  # Replace newlines with a space
    cleaned_text = re.sub(r'&nbsp;', ' ', cleaned_text)  # Replace HTML non-breaking spaces
    cleaned_text = re.sub(r'\[[^\]]*\]', '', cleaned_text)  # Remove square brackets

    # Remove RE and Subject
    cleaned_text = re.sub(r'Re: ', '', cleaned_text)
    cleaned_text = re.sub(r'Subject:', '', cleaned_text)

    # Remove all timestamp patterns
    timestamp_patterns = [
        r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2} -',  # Format: 10-02-2024 14:39:21 -
        r'(Sent:|On) [A-Za-z]+, [A-Za-z]+ \d{1,2}, \d{4}( at \d{1,2}:\d{2}(AM|PM)?)?',  # Sent: Thu, Feb 1, 2024 at 1:24PM
        r'Sent: \d{2} [A-Za-z]+ \d{4} \d{1,2}:\d{2}',  # Sent: 03 January 2024 13:39
        r'On [A-Za-z]{3}, [A-Za-z]+ \d{1,2}, \d{4} at \d{1,2}:\d{2}(AM|PM)'  # On Fri, Jan 5, 2024 at 12:14PM
    ]
    for pattern in timestamp_patterns:
        cleaned_text = re.sub(pattern, '', cleaned_text)

    # Remove standalone times like "12:34 PM" or "1:13 AM"
    cleaned_text = re.sub(r'\b\d{1,2}:\d{2}\s?(AM|PM)\b', '', cleaned_text)

    # Remove exact matches of artifacts like 'Work notes (Rich Text)'
    cleaned_text = re.sub(r'\bWork notes \(Rich Text\)\b', '', cleaned_text)

    # List of divisions
    divisions = [
        'AMW', 'Engineering', 'EO', 'GBM', 'Public Risk', 'PS Private', 'Treasury', 'Legal', 'GBM Private',
        'Controllers', 'Rothesay', 'AMW Private', 'CIS', 'GIR', 'Internal Audit', 'CRG', 'Health Exch',
        'Compl', 'GSBZ Compl', 'CPM', 'AMW Shared', 'PWM', 'PS Public'
    ]
    division_pattern = '|'.join(divisions)

    # Remove names in the specified patterns
    name_patterns = [
        rf'Cc: [\w\s,]+ \({division_pattern}\) ;',  # Pattern: 'Cc: Last, First Division ;'
        rf'To: [\w\s,]+ \({division_pattern}\) ;',  # Pattern: 'To: Last, First Division ;'
        rf'From: [\w\s,]+ \({division_pattern}\) ;',  # Pattern: 'From: Last, First Division ;'
        rf'To: [\w\s,]+ Cc: [\w\s,]+ \({division_pattern}\) ;',  # Pattern: 'To: First Last Cc: Last, First Division ;'
        rf'[\w\s,]+ \({division_pattern}\) ;'  # Pattern: 'Last, First Division ;'
    ]

    # Collect all names dynamically **before** removing them
    dynamic_name_pattern = r'\b([\w-]+), ([\w-]+)(?: [A-Z])? ;'
    matches = re.findall(dynamic_name_pattern, cleaned_text)

    # Build a set of unique words to remove
    words_to_remove = set()
    for match in matches:
        words_to_remove.update(match)  # Add LastName, FirstName, and optional Initial

    # Remove names in the specified patterns
    for pattern in name_patterns:
        cleaned_text = re.sub(pattern, '', cleaned_text)

    # Remove all instances of collected name components
    for word in words_to_remove:
        cleaned_text = re.sub(rf'\b{re.escape(word)}\b', '', cleaned_text)

    # Remove lone semicolons and clean up spaces
    cleaned_text = re.sub(r'\s+;', '', cleaned_text)  # Remove lone semicolons
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Clean up redundant spaces

    return cleaned_text
