"""Core domain types for FortuneForge."""

from dataclasses import dataclass
from enum import StrEnum


class Language(StrEnum):
    """Supported fortune languages."""

    ENGLISH = "English"
    TURKISH = "Turkish"
    POLISH = "Polish"


class Mood(StrEnum):
    """Supported fortune moods."""

    HUMOROUS = "Humorous"
    OPTIMISTIC = "Optimistic"
    PESSIMISTIC = "Pessimistic"
    OMINOUS = "Ominous"


@dataclass(frozen=True)
class GenerationRequest:
    """Validated inputs required to generate one fortune batch."""

    language: Language
    mood: Mood
    quantity: int
    seed: int | None = None