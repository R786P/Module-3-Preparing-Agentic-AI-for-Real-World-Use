import os
from langchain_groq import ChatGroq
from crewai import Agent
import logging

# Accept multiple possible env var names (fallback)
GROQ_API_KEY_NAME = None
GROQ_API_KEY = (
    os.getenv("GROQ_API_KEY")
    or os.getenv("GROK_API_KEY")   # tolerate spelling variation
    or os.getenv("grok_api_key")
    or os.getenv("API_KEY")
)
if GROQ_API_KEY:
    # detect which env name existed (for logging only)
    if os.getenv("GROQ_API_KEY"):
        GROQ_API_KEY_NAME = "GROQ_API_KEY"
    elif os.getenv("GROK_API_KEY"):
        GROQ_API_KEY_NAME = "GROK_API_KEY"
    elif os.getenv("grok_api_key"):
        GROQ_API_KEY_NAME = "grok_api_key"
    else:
        GROQ_API_KEY_NAME = "API_KEY"

# DEFAULT model: use a Groq model that README suggests (change if you use different)
MODEL_NAME = os.getenv("GROQ_MODEL") or os.getenv("MODEL_NAME") or "llama3-8b-8192"

if not GROQ_API_KEY:
    # Fail early with a readable error so logs show what's missing
    raise RuntimeError(
        "No Groq API key found. Set GROQ_API_KEY (or GROK_API_KEY / grok_api_key) in environment."
    )

logging.info(f"Using Groq API key from env var: {GROQ_API_KEY_NAME}")
logging.info(f"Using LLM model: {MODEL_NAME}")

llm = ChatGroq(
    model=MODEL_NAME,
    temperature=0,
    groq_api_key=GROQ_API_KEY
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
