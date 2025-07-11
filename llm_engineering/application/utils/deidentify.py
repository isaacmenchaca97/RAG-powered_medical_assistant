import re
from typing import Optional

# Simple patterns for demonstration; real PHI removal should be more robust and may require NLP.
PHI_PATTERNS = [
    # Emails
    (re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"), "[EMAIL]"),
    # Phone numbers (US-centric, basic)
    (re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"), "[PHONE]"),
    # Dates (YYYY-MM-DD, MM/DD/YYYY, etc)
    (
        re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{2}/\d{2}/\d{4}\b"),
        "[DATE]",
    ),
    # Medical Record Numbers (MRN, simple numeric)
    (re.compile(r"\bMRN[:\s]*\d+\b", re.IGNORECASE), "[MRN]"),
    # Addresses (very basic, street number + name)
    (
        re.compile(
            r"\b\d{1,5} [A-Za-z0-9 .,'-]+"
            r"(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b",
            re.IGNORECASE,
        ),
        "[ADDRESS]",
    ),
    # Names (if you have a list, otherwise skip; here, just a placeholder for demo)
    # (re.compile(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b"), "[NAME]"),
]


def deidentify_text(
    text: str, extra_patterns: Optional[list[tuple[re.Pattern, str]]] = None
) -> str:
    """
    Remove or mask common PHI from text. This is a simple regex-based approach.
    Args:
        text: The input text to de-identify.
        extra_patterns: Optional list of (pattern, replacement) for custom PHI.
    Returns:
        De-identified text.
    """
    patterns = PHI_PATTERNS.copy()
    if extra_patterns:
        patterns.extend(extra_patterns)
    for pattern, repl in patterns:
        text = pattern.sub(repl, text)
    return text
