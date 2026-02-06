# agents/crew.py
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instat",  # some versions use `model_name`
    temperature=0.3
)

# Define Agents (BINA KOI TOOL KE)
researcher = Agent(
    role="Research Specialist",
    goal="Analyze GitHub repo structure and content",
    backstory="Expert in open-source project analysis",
    llm=llm,
    verbose=True
)

analyst = Agent(
    role="Code Analyst",
    goal="Break down tech stack and architecture",
    backstory="Senior developer who reviews 100+ repos weekly",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Project Reviewer",
    goal="Provide improvement suggestions",
    backstory="Open-source maintainer with 10+ years experience",
    llm=llm,
    verbose=True
)

def create_analysis_task(repo_url: str):
    return Task(
        description=f"Analyze this GitHub repo: {repo_url}. Focus on: tech stack, strengths, weaknesses, and improvement suggestions.",
        expected_output="A structured report with: 1) Repo summary, 2) Languages used, 3) Key insights, 4) 3 actionable suggestions.",
        agent=researcher,
        async_execution=False
    )

def run_crew(repo_url: str):
    task = create_analysis_task(repo_url)
    crew = Crew(
        agents=[researcher, analyst, reviewer],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    result = crew.kickoff()
    return {
        "status": "✅ Analysis Complete",
        "result": str(result)
    }
