# test_gemini.py - Put this in backend folder
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("="*50)
print("GEMINI API TEST")
print("="*50)
print(f"API Key exists: {bool(GEMINI_API_KEY)}")
print(f"API Key length: {len(GEMINI_API_KEY) if GEMINI_API_KEY else 0}")
print(f"API Key starts with: {GEMINI_API_KEY[:15] if GEMINI_API_KEY else 'MISSING'}...")
print("="*50)

# Test 1: Check which models are available
print("\n[TEST 1] Checking available models...")
list_url = f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}"
response = requests.get(list_url)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    models = response.json()
    print("\nAvailable models:")
    for model in models.get('models', [])[:5]:  # Show first 5
        print(f"  - {model.get('name')}")
else:
    print(f"Error: {response.text}")
    
print("\n" + "="*50)

# Test 2: Try gemini-pro
print("\n[TEST 2] Testing gemini-pro with simple text...")
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
payload = {
    "contents": [{
        "parts": [{"text": "Say hello in one word"}]
    }]
}

response = requests.post(url, json=payload)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"Response: {result['candidates'][0]['content']['parts'][0]['text']}")
    print("✅ gemini-pro WORKS!")
else:
    print(f"❌ Error: {response.text}")

print("\n" + "="*50)

# Test 3: Try gemini-pro-vision
print("\n[TEST 3] Testing gemini-pro-vision...")
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent?key={GEMINI_API_KEY}"
payload = {
    "contents": [{
        "parts": [{"text": "Hello"}]
    }]
}

response = requests.post(url, json=payload)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✅ gemini-pro-vision WORKS!")
else:
    print(f"❌ Error: {response.text[:200]}")

print("\n" + "="*50)
print("TEST COMPLETE")
print("="*50)