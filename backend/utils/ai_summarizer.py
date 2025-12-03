import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

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
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Summary generation failed."