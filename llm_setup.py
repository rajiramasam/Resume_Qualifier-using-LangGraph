# your_llm_setup.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

# Load API key from .env file
load_dotenv()

# Set Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Instantiate LangChain-compatible Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
