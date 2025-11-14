# 🚨 FIX THE API KEY ERROR - STEP BY STEP

## You're seeing this error because the API key hasn't been added yet.

### ⚡ QUICK FIX (Copy & Paste These Commands):

**Step 1: Get your API key**
- Open: https://makersuite.google.com/app/apikey
- Sign in with Google
- Click "Create API Key"
- **COPY the key** (starts with `AIzaSy...`)

**Step 2: Add it to your project**

Open a terminal and run:
```bash
cd /Users/princemaurya/AI_StudyBuddy/backend
source venv/bin/activate
python add_api_key.py
```
When prompted, **paste your API key** and press Enter.

**Step 3: Test if it works**
```bash
python test_api_key.py
```
You should see: ✅ API key is VALID and working!

**Step 4: Restart the server**
```bash
# If server is running, stop it first (Ctrl+C)
python app.py
```

**Step 5: Test in browser**
- Go to http://localhost:3000
- Enter a topic like "Machine Learning"
- Click "Study"
- It should work! 🎉

---

## Alternative: Manual Edit

If you prefer to edit manually:

```bash
cd /Users/princemaurya/AI_StudyBuddy/backend
nano .env
```

Change this line:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

To (replace with YOUR actual key):
```
GEMINI_API_KEY=AIzaSyYourActualKeyHere
```

Save: `Ctrl+X`, then `Y`, then `Enter`

Then restart: `python app.py`

---

## ❓ Need Help?

The error happens because:
1. The `.env` file has a placeholder value
2. You need to replace it with your real API key from Google
3. The server needs to be restarted after adding the key

Once you add a valid key, the error will disappear!

