"""Tests for printable FortuneForge PDF export."""

from pathlib import Path

import pytest

from fortuneforge.pdf_export import (
    DEFAULT_FONT_PATH,
    DEFAULT_LAYOUT,
    FortuneDoesNotFitError,
    PdfExportError,
    export_pdf,
    fortune_fits,
    register_pdf_font,
    wrap_fortune,
)


def test_bundled_pdf_font_exists() -> None:
    assert DEFAULT_FONT_PATH.is_file()


def test_bundled_pdf_font_registers() -> None:
    font_name = register_pdf_font()

    assert font_name


def test_short_fortune_fits_printable_slip() -> None:
    font_name = register_pdf_font()

    assert fortune_fits(
        "Good news is on its way.",
        font_name=font_name,
    )


def test_long_fortune_wraps_to_multiple_lines() -> None:
    font_name = register_pdf_font()

    lines = wrap_fortune(
        ("At just the right moment, a welcome invitation will bring you a useful discovery."),
        font_name=font_name,
    )

    assert 2 <= len(lines) <= DEFAULT_LAYOUT.max_lines


def test_overlong_fortune_is_rejected() -> None:
    font_name = register_pdf_font()

    fortune = " ".join(["extraordinary"] * 30)

    with pytest.raises(FortuneDoesNotFitError):
        wrap_fortune(
            fortune,
            font_name=font_name,
        )


def test_export_pdf_creates_nonempty_file(tmp_path: Path) -> None:
    output_path = tmp_path / "fortunes.pdf"

    export_pdf(
        (
            "Good news is on its way.",
            "A pleasant surprise may arrive soon.",
            "Your patience will be rewarded.",
        ),
        output_path,
    )

    assert output_path.is_file()
    assert output_path.stat().st_size > 0


def test_export_pdf_supports_multiple_pages(tmp_path: Path) -> None:
    output_path = tmp_path / "fortunes.pdf"

    fortunes = tuple(f"Good fortune number {index} is on its way." for index in range(1, 56))

    export_pdf(
        fortunes,
        output_path,
    )

    assert output_path.is_file()
    assert output_path.stat().st_size > 0


def test_export_pdf_rejects_empty_batch(tmp_path: Path) -> None:
    output_path = tmp_path / "fortunes.pdf"

    with pytest.raises(PdfExportError):
        export_pdf((), output_path)

    assert not output_path.exists()


def test_export_pdf_fails_before_writing_when_fortune_does_not_fit(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "fortunes.pdf"

    fortunes = (
        "Good news is on its way.",
        " ".join(["extraordinary"] * 30),
    )

    with pytest.raises(FortuneDoesNotFitError):
        export_pdf(
            fortunes,
            output_path,
        )

    assert not output_path.exists()


def test_export_pdf_fails_when_font_is_missing(tmp_path: Path) -> None:
    output_path = tmp_path / "fortunes.pdf"
    missing_font = tmp_path / "missing-font.ttf"

    with pytest.raises(PdfExportError):
        export_pdf(
            ("Good news is on its way.",),
            output_path,
            font_path=missing_font,
        )

    assert not output_path.exists()
