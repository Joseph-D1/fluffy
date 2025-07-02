from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import httpx
import asyncio
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

STATUS_FILE = "status.json"
SITES_FILE = "sites.json"

class SiteStatus(BaseModel):
    url: str
    status: str
    status_code: int = None
    response_time: float = None
    checked_at: str = None

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_sites())

async def monitor_sites():
    ''' For each site in the sites file, check if it is up and update the status file '''
    while True:
        with open(SITES_FILE, 'r') as f:
            sites = json.load(f)
        
        results = []
        async with httpx.AsyncClient() as client:
            tasks = [check_site(client, site) for site in sites]
            results = await asyncio.gather(*tasks)
        
        with open(STATUS_FILE, 'w') as f:
            json.dump(results, f, indent=4)
            
        await asyncio.sleep(30)  # Check every 30s

async def check_site(client, url):
    ''' request the site, capture response info '''
    try:
        response = await client.get(url, follow_redirects=True, timeout=10)
        return {
            "url": url,
            "status": "Up" if response.status_code == 200 else "Down",
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "checked_at": response.headers.get('date')
        }
    except httpx.RequestError as exc:
        return {
            "url": url,
            "status": "Down",
            "error": str(exc)
        }

@app.get("/api/status", response_model=List[SiteStatus])
async def get_status():
    ''' get the information from the status file to update the frontend '''
    try:
        with open(STATUS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
