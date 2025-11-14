# Setting Up Your Gemini API Key

## Quick Steps:

1. **Get your free Gemini API key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated key

2. **Update the .env file:**

   **Option A - Using Terminal:**
   ```bash
   cd backend
   nano .env
   # Replace 'your_gemini_api_key_here' with your actual key
   # Save and exit (Ctrl+X, then Y, then Enter)
   ```

   **Option B - Using Terminal (one command):**
   ```bash
   cd backend
   # Replace YOUR_ACTUAL_KEY with your real API key
   cat > .env << EOF
   GEMINI_API_KEY=YOUR_ACTUAL_KEY
   PORT=5001
   FLASK_ENV=development
   EOF
   ```

3. **Restart the backend server:**
   - Stop the current server (Ctrl+C in the terminal running it)
   - Start it again:
   ```bash
   cd backend
   source venv/bin/activate
   python app.py
   ```

## Your API key should look like:
`AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

## Security Note:
- Never commit your `.env` file to git (it's already in .gitignore)
- Keep your API key private
- The `.env` file is for local development only

