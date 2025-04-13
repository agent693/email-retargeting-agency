import pandas as pd

class EmailCollectorAgent:
    def __init__(self, file_path="emails.csv"):
        self.file_path = file_path

    def collect_emails(self):
        df = pd.read_csv(self.file_path)
        return df["email"].dropna().tolist()
