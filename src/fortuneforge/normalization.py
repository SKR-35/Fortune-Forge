"""Fortune text normalization."""

import unicodedata


def normalize_fortune(text: str) -> str:
    """Normalize fortune text for exact duplicate comparison."""
    normalized = unicodedata.normalize("NFC", text)
    return " ".join(normalized.split()).casefold()
