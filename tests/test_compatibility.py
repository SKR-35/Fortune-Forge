"""Tests for component compatibility rules."""

from fortuneforge.compatibility import candidate_is_compatible
from fortuneforge.content import ComponentValue


def test_candidate_without_tags_is_compatible() -> None:
    values = (
        ComponentValue("patience"),
        ComponentValue("good news"),
    )

    assert candidate_is_compatible(values)


def test_required_tag_is_satisfied_by_provider() -> None:
    values = (
        ComponentValue("she", frozenset({"provides:feminine"})),
        ComponentValue("ready", frozenset({"requires:feminine"})),
    )

    assert candidate_is_compatible(values)


def test_missing_required_tag_is_incompatible() -> None:
    values = (
        ComponentValue("he", frozenset({"provides:masculine"})),
        ComponentValue("ready", frozenset({"requires:feminine"})),
    )

    assert not candidate_is_compatible(values)


def test_excluded_tag_makes_candidate_incompatible() -> None:
    values = (
        ComponentValue("night", frozenset({"provides:dark"})),
        ComponentValue("bright", frozenset({"excludes:dark"})),
    )

    assert not candidate_is_compatible(values)


def test_unrelated_tags_do_not_conflict() -> None:
    values = (
        ComponentValue("patience", frozenset({"provides:abstract"})),
        ComponentValue("luck", frozenset({"provides:positive"})),
    )

    assert candidate_is_compatible(values)
