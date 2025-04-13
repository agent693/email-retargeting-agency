from fastapi import FastAPI
import asyncio
from agents.manager import ManagerAgent

# 🎯 Update this to match your current test product/site
ADVERTISED_OBJECT = "custom phone cases"
STORE_LINK = "https://www.casetify.com"

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Email Retargeting Agency is live!"}

@app.get("/start")
async def run_agent():
    manager = ManagerAgent(advertised_object=ADVERTISED_OBJECT, store_link=STORE_LINK)
    await manager.run_pipeline()
    return {"status": "Pipeline executed"}
