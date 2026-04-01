#this is as valid of an excuse i can come up with to write red team tactics in peace
#IT ALSO STOPS (i mean you sweetie) FROM COMPLAINING ABOUT THE LACK OF A CONSENT FORM, WHICH I KNOW YOU'VE BEEN DYING TO SEE.

#should we move runme around?
#i meant structually. story beats.
#it needs to have some flair. can we add the class to a gui? more like an ibm mainframe terminal. #you should watch sneakers 

class ConsentKey:
    def __init__(self):
        self.consent_given = False
        self.out_of_scope_items = []
    def annoyingmessage(self):
        print("This is a consent form. Please read carefully.")
        print("By giving consent, you allow this session to proceed.")
        print("You may withdraw consent at any time by ending the session.")
    def __str__(self):
        return f"ConsentForm(consent_given={self.consent_given}, out_of_scope_items={self.out_of_scope_items})"
    def display(self):
        print("Welcome to the Ethical Crawler Consent Form.")
        print("By giving consent, you allow this session to proceed.")
        print("You may withdraw consent at any time by ending the session.")
        print()

    def get_consent(self):
        while True:
            response = input("Do you give your consent? (yes/no): ").strip().lower()

            if response == "yes":
                self.consent_given = True
                raw_items = input(
                    "Please list out-of-scope items, separated by commas: "
                ).strip()

                self.out_of_scope_items = [
                    item.strip()
                    for item in raw_items.split(",")
                    if item.strip()
                ] if raw_items else []

                print("Thank you. The show may begin.")
                if self.out_of_scope_items:
                    print(
                        "Out-of-scope items noted: "
                        + ", ".join(self.out_of_scope_items)
                    )
                else:
                    print("No out-of-scope items were provided.")

                return {
                    "consent_given": self.consent_given,
                    "out_of_scope_items": self.out_of_scope_items,
                }

            if response == "no":
                self.consent_given = False
                self.out_of_scope_items = []
                print("Understood. I will not collect anything.")
                print("Session terminated.")
                return {
                    "consent_given": self.consent_given,
                    "out_of_scope_items": self.out_of_scope_items,
                }

            print("Invalid response. Please enter 'yes' or 'no'.")


def get_consent():
    consent_form = ConsentKey()
    consent_form.display()
    result = consent_form.get_consent()
    print()
    print("Consent summary:")
    print(result)
    return result
