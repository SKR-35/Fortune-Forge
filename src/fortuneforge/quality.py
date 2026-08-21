"""Deterministic quality checks for generated fortune text."""

import unicodedata

MIN_FORTUNE_LENGTH = 8
MAX_FORTUNE_LENGTH = 180


def is_quality_candidate(text: str) -> bool:
    """Return whether fortune text passes basic deterministic quality checks."""
    stripped = text.strip()

    if len(stripped) < MIN_FORTUNE_LENGTH:
        return False

    if len(stripped) > MAX_FORTUNE_LENGTH:
        return False

    if "\n" in stripped or "\r" in stripped or "\t" in stripped:
        return False

    if "!!!" in stripped or "???" in stripped:
        return False

    for char in stripped:
        category = unicodedata.category(char)
        if category.startswith("C"):
            return False

    return True