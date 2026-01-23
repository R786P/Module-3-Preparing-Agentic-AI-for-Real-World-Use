from app.agents import researcher, writer, reviewer 
from crewai import Task
def create_tasks(repo_url: str):
    research_task = Task(
        description=f"""
        Step 1: Read the actual GitHub repo content from {repo_url}
        Step 2: Then research similar projects and best practices
        Step 3: Compare the actual repo with best practices
        """,
        agent=researcher,
        expected_output="Detailed analysis of the actual repo + comparison with best practices"
    )
    
    write_task = Task(
        description="Suggest 2-3 specific, actionable improvements for the project in Hindi",
        agent=writer,
        expected_output="Clear, numbered suggestions in Hindi like: '1. Add a How to Run section'"
    )
    
    review_task = Task(
        description="Validate all suggestions against the actual content of the provided GitHub repo. Reject any inaccurate or irrelevant suggestions.",
        agent=reviewer,
        expected_output="Final verified suggestions with validation notes in Hindi"
    )
    
    return [research_task, write_task, review_task]
