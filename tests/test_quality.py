"""Tests for deterministic fortune quality checks."""

import pytest

from fortuneforge.quality import is_quality_candidate


@pytest.mark.parametrize(
    "text",
    [
        "Good fortune is approaching.",
        "Sabır sana güzel bir haber getirecek.",
        "Szczęście pojawi się wcześniej, niż myślisz.",
    ],
)
def test_valid_fortunes_pass_quality_checks(text: str) -> None:
    assert is_quality_candidate(text)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        "Too",
        "Bad\nfortune",
        "Bad\tfortune",
        "Really!!!",
        "Really???",
    ],
)
def test_invalid_fortunes_fail_quality_checks(text: str) -> None:
    assert not is_quality_candidate(text)


def test_overly_long_fortune_fails_quality_check() -> None:
    text = "A" * 181

    assert not is_quality_candidate(text)


def test_control_character_fails_quality_check() -> None:
    text = "Good fortune\u0007 awaits you."

    assert not is_quality_candidate(text)