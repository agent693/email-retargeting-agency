from fastapi import FastAPI
import asyncio
from agents.manager import ManagerAgent

ADVERTISED_OBJECT = "AI-powered CRM for small businesses"
STORE_LINK = "https://yourstore.com"

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    manager = ManagerAgent(advertised_object=ADVERTISED_OBJECT, store_link=STORE_LINK)
    await manager.run_pipeline()

@app.get("/")
def read_root():
    return {"message": "Email Retargeting Agency is live!"}
