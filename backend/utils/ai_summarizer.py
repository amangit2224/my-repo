# backend/utils/ai_summarizer.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_text_from_pdf_with_ai(filepath):
    try:
        uploaded_file = genai.upload_file(filepath)
        response = model.generate_content([
            "Extract every single word from this medical report PDF exactly as it appears. Include tables, headers, numbers — do not summarize, just return raw text.",
            uploaded_file
        ])
        genai.delete_file(uploaded_file.name)
        return response.text
    except Exception as e:
        raise Exception(f"Gemini PDF read failed: {e}")

def generate_medical_summary(extracted_text):
    try:
        response = model.generate_content(f"Summarize this medical report in simple patient-friendly language:\n\n{extracted_text}")
        return response.text
    except Exception as e:
        return f"Summary failed: {e}"

def generate_quick_summary(extracted_text):
    try:
        response = model.generate_content(f"Give a 3-bullet summary of this report:\n\n{extracted_text[:2000]}")
        return response.text
    except Exception as e:
        return "Quick summary failed."