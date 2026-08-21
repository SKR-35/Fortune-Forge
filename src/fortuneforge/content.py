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
                    ComponentValue("In the days ahead"),
                    ComponentValue("When you least expect it"),
                    ComponentValue("At just the right moment"),
                ),
                "event": (
                    ComponentValue("a small opportunity"),
                    ComponentValue("an unexpected conversation"),
                    ComponentValue("a well-timed decision"),
                    ComponentValue("a welcome invitation"),
                    ComponentValue("a change of routine"),
                    ComponentValue("a new connection"),
                ),
                "result": (
                    ComponentValue("good news"),
                    ComponentValue("a welcome surprise"),
                    ComponentValue("a reason to smile"),
                    ComponentValue("fresh confidence"),
                    ComponentValue("a useful discovery"),
                    ComponentValue("a brighter direction"),
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
                    ComponentValue("kindness"),
                    ComponentValue("courage"),
                    ComponentValue("good judgment"),
                    ComponentValue("quiet confidence"),
                ),
                "outcome": (
                    ComponentValue("an unexpected opportunity"),
                    ComponentValue("a useful discovery"),
                    ComponentValue("a fortunate change"),
                    ComponentValue("a rewarding connection"),
                    ComponentValue("a satisfying result"),
                    ComponentValue("a promising new direction"),
                    ComponentValue("a moment worth remembering"),
                ),
            },
        ),
        TemplateContent(
            template="{action}, and {reward} may follow.",
            components={
                "action": (
                    ComponentValue("Trust your next thoughtful decision"),
                    ComponentValue("Keep moving toward what matters"),
                    ComponentValue("Give a new idea some room"),
                    ComponentValue("Take the opportunity in front of you"),
                    ComponentValue("Stay open to an unexpected possibility"),
                    ComponentValue("Follow the path that feels quietly promising"),
                ),
                "reward": (
                    ComponentValue("good news"),
                    ComponentValue("a pleasant surprise"),
                    ComponentValue("new confidence"),
                    ComponentValue("a useful opportunity"),
                    ComponentValue("a fortunate turn"),
                    ComponentValue("something worth celebrating"),
                ),
            },
        ),
        TemplateContent(
            template="A {thing} may soon become {benefit}.",
            components={
                "thing": (
                    ComponentValue("small change"),
                    ComponentValue("new idea"),
                    ComponentValue("chance meeting"),
                    ComponentValue("steady effort"),
                    ComponentValue("simple decision"),
                    ComponentValue("new beginning"),
                ),
                "benefit": (
                    ComponentValue("the start of something rewarding"),
                    ComponentValue("more valuable than it first appears"),
                    ComponentValue("a source of unexpected happiness"),
                    ComponentValue("an opportunity in disguise"),
                    ComponentValue("a reason for renewed confidence"),
                    ComponentValue("the answer to an old question"),
                ),
            },
        ),
        TemplateContent(
            template="{opening}; {prediction}.",
            components={
                "opening": (
                    ComponentValue("Keep your eyes open"),
                    ComponentValue("Trust the progress you cannot yet see"),
                    ComponentValue("Leave a little room for surprise"),
                    ComponentValue("Do not underestimate small beginnings"),
                    ComponentValue("Stay curious about what comes next"),
                    ComponentValue("Let patience work in your favor"),
                ),
                "prediction": (
                    ComponentValue("something encouraging is taking shape"),
                    ComponentValue("a useful opportunity is drawing closer"),
                    ComponentValue("good news may arrive from an unexpected direction"),
                    ComponentValue("a difficult question will become easier"),
                    ComponentValue("your next step will reveal more than you expect"),
                    ComponentValue("a fortunate coincidence may soon make sense"),
                ),
            },
        ),
        TemplateContent(
            template="{sign} could be the beginning of {outcome}.",
            components={
                "sign": (
                    ComponentValue("A small success"),
                    ComponentValue("An unexpected message"),
                    ComponentValue("A new possibility"),
                    ComponentValue("A change in plans"),
                    ComponentValue("A helpful conversation"),
                    ComponentValue("A moment of clarity"),
                    ComponentValue("A fresh idea"),
                ),
                "outcome": (
                    ComponentValue("something much bigger"),
                    ComponentValue("a rewarding new chapter"),
                    ComponentValue("a welcome change"),
                    ComponentValue("an opportunity worth pursuing"),
                    ComponentValue("a surprisingly good outcome"),
                    ComponentValue("a path you will be glad you followed"),
                    ComponentValue("a happier turn of events"),
                ),
            },
        ),
        TemplateContent(
            template="{time}, you may discover that {realization}.",
            components={
                "time": (
                    ComponentValue("Soon"),
                    ComponentValue("Before long"),
                    ComponentValue("In the coming days"),
                    ComponentValue("At an unexpected moment"),
                    ComponentValue("When the timing is right"),
                    ComponentValue("Earlier than you expect"),
                    ComponentValue("After a little patience"),
                ),
                "realization": (
                    ComponentValue("your effort has been noticed"),
                    ComponentValue("a difficult choice has a simple answer"),
                    ComponentValue("an old worry no longer matters"),
                    ComponentValue("a new direction suits you well"),
                    ComponentValue("someone has good news for you"),
                    ComponentValue("your patience was worth it"),
                    ComponentValue("you are closer to your goal than you thought"),
                ),
            },
        ),
        TemplateContent(
            template="Your next {choice} may open the way to {reward}.",
            components={
                "choice": (
                    ComponentValue("careful decision"),
                    ComponentValue("bold step"),
                    ComponentValue("kind gesture"),
                    ComponentValue("new idea"),
                    ComponentValue("honest conversation"),
                    ComponentValue("change of direction"),
                    ComponentValue("small act of courage"),
                    ComponentValue("patient move"),
                    ComponentValue("thoughtful risk"),
                    ComponentValue("fresh approach"),
                ),
                "reward": (
                    ComponentValue("an unexpected opportunity"),
                    ComponentValue("a satisfying result"),
                    ComponentValue("a valuable connection"),
                    ComponentValue("a welcome improvement"),
                    ComponentValue("something worth celebrating"),
                    ComponentValue("a fortunate discovery"),
                    ComponentValue("a brighter possibility"),
                    ComponentValue("a long-awaited answer"),
                    ComponentValue("renewed hope"),
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
        raise LookupError(f"No content pack exists for {language.value} / {mood.value}.") from exc
