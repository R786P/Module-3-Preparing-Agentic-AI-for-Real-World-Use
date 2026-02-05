from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Repo Analyzer - Module 3")

# Allow CORS (for safety)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"error": "Frontend not found"}

# Mock analyze endpoint (replace with your CrewAI logic later)
@app.post("/analyze")
async def analyze_repo(request: Request):
    data = await request.json()
    repo_url = data.get("repo_url", "").strip()
    
    if not repo_url:
        return {"error": "Missing 'repo_url'"}
    
    # TODO: Replace this with your real CrewAI agent call
    logger.info(f"Analyzing repo: {repo_url}")
    
    return {
        "status": "✅ Mock Analysis Complete",
        "repo_url": repo_url,
        "message": "In real version, CrewAI would analyze this repo.",
        "note": "Replace this response with actual agent output."
    }

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
