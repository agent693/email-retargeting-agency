import asyncio

class ResearchAgent:
    async def research_email(self, email):
        await asyncio.sleep(0.1)
        return {
            "email": email,
            "name": email.split("@")[0].capitalize(),
            "company": "ExampleCorp",
            "title": "Marketing Manager"
        }
