"""Tests for controlled fortune generation."""

import pytest

from fortuneforge.content import ContentPack, TemplateContent
from fortuneforge.domain import GenerationRequest, Language, Mood
from fortuneforge.generator import (
    GenerationError,
    build_candidate_pool,
    generate_batch,
)
from fortuneforge.normalization import normalize_fortune


def test_candidate_pool_expands_reusable_components() -> None:
    content_pack = ContentPack(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        templates=(
            TemplateContent(
                template="{subject} brings {result}.",
                components={
                    "subject": ("Patience", "Curiosity"),
                    "result": ("luck", "clarity"),
                },
            ),
        ),
    )

    candidates = build_candidate_pool(content_pack)

    assert set(candidates) == {
        "Patience brings luck.",
        "Patience brings clarity.",
        "Curiosity brings luck.",
        "Curiosity brings clarity.",
    }


def test_candidate_pool_removes_normalized_duplicates() -> None:
    content_pack = ContentPack(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        templates=(
            TemplateContent(
                template="{text}",
                components={
                    "text": (
                        "Good fortune awaits.",
                        "good fortune awaits.",
                        "Good   fortune awaits.",
                    ),
                },
            ),
        ),
    )

    candidates = build_candidate_pool(content_pack)

    assert candidates == ["Good fortune awaits."]


def test_generation_returns_exact_requested_quantity() -> None:
    request = GenerationRequest(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        quantity=10,
        seed=42,
    )

    batch = generate_batch(request)

    assert len(batch) == 10


def test_generation_contains_no_normalized_duplicates() -> None:
    request = GenerationRequest(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        quantity=20,
        seed=42,
    )

    batch = generate_batch(request)
    normalized = [normalize_fortune(fortune) for fortune in batch]

    assert len(normalized) == len(set(normalized))


def test_seeded_generation_is_deterministic() -> None:
    request = GenerationRequest(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        quantity=15,
        seed=-1993,
    )

    first = generate_batch(request)
    second = generate_batch(request)

    assert first == second


def test_different_seeds_normally_produce_different_batches() -> None:
    first_request = GenerationRequest(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        quantity=15,
        seed=1,
    )
    second_request = GenerationRequest(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        quantity=15,
        seed=2,
    )

    assert generate_batch(first_request) != generate_batch(second_request)


def test_generation_fails_when_capacity_is_insufficient(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    limited_pack = ContentPack(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        templates=(
            TemplateContent(
                template="{result}",
                components={
                    "result": ("One fortune.", "Another fortune."),
                },
            ),
        ),
    )

    monkeypatch.setattr(
        "fortuneforge.generator.get_content_pack",
        lambda language, mood: limited_pack,
    )

    request = GenerationRequest(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        quantity=3,
        seed=42,
    )

    with pytest.raises(GenerationError):
        generate_batch(request)


def test_generation_returns_tuple() -> None:
    request = GenerationRequest(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        quantity=5,
        seed=42,
    )

    assert isinstance(generate_batch(request), tuple)