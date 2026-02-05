from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from agents.crew import run_crew  # ← NEW IMPORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Repo Analyzer - Module 3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"error": "Frontend not found"}

@app.post("/analyze")
async def analyze_repo(request: Request):
    data = await request.json()
    repo_url = data.get("repo_url", "").strip()
    
    if not repo_url:
        return {"error": "Missing 'repo_url'"}
    
    try:
        logger.info(f"Starting CrewAI analysis for: {repo_url}")
        result = run_crew(repo_url)
        return result
    except Exception as e:
        logger.error(f"CrewAI error: {e}")
        return {
            "error": "Analysis failed",
            "details": str(e)
        }

@app.get("/health")
def health():
    return {"status": "ok"}
