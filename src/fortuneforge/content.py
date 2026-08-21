"""Content definitions used by the FortuneForge generator."""

from dataclasses import dataclass, field

from fortuneforge.domain import Language, Mood


@dataclass(frozen=True)
class ComponentValue:
    """One reusable phrase value with optional compatibility tags."""

    text: str
    tags: frozenset[str] = field(default_factory=frozenset)

@dataclass(frozen=True)
class TemplateContent:
    """Reusable components for one controlled fortune template."""

    template: str
    components: dict[str, tuple[ComponentValue, ...]]


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
                    ComponentValue("Soon"),
                    ComponentValue("Before long"),
                    ComponentValue("When you least expect it"),
                ),
                "event": (
                    ComponentValue("a small opportunity"),
                    ComponentValue("an unexpected conversation"),
                    ComponentValue("a patient decision"),
                ),
                "result": (
                    ComponentValue("good news"),
                    ComponentValue("a welcome surprise"),
                    ComponentValue("a reason to smile"),
                ),
            },
        ),
        TemplateContent(
            template="Your {quality} will lead you toward {outcome}.",
            components={
                "quality": (
                    ComponentValue("patience"),
                    ComponentValue("curiosity"),
                    ComponentValue("persistence"),
                ),
                "outcome": (
                    ComponentValue("an unexpected opportunity"),
                    ComponentValue("a useful discovery"),
                    ComponentValue("a fortunate change"),
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