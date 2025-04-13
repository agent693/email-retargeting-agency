import pandas as pd
import os

class EmailCollectorAgent:
    def __init__(self, file_path="emails.csv", sent_log_path="sent_log.txt"):
        self.file_path = file_path
        self.sent_log_path = sent_log_path
        self.exempt_emails = []  # Add emails here if you want to always send to them

    def collect_emails(self):
        if not os.path.exists(self.file_path):
            return []

        df = pd.read_csv(self.file_path)
        all_emails = df["email"].dropna().tolist()

        if os.path.exists(self.sent_log_path):
            with open(self.sent_log_path, "r") as log:
                already_sent = log.read().splitlines()
        else:
            already_sent = []

        # ✅ Allow duplicates if explicitly exempted
        unsent_emails = [
            e for e in all_emails if e not in already_sent or e in self.exempt_emails
        ]

        return unsent_emails

    def mark_as_sent(self, email):
        with open(self.sent_log_path, "a") as log:
            log.write(f"{email}\n")
