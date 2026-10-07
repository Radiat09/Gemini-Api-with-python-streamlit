import os
from google import genai
from dotenv import load_dotenv
import streamlit  as st

load_dotenv()

print("API Key loaded:", os.environ.get("GEMINI_API_KEY"))

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Give me an idea of Gemini API in 100 words"
)

print("--- Response Start ---")
#print(response.text)
st.markdown(response.text)
print("--- Response End ---")