import os 
from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

load_dotenv()

# llm = ChatGoogleGenerativeAI(model = "gemini-1.5-pro-latest",  temperature= 0 , google_api_key = os.getenv("GENAI_API_KEY"))

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model_name="llama3-70b-8192",     
    temperature=0,
    # max_tokens=1024,
)