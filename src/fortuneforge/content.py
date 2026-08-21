"""Content definitions used by the FortuneForge generator."""

from dataclasses import dataclass

from fortuneforge.domain import Language, Mood


@dataclass(frozen=True)
class TemplateContent:
    """Reusable components for one controlled fortune template."""

    template: str
    components: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class ContentPack:
    """Generation content for one language and mood."""

    language: Language
    mood: Mood
    templates: tuple[TemplateContent, ...]


ENGLISH_OPTIMISTIC = ContentPack(
    language=Language.ENGLISH,
    mood=Mood.OPTIMISTIC,
    templates=(
        TemplateContent(
            template="{time}, {event} will bring you {result}.",
            components={
                "time": (
                    "Soon",
                    "Before long",
                    "When you least expect it",
                ),
                "event": (
                    "a small opportunity",
                    "an unexpected conversation",
                    "a patient decision",
                ),
                "result": (
                    "good news",
                    "a welcome surprise",
                    "a reason to smile",
                ),
            },
        ),
        TemplateContent(
            template="Your {quality} will lead you toward {outcome}.",
            components={
                "quality": (
                    "patience",
                    "curiosity",
                    "persistence",
                ),
                "outcome": (
                    "an unexpected opportunity",
                    "a useful discovery",
                    "a fortunate change",
                ),
            },
        ),
    ),
)


CONTENT_PACKS: dict[tuple[Language, Mood], ContentPack] = {
    (Language.ENGLISH, Mood.OPTIMISTIC): ENGLISH_OPTIMISTIC,
}


def get_content_pack(language: Language, mood: Mood) -> ContentPack:
    """Return the content pack for the requested language and mood."""
    try:
        return CONTENT_PACKS[(language, mood)]
    except KeyError as exc:
        raise LookupError(
            f"No content pack exists for {language.value} / {mood.value}."
        ) from exc