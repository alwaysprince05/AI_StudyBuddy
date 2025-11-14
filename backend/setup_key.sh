#!/bin/bash

echo "🔑 Gemini API Key Setup"
echo "======================"
echo ""
echo "1. Get your free API key from: https://makersuite.google.com/app/apikey"
echo ""
read -p "2. Enter your Gemini API key: " api_key

if [ -z "$api_key" ]; then
    echo "❌ No API key provided. Exiting."
    exit 1
fi

# Create .env file
cat > .env << EOF
GEMINI_API_KEY=$api_key
PORT=5001
FLASK_ENV=development
EOF

echo ""
echo "✅ API key saved to .env file!"
echo ""
echo "Now restart your backend server:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"

