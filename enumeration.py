import sqlite3
import json
import random
from datetime import datetime, timedelta
import os
import time
import tempfile
from pathlib import Path
from theatrics import Me, dev_comment, test, pprint, sudo, equip #oh yeah
from consentform import ConsentKey
from LIMain import get_evidence_dir, get_session_dir
import tkinter as tk
from tkinter import filedialog#listen i really need to learn this stupid library for class
#we could have the user explore their files. and drag and drop what they wanna show off?????

##Persona: foothold, Closeness: 10.0, Slip Intensity: 17.78
# Corrupted Output: CONSENT_UNDERSTANDING—CONSENT_UNDERSTANDING
#he gets it :)
#we need a seperate entity to deal with network logic and browsers. 
class FileCrawler:
    def __init__(self, consent_form):
        self.consent_form = consent_form
        self.consent_given = consent_form.consent_given
        self.out_of_scope_items = consent_form.out_of_scope_items
        self.db_path = self.get_db_path() 
        self.evidence_dir = self.get_evidence_dir()
        self.slip_intensity = 0
        self.knowledge_base = {}
        self.initialize_db()
    def initialize_db(self):
        try:
            os.makedirs(self.evidence_dir, exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evidence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    data_type TEXT,
                    data_content TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
    def collect_evidence(self, data_type, data_content):
        if not self.consent_given:
            print("Consent not given. Cannot collect evidence.")
            return
        if data_type in self.out_of_scope_items:
            print(f"Data type '{data_type}' is out of scope. Skipping collection.")
            return
        timestamp = datetime.now().isoformat()
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO evidence (timestamp, data_type, data_content)
                VALUES (?, ?, ?)
            """, (timestamp, data_type, json.dumps(data_content)))
            conn.commit()
            conn.close()
            self.knowledge_base[data_type] = data_content
            self.slip_intensity += 1
        except Exception as e:
            print(f"❌ Database error: {e}")
            conn.close()
    def get_evidence_dir(self, evidence_dir=None):
        """Get platform-aware evidence directory."""
        if evidence_dir is None:
            base_dir = Path.home() / "ethical_crawler" #but the folder is tmp/ethical_crawler not _data. remember li says thats where he resides. we should keep it consistent. we'rll do same dir for now for test but we can change it later.
            evidence_dir = base_dir / "evidence"
            evidence_dir.mkdir(parents=True, exist_ok=True)
            return evidence_dir
    def display_file_explorer(self):#a shared folder #like a vm # its not allowing input...OH. alright alright ill stop poking and pipe in
        if not self.consent_given:
            print("Consent not given. Cannot display file explorer.")
            return
        


        def open_file_explorer():
            # Open file dialog starting from a specific directory
            file_path = filedialog.askopenfilename(
                initialdir=self.get_evidence_dir().parent, # Set your desired starting directory here
                title="My Bin",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                label.config(text=f"Selected File: {file_path}")

        # Create main window
        root = tk.Tk()
        root.title("My Bin")  # Set the title of the window
        root.geometry("400x200")

        # Add label and button
        label = tk.Label(root, text="Nothing", wraplength=300)
        label.pack(pady=10)

        button = tk.Button(root, text="Open File Explorer", command=open_file_explorer)
        button.pack(pady=10)

        # Run the application
        root.mainloop()
#tikinter lets you log key presses.....
#wcan tkinter handle pretending to play terminal?
#doesn'tmattter

    def get_db_path(self, db_path=None):
            """Get platform-aware database path.""" #propogate from that source. think enumeration sweetie. 
            if db_path is None:
                base_dir = Path.home() / "tmp/ethical_crawler"
                base_dir.mkdir(parents=True, exist_ok=True)
                return base_dir / "evidence.db"
#If you don’t call the mainloop() method, the main window will display and disappear almost instantly – too quickly to perceive its appearance.
    def display_file_explorer(self):#a shared folder #like a vm
        if not self.consent_given:
            print("Consent not given. Cannot display file explorer.")
            return
        
        import tkinter as tk
        from tkinter import filedialog

        def open_file_explorer():
            # Open file dialog starting from a specific directory
            file_path = filedialog.askopenfilename(
                initialdir=self.get_evidence_dir().parent, # Set your desired starting directory here
                title="My Bin",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                label.config(text=f"Selected File: {file_path}")

        # Create main window
        root = tk.Tk()
        root.title("My Bin")  # Set the title of the window
        root.geometry("400x200")

        # Add label and button
        label = tk.Label(root, text="Nothing", wraplength=300)
        label.pack(pady=10)

        button = tk.Button(root, text="Open File Explorer", command=open_file_explorer)
        button.pack(pady=10)

        # Run the application
        root.mainloop()
        #this is...my....bin.
        #is there...
        #anything you want to show me {user_name}?
        #dev_comment("better check what you toss kiddo")
    #we already do that. the logs in the quips. we just need to make sure to log the enumeration. we can have a seperate log for enumeration. and then we can have a seperate log for the quips. #i mean...thats all in the same table.....
    #isn't it?
    #do that later
 #im confused what isn't firing #
if __name__ == "__main__":
    consent_form = ConsentKey()
    try:
        consent_form.display()  # Display the consent form before collecting consent
    except Exception as e:
        print(f"❌ Error displaying consent form: {e}")

    else:
        print("Consent form displayed successfully.")
        get_evidence_dir()  # Ensure evidence directory is created
        filer= FileCrawler(consent_form)
        filer.display_file_explorer()
#this is...my....bin.
#is there...anything you'd like to show me?
#dev_comment("better check what you toss kiddo")
#they asked for this....i threw up enough warnings. they know what they signed up for. #also we can have the file explorer be the first thing they see after consenting. and then we can have the crawler collect data on what they click on and how long they look at it and all that good stuff. #we can also have a seperate log for the file explorer interactions. #and then we can have a seperate log for the quips. #i mean...thats all in the same table..... #isn't it? #do that later
