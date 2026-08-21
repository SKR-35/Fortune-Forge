"""Compatibility rules for controlled fortune components."""

from fortuneforge.content import ComponentValue


def candidate_is_compatible(values: tuple[ComponentValue, ...]) -> bool:
    """Return whether a set of component values satisfies tag constraints."""
    provided: set[str] = set()
    required: set[str] = set()
    excluded: set[str] = set()

    for value in values:
        for tag in value.tags:
            if tag.startswith("provides:"):
                provided.add(tag.removeprefix("provides:"))
            elif tag.startswith("requires:"):
                required.add(tag.removeprefix("requires:"))
            elif tag.startswith("excludes:"):
                excluded.add(tag.removeprefix("excludes:"))

    if not required.issubset(provided):
        return False

    if provided & excluded:
        return False

    return True
