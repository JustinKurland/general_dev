import re
from bs4 import BeautifulSoup

def clean_work_notes(html_text: str) -> str:
    """
    Cleans the given HTML text by:
      1. Parsing out all text using BeautifulSoup
      2. Extracting and capturing names (from 'To:', 'From:', 'Cc:' lines)
      3. Removing timestamps, subject lines, email addresses, etc.
      4. Removing any occurrence of the extracted names
      5. Returning the fully cleaned text
    """
    # -------------------------------------------------
    # 1) Parse out text from HTML
    # -------------------------------------------------
    soup = BeautifulSoup(html_text, "html.parser")
    cleaned_text = soup.get_text(separator=" ")

    # -------------------------------------------------
    # 2) Extract names from "To: ...", "From: ...", "Cc: ..."
    #    We'll store them in a set for final removal.
    # -------------------------------------------------
    found_names = set()

    # Example divisions that might appear after the name in parentheses
    # (Adjust for your actual divisions)
    divisions = [
        'AAM', 'Engineering', 'EO', 'GBM', 'Public Risk', 'PS Private',
        'Treasury', 'Legal', 'GBM Private', 'Controllers', 'Rothesay',
        'AAM Private', 'CHS', 'GRI', 'Internal Audit', 'CRG', 'Health Exch',
        'ComPl', 'GSB2 Compl', 'CPM', 'AAM Shared', 'PMM', 'PS Public'
    ]
    division_pattern = '|'.join(divisions)

    # Regex to match lines like:
    #   To: LastName, FirstName M. (Division)
    #   From: Doe, John (Engineering)
    #   Cc: Smith, Bob
    # This pattern captures <lastname> and <firstname> groups.
    name_line_regex = re.compile(rf"""
        (?P<label>To|From|Cc)\s*:\s*
        (?P<lastname>[A-Z][a-z]+)     # e.g. "Smith"
        \s*,\s*
        (?P<firstname>[A-Z][a-z]+)    # e.g. "Bob"
        (?:                          # Optional middle initial(s) + period
            \s+[A-Z]\.
        )?
        (?:                          # Optional division in parentheses
            \s*\(\s*(?:{division_pattern})\s*\)
        )?
    """, re.VERBOSE)

    def extract_names(text: str):
        """
        Finds name occurrences in lines like 'To: Last, First (Division)'
        and returns a set of all first names, last names, and combined names.
        """
        name_set = set()
        for match in name_line_regex.finditer(text):
            ln = match.group('lastname')
            fn = match.group('firstname')
            # Add them individually and combined
            name_set.add(ln)                 # e.g. "Smith"
            name_set.add(fn)                 # e.g. "Bob"
            name_set.add(f"{fn} {ln}")       # e.g. "Bob Smith"
        return name_set

    # Collect all names *before* we remove them from the text
    found_names.update(extract_names(cleaned_text))

    # -------------------------------------------------
    # 3) Perform your existing cleaning steps
    # -------------------------------------------------

    # Remove special characters / whitespace
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)      # multiple spaces -> single space
    cleaned_text = re.sub(r"\[cC]ode\{.*?\}", "", cleaned_text)  # remove code tags
    cleaned_text = re.sub(r"\[rR]\n?", " ", cleaned_text)         # remove weird line breaks
    cleaned_text = re.sub(r"&nbsp;", " ", cleaned_text)           # remove HTML non-breaking spaces
    cleaned_text = re.sub(r"\[.*?\]", "", cleaned_text)           # remove square brackets
    cleaned_text = re.sub(r"Subject:", "", cleaned_text)          # remove "Subject:"
    cleaned_text = re.sub(r"Re:", "", cleaned_text)               # remove "Re:"

    # Example patterns to remove timestamps like:
    #   "18-02-2024 14:39:21 -", "Sent: Tue, Feb 1, 2024 at 1:24PM", etc.
    timestamp_patterns = [
        r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}-?\s*",           # e.g. "18-02-2024 14:39"
        r"(Sent:\s*[A-Za-z]{3},?\s[A-Za-z]{3}\s\d{1,2},?\s\d{4}\s+at\s+\d{1,2}:\d{2}(AM|PM)?)", 
        r"(On\s[A-Za-z]{3},\s[A-Za-z]{3}\s\d{1,2},?\s\d{4}\s+at\s\d{1,2}:\d{2}(AM|PM)?)"
    ]
    for pattern in timestamp_patterns:
        cleaned_text = re.sub(pattern, "", cleaned_text)

    # Remove standalone times like "12:34 PM" or "1:13 AM"
    cleaned_text = re.sub(r"\b\d{1,2}:\d{2}\s?(AM|PM)\b", "", cleaned_text)

    # Remove unexpected artifacts like "AM?" or "PM?" if you don’t want them
    cleaned_text = re.sub(r"\b(AM|PM)\b", "", cleaned_text)

    # Remove "(Work notes (Rich Text))"
    cleaned_text = re.sub(r"\(Work notes \(Rich Text\)\)", "", cleaned_text)

    # Remove email addresses
    cleaned_text = re.sub(r"<?\b[\w\.-]+@[\w\.-]+\b>?", "", cleaned_text)

    # If you also had lines that specifically remove
    # "To: LastName, FirstName (Division)" etc., do that too:
    # (But note that we already captured these names above.)
    # Here, just remove those entire lines:
    cleaned_text = re.sub(name_line_regex, "", cleaned_text)

    # Optionally remove any leftover "From:", "To:", "Cc:" (with or without divisions)
    cleaned_text = re.sub(r"\b(From|To|Cc)\b\s*:?", "", cleaned_text)

    # Clean up redundant spaces
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    # -------------------------------------------------
    # 4) Final pass: Remove any occurrence of the extracted names
    #    (either first name, last name, or combined "First Last")
    # -------------------------------------------------
    for name in found_names:
        # Build a pattern that matches as whole words
        name_pattern = rf"\b{re.escape(name)}\b"
        cleaned_text = re.sub(name_pattern, "", cleaned_text)

    # Clean up spaces again after removing names
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    return cleaned_text
