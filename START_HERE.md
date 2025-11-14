# 🚨 START HERE - Fix the API Key Error

## The Error You're Seeing:
```
Invalid or missing Gemini API key
```

## Why This Happens:
Your `.env` file has a placeholder: `your_gemini_api_key_here`
This is NOT a real key - you need to replace it with your actual API key from Google.

---

## ✅ SOLUTION - Copy & Paste These Commands:

### Step 1: Get Your API Key (1 minute)
1. Open: **https://makersuite.google.com/app/apikey**
2. Sign in with Google
3. Click **"Create API Key"**
4. **Copy the key** (looks like: `AIzaSy...`)

### Step 2: Add It (Choose ONE method)

**EASIEST - Use the script:**
```bash
cd /Users/princemaurya/AI_StudyBuddy
./SET_API_KEY.sh
# Paste your key when asked
```

**OR - Edit manually:**
```bash
cd /Users/princemaurya/AI_StudyBuddy/backend
nano .env
# Change: GEMINI_API_KEY=your_gemini_api_key_here
# To:     GEMINI_API_KEY=AIzaSyYourActualKeyHere
# Save: Ctrl+X, Y, Enter
```

### Step 3: Start the Server
```bash
cd /Users/princemaurya/AI_StudyBuddy/backend
source venv/bin/activate
python app.py
```

### Step 4: Test It
- Open: http://localhost:3000
- Enter a topic
- Click "Study"
- It should work! ✅

---

## ⚠️ Important Notes:

- **You MUST get the API key yourself** - I cannot do this for you
- It's **100% FREE** from Google
- Takes about **1 minute** to get
- Once you add it, the error disappears forever

---

## 🆘 Still Having Issues?

If you've added the key but still see errors:
1. Make sure the key starts with `AIzaSy`
2. Make sure there are no extra spaces
3. Make sure you restarted the server after adding the key
4. Run: `cd backend && python test_api_key.py` to test

