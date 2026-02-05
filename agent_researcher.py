import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import PDFSearchTool, TavilySearchTool # Native CrewAI tools

load_dotenv()

# 1. Setup Tools
# The PDF tool for your CV
pdf_tool = PDFSearchTool(pdf="data/knowledge.pdf")

# The Native CrewAI Tavily tool (This fixes the Pydantic error)
# It will automatically look for TAVILY_API_KEY in your .env
search_tool = TavilySearchTool()

# 2. Define the Agent
researcher = Agent(
    role='UK Tech Recruitment Specialist',
    goal='Compare candidate skills from a CV to current UK market trends.',
    backstory='Expert at identifying skill gaps for AI roles in London.',
    tools=[pdf_tool, search_tool], 
    verbose=True,
    allow_delegation=False
)

# 3. Define the Task
task = Task(
    description=(
        "Search the CV (knowledge.pdf) for technical skills. "
        "Search the web for '2026 AI Engineer job requirements in London'. "
        "Compare them and recommend the #1 skill to learn next."
    ),
    expected_output="A professional report comparing skills with a learning recommendation.",
    agent=researcher,
    output_file="report.md"  # This automatically creates a file with the results
)
# 4. Kickoff
crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()

print("\n--- 🤖 CAREER GAP ANALYSIS ---")
print(result)