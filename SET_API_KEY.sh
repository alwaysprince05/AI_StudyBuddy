#!/bin/bash
echo ""
echo "🔑 GEMINI API KEY SETUP"
echo "======================"
echo ""
echo "Step 1: Get your API key from: https://makersuite.google.com/app/apikey"
echo ""
read -p "Step 2: Paste your API key here: " API_KEY

if [ -z "$API_KEY" ]; then
    echo "❌ No key provided. Exiting."
    exit 1
fi

# Update .env file
cd backend
cat > .env << EOF
GEMINI_API_KEY=$API_KEY
PORT=5001
FLASK_ENV=development
EOF

echo ""
echo "✅ API key saved!"
echo ""
echo "🔄 Restarting backend server..."
pkill -f "python app.py" 2>/dev/null
sleep 1

cd backend
source venv/bin/activate
python app.py &
sleep 3

echo ""
echo "✅ Server restarted!"
echo ""
echo "🧪 Testing API key..."
python test_api_key.py
echo ""
echo "✨ Done! Try your app at http://localhost:3000"
