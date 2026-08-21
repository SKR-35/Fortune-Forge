"""Controlled fortune generation."""

from itertools import product
from random import Random

from fortuneforge.content import ContentPack, TemplateContent, get_content_pack
from fortuneforge.domain import GenerationRequest
from fortuneforge.normalization import normalize_fortune


class GenerationError(RuntimeError):
    """Raised when a complete fortune batch cannot be generated."""


def _expand_template(template_content: TemplateContent) -> list[str]:
    """Expand one controlled template into all available combinations."""
    field_names = tuple(template_content.components)

    if not field_names:
        return [template_content.template]

    value_groups = [template_content.components[name] for name in field_names]

    fortunes: list[str] = []

    for values in product(*value_groups):
        replacements = dict(zip(field_names, values, strict=True))
        fortunes.append(template_content.template.format(**replacements))

    return fortunes


def build_candidate_pool(content_pack: ContentPack) -> list[str]:
    """Build the unique candidate pool for a content pack."""
    unique_candidates: dict[str, str] = {}

    for template_content in content_pack.templates:
        for fortune in _expand_template(template_content):
            normalized = normalize_fortune(fortune)

            if normalized:
                unique_candidates.setdefault(normalized, fortune)

    return list(unique_candidates.values())


def generate_batch(request: GenerationRequest) -> tuple[str, ...]:
    """Generate a complete deterministic or unseeded fortune batch."""
    content_pack = get_content_pack(request.language, request.mood)
    candidates = build_candidate_pool(content_pack)

    if len(candidates) < request.quantity:
        raise GenerationError(
            "The selected content pack cannot produce the requested "
            f"{request.quantity} unique fortunes."
        )

    rng = Random(request.seed)
    selected = rng.sample(candidates, request.quantity)

    return tuple(selected)