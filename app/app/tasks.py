from crewai import Task

def create_tasks(repo_url: str):
    research_task = Task(
        description=f"Research similar projects on GitHub for: {repo_url}. Focus on README quality, structure, and best practices.",
        agent=researcher,
        expected_output="List of 2-3 similar projects with key features and README strengths"
    )
    
    write_task = Task(
        description="Suggest 2-3 specific, actionable improvements for the README or project structure based on research.",
        agent=writer,
        expected_output="Clear, numbered suggestions like: '1. Add a How to Run section' or '2. Include a license file'"
    )
    
    review_task = Task(
        description="Validate all suggestions against the actual content of the provided GitHub repo. Reject any inaccurate or irrelevant suggestions.",
        agent=reviewer,
        expected_output="Final verified suggestions with validation notes like: 'Confirmed: README missing installation steps.'"
    )
    
    return [research_task, write_task, review_task]
