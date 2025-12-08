import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini with new API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def extract_text_from_pdf_with_ai(filepath):
    """Let Gemini directly read the PDF when local OCR fails (updated for v0.8+ API)"""
    try:
        # Upload the file
        uploaded_file = genai.upload_file(path=filepath, display_name="medical_report.pdf")
        
        # Generate content with prompt + file
        response = genai.generate_content([
            "Extract ALL text from this medical report PDF accurately and completely. Include every word, number, table value, and header. Do not summarize yet — just give the raw extracted text.",
            uploaded_file
        ])
        
        # Clean up the uploaded file after use (optional, but good practice)
        genai.delete_file(uploaded_file.name)
        
        return response.text
    except Exception as e:
        raise Exception(f"Gemini failed to read PDF: {str(e)}")

def generate_medical_summary(extracted_text):
    """
    Use Gemini AI to generate a patient-friendly medical report summary
    """
    
    prompt = f"""
You are a medical report interpreter helping patients understand their lab results in simple language.

Given the following medical report text, create a clear, easy-to-understand summary for the patient.

MEDICAL REPORT TEXT:
{extracted_text}

INSTRUCTIONS:
1. Identify the patient's name, age, and gender
2. List the main tests performed
3. For each test result, explain in simple terms:
   - What the test measures
   - The actual value found
   - Whether it's normal or needs attention
4. Provide an overall assessment
5. End with a reminder to discuss with their doctor

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

**Patient Information:**
[Name, Age, Gender]

**Tests Performed:**
[List the main tests]

**Your Results (Simplified):**
- [Test Name]: [Value] [Unit]
  → What it means: [Simple explanation]
  → Status: [Normal/High/Low and what to do]

**Overall Assessment:**
[Brief summary of overall health status]

**Important Reminder:**
Always discuss these results with your doctor. They can provide personalized advice based on your complete medical history.

Keep the language simple, avoid medical jargon, and be reassuring while being accurate.
"""
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def generate_quick_summary(extracted_text):
    """
    Generate a very brief one-paragraph summary
    """
    
    prompt = f"""
Summarize this medical report in 2-3 sentences that a patient can understand:

{extracted_text[:1000]}

Be concise and focus on the most important findings.
"""
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Summary generation failed."