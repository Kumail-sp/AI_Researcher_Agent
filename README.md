🤖 AI Researcher Agent: Agentic RAG Pipeline
A professional Agentic Retrieval-Augmented Generation (RAG) system built with CrewAI and LangChain. This agent doesn't just "chat"—it autonomously decides when to search a local knowledge base (PDF) and when to perform live web research to provide comprehensive career gap analyses.

🌟 Key Features
Autonomous Reasoning: Uses the ReAct (Reason + Act) pattern to decide between multiple tools.

Agentic RAG: Dynamically retrieves context from a local PDF vector store (ChromaDB).

Live Web Integration: Integrated with the Tavily Search API for real-time market data.

Automated Reporting: Generates professional PDF reports summarizing findings using Python's fpdf2.

🛠 Tech Stack
Framework: CrewAI (Multi-agent orchestration)

LLM: OpenAI GPT-4o-mini

Vector Database: ChromaDB

Search Engine: Tavily AI

Language: Python 3.12+ (managed with uv)

🚀 Quick Start
1. Prerequisites

Ensure you have a modern Python environment. It is recommended to use uv for 10x faster dependency management.

2. Installation

Bash
# Clone the repository
git clone:  https://github.com/Kumail-sp/AI_Researcher_Agent.git
cd AI_Researcher_Agent

# Create and activate virtual environment
uv venv
source venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
3. Environment Setup

Create a .env file in the root directory and add your API keys:

Plaintext
OPENAI_API_KEY=sk-xxxx
TAVILY_API_KEY=tvly-xxxx
4. Usage

Place your target PDF in the data/ folder and name it knowledge.pdf. Then run the researcher:

Bash
python agent_researcher.py
📂 Project Structure

Plaintext:

├── data/               # Local PDF storage (ignored by git)
├── chroma_db/          # Persistent vector database
├── agent_researcher.py # Main agentic logic
├── make_pdf.py         # PDF report generation script
├── .env                # Private API keys
└── requirements.txt    # Project dependencies
🛡 Security & Best Practices
Privacy: The data/ and chroma_db/ folders are excluded via .gitignore to protect personal data.

Environment Management: Uses .env to prevent API key leakage.

What i did in this Project: 

Data Ingestion: I handled unstructured data (PDFs) and turned them into searchable "Vectors".

Orchestration: I used CrewAI to manage an agent that can "think" before it acts.

Tool Integration: Agent uses both a Vector Database (ChromaDB) and a Real-time Web Search (Tavily).

Production Standards: I used .env for security, .gitignore for privacy, and uv for modern dependency management.