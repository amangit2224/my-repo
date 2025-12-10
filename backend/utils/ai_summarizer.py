# backend/utils/ai_summarizer.py
import requests
import os
from dotenv import load_dotenv
import base64

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def extract_text_from_pdf_with_ai(filepath):
    """
    Extract text from PDF using Gemini 2.5 Flash API
    """
    try:
        # Read PDF and convert to base64
        with open(filepath, 'rb') as f:
            pdf_bytes = f.read()
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        # CORRECT MODEL: gemini-2.5-flash (supports PDFs!)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [
                    {
                        "text": "Extract every single word from this medical report PDF exactly as written. Include all tables, numbers, and headers. Do not summarize - just extract the raw text."
                    },
                    {
                        "inline_data": {
                            "mime_type": "application/pdf",
                            "data": pdf_base64
                        }
                    }
                ]
            }]
        }
        
        # Make the API call
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            extracted_text = result['candidates'][0]['content']['parts'][0]['text']
            return extracted_text.strip()
        else:
            error_detail = response.json() if response.text else response.text
            raise Exception(f"Gemini API Error {response.status_code}: {error_detail}")
            
    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")


def generate_medical_summary(text):
    """
    Generate patient-friendly summary with STRUCTURED test values for Health Trends
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        prompt = f"""Analyze this medical report and create a patient-friendly summary.

CRITICAL: Format ALL test results EXACTLY like this:
**Test Name**: value unit

Examples:
**Hemoglobin**: 14.5 g/dL
**Blood Glucose**: 95 mg/dL
**Cholesterol**: 180 mg/dL

Then add a friendly explanation in simple language for a 15-year-old.

Medical Report:
{text[:12000]}

Remember: Use **Test Name**: value unit format for ALL numeric results!"""
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Summary generation failed: API returned {response.status_code}"
            
    except Exception as e:
        return f"Summary generation failed: {str(e)}"


def generate_quick_summary(text):
    """
    Generate 3-bullet summary using Gemini 2.5 Flash
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        prompt = f"""Create exactly 3 bullet points summarizing the key findings of this medical report. 
Be concise and focus on the most important information.

Medical Report:
{text[:4000]}"""
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Quick summary generation failed"
            
    except Exception as e:
        return f"Quick summary failed: {str(e)}"