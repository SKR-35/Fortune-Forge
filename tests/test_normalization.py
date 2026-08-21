"""Tests for fortune normalization."""

import pytest

from fortuneforge.normalization import normalize_fortune


def test_normalization_collapses_whitespace() -> None:
    assert normalize_fortune("Good   fortune\nawaits.") == "good fortune awaits."


def test_normalization_is_case_insensitive() -> None:
    assert normalize_fortune("FORTUNE") == normalize_fortune("fortune")


@pytest.mark.parametrize(
    ("original", "expected"),
    [
        ("İ", "i̇"),
        ("ı", "ı"),
        ("Ş", "ş"),
        ("ş", "ş"),
        ("Ğ", "ğ"),
        ("ğ", "ğ"),
        ("Ç", "ç"),
        ("ç", "ç"),
        ("Ö", "ö"),
        ("ö", "ö"),
        ("Ü", "ü"),
        ("ü", "ü"),
    ],
)
def test_normalization_preserves_turkish_characters(
    original: str,
    expected: str,
) -> None:
    assert normalize_fortune(original) == expected


@pytest.mark.parametrize(
    ("original", "expected"),
    [
        ("Ą", "ą"),
        ("ą", "ą"),
        ("Ć", "ć"),
        ("ć", "ć"),
        ("Ę", "ę"),
        ("ę", "ę"),
        ("Ł", "ł"),
        ("ł", "ł"),
        ("Ń", "ń"),
        ("ń", "ń"),
        ("Ó", "ó"),
        ("ó", "ó"),
        ("Ś", "ś"),
        ("ś", "ś"),
        ("Ź", "ź"),
        ("ź", "ź"),
        ("Ż", "ż"),
        ("ż", "ż"),
    ],
)
def test_normalization_preserves_polish_characters(
    original: str,
    expected: str,
) -> None:
    assert normalize_fortune(original) == expected


def test_normalization_preserves_full_turkish_sentence() -> None:
    text = "İyi şans, güzel günler yakında."

    assert normalize_fortune(text) == "i̇yi şans, güzel günler yakında."


def test_normalization_preserves_full_polish_sentence() -> None:
    text = "Łagodny żart przyniesie ci szczęście."

    assert normalize_fortune(text) == "łagodny żart przyniesie ci szczęście."
