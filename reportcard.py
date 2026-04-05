from theatrics import dev_comment, clear
from consentform import ConsentKey
import time


class ReportCard:
    def __init__(self, consent_form):
        self.consent_form = consent_form
        self.consent_given = consent_form.consent_given
        self.out_of_scope_items = consent_form.out_of_scope_items

    def _is_out_of_scope(self, data_type: str) -> bool:
        return data_type.strip().lower() in self.out_of_scope_items

    def generate(self, store, session_id, me, autosave=None):
        if not self.consent_given:
            dev_comment("ReportCard: consent not given, skipping.")
            return {}
        if self._is_out_of_scope("report card"):
            dev_comment("ReportCard: out of scope, skipping.")
            return {}

        rows = store.get_log()
        report_card = {
            "session_id": session_id,
            "persona": me.persona,
            "total_entries": len(rows),
            "by_context": {
                "enumeration":     [r for r in rows if r["context"] == "enumeration"],
                "web_crawling":    [r for r in rows if r["context"] == "web_crawling"],
                "system_profiler": [r for r in rows if r["context"] == "system_profiler"],
                "services":        [r for r in rows if r["context"] == "services"],
            }, 
            "timestamp": time.time(),
        }
        dev_comment(f"ReportCard: {len(rows)} entries across {len(report_card['by_context'])} contexts.")
        return report_card

def report():
    consent_form = ConsentKey()
    consent_form.display()
    consent_data = consent_form.get_consent()
    print(consent_data)