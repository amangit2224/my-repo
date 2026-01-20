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
    REDUCED TIMEOUT FOR FASTER RESPONSE
    """
    try:
        # Read PDF and convert to base64
        with open(filepath, 'rb') as f:
            pdf_bytes = f.read()
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [
                    {
                        "text": "Extract all text from this medical report PDF. Include test names, values, units, and reference ranges. Output plain text only."
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
        
        # REDUCED TIMEOUT: 15 seconds instead of 60
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            extracted_text = result['candidates'][0]['content']['parts'][0]['text']
            return extracted_text.strip()
        else:
            error_detail = response.json() if response.text else response.text
            raise Exception(f"Gemini API Error {response.status_code}: {error_detail}")
            
    except requests.Timeout:
        raise Exception("Gemini API timeout - PDF too large or slow response")
    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")


def generate_medical_summary(text):
    """
    Generate patient-friendly summary using Gemini 2.5 Flash
    OPTIONAL - Only used if rule-based system fails
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        prompt = f"""Explain this medical report in simple, clear language that a patient can understand. 
Be concise, encouraging, and avoid medical jargon. Focus on what the results mean in practical terms.

Medical Report:
{text[:10000]}"""
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        # REDUCED TIMEOUT
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Summary generation failed: API returned {response.status_code}"
            
    except requests.Timeout:
        return "Summary generation timed out"
    except Exception as e:
        return f"Summary generation failed: {str(e)}"


def generate_quick_summary(text):
    """
    Generate 3-bullet summary using Gemini 2.5 Flash
    OPTIONAL - Only used if rule-based system fails
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
        
        # REDUCED TIMEOUT
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Quick summary generation failed"
            
    except requests.Timeout:
        return "Quick summary timed out"
    except Exception as e:
        return f"Quick summary failed: {str(e)}"


def enhance_summary_with_ai(rule_based_summary):
    """
    Polish rule-based summary with AI for better readability
    NOT for core analysis - just for language enhancement
    
    This is the OPTIONAL layer - only used when toggle is ON
    """
    try:
        print("Enhancing summary with AI...")
        
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        prompt = f"""You are enhancing a medical report summary. The summary was generated by a rule-based system and contains accurate medical information.

Your job is ONLY to:
1. Make the language more conversational and friendly
2. Add smooth transitions between sections
3. Rephrase technical terms in simpler ways (but keep medical accuracy)
4. Keep ALL medical facts, numbers, and recommendations EXACTLY as they are
5. Remove any emojis or symbols, use clean text only

DO NOT:
- Change any medical values or interpretations
- Add new medical advice
- Remove any information
- Change the structure significantly
- Add information not in the original

Original rule-based summary:
{rule_based_summary[:15000]}

Enhanced version (keep it similar length, just more conversational, no emojis):"""
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            enhanced = result['candidates'][0]['content']['parts'][0]['text']
            print(f"AI enhancement complete! ({len(enhanced)} chars)")
            return enhanced
        else:
            print(f"AI enhancement failed: {response.status_code}")
            return rule_based_summary  # Fallback to original
            
    except Exception as e:
        print(f"AI enhancement error: {e}")
        return rule_based_summary  # Fallback to original