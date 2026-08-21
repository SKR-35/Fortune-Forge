"""Tests for FortuneForge content-pack validation."""

import pytest

from fortuneforge.content import (
    ENGLISH_OPTIMISTIC,
    ContentPack,
    TemplateContent,
)
from fortuneforge.content_validation import (
    ContentValidationError,
    get_template_fields,
    validate_content_pack,
    validate_template_content,
)
from fortuneforge.domain import Language, Mood


def test_get_template_fields_returns_all_referenced_fields() -> None:
    assert get_template_fields(
        "{time}, {event} will bring {result}."
    ) == {"time", "event", "result"}


def test_template_without_fields_has_empty_field_set() -> None:
    assert get_template_fields("Fortune favors patience.") == set()


def test_reference_content_pack_is_structurally_valid() -> None:
    validate_content_pack(ENGLISH_OPTIMISTIC)


def test_template_rejects_empty_template() -> None:
    template_content = TemplateContent(
        template="   ",
        components={},
    )

    with pytest.raises(
        ContentValidationError,
        match="must not be empty",
    ):
        validate_template_content(template_content)


def test_template_rejects_missing_component() -> None:
    template_content = TemplateContent(
        template="{subject} brings {result}.",
        components={
            "subject": ("Patience",),
        },
    )

    with pytest.raises(
        ContentValidationError,
        match="missing component fields: result",
    ):
        validate_template_content(template_content)


def test_template_rejects_unused_component() -> None:
    template_content = TemplateContent(
        template="{subject} brings luck.",
        components={
            "subject": ("Patience",),
            "unused": ("clarity",),
        },
    )

    with pytest.raises(
        ContentValidationError,
        match="unused component fields: unused",
    ):
        validate_template_content(template_content)


def test_template_rejects_empty_component_pool() -> None:
    template_content = TemplateContent(
        template="{subject} brings luck.",
        components={
            "subject": (),
        },
    )

    with pytest.raises(
        ContentValidationError,
        match="must contain at least one value",
    ):
        validate_template_content(template_content)


@pytest.mark.parametrize("empty_value", ["", " ", "\t", "\n"])
def test_template_rejects_blank_component_values(empty_value: str) -> None:
    template_content = TemplateContent(
        template="{subject} brings luck.",
        components={
            "subject": ("Patience", empty_value),
        },
    )

    with pytest.raises(
        ContentValidationError,
        match="contains an empty value",
    ):
        validate_template_content(template_content)


def test_pack_rejects_missing_templates() -> None:
    content_pack = ContentPack(
        language=Language.TURKISH,
        mood=Mood.HUMOROUS,
        templates=(),
    )

    with pytest.raises(
        ContentValidationError,
        match="contains no templates",
    ):
        validate_content_pack(content_pack)


def test_pack_accepts_multiple_valid_templates() -> None:
    content_pack = ContentPack(
        language=Language.POLISH,
        mood=Mood.OPTIMISTIC,
        templates=(
            TemplateContent(
                template="{subject} przyniesie {result}.",
                components={
                    "subject": ("Cierpliwość",),
                    "result": ("dobrą wiadomość",),
                },
            ),
            TemplateContent(
                template="{time} pojawi się okazja.",
                components={
                    "time": ("Wkrótce",),
                },
            ),
        ),
    )

    validate_content_pack(content_pack)