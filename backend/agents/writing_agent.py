from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from urllib.parse import urlparse

class WritingAgent:
    def __init__(self, advertised_object, store_link, bundle_deal=None):
        self.llm = ChatOpenAI(temperature=0.7)
        self.object = advertised_object
        self.link = store_link
        self.bundle = bundle_deal
        self.business_name = self._extract_business_name(store_link)

    def _extract_business_name(self, url):
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "").split(".")[0]
        return domain.capitalize()

    async def write_email(self, research_data):
        followup = research_data.get("followup", False)

        if followup:
            base_prompt = """
You are a sharp email copywriter helping a brand re-engage potential customers.

Write a short follow-up email (max 120 words) to {name}, a {title} at {company}, who has previously seen our product: {object}.

- Start with a strong subject line
- Mention urgency or a fresh reason to revisit
{bundle_line}
- Include a clear call-to-action (link: {link})
- Close with the brand name: {brand}
Output:
Subject: ...
Body: ...
"""
        else:
            base_prompt = """
You are a pro at cold email retargeting.

Write a short first-touch email (max 120 words) to {name}, a {title} at {company}, introducing our product: {object}.

- Use a punchy subject line
- Keep it clear and curiosity-driven
{bundle_line}
- Include this link: {link}
- Sign off as the brand: {brand}
Output:
Subject: ...
Body: ...
"""

        # ✅ Conditionally include bundle line
        bundle_line = f"- Include this special deal: {self.bundle}" if self.bundle else ""

        prompt_template = base_prompt.replace("{bundle_line}", bundle_line)

        prompt = ChatPromptTemplate.from_template(prompt_template)
        messages = prompt.format_messages(
            **research_data,
            object=self.object,
            link=self.link,
            brand=self.business_name
        )
        response = await self.llm.apredict_messages(messages)
        return str(response.content)
