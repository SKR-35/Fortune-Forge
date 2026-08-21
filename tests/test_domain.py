"""Tests for FortuneForge domain types."""

from dataclasses import FrozenInstanceError

import pytest

from fortuneforge.domain import GenerationRequest, Language, Mood


def test_supported_languages_are_exactly_the_v1_set() -> None:
    assert list(Language) == [
        Language.ENGLISH,
        Language.TURKISH,
        Language.POLISH,
    ]


def test_supported_moods_are_exactly_the_v1_set() -> None:
    assert list(Mood) == [
        Mood.HUMOROUS,
        Mood.OPTIMISTIC,
        Mood.PESSIMISTIC,
        Mood.OMINOUS,
    ]


def test_generation_request_preserves_values() -> None:
    request = GenerationRequest(
        language=Language.TURKISH,
        mood=Mood.OMINOUS,
        quantity=20,
        seed=-42,
    )

    assert request.language is Language.TURKISH
    assert request.mood is Mood.OMINOUS
    assert request.quantity == 20
    assert request.seed == -42


def test_generation_request_is_immutable() -> None:
    request = GenerationRequest(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        quantity=20,
    )

    with pytest.raises(FrozenInstanceError):
        request.quantity = 30  # type: ignore[misc]