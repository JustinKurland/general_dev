import re
from bs4 import BeautifulSoup

def clean_work_notes(html_text: str) -> str:
    """
    Cleans the given HTML text by:
      1. Parsing out all text using BeautifulSoup
      2. Removing special characters, timestamps, code tags, subject lines, email addresses, etc.
      3. Capturing names in LastName, FirstName patterns (also storing reversed FirstName LastName)
      4. Removing any occurrence of those names in the final text
      5. Returning the fully cleaned text
    """

    soup = BeautifulSoup(html_text, "html.parser")
    cleaned_text = soup.get_text(separator=" ")

    # ----------------------------------------------------------------
    # Remove special characters and extra whitespace
    # (You had these steps in your code)
    # ----------------------------------------------------------------
    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    # Remove `\[cC]ode\{...\}`
    cleaned_text = re.sub(r"\[cC]ode\{.*?\}", "", cleaned_text)
    # Remove newlines with a space
    cleaned_text = re.sub(r"[\r\n]+", " ", cleaned_text)
    # Replace HTML non-breaking spaces
    cleaned_text = re.sub(r"&nbsp;", " ", cleaned_text)
    # Remove square brackets
    cleaned_text = re.sub(r"\[.*?\]", "", cleaned_text)
    # Remove "Subject:"
    cleaned_text = re.sub(r"Subject:", "", cleaned_text)
    # Remove "Re:"
    cleaned_text = re.sub(r"Re:", "", cleaned_text)

    # ----------------------------------------------------------------
    # Remove timestamps or date/time patterns you had (example regexes)
    # ----------------------------------------------------------------
    timestamp_patterns = [
        # ex: "18-02-2024 14:39:21 -"
        r"\d{1,2}-\d{1,2}-\d{4}\s+\d{1,2}:\d{2}:\d{2}-?\s*",
        # ex: "Sent: Thu, Feb 1, 2024 at 1:24PM"
        r"(Sent:\s*[A-Za-z]{3},?\s[A-Za-z]{3}\s\d{1,2},?\s\d{4}\s+at\s+\d{1,2}:\d{2}(AM|PM)?)",
        # ex: "On Fri, Jan 5, 2024 at 12:14PM"
        r"(On\s[A-Za-z]{3},?\s[A-Za-z]{3}\s\d{1,2},?\s\d{4}\s+at\s+\d{1,2}:\d{2}(AM|PM)?)",
    ]
    for pattern in timestamp_patterns:
        cleaned_text = re.sub(pattern, "", cleaned_text)

    # Remove standalone times like "12:34 PM" or "1:13 AM"
    cleaned_text = re.sub(r"\b\d{1,2}:\d{2}\s?(AM|PM)\b", "", cleaned_text)
    # Remove leftover "AM" or "PM" if they appear alone
    cleaned_text = re.sub(r"\b(AM|PM)\b", "", cleaned_text)

    # Remove "(Work notes (Rich Text))"
    cleaned_text = re.sub(r"\(Work notes \(Rich Text\)\)", "", cleaned_text)

    # ----------------------------------------------------------------
    # Remove email addresses
    # ----------------------------------------------------------------
    cleaned_text = re.sub(r"<?\b[\w\.-]+@[\w\.-]+\b>?", "", cleaned_text)

    # ----------------------------------------------------------------
    # Divisions and name patterns from your snippet
    # (We’ll keep them here for reference)
    # ----------------------------------------------------------------
    divisions = [
        'AAM', 'Engineering', 'EO', 'GBM', 'Public Risk', 'PS Private',
        'Treasury', 'Legal', 'GBM Private', 'Controllers', 'Rothesay',
        'AAM Private', 'CHS', 'GRI', 'Internal Audit', 'CRG', 'Health Exch',
        'GSB2 Compl', 'CPM', 'AAM Shared', 'PMM', 'PS Public'
    ]
    division_pattern = '|'.join(divisions)

    # Example name patterns (these remove lines like "Cc: Last, First Division ;", etc.)
    name_patterns = [
        rf"(Cc:\s+[A-Z][a-z]+,\s+[A-Z][a-z]+\s*\(?({division_pattern})?\)?)",
        rf"(To:\s+[A-Z][a-z]+,\s+[A-Z][a-z]+\s*\(?({division_pattern})?\)?)",
        rf"(From:\s+[A-Z][a-z]+,\s+[A-Z][a-z]+\s*\(?({division_pattern})?\)?)",
        # You could add more patterns if needed
    ]

    # ----------------------------------------------------------------
    # 1) CAPTURE NAMES from lines like "To: LastName, FirstName"
    #    so we can remove them ANYWHERE in the text (including "FirstName LastName")
    # ----------------------------------------------------------------
    found_names = set()

    # This pattern specifically captures "Label: LastName, FirstName"
    # with optional division in parentheses
    # E.g. "To: Smith, John P. (Engineering)"
    # We’ll store:
    #   - LastName
    #   - FirstName
    #   - "FirstName LastName"
    #   - possibly with or without middle initials
    capturing_pattern = re.compile(
        rf"(?:To|From|Cc)\s*:\s*"
        rf"(?P<last>[A-Z][a-z]+)"         # e.g. "Smith"
        rf"\s*,\s*"
        rf"(?P<first>[A-Z][a-z]+)"        # e.g. "John"
        rf"(?:\s+[A-Z]\.)?"               # optional middle initial
        rf"(?:\s*\(\s*(?:{division_pattern})\s*\))?",  # optional (Division)
    )

    # Let’s extract all matches:
    for match in capturing_pattern.finditer(cleaned_text):
        last = match.group("last").strip()
        first = match.group("first").strip()
        # Store both "Last", "First", and "First Last"
        found_names.add(last)                 # "Smith"
        found_names.add(first)                # "John"
        found_names.add(f"{first} {last}")    # "John Smith"

    # ----------------------------------------------------------------
    # 2) REMOVE NAME PATTERNS from the text (the big blocks like "To: Smith, John...")
    #    So these lines get cleaned out. (This was in your original code.)
    # ----------------------------------------------------------------
    for pattern in name_patterns:
        cleaned_text = re.sub(pattern, '', cleaned_text)

    # Also remove entire lines that match the capturing_pattern
    cleaned_text = re.sub(capturing_pattern, '', cleaned_text)

    # ----------------------------------------------------------------
    # Remove leftover "From:", "To:", "Cc:" if desired
    # ----------------------------------------------------------------
    cleaned_text = re.sub(r"\b(From|To|Cc)\b\s*:?","", cleaned_text)

    # ----------------------------------------------------------------
    # Remove patterns for "from:", "to:", and "cc:" with or without division
    # (If that was in your original code, keep it as well)
    # ----------------------------------------------------------------
    cleaned_text = re.sub(r"\b(?:[Ff]rom|[Tt]o|[Cc]c)\b:\s*[A-Za-z0-9,()\.\s]+", "", cleaned_text)

    # ----------------------------------------------------------------
    # 3) CLEAN UP REDUNDANT SPACES
    # ----------------------------------------------------------------
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    # ----------------------------------------------------------------
    # 4) FINAL PASS: Remove ANY occurrence of the captured names
    #    (including “FirstName”, “LastName”, or “FirstName LastName”)
    # ----------------------------------------------------------------
    for name in found_names:
        # Match as a separate word
        pattern = rf"\b{re.escape(name)}\b"
        cleaned_text = re.sub(pattern, "", cleaned_text)

    # After removing names, clean up extra spaces again
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    return cleaned_text
