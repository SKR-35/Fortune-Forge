"""Content-pack capacity analysis for FortuneForge."""

from dataclasses import dataclass

from fortuneforge.content import ContentPack
from fortuneforge.generator import build_candidate_pool


@dataclass(frozen=True)
class CapacityReport:
    """Validated candidate capacity for one content pack."""

    candidate_count: int
    required_count: int

    @property
    def passes(self) -> bool:
        """Return whether the content pack satisfies required capacity."""
        return self.candidate_count >= self.required_count


def analyze_capacity(
    content_pack: ContentPack,
    *,
    required_count: int = 500,
) -> CapacityReport:
    """Measure usable candidate capacity using production generation rules."""
    candidates = build_candidate_pool(content_pack)

    return CapacityReport(
        candidate_count=len(candidates),
        required_count=required_count,
    )
