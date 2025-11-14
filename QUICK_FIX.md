# 🔧 Quick Fix: API Key Error

## The Problem
You're seeing: "Invalid or missing Gemini API key"

## The Solution (3 Simple Steps)

### Step 1: Get Your Free API Key
1. Visit: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. **Copy the key** (it starts with `AIzaSy...`)

### Step 2: Add the Key to Your Project

**Option A - Use the helper script (Easiest):**
```bash
cd backend
source venv/bin/activate
python add_api_key.py
# Paste your API key when prompted
```

**Option B - Edit manually:**
```bash
cd backend
nano .env
# Change: GEMINI_API_KEY=your_gemini_api_key_here
# To:     GEMINI_API_KEY=AIzaSyYourActualKeyHere
# Save: Ctrl+X, then Y, then Enter
```

### Step 3: Restart the Backend Server

**If server is running:**
1. Find the terminal running `python app.py`
2. Press `Ctrl+C` to stop it
3. Start it again:
   ```bash
   cd backend
   source venv/bin/activate
   python app.py
   ```

**If server is not running:**
```bash
cd backend
source venv/bin/activate
python app.py
```

## ✅ Test It
1. Go to http://localhost:3000
2. Enter a topic like "Machine Learning"
3. Click "Study"
4. You should see summary, quiz, and study tip!

## 🆘 Still Having Issues?
- Make sure the API key starts with `AIzaSy`
- Make sure there are no extra spaces in the .env file
- Make sure you restarted the server after adding the key
- Check that the backend is running on port 5001

