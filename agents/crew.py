# agents/crew.py
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from tavily import TavilyClient
import os

# Initialize LLM & Tools
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Define Agents
researcher = Agent(
    role="Research Specialist",
    goal="Find key facts about the GitHub repo using search and code analysis",
    backstory="Expert in open-source project research",
    llm=llm,
    tools=[tavily.search],
    verbose=True
)

analyst = Agent(
    role="Code Analyst",
    goal="Analyze repo structure, languages, and patterns",
    backstory="Senior developer who reads 1000+ repos",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Project Reviewer",
    goal="Give actionable suggestions to improve the repo",
    backstory="Open-source maintainer with 10+ years experience",
    llm=llm,
    verbose=True
)

# Define Task
def create_analysis_task(repo_url: str):
    return Task(
        description=f"Analyze this GitHub repo: {repo_url}. Focus on: tech stack, strengths, weaknesses, and improvement suggestions.",
        expected_output="A structured report with: 1) Repo summary, 2) Language used, 3) Key insights, 4) 3 actionable suggestions.",
        agent=researcher,
        async_execution=False
    )

# Run Crew
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
        "status": "✅ Real Analysis Complete",
        "repo_url": repo_url,
        "analysis": str(result),
        "language": "Python",  # TODO: extract from real analysis
        "stars": "N/A"
  }
