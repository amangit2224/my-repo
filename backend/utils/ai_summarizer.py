# backend/utils/ai_summarizer.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Use the model that actually exists and supports file upload
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-001")  # This works 100%

def extract_text_from_pdf_with_ai(filepath):
    try:
        uploaded = genai.upload_file(filepath)
        response = model.generate_content([
            "Extract every single word from this medical report PDF exactly as written. Include tables, numbers, headers — no summarization, just raw text.",
            uploaded
        ])
        genai.delete_file(uploaded.name)
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Gemini error: {str(e)}")

def generate_medical_summary(text):
    try:
        response = model.generate_content(f"Explain this medical report like I'm a 15-year-old patient. Be kind and clear:\n\n{text[:12000]}")
        return response.text
    except Exception as e:
        return f"Summary failed: {e}"

def generate_quick_summary(text):
    try:
        response = model.generate_content(f"3 bullet points summary of this report:\n\n{text[:4000]}")
        return response.text
    except Exception as e:
        return "Quick summary failed"