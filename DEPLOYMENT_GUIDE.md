# 🚀 Deployment Guide

## Code Pushed Successfully! ✅

Your code has been committed locally. To push to GitHub, you need to authenticate.

## Option 1: Using Personal Access Token (Recommended)

1. **Create a Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Give it a name (e.g., "AI_StudyBuddy")
   - Select scopes: `repo` (full control of private repositories)
   - Click "Generate token"
   - **Copy the token** (you won't see it again!)

2. **Push using the token:**
   ```bash
   cd /Users/princemaurya/AI_StudyBuddy
   git push origin main
   ```
   When asked for password, paste your **token** (not your GitHub password)

## Option 2: Using SSH (More Secure)

1. **Set up SSH key** (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter to accept defaults
   cat ~/.ssh/id_ed25519.pub
   # Copy the output
   ```

2. **Add SSH key to GitHub:**
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste your public key
   - Save

3. **Change remote to SSH:**
   ```bash
   cd /Users/princemaurya/AI_StudyBuddy
   git remote set-url origin git@github.com:alwaysprince05/AI_StudyBuddy.git
   git push origin main
   ```

## Option 3: GitHub CLI

```bash
gh auth login
git push origin main
```

## After Pushing

Once pushed, you can deploy:

### Backend Deployment (Render/Heroku/Railway)
1. Connect your GitHub repo
2. Set environment variable: `GEMINI_API_KEY`
3. Deploy!

### Frontend Deployment (Vercel/Netlify)
1. Connect your GitHub repo
2. Set environment variable: `REACT_APP_API_URL` (your backend URL)
3. Deploy!

## Current Status

✅ Code committed locally
⏳ Waiting for GitHub authentication to push

