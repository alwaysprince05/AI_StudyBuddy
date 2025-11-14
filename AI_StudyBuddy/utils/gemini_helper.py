import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ Gemini API key not found in .env file!")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

MODEL = "models/gemini-2.5-flash"

def generate_response(prompt: str) -> str:
    """Generate response from Gemini model."""
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "⚠️ No response generated."
    except Exception as e:
        return f"❌ Error generating response: {e}"
