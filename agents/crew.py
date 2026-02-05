# agents/crew.py
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults  # ← IMPORTANT
import os

# Initialize LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)

# ✅ Correct Tavily tool (LangChain compatible)
tavily_tool = TavilySearchResults(
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
    max_results=3
)

# Define Agents
researcher = Agent(
    role="Research Specialist",
    goal="Find key facts about the GitHub repo using search",
    backstory="Expert in open-source project research",
    llm=llm,
    tools=[tavily_tool],  # ← Now valid!
    verbose=True
)

analyst = Agent(
    role="Code Analyst",
    goal="Analyze repo structure and tech stack",
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

def create_analysis_task(repo_url: str):
    return Task(
        description=f"Analyze this GitHub repo: {repo_url}. Focus on: tech stack, strengths, weaknesses, and improvement suggestions.",
        expected_output="A structured report with: 1) Repo summary, 2) Language used, 3) Key insights, 4) 3 actionable suggestions.",
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
        "status": "✅ Real Analysis Complete",
        "repo_url": repo_url,
        "analysis": str(result)
    }
