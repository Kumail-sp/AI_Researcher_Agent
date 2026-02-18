# 🤖 AI Career Agent: Agentic RAG Career Advisor

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Latest-orange.svg)](https://www.crewai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)](https://streamlit.io/)

> **A multi-agent AI system that bridges the gap between candidate skills and market demands through intelligent CV analysis and real-time market research.**

Transform your career planning with AI-powered insights that compare your skills against live 2026 market trends and generate personalized career gap analysis reports.

---

## 🎯 Problem Statement

Career transitions are challenging because:
- ❌ Job descriptions are vague and generic
- ❌ Skills requirements change rapidly
- ❌ No data-driven way to identify skill gaps
- ❌ Difficult to prioritize which skills to learn next

**Solution:** An autonomous AI agent that reads your CV, researches current market trends, and provides actionable recommendations based on real data.

---

## ✨ Features

### 🚀 Core Capabilities
- **Intelligent CV Parsing**: Extracts skills, experience, and qualifications from any PDF resume
- **Live Market Research**: Searches 2026 job trends using Tavily AI Search
- **Comparative Analysis**: Identifies exact skill gaps between your profile and market demands
- **Professional Reporting**: Generates downloadable PDF career gap analysis reports
- **Human-in-the-Loop**: Review and refine extracted data before final analysis

### 💎 Technical Highlights
- **Multi-Agent Architecture**: Specialized agents for extraction and analysis
- **RAG Implementation**: Retrieval-Augmented Generation without vector database caching issues
- **Session Management**: Isolated user sessions for concurrent multi-user support
- **Real-Time Processing**: Direct text extraction for instant analysis
- **Error-Resilient**: Comprehensive error handling and validation

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│                   (Streamlit App)                        │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴────────────┐
         │                        │
         ▼                        ▼
┌────────────────┐       ┌────────────────┐
│  Agent 1:      │       │  Agent 2:      │
│  CV Extractor  │       │  Market        │
│                │       │  Analyst       │
│  - Reads PDF   │       │  - Web Search  │
│  - Extracts    │       │  - Compares    │
│    Skills      │       │  - Generates   │
│                │       │    Report      │
└────────┬───────┘       └────────┬───────┘
         │                        │
         ▼                        ▼
    ┌────────────────────────────────┐
    │       Knowledge Sources        │
    ├────────────────────────────────┤
    │  • PDF Text Extraction         │
    │  • Tavily AI Search API        │
    │  • OpenAI GPT-4 Reasoning      │
    └────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Purpose | Why This Choice |
|------------|---------|-----------------|
| **CrewAI** | Multi-agent orchestration | Industry-leading agentic framework with built-in coordination |
| **OpenAI GPT-4** | Language model | Best-in-class reasoning and analysis capabilities |
| **Streamlit** | Web interface | Rapid prototyping with Python-native UI |
| **Tavily AI** | Web search | Optimized for LLM consumption with fact-based results |
| **pdfplumber** | PDF extraction | Reliable text extraction without OCR overhead |
| **FPDF2** | Report generation | Lightweight PDF creation with full control |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- OpenAI API key
- Tavily API key

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-career-agent.git
cd ai-career-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys:
# OPENAI_API_KEY=your_openai_key_here
# TAVILY_API_KEY=your_tavily_key_here
```

### Run the Application

```bash
streamlit run main.py
```

Navigate to `http://localhost:8501` in your browser.

---

## 📖 Usage

### Step 1: Upload Your CV
```
Click "Browse files" → Select your PDF resume → Click "Begin Profile Extraction"
```

### Step 2: Review Extracted Data
```
✓ Verify skills and experience are correctly identified
✓ Add extra context (e.g., "Targeting London Finance roles")
✓ Click "Approve & Start Market Research"
```

### Step 3: Get Your Report
```
✓ AI searches 2026 market trends
✓ Compares your skills to market demands
✓ Generates comprehensive gap analysis
✓ Download professional PDF report
```

---

## 🎬 Demo

### Screenshots

**1. CV Upload Interface**
```
[Upload CV] 
📄 Kumail_AI_Engineer.pdf
📊 Size: 59,520 bytes | Text: 4,823 chars
```

**2. Extracted Profile**
```
📋 Extracted Profile:
- Python, TensorFlow, PyTorch
- Machine Learning, Computer Vision
- NLP, RAG Systems
- 3 years experience in AI Engineering
```

**3. Career Gap Analysis**
```
🌍 2026 London Market Trends:
• GenAI/LLM expertise is critical
• MLOps & deployment skills highly valued
• Real-time AI systems demand growing

📊 Skill Gaps:
1. Advanced LLM fine-tuning
2. Kubernetes & cloud deployment
3. Real-time inference optimization

✅ Recommendations:
→ Complete LLM bootcamp
→ Build 2-3 production ML projects
→ Obtain AWS/Azure ML certification
```

---

## 🔧 Configuration

### Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...

# Optional
OPENAI_MODEL=gpt-4o-mini  # Default model
TAVILY_MAX_RESULTS=5       # Search result count
```

### Agent Configuration

Customize agents in `main.py`:

```python
# CV Extractor Agent
extractor = Agent(
    role='CV Skills Extractor',
    goal='Extract all skills from CV',
    backstory='Expert CV analyst...',
    verbose=True,
    memory=False  # Disable to prevent cross-contamination
)

# Market Analyst Agent
analyst = Agent(
    role='Senior London Career Strategist',
    goal='Provide gap analysis for 2026 market',
    backstory='15+ years in tech recruitment...',
    tools=[TavilySearchTool()],
    memory=False
)
```

---

## 🐛 Debugging Journey: The Caching Bug

### The Problem
During development, I encountered a critical bug: **the agent analyzed the FIRST CV uploaded, even after uploading new CVs.**

### Investigation
```
✓ Unique filenames per upload → Still broken
✓ Clear vector database → Still broken  
✓ Unique database paths → Still broken
```

### Root Cause
**PDFSearchTool + ChromaDB** were caching embeddings internally, causing cross-contamination between uploads.

### Solution
**Bypass the vector database entirely:**
1. Extract PDF text directly using `pdfplumber`
2. Pass raw text to agent in task description
3. No caching = No contamination

```python
# ❌ Old approach (broken)
pdf_tool = PDFSearchTool(pdf=file_path)
agent = Agent(tools=[pdf_tool])

# ✅ New approach (working)
cv_text = extract_pdf_text(file_path)
task = Task(
    description=f"Analyze this CV:\n{cv_text}",
    agent=agent  # No tools needed!
)
```

### Lessons Learned
1. **Simpler is often better**: Direct text extraction > Vector database for this use case
2. **Debug systematically**: Isolate each component to find the exact failure point
3. **Read the source**: Understanding library internals saved days of debugging
4. **Test with real data**: The bug only appeared with multiple sequential uploads

---

## 📁 Project Structure

```
ai-career-agent/
├── main.py                  # Main Streamlit application
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
│
├── data/                   # User-uploaded CVs (gitignored)
│   └── cv_*.pdf
│
├── legacy/                 # Development history (for reference)
│   ├── agent_rag.py       # Early RAG implementation
│   ├── agent_researcher.py # CLI version
│   └── rag_test.py        # Vector DB experiments
│
└── README.md              # This file
```

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] Upload CV → Verify correct text extraction
- [ ] Review Stage → Check skills match uploaded CV
- [ ] Market Research → Confirm live data retrieval
- [ ] PDF Download → Verify report generation
- [ ] New Upload → Ensure old CV data is cleared
- [ ] Concurrent Users → Test session isolation

### Run Tests

```bash
# Test PDF extraction
python -c "from main import extract_pdf_text; print(extract_pdf_text('test.pdf')[:500])"

# Test agent without UI
python agent_researcher.py
```

---

## 🚦 Performance

| Metric | Value |
|--------|-------|
| CV Upload | <1 second |
| Text Extraction | 2-3 seconds |
| Agent Analysis | 15-30 seconds |
| Market Research | 20-40 seconds |
| Total Time | ~1 minute |

---

## 🔐 Security & Privacy

- ✅ **No training data**: CVs are processed locally and never used to train models
- ✅ **Session isolation**: Each user's data is completely separate
- ✅ **Temporary storage**: Uploaded files are automatically cleaned up
- ✅ **API key management**: Credentials stored in `.env` (gitignored)

---

## 🛣️ Roadmap

### Phase 1: Core Features ✅
- [x] PDF CV parsing
- [x] Market research integration
- [x] Gap analysis generation
- [x] PDF report export

### Phase 2: Enhancements 🚧
- [ ] Support for multiple file formats (DOCX, TXT)
- [ ] Interactive skill comparison charts
- [ ] Email delivery of reports
- [ ] Historical trend analysis

### Phase 3: Advanced Features 🔮
- [ ] Multi-language support
- [ ] Industry-specific analysis
- [ ] Salary benchmarking
- [ ] Learning resource recommendations
- [ ] Interview preparation tips

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [CrewAI](https://www.crewai.com/) for the excellent multi-agent framework
- [OpenAI](https://openai.com/) for GPT-4 API
- [Tavily AI](https://tavily.com/) for search capabilities
- [Streamlit](https://streamlit.io/) for rapid prototyping tools

---

## 📧 Contact

**Kumail Haider** - AI Engineer

- LinkedIn: [Your LinkedIn URL]
- Portfolio: [Your Portfolio URL]
- Email: [Your Email]

**Project Link**: [https://github.com/yourusername/ai-career-agent](https://github.com/yourusername/ai-career-agent)

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-career-agent?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/ai-career-agent?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/ai-career-agent?style=social)

---

<div align="center">
Made with ❤️ by Kumail Haider

⭐ Star this repo if you find it helpful!
</div>
