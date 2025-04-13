from .email_collector import EmailCollectorAgent
from .research_agent import ResearchAgent
from .writing_agent import WritingAgent
from .delivery_agent import DeliveryAgent
from .analytics_agent import AnalyticsAgent
from .reply_agent import ReplyAgent
from .company_research_agent import CompanyResearchAgent

class ManagerAgent:
    def __init__(self, advertised_object, store_link, emails=None):
        self.email_agent = EmailCollectorAgent() if emails is None else None
        self.research_agent = ResearchAgent()
        self.company_agent = CompanyResearchAgent()
        self.writer = WritingAgent(advertised_object, store_link)
        self.deliverer = DeliveryAgent()
        self.analytics = AnalyticsAgent()
        self.reply_handler = ReplyAgent()
        self.email_list_override = emails
        self.store_link = store_link

    async def run_pipeline(self):
        emails = self.email_agent.collect_emails() if self.email_agent else self.email_list_override
        company_info = await self.company_agent.fetch_metadata(self.store_link)

        delivery_results = []

        if emails:
            email = emails[0]  # ✅ Only send to first email
            data = await self.research_agent.research_email(email)
            data.update(company_info)
            content = await self.writer.write_email(data)
            result = await self.deliverer.send_email(email, content)
            delivery_results.append(result)

        clicked = self.analytics.analyze_clicks(delivery_results)
        replies = self.reply_handler.handle_replies(clicked)
        print("\n[INTERESTED LEADS]", replies)
