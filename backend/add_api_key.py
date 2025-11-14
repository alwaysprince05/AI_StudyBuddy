#!/usr/bin/env python3
"""
Simple script to add your Gemini API key to .env file
"""
import os

print("🔑 Gemini API Key Setup")
print("=" * 50)
print("\n1. Get your free API key from: https://makersuite.google.com/app/apikey")
print("2. Copy your API key (it should start with 'AIzaSy...')")
print()

api_key = input("Enter your Gemini API key: ").strip()

if not api_key:
    print("❌ No API key provided. Exiting.")
    exit(1)

if not api_key.startswith("AIza"):
    print("⚠️  Warning: API keys usually start with 'AIza'. Are you sure this is correct?")
    confirm = input("Continue anyway? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        exit(1)

# Create .env file
env_content = f"""GEMINI_API_KEY={api_key}
PORT=5001
FLASK_ENV=development
"""

with open('.env', 'w') as f:
    f.write(env_content)

print("\n✅ API key saved to .env file!")
print("\n📝 Next steps:")
print("   1. Restart the backend server:")
print("      cd backend")
print("      source venv/bin/activate")
print("      python app.py")
print("\n   2. Or if the server is already running, stop it (Ctrl+C) and restart it.")
print("\n✨ Your app should now work!")

