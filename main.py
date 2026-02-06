import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import PDFSearchTool, TavilySearchTool

load_dotenv()

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="AI Career Researcher", page_icon="🤖")
st.title("🚀 AI Career Researcher Agent")
st.markdown("Upload your CV and let the Agent analyze your career gap against 2026 market trends.")

# --- SIDEBAR: Upload PDF ---
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file:
        # Save the uploaded file to your 'data' folder
        with open("data/knowledge.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("CV Uploaded Successfully!")

# --- MAIN INTERFACE ---
query = st.text_input("Ask the Agent a specific question:", "What is the #1 skill I should learn to become a Senior AI Engineer in London?")


if st.button("Run Research Agent"):
    if not os.path.exists("data/knowledge.pdf"):
        st.error("Please upload a CV in the sidebar first!")
    else:
        with st.status("🤖 Agent is analyzing your profile and market trends...", expanded=True) as status:
            # 1. Setup Tools (Force specific file path)
            pdf_tool = PDFSearchTool(pdf="data/knowledge.pdf")
            search_tool = TavilySearchTool()

            # 2. Define the Agent with a more "Comparative" role
            researcher = Agent(
                role='Expert Career Gap Analyst',
                goal='Identify the exact gap between a candidate CV and London 2026 AI market trends.',
                backstory=(
                    'You are a high-end technical headhunter in London. '
                    'You never give generic advice. You always start by extracting real data '
                    'from the provided CV before looking at the market.'
                ),
                tools=[pdf_tool, search_tool],
                verbose=True,
                allow_delegation=False # Keeps the agent focused on its own tools
            )

            # 3. THE FIX: Define a Multi-Step Task Description
            task = Task(
                description=(
                    "Step 1: Use the PDF Tool to extract a detailed summary of the candidate's actual skills from 'data/knowledge.pdf'.\n"
                    "Step 2: Use the Tavily tool to search for 'AI Engineer skills and salary trends in London for 2026'.\n"
                    "Step 3: Compare the CV findings against the market trends.\n"
                    f"Step 4: Answer the user's specific question: '{query}' by creating a report that includes: \n"
                    "- Candidate Skills Summary (from CV)\n"
                    "- 2026 Market Requirements\n"
                    "- Detailed Gap Analysis\n"
                    "- Final Professional Recommendation"
                ),
                expected_output="A structured 4-part Career Gap Analysis report based on the uploaded CV and live web data.",
                agent=researcher
            )

            # 4. Kickoff
            crew = Crew(agents=[researcher], tasks=[task])
            result = crew.kickoff()
            
            status.update(label="✅ Analysis Complete!", state="complete")

        # Display Result using professional formatting
        st.divider()
        st.header("🤖 Your Personalized Career Report")
        st.markdown(result)