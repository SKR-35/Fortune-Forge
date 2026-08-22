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


def test_preview_is_read_only_after_render(
    app: FortuneForgeApp,
) -> None:
    app.preview_batch = ("A good opportunity is approaching.",)

    app._render_preview()

    assert app.preview_text.cget("state") == "disabled"


def test_preview_preserves_batch_order(
    app: FortuneForgeApp,
) -> None:
    app.preview_batch = (
        "First fortune.",
        "Second fortune.",
        "Third fortune.",
    )

    app._render_preview()

    rendered = app.preview_text.get("1.0", "end-1c")

    assert rendered.index("First fortune.") < rendered.index("Second fortune.")
    assert rendered.index("Second fortune.") < rendered.index("Third fortune.")
