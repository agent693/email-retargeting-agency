from .email_collector import EmailCollectorAgent
from .research_agent import ResearchAgent
from .writing_agent import WritingAgent
from .delivery_agent import DeliveryAgent
from .analytics_agent import AnalyticsAgent
from .reply_agent import ReplyAgent
from .company_research_agent import CompanyResearchAgent
import os

class ManagerAgent:
    def __init__(self, advertised_object, store_link, bundle_deal=None, emails=None):
        self.email_agent = EmailCollectorAgent() if emails is None else None
        self.research_agent = ResearchAgent()
        self.company_agent = CompanyResearchAgent()
        self.writer = WritingAgent(advertised_object, store_link, bundle_deal)
        self.deliverer = DeliveryAgent()
        self.analytics = AnalyticsAgent()
        self.reply_handler = ReplyAgent()
        self.email_list_override = emails
        self.store_link = store_link

        # ✅ Always send to these emails even if already contacted
        if self.email_agent:
            self.email_agent.exempt_emails = [
                "mdowd815@gmail.com",
                "mdowd706@gmail.com"
            ]

    async def run_pipeline(self):
        emails = self.email_agent.collect_emails() if self.email_agent else self.email_list_override
        company_info = await self.company_agent.fetch_metadata(self.store_link)

        delivery_results = []

        if not emails:
            print("No emails to process.")
            return

        for email in emails[:1]:  # Only send one email per /start
            already_sent = []
            if os.path.exists("sent_log.txt"):
                with open("sent_log.txt", "r") as f:
                    already_sent = f.read().splitlines()

            is_repeat = email in already_sent

            data = await self.research_agent.research_email(email)
            data.update(company_info)
            data["followup"] = is_repeat

            content = await self.writer.write_email(data)
            result = await self.deliverer.send_email(email, content)
            self.email_agent.mark_as_sent(email)
            delivery_results.append(result)

        clicked = self.analytics.analyze_clicks(delivery_results)
        replies = self.reply_handler.handle_replies(clicked)
        print("\n[INTERESTED LEADS]", replies)
