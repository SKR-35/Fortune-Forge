"""Validation for FortuneForge content packs."""

from string import Formatter

from fortuneforge.content import ContentPack, TemplateContent


class ContentValidationError(ValueError):
    """Raised when fortune generation content is structurally invalid."""


def get_template_fields(template: str) -> set[str]:
    """Return replacement-field names referenced by a format template."""
    fields: set[str] = set()

    for _, field_name, _, _ in Formatter().parse(template):
        if field_name is not None:
            fields.add(field_name)

    return fields


def validate_template_content(template_content: TemplateContent) -> None:
    """Validate one controlled fortune template and its component pools."""
    if not template_content.template.strip():
        raise ContentValidationError("Fortune template must not be empty.")

    template_fields = get_template_fields(template_content.template)
    component_fields = set(template_content.components)

    missing_components = template_fields - component_fields
    if missing_components:
        missing = ", ".join(sorted(missing_components))
        raise ContentValidationError(
            f"Template references missing component fields: {missing}."
        )

    unused_components = component_fields - template_fields
    if unused_components:
        unused = ", ".join(sorted(unused_components))
        raise ContentValidationError(
            f"Template defines unused component fields: {unused}."
        )

    for field_name, values in template_content.components.items():
        if not values:
            raise ContentValidationError(
                f"Component field '{field_name}' must contain at least one value."
            )

        for value in values:
            if not value.text.strip():
                raise ContentValidationError(
                    f"Component field '{field_name}' contains an empty value."
                )
                
            for tag in value.tags:
                if ":" not in tag:
                    raise ContentValidationError(
                    f"Component field '{field_name}' contains malformed tag '{tag}'."
                    )

                prefix, name = tag.split(":", 1)

                if prefix not in {"provides", "requires", "excludes"} or not name:
                    raise ContentValidationError(
                        f"Component field '{field_name}' contains malformed tag '{tag}'."
                    )


def validate_content_pack(content_pack: ContentPack) -> None:
    """Validate the structural integrity of one language/mood content pack."""
    if not content_pack.templates:
        raise ContentValidationError(
            f"{content_pack.language.value} / {content_pack.mood.value} "
            "content pack contains no templates."
        )

    for template_content in content_pack.templates:
        validate_template_content(template_content)