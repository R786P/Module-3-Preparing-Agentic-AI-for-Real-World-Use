from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from crewai import Crew
from app.agents import researcher, writer, reviewer
from app.tasks import create_tasks

app = FastAPI(title="AI Project Analyzer")

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, repo_url: str = Form(...)):
    if not repo_url or not repo_url.strip():
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "❌ Error: Please provide a valid GitHub repository URL",
            "repo_url": ""
        })
    
    try:
        tasks = create_tasks(repo_url.strip())
        crew = Crew(
            agents=[researcher, writer, reviewer],
            tasks=tasks,
            verbose=True
        )
        result = crew.kickoff()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": str(result),
            "repo_url": repo_url
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"❌ Error: {str(e)}",
            "repo_url": repo_url
        })

