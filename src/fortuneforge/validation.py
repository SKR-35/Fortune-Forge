"""Input parsing and validation for FortuneForge."""

from fortuneforge.domain import GenerationRequest, Language, Mood

MIN_QUANTITY = 1
MAX_QUANTITY = 500


class ValidationError(ValueError):
    """Raised when user-supplied generation input is invalid."""


def parse_quantity(value: str) -> int:
    """Parse and validate the requested fortune quantity."""
    text = value.strip()

    if not text:
        raise ValidationError("Quantity is required.")

    try:
        quantity = int(text)
    except ValueError as exc:
        raise ValidationError("Quantity must be a whole number.") from exc

    if quantity < MIN_QUANTITY or quantity > MAX_QUANTITY:
        raise ValidationError(f"Quantity must be between {MIN_QUANTITY} and {MAX_QUANTITY}.")

    return quantity


def parse_seed(value: str) -> int | None:
    """Parse an optional signed base-10 integer seed."""
    text = value.strip()

    if not text:
        return None

    try:
        return int(text)
    except ValueError as exc:
        raise ValidationError("Seed must be a whole number.") from exc


def build_generation_request(
    *,
    language: Language,
    mood: Mood,
    quantity_text: str,
    seed_text: str,
) -> GenerationRequest:
    """Build a validated generation request from user-facing inputs."""
    return GenerationRequest(
        language=language,
        mood=mood,
        quantity=parse_quantity(quantity_text),
        seed=parse_seed(seed_text),
    )
