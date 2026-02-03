import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load the secret key
load_dotenv()

# Initialize the model
llm = ChatOpenAI(model="gpt-4o-mini")

# Run a simple test
try:
    response = llm.invoke("Hi! I am Kumail. Give me one sentence of advice for a new AI Engineer in the UK.")
    print("\n--- AI Response ---")
    print(response.content)
except Exception as e:
    print(f"❌ Error: {e}")