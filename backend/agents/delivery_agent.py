import smtplib
from email.mime.text import MIMEText
import os
import asyncio

class DeliveryAgent:
    def __init__(self):
        self.email = os.getenv("AGENCY_EMAIL")
        self.password = os.getenv("AGENCY_PASSWORD")
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.email, self.password)

    async def send_email(self, to, content):
        await asyncio.sleep(0.1)
        msg = MIMEText(content)
        msg['Subject'] = 'A quick idea for you'
        msg['From'] = self.email
        msg['To'] = to
        self.server.sendmail(self.email, [to], msg.as_string())
        print(f"[SENT] Email to {to}")
        return {"email": to, "status": "sent", "clicked": True}
