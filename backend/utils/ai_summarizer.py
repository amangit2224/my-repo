# backend/utils/ai_summarizer.py
import requests
import os
from dotenv import load_dotenv
import base64
import time

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def extract_text_from_pdf_with_ai(filepath):
    """
    Extract text from PDF using Gemini 2.5 Flash API
    INCREASED TIMEOUT + RETRY LOGIC for scanned PDFs
    """
    max_retries = 2
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"\n{'='*60}")
            print(f"GEMINI AI OCR - Attempt {attempt + 1}/{max_retries}")
            print(f"{'='*60}")
            
            # Read PDF and convert to base64
            print("Reading PDF file...")
            with open(filepath, 'rb') as f:
                pdf_bytes = f.read()
                pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            
            file_size_kb = len(pdf_bytes) / 1024
            print(f"File size: {file_size_kb:.2f} KB")
            
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"
            
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "contents": [{
                    "parts": [
                        {
                            "text": "Extract all text from this medical report PDF. Include test names, values, units, and reference ranges. Output plain text only, no formatting."
                        },
                        {
                            "inline_data": {
                                "mime_type": "application/pdf",
                                "data": pdf_base64
                            }
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 4096
                }
            }
            
            # INCREASED TIMEOUT: 45 seconds (was 15)
            print(f"Sending request to Gemini API (45s timeout)...")
            start_time = time.time()
            
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            
            elapsed = time.time() - start_time
            print(f"API response time: {elapsed:.2f}s")
            
            if response.status_code == 200:
                result = response.json()
                
                # Check if we got a valid response
                if 'candidates' in result and len(result['candidates']) > 0:
                    extracted_text = result['candidates'][0]['content']['parts'][0]['text']
                    
                    if extracted_text and len(extracted_text.strip()) > 50:
                        print(f"SUCCESS! Extracted {len(extracted_text)} characters")
                        print(f"{'='*60}\n")
                        return extracted_text.strip()
                    else:
                        print(f"Response too short: {len(extracted_text or '')} chars")
                else:
                    print(f"Invalid response structure: {result}")
                
            else:
                error_detail = response.json() if response.text else response.text
                print(f"API Error {response.status_code}: {error_detail}")
                
                # Don't retry on 400 errors (bad request)
                if response.status_code == 400:
                    raise Exception(f"Gemini API Bad Request: {error_detail}")
            
            # If we got here, retry
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            
        except requests.Timeout:
            print(f"Request timeout after 45s")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                raise Exception("Gemini API timeout - PDF OCR took too long after 2 attempts")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            if attempt < max_retries - 1 and "timeout" not in str(e).lower():
                print(f"Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"PDF extraction failed: {str(e)}")
    
    # If all retries failed
    raise Exception("Gemini API OCR failed after all retry attempts")


def generate_medical_summary(text):
    """
    Generate patient-friendly summary using Gemini 2.5 Flash
    OPTIONAL - Only used if rule-based system fails
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"
        
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
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
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
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"
        
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
            }],
            "generationConfig": {
                "temperature": 0.5,
                "maxOutputTokens": 512
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
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
        print("\nAI Enhancement - Polishing summary...")
        
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"
        
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
            }],
            "generationConfig": {
                "temperature": 0.5,
                "maxOutputTokens": 4096
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
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