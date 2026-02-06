# 🤖 Agentic Career Researcher: End-to-End RAG Pipeline

A sophisticated **Multi-Agent Research System** built with **CrewAI** and **Streamlit**. This application autonomously bridges the gap between a candidate's local data (CV/PDF) and live market trends by utilizing an **Agentic RAG** workflow.

[Image of AI Agent Workflow: PDF Data -> Vector Store -> Agent Reasoning -> Web Search -> Final PDF Report]

## 🚀 The Value Proposition
Unlike static "Chat-with-PDF" apps, this system uses a **specialized Agent** that acts as a London-based Tech Headhunter. It performs a multi-step reasoning process:
1. **Context Extraction:** Deep-scans the uploaded PDF using an underlying vector database.
2. **Real-time Research:** Queries the **Tavily Search API** for 2026 London AI market data.
3. **Comparative Analysis:** Quantifies the "Skill Gap" between the user's profile and current hiring standards.
4. **Structured Reporting:** Synthesizes findings into a professional recommendation.

## 🛠 Tech Stack & Architecture
* **Orchestration:** [CrewAI](https://www.crewai.com/) (Managing autonomous agentic workflows).
* **Intelligence:** OpenAI **GPT-4o-mini** (Optimized for reasoning and cost-efficiency).
* **Vector Store:** **ChromaDB** (Efficient local indexing of PDF content).
* **Frontend:** **Streamlit** (Clean, Python-native web interface).
* **Package Management:** `uv` (Next-gen, ultra-fast Python dependency management).

## 📂 Project Structure
```text
├── main.py             # Streamlit Entrypoint & Agent Orchestration
├── agent_researcher.py # CLI version of the Agentic logic
├── make_pdf.py         # Post-processing script for PDF generation
├── data/               # Persistent storage for uploaded CVs
├── .env                # API Keys (OpenAI & Tavily)
└── requirements.txt    # Project dependencies

⚙️ Installation & Setup
1. Environment Setup

Clone the repository and install dependencies using uv for 10x faster setup:

git clone [https://github.com/yourusername/AI_Researcher_Agent.git]
<!-- cd AI_Researcher_Agent
uv venv
source venv/bin/activate
uv pip install -r requirements.txt -->

2. Configuration

Create a .env file in the root directory:
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here

3. Execution

Launch the web interface:
streamlit run main.py

🛡 Security & Privacy
Local Processing: PDF data is indexed locally in a vector store and never used for training external models.

Environment Safety: All API keys are managed via .env and excluded from version control via .gitignore.

Developed by Kumail  AI Engineer & Career Strategist