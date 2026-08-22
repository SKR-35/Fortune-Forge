"""Printable PDF export for FortuneForge."""

from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

FONT_NAME = "FortuneForgeNotoSans"

PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_FONT_PATH = PACKAGE_ROOT / "assets" / "fonts" / "NotoSans-Regular.ttf"


class PdfExportError(RuntimeError):
    """Raised when a printable FortuneForge PDF cannot be created."""


class FortuneDoesNotFitError(PdfExportError):
    """Raised when a fortune cannot fit inside the configured slip."""


@dataclass(frozen=True)
class PdfLayout:
    """Physical configuration for printable fortune slips."""

    page_width: float = A4[0]
    page_height: float = A4[1]

    margin_x: float = 10 * mm
    margin_y: float = 10 * mm

    columns: int = 3
    rows: int = 18

    slip_width: float = 60 * mm
    slip_height: float = 15 * mm

    padding_x: float = 3 * mm
    padding_y: float = 2 * mm

    font_size: float = 8.5
    line_spacing: float = 10.0
    max_lines: int = 3

    guide_line_width: float = 0.25


DEFAULT_LAYOUT = PdfLayout()


def register_pdf_font(font_path: Path = DEFAULT_FONT_PATH) -> str:
    """Register the bundled Unicode font used by FortuneForge PDFs."""
    if not font_path.is_file():
        raise PdfExportError(f"Required PDF font was not found: {font_path}")

    try:
        pdfmetrics.registerFont(
            TTFont(
                FONT_NAME,
                str(font_path),
            )
        )
    except Exception as exc:
        raise PdfExportError(f"Required PDF font could not be loaded: {font_path}") from exc

    return FONT_NAME


def _measure_text(text: str, font_name: str, font_size: float) -> float:
    """Measure one text fragment using the actual PDF font metrics."""
    return pdfmetrics.stringWidth(
        text,
        font_name,
        font_size,
    )


def wrap_fortune(
    text: str,
    *,
    font_name: str,
    layout: PdfLayout = DEFAULT_LAYOUT,
) -> tuple[str, ...]:
    """Wrap a fortune to the configured slip width using PDF metrics."""
    available_width = layout.slip_width - 2 * layout.padding_x

    if _measure_text(text, font_name, layout.font_size) <= available_width:
        return (text,)

    words = text.split()

    if not words:
        raise FortuneDoesNotFitError("Fortune text is empty.")

    lines: list[str] = []
    current_line = words[0]

    for word in words[1:]:
        candidate = f"{current_line} {word}"

        if (
            _measure_text(
                candidate,
                font_name,
                layout.font_size,
            )
            <= available_width
        ):
            current_line = candidate
            continue

        lines.append(current_line)
        current_line = word

    lines.append(current_line)

    if len(lines) > layout.max_lines:
        raise FortuneDoesNotFitError(f"Fortune requires more than {layout.max_lines} lines: {text}")

    for line in lines:
        if (
            _measure_text(
                line,
                font_name,
                layout.font_size,
            )
            > available_width
        ):
            raise FortuneDoesNotFitError(f"Fortune contains text too wide for one slip: {text}")

    required_height = len(lines) * layout.line_spacing
    available_height = layout.slip_height - 2 * layout.padding_y

    if required_height > available_height:
        raise FortuneDoesNotFitError(f"Fortune is too tall for one slip: {text}")

    return tuple(lines)


def fortune_fits(
    text: str,
    *,
    font_name: str,
    layout: PdfLayout = DEFAULT_LAYOUT,
) -> bool:
    """Return whether a fortune fits the configured printable slip."""
    try:
        wrap_fortune(
            text,
            font_name=font_name,
            layout=layout,
        )
    except FortuneDoesNotFitError:
        return False

    return True


def _draw_slip(
    canvas: Canvas,
    fortune: str,
    *,
    x: float,
    y: float,
    font_name: str,
    layout: PdfLayout,
) -> None:
    """Draw one fortune and its cutting boundary."""
    canvas.setStrokeColor(colors.HexColor("#B5B5B5"))
    canvas.setLineWidth(layout.guide_line_width)
    canvas.rect(
        x,
        y,
        layout.slip_width,
        layout.slip_height,
        stroke=1,
        fill=0,
    )

    lines = wrap_fortune(
        fortune,
        font_name=font_name,
        layout=layout,
    )

    canvas.setFillColor(colors.black)
    canvas.setFont(
        font_name,
        layout.font_size,
    )

    text_height = len(lines) * layout.line_spacing

    baseline = y + (layout.slip_height + text_height) / 2 - layout.line_spacing

    for line in lines:
        line_width = _measure_text(
            line,
            font_name,
            layout.font_size,
        )

        text_x = x + (layout.slip_width - line_width) / 2

        canvas.drawString(
            text_x,
            baseline,
            line,
        )

        baseline -= layout.line_spacing


def export_pdf(
    fortunes: tuple[str, ...],
    output_path: str | Path,
    *,
    font_path: Path = DEFAULT_FONT_PATH,
    layout: PdfLayout = DEFAULT_LAYOUT,
) -> None:
    """Export one preview batch as printable A4 fortune slips."""
    if not fortunes:
        raise PdfExportError("No fortunes were provided for PDF export.")

    font_name = register_pdf_font(font_path)

    # Validate the entire batch before creating output so export fails
    # atomically if even one fortune cannot fit the physical layout.
    for fortune in fortunes:
        wrap_fortune(
            fortune,
            font_name=font_name,
            layout=layout,
        )

    output_path = Path(output_path)

    try:
        canvas = Canvas(
            str(output_path),
            pagesize=(layout.page_width, layout.page_height),
        )
    except OSError as exc:
        raise PdfExportError(f"PDF file could not be created: {output_path}") from exc

    fortunes_per_page = layout.columns * layout.rows

    try:
        for index, fortune in enumerate(fortunes):
            page_index = index % fortunes_per_page

            if index > 0 and page_index == 0:
                canvas.showPage()

            row = page_index // layout.columns
            column = page_index % layout.columns

            x = layout.margin_x + column * layout.slip_width

            y = layout.page_height - layout.margin_y - (row + 1) * layout.slip_height

            _draw_slip(
                canvas,
                fortune,
                x=x,
                y=y,
                font_name=font_name,
                layout=layout,
            )

        canvas.save()

    except PdfExportError:
        raise
    except OSError as exc:
        raise PdfExportError(f"PDF file could not be written: {output_path}") from exc
