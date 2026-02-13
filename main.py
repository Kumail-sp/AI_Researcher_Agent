import streamlit as st
import os
import shutil
import uuid
import stat
from fpdf import FPDF
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import TavilySearchTool

load_dotenv()

# --- PDF READING FUNCTION ---
def extract_pdf_text(pdf_path):
    """Extract text from PDF"""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text
    except ImportError:
        try:
            import pypdf
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
                return text
        except ImportError:
            return "❌ Install: pip install pdfplumber"
    except Exception as e:
        return f"❌ Error: {e}"

# --- SESSION ID ---
def get_session_id():
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        if ctx: return ctx.session_id
    except Exception:
        pass
    if "session_id" not in st.session_state:
        st.session_state.session_id = uuid.uuid4().hex[:8]
    return st.session_state.session_id

session_id = get_session_id()

# --- HELPERS ---
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def create_pdf_bytes(report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Career Gap Analysis Report", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    clean_text = report_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, text=clean_text)
    
    # Handle both old and new FPDF versions
    output = pdf.output(dest='S')
    
    # Convert to bytes regardless of type
    if isinstance(output, (bytes, bytearray)):
        return bytes(output)  # Convert bytearray or bytes to bytes
    else:
        return output.encode('latin-1')  # Old version returns string

# --- SESSION STATE ---
if "stage" not in st.session_state:
    st.session_state.stage = "upload"
if "cv_data" not in st.session_state:
    st.session_state.cv_data = None
if "final_report" not in st.session_state:
    st.session_state.final_report = None
if "cv_text" not in st.session_state:
    st.session_state.cv_text = None

st.set_page_config(page_title="AI Career Agent", layout="wide")
st.title("🤖 Agentic Researcher (No PDFSearchTool - Raw Text)")

# --- STAGE 1: UPLOAD ---
with st.sidebar:
    st.header("1. Upload CV")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    
    if uploaded_file and st.session_state.stage == "upload":
        if not os.path.exists("data"):
            os.makedirs("data")
        
        upload_id = uuid.uuid4().hex[:8]
        file_path = f"data/cv_{upload_id}.pdf"
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # ✅ EXTRACT TEXT IMMEDIATELY
        cv_text = extract_pdf_text(file_path)
        
        st.session_state.current_file = file_path
        st.session_state.current_upload_id = upload_id
        st.session_state.cv_text = cv_text
        
        file_size = os.path.getsize(file_path)
        st.success(f"✓ Saved: {uploaded_file.name}")
        st.info(f"📊 Size: {file_size:,} bytes | Text: {len(cv_text):,} chars")
        
        # Preview
        with st.expander("📄 Preview CV content"):
            st.text_area("First 500 characters:", cv_text[:500], height=150)
        
        # Clean old files
        for f in os.listdir("data"):
            if f.startswith("cv_") and f != f"cv_{upload_id}.pdf":
                try: 
                    os.remove(os.path.join("data", f))
                except: 
                    pass
        
        if st.button("Begin Profile Extraction"):
            st.session_state.stage = "review"
            st.session_state.cv_data = None
            st.rerun()

# --- STAGE 2: EXTRACTION (NO PDFSearchTool!) ---
if st.session_state.stage == "review":
    st.header("🕵️ Step 1: Profile Extraction")
    st.caption(f"📄 File: {os.path.basename(st.session_state.current_file)}")
    st.caption(f"🔑 Upload ID: {st.session_state.current_upload_id}")
    
    # Show CV content
    with st.expander("📖 CV Content Being Analyzed", expanded=True):
        st.text_area("Full CV Text:", st.session_state.cv_text, height=300)
        st.caption(f"Total characters: {len(st.session_state.cv_text):,}")
    
    # Only extract if needed
    if st.session_state.cv_data is None:
        with st.status("Extracting skills from CV text...", expanded=True):
            st.write(f"📝 Analyzing {len(st.session_state.cv_text):,} characters")
            st.write(f"🔑 Upload ID: {st.session_state.current_upload_id}")
            
            # ✅ AGENT WITHOUT PDFSearchTool - Uses raw text directly
            extractor = Agent(
                role='CV Skills Extractor',
                goal=f'Extract all skills and experience from the CV text for Upload ID: {st.session_state.current_upload_id}',
                backstory="""You are an expert CV analyst. You carefully read CV text and extract:
- Technical skills
- Professional experience
- Qualifications and certifications
- Key competencies

You ONLY extract what is explicitly mentioned in the text provided.""",
                verbose=True,
                allow_delegation=False,
                memory=False
            )
            
            # ✅ PASS RAW TEXT IN DESCRIPTION - No PDFSearchTool needed!
            extraction_task = Task(
                description=f"""Analyze this CV for Upload ID: {st.session_state.current_upload_id}

CV TEXT:
---
{st.session_state.cv_text}
---

TASK:
1. Extract ALL skills (technical and soft skills)
2. Extract ALL work experience and roles
3. Extract ALL qualifications, certifications, education
4. Organize the output clearly

Start your response with: "CV Analysis for Upload ID {st.session_state.current_upload_id}:"

IMPORTANT: Only extract information from the CV text above. Do not add or infer anything.""",
                expected_output=f"Comprehensive CV analysis starting with 'CV Analysis for Upload ID {st.session_state.current_upload_id}:' followed by organized lists of skills, experience, and qualifications.",
                agent=extractor
            )
            
            crew = Crew(
                agents=[extractor], 
                tasks=[extraction_task],
                verbose=True,
                memory=False
            )
            
            st.write("🚀 Starting extraction...")
            result = crew.kickoff()
            st.session_state.cv_data = str(result)
            st.write("✓ Extraction complete!")
    
    st.subheader("📋 Extracted Profile:")
    st.info(st.session_state.cv_data)
    
    # Verification
    st.subheader("🔬 Verification")
    cv_text_lower = st.session_state.cv_text.lower()
    cv_data_lower = st.session_state.cv_data.lower()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**CV Text Contains:**")
        if "personal trainer" in cv_text_lower or "fitness" in cv_text_lower:
            st.error("🏋️ Personal Trainer content")
        if "python" in cv_text_lower or "machine learning" in cv_text_lower or "engineer" in cv_text_lower:
            st.success("💻 AI/Engineering content")
    
    with col2:
        st.write("**Agent Extracted:**")
        if "personal trainer" in cv_data_lower or "fitness" in cv_data_lower:
            st.error("🏋️ Personal Trainer content")
        if "python" in cv_data_lower or "machine learning" in cv_data_lower or "engineer" in cv_data_lower:
            st.success("💻 AI/Engineering content")
    
    # Check match
    is_trainer_in_text = "personal trainer" in cv_text_lower or "fitness" in cv_text_lower
    is_trainer_in_data = "personal trainer" in cv_data_lower or "fitness" in cv_data_lower
    is_ai_in_text = "python" in cv_text_lower or "machine learning" in cv_text_lower
    is_ai_in_data = "python" in cv_data_lower or "machine learning" in cv_data_lower
    
    if (is_trainer_in_text == is_trainer_in_data) and (is_ai_in_text == is_ai_in_data):
        st.success("✅ MATCH: Agent correctly extracted the CV content!")
    else:
        st.error("❌ MISMATCH: Agent extracted different content!")
        st.info("💡 This shouldn't happen with raw text approach. If it does, it's an LLM hallucination.")
    
    st.caption(f"✓ Upload ID: {st.session_state.current_upload_id}")
    
    user_feedback = st.text_area("Extra context? (e.g. 'Targeting London Finance')")
    if st.button("Approve & Start Market Research"):
        st.session_state.user_notes = user_feedback
        st.session_state.stage = "final_report"
        st.rerun()

# --- STAGE 3: MARKET RESEARCH ---
if st.session_state.stage == "final_report":
    st.header("🌍 Step 2: Market Comparison")
    
    if st.session_state.final_report is None:
        with st.status("Searching 2026 London market trends...", expanded=True):
            search_tool = TavilySearchTool()
            analyst = Agent(
                role='Senior London Career Strategist',
                goal='Provide gap analysis for 2026 London market',
                backstory="""Expert career consultant in London tech sector with 15+ years experience.""",
                tools=[search_tool],
                allow_delegation=False,
                verbose=True,
                memory=False
            )
            
            final_task = Task(
                description=(
                    f"Candidate Profile:\n{st.session_state.cv_data}\n\n"
                    f"User Context: {st.session_state.get('user_notes', 'None')}\n\n"
                    "Research 2026 London hiring trends for roles matching this profile. "
                    "Compare candidate's skills to market demands and provide gap analysis."
                ),
                expected_output="Career Gap Analysis Report in Markdown format with: 1) Current Skills Assessment, 2) Market Trends, 3) Skill Gaps and Recommendations.",
                agent=analyst
            )
            
            crew = Crew(agents=[analyst], tasks=[final_task], memory=False)
            st.session_state.final_report = str(crew.kickoff())
    
    st.markdown(st.session_state.final_report)
    
    pdf_data = create_pdf_bytes(st.session_state.final_report)
    st.download_button("📥 Download PDF", data=pdf_data, file_name="Career_Report.pdf", mime="application/pdf")
    
    if st.button("Start New Analysis"):
        # Clean files
        if os.path.exists("data"):
            for f in os.listdir("data"):
                if f.startswith("cv_"):
                    try:
                        os.remove(os.path.join("data", f))
                    except:
                        pass
        
        # Reset state
        for key in list(st.session_state.keys()):
            if key != "session_id":
                del st.session_state[key]
        
        st.session_state.stage = "upload"
        st.rerun()