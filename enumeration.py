import os
from pathlib import Path
from time import sleep
from importlib.metadata  import files, version
from theatrics import Me, speak, typewriter_effect, clear
from tkinter import filedialog
import tkinter as tk
#we work on this first.
class FileCrawler:
    #stays
    def __init__(self, consent_form):
        self.consent_form = consent_form
        self.consent_given = consent_form.consent_given
        self.out_of_scope_items = {
            item.strip().lower() for item in (consent_form.out_of_scope_items or []) if item.strip()
        }


    def _is_out_of_scope(self, data_type: str) -> bool:
        return data_type.strip().lower() in self.out_of_scope_items
    
    def _pick_folder(self):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)  # Bring the dialog to the front

        folder_path = filedialog.askdirectory(title="Select a folder to crawl")
        return folder_path if folder_path else None
#yeth
    def _build_payload(self, folder_path: str):
        """
        Build a payload dictionary with file metadata and a content preview. This includes the file path, name, extension, size in bytes, and a preview of the first 300 characters of the file content (with non-text files handled gracefully). takes file_path as a parameter and returns a dictionary with the collected data. Needs to also take file size, type, and metadta from details if possible. #yeth
        """
        selected = Path(folder_path)
        size_bytes = selected.stat().st_size
        preview = ""
        if selected.is_file():
            try:
                with selected.open("r", encoding="utf-8", errors="ignore") as f:
                    preview = f.read(300) #oh
                folderstep = {
                    "enumeration_file_path": str(selected),
                    "enumeration_file_name": selected.name,
                    "enumeration_file_extension": selected.suffix.lower() or "<none>",
                    "enumeration_file_size_bytes": size_bytes,
                    "enumeration_file_type": "text" if preview else "binary_or_unreadable",
                    "enumeration_details": {},  # Placeholder for future metadata extraction
                    "enumeration_file_preview": preview or "<empty_or_binary>",
                } 
                return folderstep
            except Exception as e:
                folderstep = {
                    "File skipped due to error": f"{type(e).__name__}: {str(e)}"
                }
                return folderstep
        else: 
            folderstep = {
                "enumeration_folder_path": str(selected),
                "enumeration_folder_name": selected.name,
                "enumeration_folder_size_bytes": size_bytes,
                "enumeration_details": {},  # Placeholder for future metadata extraction
            }
            return folderstep

    def collect(self, cores, frequency, autosave=None):
        if not self.consent_given:
            return {}

        # Blanket file exclusion — per-type/directory refinement planned for Act II
        if self._is_out_of_scope("files"):
            return {}

        collected_folder = self._pick_folder()
        if collected_folder is None:
            return {}

        collected_folder = Path(collected_folder)
        for file in collected_folder.rglob("*"):
            if file.suffix.lower() in [".txt", ".log"]: 
                payload = self._build_payload(file)
                sleep(1 / frequency)
                return payload
        payload = self._build_payload(collected_folder)
        return payload


#digestion logic per fileshould go here