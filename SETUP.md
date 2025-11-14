# Quick Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- Gemini API Key: https://makersuite.google.com/app/apikey

## Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
python app.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 3. Access
Open http://localhost:3000 in your browser.

## Testing Backend
```bash
cd backend
python test_backend.py
```

