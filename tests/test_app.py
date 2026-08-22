"""Tests for FortuneForge application state and preview behavior."""

import tkinter as tk

import pytest

from fortuneforge.app import (
    DEFAULT_LANGUAGE,
    DEFAULT_MOOD,
    DEFAULT_QUANTITY,
    FortuneForgeApp,
)
from fortuneforge.domain import Language, Mood
from fortuneforge.generator import GenerationError
from fortuneforge.pdf_export import PdfExportError


@pytest.fixture
def app() -> FortuneForgeApp:
    """Create a FortuneForge application instance for GUI behavior tests."""
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tkinter display is not available.")

    root.withdraw()
    application = FortuneForgeApp(root)

    yield application

    root.destroy()


def test_default_control_values(app: FortuneForgeApp) -> None:
    assert app.language_var.get() == DEFAULT_LANGUAGE.value
    assert app.mood_var.get() == DEFAULT_MOOD.value
    assert app.quantity_var.get() == str(DEFAULT_QUANTITY)
    assert app.seed_var.get() == ""


def test_v1_language_selector_exposes_english_only(
    app: FortuneForgeApp,
) -> None:
    assert app.language_combo["values"] == (Language.ENGLISH.value,)


def test_mood_selector_exposes_all_four_moods(
    app: FortuneForgeApp,
) -> None:
    assert app.mood_combo["values"] == tuple(mood.value for mood in Mood)


def test_successful_generation_commits_new_preview(
    app: FortuneForgeApp,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    generated_batch = (
        "Fortune favors the prepared.",
        "A pleasant surprise is approaching.",
    )

    monkeypatch.setattr(
        "fortuneforge.app.generate_batch",
        lambda request: generated_batch,
    )

    app.quantity_var.set("2")
    app._generate()

    assert app.preview_batch == generated_batch
    assert app.status_var.get() == "2 fortunes in current preview."


def test_control_changes_do_not_modify_preview(
    app: FortuneForgeApp,
) -> None:
    existing_batch = (
        "Fortune favors the prepared.",
        "A pleasant surprise is approaching.",
    )
    app.preview_batch = existing_batch
    app._render_preview()

    app.mood_var.set(Mood.OMINOUS.value)
    app.quantity_var.set("100")
    app.seed_var.set("42")

    assert app.preview_batch == existing_batch


def test_generation_failure_preserves_existing_preview(
    app: FortuneForgeApp,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    existing_batch = (
        "Fortune favors the prepared.",
        "A pleasant surprise is approaching.",
    )
    app.preview_batch = existing_batch
    app._render_preview()

    def fail_generation(request: object) -> tuple[str, ...]:
        raise GenerationError("Generation failed for testing.")

    monkeypatch.setattr(
        "fortuneforge.app.generate_batch",
        fail_generation,
    )
    monkeypatch.setattr(
        "fortuneforge.app.messagebox.showerror",
        lambda *args, **kwargs: None,
    )

    app._generate()

    assert app.preview_batch == existing_batch
    assert app.status_var.get() == "2 fortunes in current preview."


def test_preview_renders_noneditable_labels(app: FortuneForgeApp) -> None:
    app.preview_batch = ("A good opportunity is approaching.",)

    app._render_preview()

    assert len(app.fortune_labels) == 1
    assert app.fortune_labels[0].cget("text") == ("1. A good opportunity is approaching.")


def test_preview_preserves_batch_order(
    app: FortuneForgeApp,
) -> None:
    app.preview_batch = (
        "First fortune.",
        "Second fortune.",
        "Third fortune.",
    )

    app._render_preview()

    rendered_texts = [label.cget("text") for label in app.fortune_labels]

    assert rendered_texts == [
        "1. First fortune.",
        "2. Second fortune.",
        "3. Third fortune.",
    ]


def test_text_export_writes_current_preview_in_order(
    app: FortuneForgeApp,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    batch = (
        "First fortune.",
        "Second fortune.",
        "Third fortune.",
    )
    app.preview_batch = batch
    app._render_preview()

    output_path = tmp_path / "fortunes.txt"

    monkeypatch.setattr(
        "fortuneforge.app.filedialog.asksaveasfilename",
        lambda **kwargs: str(output_path),
    )
    monkeypatch.setattr(
        "fortuneforge.app.messagebox.showinfo",
        lambda *args, **kwargs: None,
    )

    app._export_txt()

    assert output_path.read_text(encoding="utf-8") == (
        "First fortune.\nSecond fortune.\nThird fortune.\n"
    )


def test_text_export_uses_preview_snapshot_after_controls_change(
    app: FortuneForgeApp,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    batch = (
        "Fortune one.",
        "Fortune two.",
    )
    app.preview_batch = batch
    app._render_preview()

    app.mood_var.set(Mood.OMINOUS.value)
    app.quantity_var.set("500")
    app.seed_var.set("-42")

    output_path = tmp_path / "fortunes.txt"

    monkeypatch.setattr(
        "fortuneforge.app.filedialog.asksaveasfilename",
        lambda **kwargs: str(output_path),
    )
    monkeypatch.setattr(
        "fortuneforge.app.messagebox.showinfo",
        lambda *args, **kwargs: None,
    )

    app._export_txt()

    assert output_path.read_text(encoding="utf-8") == ("Fortune one.\nFortune two.\n")


def test_text_export_cancel_creates_no_file(
    app: FortuneForgeApp,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    app.preview_batch = ("Fortune one.",)

    monkeypatch.setattr(
        "fortuneforge.app.filedialog.asksaveasfilename",
        lambda **kwargs: "",
    )

    app._export_txt()

    assert list(tmp_path.iterdir()) == []


def test_text_export_without_preview_shows_error(
    app: FortuneForgeApp,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    errors: list[tuple[tuple[object, ...], dict[str, object]]] = []

    monkeypatch.setattr(
        "fortuneforge.app.messagebox.showerror",
        lambda *args, **kwargs: errors.append((args, kwargs)),
    )

    app._export_txt()

    assert len(errors) == 1
    assert errors[0][0][0] == "Nothing to export"


def test_text_export_write_failure_preserves_preview(
    app: FortuneForgeApp,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    batch = (
        "Fortune one.",
        "Fortune two.",
    )
    app.preview_batch = batch
    app._render_preview()

    output_path = tmp_path / "missing" / "fortunes.txt"

    errors: list[tuple[tuple[object, ...], dict[str, object]]] = []

    monkeypatch.setattr(
        "fortuneforge.app.filedialog.asksaveasfilename",
        lambda **kwargs: str(output_path),
    )
    monkeypatch.setattr(
        "fortuneforge.app.messagebox.showerror",
        lambda *args, **kwargs: errors.append((args, kwargs)),
    )

    app._export_txt()

    assert app.preview_batch == batch
    assert len(errors) == 1
    assert errors[0][0][0] == "Export failed"


def test_pdf_export_uses_current_preview(
    app: FortuneForgeApp,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    batch = (
        "First fortune.",
        "Second fortune.",
    )
    app.preview_batch = batch

    output_path = tmp_path / "fortunes.pdf"
    exported: list[tuple[tuple[str, ...], str]] = []

    monkeypatch.setattr(
        "fortuneforge.app.filedialog.asksaveasfilename",
        lambda **kwargs: str(output_path),
    )
    monkeypatch.setattr(
        "fortuneforge.app.export_pdf",
        lambda fortunes, path: exported.append((fortunes, path)),
    )
    monkeypatch.setattr(
        "fortuneforge.app.messagebox.showinfo",
        lambda *args, **kwargs: None,
    )

    app._export_pdf()

    assert exported == [(batch, str(output_path))]


def test_pdf_export_without_preview_shows_error(
    app: FortuneForgeApp,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    errors: list[tuple[tuple[object, ...], dict[str, object]]] = []

    monkeypatch.setattr(
        "fortuneforge.app.messagebox.showerror",
        lambda *args, **kwargs: errors.append((args, kwargs)),
    )

    app._export_pdf()

    assert len(errors) == 1
    assert errors[0][0][0] == "Nothing to export"


def test_pdf_export_failure_preserves_preview(
    app: FortuneForgeApp,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    batch = (
        "First fortune.",
        "Second fortune.",
    )
    app.preview_batch = batch

    monkeypatch.setattr(
        "fortuneforge.app.filedialog.asksaveasfilename",
        lambda **kwargs: str(tmp_path / "fortunes.pdf"),
    )

    def fail_export(*args: object, **kwargs: object) -> None:
        raise PdfExportError("PDF export failed for testing.")

    monkeypatch.setattr(
        "fortuneforge.app.export_pdf",
        fail_export,
    )
    monkeypatch.setattr(
        "fortuneforge.app.messagebox.showerror",
        lambda *args, **kwargs: None,
    )

    app._export_pdf()

    assert app.preview_batch == batch

    def test_select_all_selects_every_fortune(app: FortuneForgeApp) -> None:

        app.preview_batch = ("First.", "Second.", "Third.")
        app._render_preview()

        app.select_all_var.set(False)
        app._toggle_select_all()

        assert not any(var.get() for var in app.selection_vars)

        app.select_all_var.set(True)
        app._toggle_select_all()

        assert all(var.get() for var in app.selection_vars)

    def test_individual_selection_updates_select_all_state(
        app: FortuneForgeApp,
    ) -> None:
        app.preview_batch = ("First.", "Second.", "Third.")
        app._render_preview()

        app.selection_vars[1].set(False)
        app._sync_select_all_state()

        assert app.select_all_var.get() is False

        app.selection_vars[1].set(True)
        app._sync_select_all_state()

        assert app.select_all_var.get() is True

    def test_apply_selection_keeps_only_selected_fortunes(
        app: FortuneForgeApp,
    ) -> None:
        app.generated_batch = ("First.", "Second.", "Third.")
        app.preview_batch = ("First.", "Second.", "Third.")
        app._render_preview()

        app.selection_vars[1].set(False)

        app._apply_selection()

        assert app.generated_batch == ("First.", "Second.", "Third.")
        assert app.preview_batch == ("First.", "Third.")
        assert len(app.selection_vars) == 2
        assert all(var.get() for var in app.selection_vars)

    def test_apply_selection_preserves_original_order(
        app: FortuneForgeApp,
    ) -> None:
        app.preview_batch = ("First.", "Second.", "Third.", "Fourth.")
        app._render_preview()

        app.selection_vars[0].set(False)
        app.selection_vars[2].set(False)

        app._apply_selection()

        assert app.preview_batch == ("Second.", "Fourth.")

    def test_apply_empty_selection_preserves_preview(
        app: FortuneForgeApp,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        batch = ("First.", "Second.", "Third.")
        app.preview_batch = batch
        app._render_preview()

        for selection_var in app.selection_vars:
            selection_var.set(False)

        errors: list[str] = []

        monkeypatch.setattr(
            "fortuneforge.app.messagebox.showerror",
            lambda title, message, **kwargs: errors.append(message),
        )

        app._apply_selection()

        assert app.preview_batch == batch
        assert len(errors) == 1
        assert "Select at least one fortune" in errors[0]

    def test_generation_preserves_complete_generated_batch(
        app: FortuneForgeApp,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        batch = ("First.", "Second.", "Third.")

        monkeypatch.setattr(
            "fortuneforge.app.generate_batch",
            lambda request: batch,
        )

        app._generate()

        assert app.generated_batch == batch
        assert app.preview_batch == batch
        assert all(var.get() for var in app.selection_vars)
