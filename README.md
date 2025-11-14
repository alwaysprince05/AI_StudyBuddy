# 🧠 Smart Study Assistant

A full-stack AI-powered web application that helps students learn smarter. Enter any study topic, and the app fetches information from Wikipedia, then uses AI to generate concise summaries, quiz questions, and study tips. Includes a special Math Mode for quantitative and logic-based questions.

![React](https://img.shields.io/badge/Frontend-React-blue?logo=react)
![Flask](https://img.shields.io/badge/Backend-Flask-green?logo=flask)
![Gemini AI](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange?logo=google)
![Python](https://img.shields.io/badge/Language-Python-yellow?logo=python)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Prompt Engineering](#prompt-engineering)
- [Testing](#testing)
- [Deployment](#deployment)
- [AI Tools Disclosure](#ai-tools-disclosure)

---

## 🎯 Overview

Smart Study Assistant is a mini full-stack web application designed to enhance student learning through AI-powered content generation. The application:

1. **Fetches** topic data from Wikipedia API
2. **Generates** AI-powered summaries (3 bullet points)
3. **Creates** interactive quiz questions (3 MCQs)
4. **Provides** personalized study tips
5. **Supports** Math Mode for quantitative/logic questions

---

## ✨ Features

### Core Functionality
- ✅ Topic-based study material generation
- ✅ Wikipedia API integration for content fetching
- ✅ AI-powered summary generation (3 key points)
- ✅ Interactive quiz with 3 multiple-choice questions
- ✅ Personalized study tips
- ✅ Math Mode for quantitative/logic questions with detailed explanations

### Frontend Features
- 🎨 Modern, responsive UI with dark mode support
- ⚡ Loading states and error handling
- 📚 Topic history via localStorage
- 🎭 Smooth animations and transitions
- 📱 Mobile-friendly design

### Backend Features
- 🔒 Proper error handling and status codes
- 📊 JSON API responses
- 🌐 CORS enabled for frontend integration
- 🧪 Health check endpoint

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Frontend** | React 19.2.0 |
| **Backend** | Flask 3.0.0, Python 3.8+ |
| **AI Engine** | Google Gemini 2.5 Flash API |
| **Data Source** | Wikipedia REST API |
| **Styling** | CSS3 with CSS Variables |
| **State Management** | React Hooks (useState, useEffect) |
| **Storage** | localStorage (browser) |

---

## 📁 Project Structure

```
AI_StudyBuddy/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── requirements.txt       # Python dependencies
│   ├── test_backend.py        # Backend test cases
│   └── .env.example           # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── App.css            # Styling
│   │   └── index.js           # React entry point
│   ├── package.json           # Node.js dependencies
│   └── .env.example           # Frontend environment variables
├── README.md                  # This file
└── .gitignore                 # Git ignore rules
```

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 16+ and npm
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key:
   GEMINI_API_KEY=your_actual_api_key_here
   PORT=5001
   FLASK_ENV=development
   ```

5. **Run the backend server:**
   ```bash
   python app.py
   ```

   The backend will run on `http://localhost:5001`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create `.env` file (optional, defaults to localhost:5001):**
   ```bash
   REACT_APP_API_URL=http://localhost:5001
   ```

4. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will run on `http://localhost:3000`

### Running Both Services

Open two terminal windows:
- **Terminal 1:** Run backend (`cd backend && python app.py`)
- **Terminal 2:** Run frontend (`cd frontend && npm start`)

Visit `http://localhost:3000` in your browser.

---

## 📡 API Documentation

### Endpoint: `/study`

**Method:** `GET`

**Query Parameters:**
- `topic` (required): The study topic (e.g., "Machine Learning", "Calculus")
- `mode` (optional): Set to `"math"` for math mode, otherwise normal mode

**Example Requests:**

```bash
# Normal mode
GET /study?topic=Python&mode=

# Math mode
GET /study?topic=Calculus&mode=math
```

**Response Format (Normal Mode):**

```json
{
  "topic": "Python",
  "mode": "normal",
  "summary": [
    "Python is a high-level, interpreted programming language known for its simplicity and readability.",
    "It supports multiple programming paradigms including procedural, object-oriented, and functional programming.",
    "Python has a vast ecosystem of libraries and frameworks, making it popular for web development, data science, and AI."
  ],
  "quiz": [
    {
      "question": "What is Python primarily known for?",
      "options": [
        "Speed and performance",
        "Simplicity and readability",
        "Low-level system access",
        "Memory efficiency"
      ],
      "correct": "B"
    },
    // ... 2 more questions
  ],
  "study_tip": "Focus on understanding Python's core concepts like data structures, functions, and object-oriented programming. Practice by building small projects to reinforce your learning.",
  "source": "Wikipedia + Gemini AI"
}
```

**Response Format (Math Mode):**

```json
{
  "topic": "Calculus",
  "mode": "math",
  "math_question": {
    "question": "Find the derivative of f(x) = x³ + 2x² - 5x + 1",
    "answer": "f'(x) = 3x² + 4x - 5",
    "explanation": "To find the derivative, apply the power rule: d/dx(xⁿ) = nxⁿ⁻¹. For each term: d/dx(x³) = 3x², d/dx(2x²) = 4x, d/dx(-5x) = -5, and d/dx(1) = 0. Combining these gives f'(x) = 3x² + 4x - 5."
  },
  "source": "Wikipedia + Gemini AI"
}
```

**Error Responses:**

```json
{
  "error": "Topic parameter is required"
}
```
Status: `400 Bad Request`

```json
{
  "error": "Internal server error: [error message]"
}
```
Status: `500 Internal Server Error`

### Endpoint: `/health`

**Method:** `GET`

**Response:**
```json
{
  "status": "healthy",
  "service": "Smart Study Assistant API"
}
```

---

## 🎨 Prompt Engineering

The application uses carefully crafted prompts to ensure consistent, high-quality outputs from the Gemini AI model.

### Summary Prompt Strategy
- **Format:** Request exactly 3 bullet points
- **Content:** Focus on most important aspects
- **Length:** Single, clear sentences per bullet
- **Context:** Include Wikipedia content (first 1500 chars)

### Quiz Prompt Strategy
- **Format:** Structured MCQ with 4 options (A-D)
- **Quantity:** Exactly 3 questions
- **Clarity:** Clear question text and distinct options
- **Answer Indication:** Explicitly mark correct answer

### Study Tip Prompt Strategy
- **Format:** Single, concise tip (1-2 sentences)
- **Focus:** Practical, actionable advice
- **Tone:** Encouraging and helpful

### Math Mode Prompt Strategy
- **Format:** Structured with QUESTION, ANSWER, EXPLANATION sections
- **Type:** Quantitative or logic-based problems
- **Detail:** Include step-by-step explanation
- **Difficulty:** Challenging but solvable

**Example Prompts:**

See `backend/app.py` for the exact prompt templates used in production.

---

## 🧪 Testing

### Backend Tests

Run the test suite:

```bash
cd backend
python test_backend.py
```

**Test Cases:**
1. ✅ Health check endpoint
2. ✅ Normal mode study endpoint
3. ✅ Math mode study endpoint
4. ✅ Error handling (missing topic parameter)

### Manual Testing Plan

1. **Normal Mode:**
   - Enter topic: "Machine Learning"
   - Verify: Summary (3 bullets), Quiz (3 MCQs), Study Tip displayed
   - Check: All sections render correctly

2. **Math Mode:**
   - Enable Math Mode toggle
   - Enter topic: "Calculus"
   - Verify: Math question with answer and explanation
   - Test: "Show Answer" expandable section

3. **Error Handling:**
   - Submit empty topic → Should show error
   - Test with invalid topic → Should handle gracefully

4. **UI Features:**
   - Toggle dark mode → Should persist in localStorage
   - Test topic history → Should save and load from localStorage
   - Test responsive design on mobile

---

## 🌐 Deployment

### Backend Deployment (Render/Heroku/Railway)

**Render Example:**

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`
5. Add environment variables:
   - `GEMINI_API_KEY`: Your API key
   - `PORT`: 5001 (or auto-assigned)
   - `FLASK_ENV`: production

**Backend URL:** `https://your-backend.onrender.com`

### Frontend Deployment (Vercel/Netlify)

**Vercel Example:**

1. Install Vercel CLI: `npm i -g vercel`
2. Navigate to frontend: `cd frontend`
3. Deploy: `vercel`
4. Set environment variable:
   - `REACT_APP_API_URL`: Your backend URL

**Frontend URL:** `https://your-app.vercel.app`

### Environment Variables

**Backend (.env):**
```
GEMINI_API_KEY=your_key_here
PORT=5001
FLASK_ENV=production
```

**Frontend (.env):**
```
REACT_APP_API_URL=https://your-backend.onrender.com
```

### Hosted URLs

After deployment, update this section with your live URLs:

- **Frontend:** `https://your-frontend.vercel.app`
- **Backend:** `https://your-backend.onrender.com`

---

## 🤖 AI Tools Disclosure

This project was developed with the assistance of AI tools for productivity and code generation. The following parts were AI-assisted:

- **Initial project structure setup** - AI-assisted for boilerplate code
- **Prompt engineering** - Iteratively refined with AI assistance
- **CSS styling and animations** - AI-assisted for modern UI design
- **Error handling patterns** - AI-assisted for best practices
- **Documentation** - AI-assisted for comprehensive README

**Original Work:**
- Core application logic and architecture decisions
- API endpoint design and implementation
- React component structure and state management
- Wikipedia API integration approach
- Testing strategy and test cases

All code has been reviewed, understood, and customized for this specific project. No code was copy-pasted without understanding or modification.

---

## 📝 License

This project is open source and available for educational purposes.

---

## 👨‍💻 Author

**Prince Maurya**

- GitHub: [@princemaurya](https://github.com/princemaurya)

---

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- Wikipedia for content source
- React and Flask communities for excellent documentation

---

**🌟 If you find this project useful, please give it a star! 🌟**
