# backend/utils/ai_summarizer.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Try multiple model names in order of preference
MODEL_NAMES = [
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro-latest", 
    "gemini-pro",
    "models/gemini-1.5-flash",
    "models/gemini-pro"
]

def get_model():
    """Try different model names until one works"""
    for model_name in MODEL_NAMES:
        try:
            return genai.GenerativeModel(model_name)
        except Exception:
            continue
    # Fallback to the most basic one
    return genai.GenerativeModel("gemini-pro")

model = get_model()

def extract_text_from_pdf_with_ai(filepath):
    """
    Upload PDF to Gemini and extract all text content.
    """
    try:
        # Upload the file
        uploaded = genai.upload_file(filepath)
        
        # Generate content with the uploaded file
        response = model.generate_content([
            "Extract every single word from this medical report PDF exactly as written. Include tables, numbers, headers — no summarization, just raw text.",
            uploaded
        ])
        
        # Clean up the uploaded file
        try:
            genai.delete_file(uploaded.name)
        except:
            pass  # If delete fails, continue anyway
            
        return response.text.strip()
        
    except Exception as e:
        error_msg = str(e)
        # Provide more helpful error message
        if "404" in error_msg:
            raise Exception(f"Model not available. Try updating google-generativeai package. Error: {error_msg}")
        else:
            raise Exception(f"Gemini PDF extraction failed: {error_msg}")

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