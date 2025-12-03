# backend/utils/ai_explainer.py
from groq import Groq
import os
import json
from dotenv import load_dotenv

# Load .env from backend root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_medical_term(term):
    if not client.api_key:
        raise Exception("Groq API key missing. Check .env file.")

    prompt = f"""
    Explain the medical term "{term}" in simple English for a patient.
    Return ONLY a valid JSON object with these exact keys:
    {{
      "definition": "1-2 sentence definition",
      "pronunciation": "phonetic spelling",
      "example": "1 real-life example"
    }}
    No extra text. No markdown. Just JSON.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3,
            response_format={ "type": "json_object" }
        )
        text = response.choices[0].message.content.strip()
        
        # Parse JSON safely
        data = json.loads(text)
        
        return {
            "term": term.capitalize(),
            "definition": data.get("definition", "No definition available."),
            "pronunciation": data.get("pronunciation", "Not available"),
            "example": data.get("example", "No example available.")
        }
    except Exception as e:
        raise Exception(f"AI failed: {str(e)}")