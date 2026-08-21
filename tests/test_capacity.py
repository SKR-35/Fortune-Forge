"""Tests for FortuneForge content capacity analysis."""

from fortuneforge.capacity import CapacityReport, analyze_capacity
from fortuneforge.content import ComponentValue, ContentPack, TemplateContent
from fortuneforge.domain import Language, Mood


def test_capacity_report_passes_at_required_capacity() -> None:
    report = CapacityReport(
        candidate_count=500,
        required_count=500,
    )

    assert report.passes


def test_capacity_report_passes_above_required_capacity() -> None:
    report = CapacityReport(
        candidate_count=750,
        required_count=500,
    )

    assert report.passes


def test_capacity_report_fails_below_required_capacity() -> None:
    report = CapacityReport(
        candidate_count=499,
        required_count=500,
    )

    assert not report.passes


def test_capacity_uses_actual_candidate_pool() -> None:
    content_pack = ContentPack(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        templates=(
            TemplateContent(
                template="{subject} brings {result}.",
                components={
                    "subject": (
                        ComponentValue("Patience"),
                        ComponentValue("Curiosity"),
                    ),
                    "result": (
                        ComponentValue("good news"),
                        ComponentValue("new opportunities"),
                    ),
                },
            ),
        ),
    )

    report = analyze_capacity(content_pack, required_count=4)

    assert report.candidate_count == 4
    assert report.passes


def test_capacity_does_not_count_normalized_duplicates() -> None:
    content_pack = ContentPack(
        language=Language.ENGLISH,
        mood=Mood.OPTIMISTIC,
        templates=(
            TemplateContent(
                template="{fortune}",
                components={
                    "fortune": (
                        ComponentValue("Good fortune awaits."),
                        ComponentValue("good fortune awaits."),
                    ),
                },
            ),
        ),
    )

    report = analyze_capacity(content_pack, required_count=2)

    assert report.candidate_count == 1
    assert not report.passes