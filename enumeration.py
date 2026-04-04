import os
from pathlib import Path
from time import sleep
from importlib.metadata  import version
from theatrics import Me, speak, typewriter_effect, clear
from tkinter import filedialog
import tkinter as tk

class FileCrawler:
    #stays
    def __init__(self, consent_form):
        self.consent_form = consent_form
        self.consent_given = consent_form.consent_given
        self.out_of_scope_items = {
            item.strip().lower() for item in (consent_form.out_of_scope_items or []) if item.strip()
        }

#yeth pick file is dead code and breaking it. 
    def _is_out_of_scope(self, data_type: str) -> bool:
        return data_type.strip().lower() in self.out_of_scope_items
    
    def _pick_file(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(title="Select a file to crawl")
        return file_path if file_path else None
#stays
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

        filesteps = {
            "enumeration_file_path": str(selected),
            "enumeration_file_name": selected.name,
            "enumeration_file_extension": selected.suffix.lower() or "<none>",
            "enumeration_file_size_bytes": size_bytes,
            "enumeration_file_preview": preview or "<empty_or_binary>",
        }
        return filesteps
    def collect(self, cores, frequency, autosave=None):
        if not self.consent_given:
            return {}

        # Blanket file exclusion — per-type/directory refinement planned for Act II
        if self._is_out_of_scope("files"):
            return {}
        
        for file in os.listdir("."):
            if file.endswith(".txt") or file.endswith(".log"):
                payload = self._build_payload(file)
                sleep(1 / frequency)
                return payload
        collected_files = self._pick_file()
        if collected_files:
            payload = self._build_payload(collected_files)
            return payload
        else:
            return {} 