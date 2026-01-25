import os
from langchain_groq import ChatGroq
from crewai import Agent

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="gpt-oss-20b",
    temperature=0,
    groq_api_key=groq_api_key
)

researcher = Agent(
    role="Senior Researcher",
    goal="Analyze the GitHub repository and extract key insights",
    backstory="You are an expert in code analysis and software architecture.",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Technical Writer",
    goal="Write a clear and structured report",
    backstory="You specialize in explaining technical concepts simply.",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Ensure accuracy and completeness of the report",
    backstory="You have 10+ years of experience in software documentation.",
    llm=llm,
    verbose=True
)
