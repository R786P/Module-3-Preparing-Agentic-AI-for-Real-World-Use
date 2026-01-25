from crewai import Agent
from langchain_groq import ChatGroq
import os
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)
# Tools (Tavily - free web search)
from crewai_tools import TavilySearchTool
tavily_tool = TavilySearchTool()

# Agents
researcher = Agent(
    role="Senior Researcher",
    goal="Find relevant info about the GitHub project using web search",
    backstory="Expert in web research with 10+ years of experience",
    tools=[tavily_tool],
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="सुझाव हिंदी में दें",
    backstory="आप हिंदी में स्पष्ट और क्रियाशील सुझाव लिखते हैं",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Validate suggestions against facts",
    backstory="Ensures accuracy and relevance",
    llm=llm,
    verbose=True
)
