from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class WritingAgent:
    def __init__(self, advertised_object, store_link):
        self.llm = ChatOpenAI(temperature=0.7)
        self.object = advertised_object
        self.link = store_link

    async def write_email(self, research_data):
        prompt = ChatPromptTemplate.from_template(
            """You are a professional cold email copywriter. Write a compelling, personalized retargeting email to {name}, a {title} at {company}.
Promote the following product: {object}.
Use expert B2B strategies:
- Friendly but professional tone
- Focus on benefits and ROI
- Include this CTA link: {link}
- Keep it under 150 words"""
        )
        messages = prompt.format_messages(**research_data, object=self.object, link=self.link)
        response = await self.llm.apredict_messages(messages)
        return str(response.content)
