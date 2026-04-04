from pathlib import Path
from tkinter import filedialog
import tkinter as tk

class FileCrawler:
    def __init__(self, consent_form):
        self.consent_form = consent_form
        self.consent_given = consent_form.consent_given
        self.out_of_scope_items = {
            item.strip().lower() for item in (consent_form.out_of_scope_items or []) if item.strip()
        }

    def _is_out_of_scope(self, data_type: str) -> bool:
        return data_type.strip().lower() in self.out_of_scope_items
    def _pick_file(self):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        file_path = filedialog.askopenfilename(
            title="My Bin",
            filetypes=[ ("All files", "*.*")], 
        )
        root.destroy()
        return file_path

    def _build_payload(self, file_path: str):
        """
        Build a payload dictionary with file metadata and a content preview. This includes the file path, name, extension, size in bytes, and a preview of the first 300 characters of the file content (with non-text files handled gracefully). takes file_path as a parameter and returns a dictionary with the collected data.
        """
        selected = Path(file_path)
        size_bytes = selected.stat().st_size
        preview = ""
        try:
            with selected.open("r", encoding="utf-8", errors="replace") as handle:
                preview = handle.read(300).strip()
        except OSError:
            preview = ""

        return {
            "enumeration_file_path": str(selected),
            "enumeration_file_name": selected.name,
            "enumeration_file_extension": selected.suffix.lower() or "<none>",
            "enumeration_file_size_bytes": size_bytes,
            "enumeration_file_preview": preview or "<empty_or_binary>",
        }

    def collect(self):
        if not self.consent_given:
            return {}

        # Blanket file exclusion — per-type/directory refinement planned for Act II
        if self._is_out_of_scope("files"):
            return {}

        selected_file = self._pick_file()
        if not selected_file:
            return {}

        return self._build_payload(selected_file)

    def collect_and_log(self, autosave=None):
        """Compatibility wrapper; orchestration owns logging and narration."""
        return self.collect()

# TODO: loop collect() to allow multi-file picks, returning a list logged one at a time.
# Separate links table planned; background crawl process post-report-card.