from pathlib import Path
from tkinter import filedialog
import tkinter as tk

from database import log
from theatrics import test


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
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        root.destroy()
        return file_path

    def _build_payload(self, file_path: str):
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

    def collect_and_log(self, cursor, session_id, me, autosave=None):
        if not self.consent_given:
            return {}

        if self._is_out_of_scope("files"):
            return {}

        selected_file = self._pick_file()
        if not selected_file:
            return {}

        payload = self._build_payload(selected_file)
        for field, value in payload.items():
            log(cursor, session_id, field, value, me, context="enumeration")
            if autosave is not None:
                autosave.add(field, value, context="enumeration")

        test(me, "file_understanding")
        return payload

