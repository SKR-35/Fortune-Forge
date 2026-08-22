"""FortuneForge desktop application."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from fortuneforge.domain import GenerationRequest, Language, Mood
from fortuneforge.generator import GenerationError, generate_batch
from fortuneforge.pdf_export import PdfExportError, export_pdf

APP_TITLE = "FortuneForge"
WINDOW_WIDTH = 820
WINDOW_HEIGHT = 620

DEFAULT_LANGUAGE = Language.ENGLISH
DEFAULT_MOOD = Mood.OPTIMISTIC
DEFAULT_QUANTITY = 20

MIN_QUANTITY = 1
MAX_QUANTITY = 500


class FortuneForgeApp:
    """Tkinter application controller for FortuneForge."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        # Preview state is deliberately separate from control state.
        # Changing controls must not change the last successfully generated batch.
        self.preview_batch: tuple[str, ...] = ()

        self.language_var = tk.StringVar(value=DEFAULT_LANGUAGE.value)
        self.mood_var = tk.StringVar(value=DEFAULT_MOOD.value)
        self.quantity_var = tk.StringVar(value=str(DEFAULT_QUANTITY))
        self.seed_var = tk.StringVar()

        self._build_window()
        self._build_controls()
        self._build_preview()

    def _build_window(self) -> None:
        """Configure the main application window."""
        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(700, 500)

        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(
            self.main_frame,
            text=APP_TITLE,
            font=("TkDefaultFont", 20, "bold"),
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            self.main_frame,
            text="Fortune Cookie Generator",
        )
        subtitle_label.pack(anchor="w", pady=(2, 16))

    def _build_controls(self) -> None:
        """Create generation controls."""
        controls = ttk.LabelFrame(
            self.main_frame,
            text="Generate fortunes",
            padding=12,
        )
        controls.pack(fill="x", pady=(0, 16))

        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(3, weight=1)

        ttk.Label(controls, text="Language:").grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=4,
        )

        self.language_combo = ttk.Combobox(
            controls,
            textvariable=self.language_var,
            values=(Language.ENGLISH.value,),
            state="readonly",
            width=18,
        )
        self.language_combo.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(0, 16),
            pady=4,
        )

        ttk.Label(controls, text="Mood:").grid(
            row=0,
            column=2,
            sticky="w",
            padx=(0, 8),
            pady=4,
        )

        self.mood_combo = ttk.Combobox(
            controls,
            textvariable=self.mood_var,
            values=tuple(mood.value for mood in Mood),
            state="readonly",
            width=18,
        )
        self.mood_combo.grid(
            row=0,
            column=3,
            sticky="ew",
            pady=4,
        )

        ttk.Label(controls, text="Quantity:").grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=4,
        )

        self.quantity_entry = ttk.Entry(
            controls,
            textvariable=self.quantity_var,
            width=20,
        )
        self.quantity_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(0, 16),
            pady=4,
        )

        ttk.Label(controls, text="Seed (optional):").grid(
            row=1,
            column=2,
            sticky="w",
            padx=(0, 8),
            pady=4,
        )

        self.seed_entry = ttk.Entry(
            controls,
            textvariable=self.seed_var,
            width=20,
        )
        self.seed_entry.grid(
            row=1,
            column=3,
            sticky="ew",
            pady=4,
        )

        self.generate_button = ttk.Button(
            controls,
            text="Generate",
            command=self._generate,
        )
        self.generate_button.grid(
            row=2,
            column=0,
            columnspan=4,
            pady=(12, 0),
        )

    def _build_preview(self) -> None:
        """Create the read-only scrollable preview."""
        preview_frame = ttk.LabelFrame(
            self.main_frame,
            text="Preview",
            padding=12,
        )
        preview_frame.pack(fill="both", expand=True)

        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)

        self.preview_text = tk.Text(
            preview_frame,
            wrap="word",
            state="disabled",
            padx=10,
            pady=10,
        )
        self.preview_text.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        scrollbar = ttk.Scrollbar(
            preview_frame,
            orient="vertical",
            command=self.preview_text.yview,
        )
        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        self.preview_text.configure(yscrollcommand=scrollbar.set)

        self.status_var = tk.StringVar(value="No batch generated yet.")

        status_label = ttk.Label(
            preview_frame,
            textvariable=self.status_var,
        )
        status_label.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(8, 0),
        )

        export_frame = ttk.Frame(preview_frame)
        export_frame.grid(
            row=1,
            column=1,
            sticky="e",
            pady=(8, 0),
        )

        self.export_txt_button = ttk.Button(
            export_frame,
            text="Export TXT",
            command=self._export_txt,
        )
        self.export_txt_button.pack(
            side="left",
            padx=(0, 8),
        )

        self.export_pdf_button = ttk.Button(
            export_frame,
            text="Export PDF",
            command=self._export_pdf,
        )
        self.export_pdf_button.pack(side="left")

    def _parse_quantity(self) -> int:
        """Parse and validate the quantity control."""
        raw_value = self.quantity_var.get().strip()

        if not raw_value:
            raise ValueError("Quantity is required.")

        try:
            quantity = int(raw_value)
        except ValueError as exc:
            raise ValueError("Quantity must be a whole number.") from exc

        if not MIN_QUANTITY <= quantity <= MAX_QUANTITY:
            raise ValueError(f"Quantity must be between {MIN_QUANTITY} and {MAX_QUANTITY}.")

        return quantity

    def _parse_seed(self) -> int | None:
        """Parse and validate the optional signed integer seed."""
        raw_value = self.seed_var.get().strip()

        if not raw_value:
            return None

        try:
            return int(raw_value)
        except ValueError as exc:
            raise ValueError("Seed must be a signed whole number or left blank.") from exc

    def _build_request(self) -> GenerationRequest:
        """Create one validated generation request from control state."""
        return GenerationRequest(
            language=Language(self.language_var.get()),
            mood=Mood(self.mood_var.get()),
            quantity=self._parse_quantity(),
            seed=self._parse_seed(),
        )

    def _generate(self) -> None:
        """Generate a complete batch and replace preview only on success."""
        try:
            request = self._build_request()
            new_batch = generate_batch(request)
        except ValueError as exc:
            messagebox.showerror(
                "Invalid input",
                str(exc),
                parent=self.root,
            )
            return
        except GenerationError as exc:
            messagebox.showerror(
                "Generation failed",
                str(exc),
                parent=self.root,
            )
            return
        except LookupError:
            messagebox.showerror(
                "Content unavailable",
                "The selected fortune content is not available.",
                parent=self.root,
            )
            return

        # Only commit preview state after the entire generation succeeds.
        self.preview_batch = new_batch
        self._render_preview()

    def _render_preview(self) -> None:
        """Render the committed preview batch without making it editable."""
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", tk.END)

        for index, fortune in enumerate(self.preview_batch, start=1):
            self.preview_text.insert(
                tk.END,
                f"{index}. {fortune}\n\n",
            )

        self.preview_text.configure(state="disabled")
        self.preview_text.yview_moveto(0)

        count = len(self.preview_batch)

        if count == 1:
            self.status_var.set("1 fortune in current preview.")
        else:
            self.status_var.set(f"{count} fortunes in current preview.")

    def _export_txt(self) -> None:
        """Export the current preview batch as a UTF-8 text file."""
        if not self.preview_batch:
            messagebox.showerror(
                "Nothing to export",
                "Generate a fortune batch before exporting.",
                parent=self.root,
            )
            return

        file_path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export fortunes as text",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"),),
        )

        if not file_path:
            return

        try:
            content = "\n".join(self.preview_batch) + "\n"
            with open(file_path, "w", encoding="utf-8", newline="\n") as file:
                file.write(content)
        except OSError as exc:
            messagebox.showerror(
                "Export failed",
                f"The text file could not be saved.\n\n{exc}",
                parent=self.root,
            )
            return

        messagebox.showinfo(
            "Export complete",
            "The fortune batch was exported successfully.",
            parent=self.root,
        )

    def _export_pdf(self) -> None:
        """Export the current preview batch as printable A4 PDF slips."""
        if not self.preview_batch:
            messagebox.showerror(
                "Nothing to export",
                "Generate a fortune batch before exporting.",
                parent=self.root,
            )
            return

        file_path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export printable fortune PDF",
            defaultextension=".pdf",
            filetypes=(("PDF files", "*.pdf"),),
        )

        if not file_path:
            return

        try:
            export_pdf(
                self.preview_batch,
                file_path,
            )
        except PdfExportError as exc:
            messagebox.showerror(
                "PDF export failed",
                str(exc),
                parent=self.root,
            )
            return

        messagebox.showinfo(
            "Export complete",
            "The printable fortune PDF was exported successfully.",
            parent=self.root,
        )


def build_app() -> tk.Tk:
    """Create and configure the FortuneForge main window."""
    root = tk.Tk()
    FortuneForgeApp(root)
    return root


def main() -> None:
    """Launch the FortuneForge desktop application."""
    app = build_app()
    app.mainloop()


if __name__ == "__main__":
    main()
