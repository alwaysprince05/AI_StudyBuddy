#!/usr/bin/env python3
"""
Test if your Gemini API key is working
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key or api_key == 'your_gemini_api_key_here':
    print("❌ API key not set or still using placeholder!")
    print("\nTo add your API key:")
    print("1. Get it from: https://makersuite.google.com/app/apikey")
    print("2. Run: python add_api_key.py")
    print("   OR edit .env file manually")
    exit(1)

print(f"✅ API key found: {api_key[:10]}...")
print("\nTesting API key...")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Say 'Hello' in one word.")
    
    if response and response.text:
        print("✅ API key is VALID and working!")
        print(f"   Test response: {response.text.strip()}")
    else:
        print("⚠️  API key accepted but got empty response")
except Exception as e:
    error_msg = str(e)
    if "API key" in error_msg or "API_KEY" in error_msg:
        print("❌ API key is INVALID!")
        print(f"   Error: {error_msg}")
        print("\nPlease check:")
        print("1. The key is correct (starts with AIzaSy...)")
        print("2. The key has no extra spaces")
        print("3. You got the key from: https://makersuite.google.com/app/apikey")
    else:
        print(f"❌ Error: {error_msg}")

