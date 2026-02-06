import streamlit as st
import os
from io import BytesIO
from fpdf import FPDF
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import PDFSearchTool, TavilySearchTool

load_dotenv()

# --- HELPER FUNCTION: Convert Markdown to PDF Bytes ---
def create_pdf_bytes(report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Career Gap Analysis Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=11)
    # The 'latin-1' encoding prevents common fpdf encoding errors
    clean_text = report_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    
    # The bytes() wrapper is the key fix for your error
    return bytes(pdf.output(dest='S'))

# --- INITIALIZE SESSION STATE ---
if "stage" not in st.session_state:
    st.session_state.stage = "upload"
if "cv_data" not in st.session_state:
    st.session_state.cv_data = None
if "final_report" not in st.session_state:
    st.session_state.final_report = None

st.set_page_config(page_title="AI Career Agent", layout="wide")
st.title("🤖 Agentic Researcher (End-to-End)")

# --- STAGE 1: UPLOAD ---
import os  # Make sure this is imported at the top!

with st.sidebar:
    st.header("1. Upload CV")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    if uploaded_file and st.session_state.stage == "upload":
        # --- NEW: Ensure the 'data' directory exists ---
        if not os.path.exists("data"):
            os.makedirs("data")
        
        # Save the file to your 'data' folder
        # Save with the actual name instead of a hardcoded one
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.current_file = file_path # Save path for the Agent
        
        st.success("File Ready!")
        if st.button("Begin Profile Extraction"):
            st.session_state.stage = "review"
            st.rerun()

# --- STAGE 2: REVIEW & FEEDBACK ---
if st.session_state.stage == "review":
    st.header("🕵️ Step 1: Profile Extraction")
    with st.status("Agent is reading your CV...", expanded=True):
        # Tell the Agent to look at the specific file the user just gave us
        pdf_tool = PDFSearchTool(pdf=st.session_state.current_file)
        extractor = Agent(
            role='Data Extraction Specialist',
            goal='Accurately list every technical skill in the PDF.',
            backstory='Precision-focused parser.',
            tools=[pdf_tool],
            verbose=True
        )
        extraction_task = Task(
            description="Extract all technical skills and years of experience from 'data/knowledge.pdf'.",
            expected_output="A bulleted list of skills and experience.",
            agent=extractor
        )
        crew = Crew(agents=[extractor], tasks=[extraction_task])
        st.session_state.cv_data = str(crew.kickoff())
    
    st.subheader("What the Agent found:")
    st.info(st.session_state.cv_data)
    
    user_feedback = st.text_area("Anything to add or correct? (Optional)")
    if st.button("Approve & Start Market Research"):
        st.session_state.user_notes = user_feedback
        st.session_state.stage = "final_report"
        st.rerun()

# --- STAGE 3: FINAL EXECUTION & DOWNLOAD ---
if st.session_state.stage == "final_report":
    st.header("🌍 Step 2: Market Comparison")
    
    # Run the report if we haven't yet
    if st.session_state.final_report is None:
        with st.status("Agent is searching 2026 London market trends...", expanded=True):
            search_tool = TavilySearchTool()
            analyst = Agent(
                role='London Tech Career Consultant',
                goal='Identify the gap between user skills and 2026 trends.',
                backstory='Expert in the UK AI market.',
                tools=[search_tool],
                verbose=True
            )
            final_task = Task(
                description=(
                    f"Candidate Skills: {st.session_state.cv_data}\n"
                    f"User Extra Notes: {st.session_state.user_notes}\n"
                    "Task: Compare candidate to 2026 London AI Engineer market trends and provide a gap analysis."
                ),
                expected_output="A final 3-part Career Gap Analysis Report.",
                agent=analyst
            )
            crew = Crew(agents=[analyst], tasks=[final_task])
            st.session_state.final_report = str(crew.kickoff())
    
    st.success("Analysis Complete!")
    st.markdown(st.session_state.final_report)
    
    # --- THE DOWNLOAD BUTTON ---
    st.divider()
    pdf_data = create_pdf_bytes(st.session_state.final_report)

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_data,  # This is now valid 'bytes'
        file_name="Career_Analysis.pdf",
        mime="application/pdf"
    )
    
    if st.button("Start New Analysis"):
        st.session_state.stage = "upload"
        st.session_state.final_report = None
        st.rerun()