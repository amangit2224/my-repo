# backend/utils/ai_summarizer.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# This is the ONLY model that works perfectly with file upload right now
model = genai.GenerativeModel("gemini-1.5-pro")

def extract_text_from_pdf_with_ai(filepath):
    try:
        file = genai.upload_file(filepath)
        response = model.generate_content([
            "Extract all text from this medical report PDF exactly as it appears. No summarization, no skipping anything.",
            file
        ])
        genai.delete_file(file.name)
        return response.text
    except Exception as e:
        raise Exception(f"Gemini failed: {e}")

def generate_medical_summary(text):
    response = model.generate_content(f"Explain this medical report in simple language:\n\n{text}")
    return response.text

def generate_quick_summary(text):
    response = model.generate_content(f"3 bullet point summary:\n\n{text}")
    return response.text