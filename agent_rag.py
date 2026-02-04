import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool

load_dotenv()

# 1. Define the PDF Tool (Points to your CV)
# This allows the Agent to "search" the PDF whenever it needs to
pdf_tool = PDFSearchTool(pdf="data/knowledge.pdf")

# 2. Define the Agent
# We give it a "Role" and a "Goal" so it knows its purpose
researcher = Agent(
    role='Expert Career Advisor',
    goal='Answer questions about the candidate based on their CV.',
    backstory='You are a specialist recruiter in the UK tech market. You use the provided CV to give accurate advice.',
    tools=[pdf_tool],
    verbose=True, # This lets us see the Agent "thinking" in the terminal
    allow_delegation=False,
    memory=True
)

# 3. Define the Task
task = Task(
    description="Analyze the CV and answer: 'What are the top 3 technical skills of this candidate?'",
    expected_output="A bulleted list of the top 3 skills found in the CV with a brief explanation for each.",
    agent=researcher
)

# 4. Create the Crew (The Team)
crew = Crew(
    agents=[researcher],
    tasks=[task],
    process=Process.sequential
)

# ... (rest of your code above)

# 5. Kick off the work!
print("--- 🚀 Agent is starting to think... ---")
try:
    # Adding a print here to confirm the result is being captured
    result = crew.kickoff()
    
    print("\n" + "="*30)
    print("--- 🤖 FINAL AGENT RESPONSE ---")
    print(result)
    print("="*30 + "\n")
except Exception as e:
    print(f"❌ An error occurred: {e}")