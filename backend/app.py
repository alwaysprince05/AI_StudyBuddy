"""
Smart Study Assistant - Backend API
Flask backend that fetches Wikipedia data and uses AI to generate study materials
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import re

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in environment variables!")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def fetch_wikipedia_content(topic: str) -> str:
    """
    Fetch content from Wikipedia API for the given topic.
    Returns the first 2000 characters of the Wikipedia page content.
    """
    try:
        # Clean topic name for URL
        topic_clean = topic.strip().replace(" ", "_")
        
        # Wikipedia API endpoint for summary/extract
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic_clean}"
        response = requests.get(url, timeout=10, headers={'User-Agent': 'SmartStudyAssistant/1.0'})
        
        if response.status_code == 200:
            data = response.json()
            # Get extract (summary) - this is usually 2-3 paragraphs
            extract = data.get("extract", "")
            
            # Try to get more detailed content from the full page
            try:
                # Use the mobile content API for cleaner text
                content_url = f"https://en.wikipedia.org/api/rest_v1/page/mobile-sections/{topic_clean}"
                content_response = requests.get(content_url, timeout=10, headers={'User-Agent': 'SmartStudyAssistant/1.0'})
                
                if content_response.status_code == 200:
                    content_data = content_response.json()
                    # Extract text from sections
                    full_text = extract
                    if 'lead' in content_data:
                        full_text += " " + content_data['lead'].get('text', '')
                    if 'remaining' in content_data:
                        for section in content_data['remaining'][:2]:  # First 2 sections
                            if 'text' in section:
                                full_text += " " + section['text']
                    
                    # Remove HTML tags and clean up
                    text = re.sub(r'<[^>]+>', '', full_text)
                    text = re.sub(r'\s+', ' ', text).strip()
                    
                    # Limit to 2000 characters
                    if len(text) > 2000:
                        text = text[:2000] + "..."
                    
                    return text if text.strip() else extract
            except:
                pass  # Fall back to extract if detailed fetch fails
            
            # Return the extract if we have it
            if extract:
                return extract
            else:
                return f"Information about {topic}"
        else:
            # Fallback: return a message that AI will use its knowledge
            return f"Information about {topic}"
    except Exception as e:
        print(f"Error fetching Wikipedia: {e}")
        # Return a basic message - AI will use its knowledge base
        return f"Information about {topic}"


def generate_ai_response(prompt: str) -> str:
    """Generate response using Gemini AI."""
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        else:
            raise ValueError("Empty response from AI")
    except Exception as e:
        error_msg = str(e)
        print(f"AI Error: {error_msg}")
        # Check for API key errors
        if "API key" in error_msg or "API_KEY" in error_msg or "API_KEY_INVALID" in error_msg:
            raise ValueError("Invalid or missing Gemini API key. Please check your GEMINI_API_KEY in the .env file.")
        raise ValueError(f"AI generation failed: {error_msg}")


def parse_summary(text: str) -> list:
    """Parse AI summary into 3 bullet points."""
    # Extract bullet points
    bullets = re.findall(r'[-•*]\s*(.+?)(?=\n[-•*]|\n\n|$)', text, re.MULTILINE)
    if bullets:
        return bullets[:3]
    
    # Fallback: split by newlines
    lines = [line.strip() for line in text.split('\n') if line.strip() and not line.strip().startswith('#')]
    return lines[:3] if lines else [text[:200]]


def parse_quiz(text: str) -> list:
    """Parse AI quiz into structured MCQ format."""
    questions = []
    
    # Split by "Question" markers
    parts = re.split(r'(?:Question\s*\d+[:.]?\s*|^\d+[\.\)]\s*)', text, flags=re.MULTILINE | re.IGNORECASE)
    
    for part in parts[1:4]:  # Take first 3 questions
        if not part.strip():
            continue
            
        lines = [l.strip() for l in part.split('\n') if l.strip() and len(l.strip()) > 1]
        if len(lines) < 2:
            continue
            
        question_text = lines[0].strip()
        # Remove question number if present
        question_text = re.sub(r'^\d+[\.\)]\s*', '', question_text)
        options = []
        correct_answer = None
        
        # Extract options (A-D format)
        for line in lines[1:]:
            option_match = re.match(r'^([A-D])[\.\)]\s*(.+)', line, re.IGNORECASE)
            if option_match:
                option_text = option_match.group(2).strip()
                options.append(option_text)
            elif 'correct' in line.lower() or 'answer' in line.lower():
                # Extract correct answer
                match = re.search(r'([A-D])', line, re.IGNORECASE)
                if match:
                    correct_answer = match.group(1).upper()
        
        # Ensure we have at least 2 options
        if len(options) >= 2:
            # Pad to 4 options if needed
            while len(options) < 4:
                options.append(f"Option {chr(65 + len(options))}")
            
            questions.append({
                "question": question_text,
                "options": options[:4],  # Max 4 options
                "correct": correct_answer or "A"
            })
    
    # If parsing failed, create structured format from text
    if not questions or len(questions) < 3:
        # Try alternative parsing: look for numbered questions
        alt_parts = re.split(r'\n(?=\d+[\.\)]|\*\s*[A-Z])', text)
        for part in alt_parts[:3]:
            if len(questions) >= 3:
                break
            lines = [l.strip() for l in part.split('\n') if l.strip()]
            if len(lines) >= 3:
                question_text = lines[0]
                options = [l for l in lines[1:5] if re.match(r'^[A-D]', l, re.IGNORECASE)]
                if len(options) >= 2:
                    questions.append({
                        "question": question_text,
                        "options": [re.sub(r'^[A-D][\.\)]\s*', '', opt).strip() for opt in options[:4]],
                        "correct": "A"
                    })
    
    # Final fallback: create basic questions
    if len(questions) < 3:
        sentences = re.split(r'[.!?]+', text)
        for i in range(min(3 - len(questions), len(sentences) // 4)):
            start = (len(questions) * 4) + i * 4
            if start < len(sentences):
                question_text = sentences[start].strip()
                if question_text:
                    questions.append({
                        "question": question_text + "?",
                        "options": [
                            sentences[start + 1].strip() if start + 1 < len(sentences) else "Option A",
                            sentences[start + 2].strip() if start + 2 < len(sentences) else "Option B",
                            sentences[start + 3].strip() if start + 3 < len(sentences) else "Option C",
                            "None of the above"
                        ],
                        "correct": "A"
                    })
    
    return questions[:3]  # Return max 3 questions


@app.route('/study', methods=['GET'])
def study_endpoint():
    """
    Main study endpoint: /study?topic=<topic>&mode=<mode>
    
    Returns:
    - summary: list of 3 bullet points
    - quiz: list of 3 MCQs
    - study_tip: string
    - math_question: (if mode=math) object with question, answer, explanation
    """
    try:
        topic = request.args.get('topic', '').strip()
        mode = request.args.get('mode', '').strip().lower()
        
        if not topic:
            return jsonify({
                "error": "Topic parameter is required"
            }), 400
        
        # Fetch Wikipedia content
        wiki_content = fetch_wikipedia_content(topic)
        
        if mode == 'math':
            # Math mode: Generate one quantitative/logic question
            try:
                math_prompt = f"""
                Based on the following information about {topic}, create ONE quantitative or logic-based question.
                
                Information:
                {wiki_content[:1500]}
                
                Generate:
                1. A challenging quantitative or logic question related to {topic}
                2. The correct answer (with calculation if applicable)
                3. A detailed explanation of how to solve it
                
                Format your response as:
                QUESTION: [the question]
                ANSWER: [the answer]
                EXPLANATION: [detailed explanation]
                """
                
                math_response = generate_ai_response(math_prompt)
                
                # Parse math response
                question_match = re.search(r'QUESTION:\s*(.+?)(?=ANSWER:|$)', math_response, re.DOTALL)
                answer_match = re.search(r'ANSWER:\s*(.+?)(?=EXPLANATION:|$)', math_response, re.DOTALL)
                explanation_match = re.search(r'EXPLANATION:\s*(.+?)$', math_response, re.DOTALL)
                
                math_question = {
                    "question": question_match.group(1).strip() if question_match else "Math question about " + topic,
                    "answer": answer_match.group(1).strip() if answer_match else "Answer",
                    "explanation": explanation_match.group(1).strip() if explanation_match else math_response
                }
                
                return jsonify({
                    "topic": topic,
                    "mode": "math",
                    "math_question": math_question,
                    "source": "Wikipedia + Gemini AI"
                }), 200
            except ValueError as e:
                if "API key" in str(e):
                    return jsonify({
                        "error": "Invalid or missing Gemini API key. Please check your GEMINI_API_KEY in the backend/.env file.",
                        "details": "Get your free API key from: https://makersuite.google.com/app/apikey"
                    }), 401
                raise
        
        else:
            # Normal mode: Generate summary, quiz, and study tip
            
            try:
                # Generate summary (3 bullets)
                summary_prompt = f"""
                Based on the following information about {topic}, create a concise summary with exactly 3 key bullet points.
                Each bullet should be a single, clear sentence covering the most important aspects.
                
                Information:
                {wiki_content[:1500]}
                
                Format as:
                - First key point
                - Second key point  
                - Third key point
                """
                
                summary_text = generate_ai_response(summary_prompt)
                summary = parse_summary(summary_text)
            except ValueError as e:
                if "API key" in str(e):
                    return jsonify({
                        "error": "Invalid or missing Gemini API key. Please check your GEMINI_API_KEY in the backend/.env file.",
                        "details": "Get your free API key from: https://makersuite.google.com/app/apikey"
                    }), 401
                raise
            
            try:
                # Generate quiz (3 MCQs)
                quiz_prompt = f"""
                Based on the following information about {topic}, create exactly 3 multiple-choice questions.
                Each question should have 4 options (A, B, C, D) and clearly indicate the correct answer.
                
                Information:
                {wiki_content[:1500]}
                
                Format each question as:
                Question 1: [question text]
                A. [option A]
                B. [option B]
                C. [option C]
                D. [option D]
                Correct Answer: [A/B/C/D]
                
                Question 2: ...
                """
                
                quiz_text = generate_ai_response(quiz_prompt)
                quiz = parse_quiz(quiz_text)
            except ValueError as e:
                if "API key" in str(e):
                    return jsonify({
                        "error": "Invalid or missing Gemini API key. Please check your GEMINI_API_KEY in the backend/.env file.",
                        "details": "Get your free API key from: https://makersuite.google.com/app/apikey"
                    }), 401
                raise
            
            try:
                # Generate study tip
                tip_prompt = f"""
                Based on the following information about {topic}, provide ONE practical study tip 
                that would help a student learn and remember this topic effectively.
                Keep it concise (1-2 sentences).
                
                Information:
                {wiki_content[:1500]}
                """
                
                study_tip = generate_ai_response(tip_prompt).strip()
                if not study_tip:
                    study_tip = f"Focus on understanding the core concepts of {topic} and practice applying them."
            except ValueError as e:
                if "API key" in str(e):
                    return jsonify({
                        "error": "Invalid or missing Gemini API key. Please check your GEMINI_API_KEY in the backend/.env file.",
                        "details": "Get your free API key from: https://makersuite.google.com/app/apikey"
                    }), 401
                # If study tip fails, use a default
                study_tip = f"Focus on understanding the core concepts of {topic} and practice applying them."
            
            return jsonify({
                "topic": topic,
                "mode": "normal",
                "summary": summary,
                "quiz": quiz,
                "study_tip": study_tip,
                "source": "Wikipedia + Gemini AI"
            }), 200
    
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "Smart Study Assistant API"}), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')

