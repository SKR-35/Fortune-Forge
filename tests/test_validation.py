"""Tests for FortuneForge input validation."""

import pytest

from fortuneforge.domain import Language, Mood
from fortuneforge.validation import (
    ValidationError,
    build_generation_request,
    parse_quantity,
    parse_seed,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("1", 1),
        ("20", 20),
        ("500", 500),
        (" 20 ", 20),
        ("+12", 12),
    ],
)
def test_parse_quantity_accepts_valid_values(value: str, expected: int) -> None:
    assert parse_quantity(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "",
        " ",
        "0",
        "-1",
        "501",
        "1.5",
        "twenty",
    ],
)
def test_parse_quantity_rejects_invalid_values(value: str) -> None:
    with pytest.raises(ValidationError):
        parse_quantity(value)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", None),
        (" ", None),
        ("0", 0),
        ("42", 42),
        ("-42", -42),
        ("+42", 42),
    ],
)
def test_parse_seed_accepts_blank_or_signed_integer(
    value: str,
    expected: int | None,
) -> None:
    assert parse_seed(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "1.5",
        "abc",
        "12x",
        "--4",
    ],
)
def test_parse_seed_rejects_malformed_values(value: str) -> None:
    with pytest.raises(ValidationError):
        parse_seed(value)


def test_build_generation_request_returns_validated_request() -> None:
    request = build_generation_request(
        language=Language.POLISH,
        mood=Mood.PESSIMISTIC,
        quantity_text="25",
        seed_text="-1993",
    )

    assert request.language is Language.POLISH
    assert request.mood is Mood.PESSIMISTIC
    assert request.quantity == 25
    assert request.seed == -1993


def test_build_generation_request_rejects_invalid_quantity() -> None:
    with pytest.raises(ValidationError):
        build_generation_request(
            language=Language.ENGLISH,
            mood=Mood.HUMOROUS,
            quantity_text="501",
            seed_text="",
        )