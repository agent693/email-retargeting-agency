import requests
from bs4 import BeautifulSoup

class CompanyResearchAgent:
    async def fetch_metadata(self, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string if soup.title else "No title found"
            desc = soup.find("meta", attrs={"name": "description"})
            description = desc.get("content") if desc and desc.get("content") else "No description found"

            return {
                "site_title": title.strip(),
                "site_description": description.strip()
            }

        except Exception as e:
            return {
                "site_title": "Site info unavailable",
                "site_description": str(e)
            }
