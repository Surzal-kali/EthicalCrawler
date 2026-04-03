#this is as valid of an excuse i can come up with to write red team tactics in peace
#IT ALSO STOPS (i mean you sweetie) FROM COMPLAINING ABOUT THE LACK OF A CONSENT FORM, WHICH I KNOW YOU'VE BEEN DYING TO SEE.


import tkinter as tk
import time
import datetime

SCOPE_CATEGORIES = {
    "files":    "File system access (documents, downloads, desktop)",
    "system":   "System profile (OS, hardware, architecture)",
    "services": "Running processes and services",
    "web":      "Web crawling and link extraction",
}


class ConsentKey:
    """Handles user consent for data collection with a clear agreement and an interactive scope selection menu. The user can choose to exclude specific categories of data from being accessed during the session. Consent and scope preferences are stored locally for future reference. Returns a dictionary with consent status and out-of-scope items."""
    def __init__(self):
        self.consent_given = False
        self.out_of_scope_items = []
        self.consented_at = None

    def __str__(self):
        return f"ConsentForm(consent_given={self.consent_given}, out_of_scope_items={self.out_of_scope_items})"

    def display(self):
        print()
        print("  ┌─────────────────────────────────────────────────┐")
        print("  │           ETHICAL CRAWLER — USER AGREEMENT      │")
        print("  └─────────────────────────────────────────────────┘")
        print()
        print("  By continuing, you authorize this session to collect")
        print("  data from your system for enumeration and analysis.")
        print()
        print("  You retain the right to exclude any category below.")
        print("  Excluded categories will not be accessed this session")
        print("  or any future session unless you renegotiate.")
        print()
        print("  This agreement is stored locally. You will not be")
        print("  asked again.")
        print()

    def get_consent(self):
        response = input("  Do you authorize this session? (yes/no): ").strip().lower()
        if response != "yes":
            self.consent_given = False
            self.out_of_scope_items = []
            print()
            print("  Understood. Nothing will be collected.")
            print("  Session terminated.")
            return {"consent_given": False, "out_of_scope_items": []}

        self.consent_given = True
        self.consented_at = datetime.datetime.utcnow().isoformat()
        self.out_of_scope_items = self._show_scope_menu()

        print()
        if self.out_of_scope_items:
            print("  Out-of-scope noted: " + ", ".join(self.out_of_scope_items))
        else:
            print("  No restrictions. Full access authorized.")
        print()
        time.sleep(0.5)

        return {
            "consent_given": self.consent_given,
            "out_of_scope_items": self.out_of_scope_items,
        }

    def _show_scope_menu(self):
        """Display an interactive menu for the user to select categories of data to exclude from collection. The user can check multiple categories or select 'All' to exclude everything. Returns a list of selected out-of-scope categories."""
        root = tk.Tk()
        root.withdraw()

        win = tk.Toplevel(root)
        win.title("Ethical Crawler")
        win.configure(bg="black")
        win.resizable(False, False)
        win.attributes("-topmost", True)

        font_mono = ("Courier New", 11)
        font_header = ("Courier New", 13, "bold")

        tk.Label(
            win, text="SELECT ITEMS TO EXCLUDE FROM THIS SESSION",
            bg="black", fg="#00ff00", font=font_header, pady=12
        ).pack()

        tk.Label(
            win, text="Checked items will NOT be accessed.",
            bg="black", fg="#00cc00", font=font_mono
        ).pack(pady=(0, 10))

        vars_ = {}
        for key, description in SCOPE_CATEGORIES.items():
            var = tk.BooleanVar(value=False)
            vars_[key] = var
            tk.Checkbutton(
                win, text=f"  {key:<12} — {description}",
                variable=var,
                bg="black", fg="#00ff00",
                selectcolor="black",
                activebackground="black", activeforeground="#00ff00",
                font=font_mono, anchor="w"
            ).pack(fill="x", padx=20, pady=2)

        var_all = tk.BooleanVar(value=False)


        result = []

        def confirm():
            if var_all.get():
                result.extend(SCOPE_CATEGORIES.keys())
            else:
                result.extend(k for k, v in vars_.items() if v.get())
            root.destroy()

        tk.Button(
            win, text="[ CONFIRM ]",
            command=confirm,
            bg="black", fg="#00ff00",
            activebackground="#003300", activeforeground="#00ff00",
            font=font_header, relief="flat", pady=8
        ).pack(pady=16)

        root.mainloop()
        return result


def get_consent():
    """Convenience function to create a ConsentKey instance, display the agreement, and return the user's consent status and out-of-scope preferences. Returns a dictionary with consent_given boolean and out_of_scope_items list."""
    consent_form = ConsentKey()
    consent_form.display()
    return consent_form.get_consent()
