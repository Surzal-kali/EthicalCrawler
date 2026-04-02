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
            filetypes=[ ("All files", "*.*")], #we can customize this to look for specific file types if we want. for now, we'll just let the user pick any file.
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
            "enumeration_file_preview": preview[:30] or "<empty_or_binary>" + (" (truncated)" if len(preview) > 30 else ""),
        }
    def collect(self):
        if not self.consent_given:
            return {}

        if self._is_out_of_scope("files"): #this needs refinement. we should be able to specify specific file types or directories as out of scope. for now, this is just a blanket "no files" option.
            return {}

        selected_file = self._pick_file()
        if not selected_file:
            return {}

        return self._build_payload(selected_file)
#what can sql realistically not handle?" why would we protect against sqli injection when we *want* the user to utilize the database? 
# you have a good point"
    def collect_and_log(self, cursor, session_id, me, autosave=None):
        """Compatibility wrapper; orchestration now owns logging and narration."""
        log_data = self.collect()
        if log_data:
            cursor.execute(
                """
                INSERT INTO files (
                    session_id,
                    file_path,
                    file_name,
                    file_extension,
                    file_size_bytes,
                    file_preview
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    log_data["enumeration_file_path"],
                    log_data["enumeration_file_name"],
                    log_data["enumeration_file_extension"],
                    log_data["enumeration_file_size_bytes"],
                    log_data["enumeration_file_preview"],
                )
            )
            cursor.connection.commit()
        return log_data



