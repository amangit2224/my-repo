# backend/utils/ai_summarizer.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# FIXED: Use the correct model name that's currently available
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")  # Removed the -001 suffix

def extract_text_from_pdf_with_ai(filepath):
    """
    Upload PDF to Gemini and extract all text content.
    """
    try:
        uploaded = genai.upload_file(filepath)
        response = model.generate_content([
            "Extract every single word from this medical report PDF exactly as written. Include tables, numbers, headers — no summarization, just raw text.",
            uploaded
        ])
        genai.delete_file(uploaded.name)
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Gemini PDF extraction failed: {str(e)}")

def generate_medical_summary(text):
    """
    Generate a patient-friendly explanation of the medical report.
    """
    try:
        prompt = f"""Explain this medical report in simple, clear language that a 15-year-old patient can understand. 
Be kind, encouraging, and avoid medical jargon. Focus on what the results mean in practical terms.

Medical Report:
{text[:12000]}"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Summary generation failed: {str(e)}"

def generate_quick_summary(text):
    """
    Generate a 3-bullet point summary of the medical report.
    """
    try:
        prompt = f"""Create exactly 3 bullet points summarizing the key findings of this medical report. 
Be concise and focus on the most important information.

Medical Report:
{text[:4000]}"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Quick summary generation failed: {str(e)}"