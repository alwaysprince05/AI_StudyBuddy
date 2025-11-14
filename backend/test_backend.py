"""
Backend API Test Cases
Run with: python test_backend.py
"""
import requests
import json

BASE_URL = "http://localhost:5001"

def test_health_check():
    """Test health check endpoint."""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed")

def test_study_endpoint_normal():
    """Test /study endpoint in normal mode."""
    print("\nTesting /study endpoint (normal mode)...")
    response = requests.get(f"{BASE_URL}/study?topic=Python&mode=")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "topic" in data
    assert "summary" in data
    assert "quiz" in data
    assert "study_tip" in data
    assert len(data["summary"]) == 3
    assert len(data["quiz"]) == 3
    
    print("✅ Normal mode test passed")
    print(f"   Topic: {data['topic']}")
    print(f"   Summary bullets: {len(data['summary'])}")
    print(f"   Quiz questions: {len(data['quiz'])}")

def test_study_endpoint_math():
    """Test /study endpoint in math mode."""
    print("\nTesting /study endpoint (math mode)...")
    response = requests.get(f"{BASE_URL}/study?topic=Calculus&mode=math")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "topic" in data
    assert "mode" in data
    assert data["mode"] == "math"
    assert "math_question" in data
    assert "question" in data["math_question"]
    assert "answer" in data["math_question"]
    assert "explanation" in data["math_question"]
    
    print("✅ Math mode test passed")
    print(f"   Topic: {data['topic']}")
    print(f"   Question: {data['math_question']['question'][:50]}...")

def test_study_endpoint_error():
    """Test error handling for missing topic."""
    print("\nTesting error handling...")
    response = requests.get(f"{BASE_URL}/study?topic=")
    
    assert response.status_code == 400
    assert "error" in response.json()
    
    print("✅ Error handling test passed")

if __name__ == "__main__":
    print("=" * 50)
    print("Backend API Test Suite")
    print("=" * 50)
    print("\n⚠️  Make sure the backend server is running on http://localhost:5001")
    print("   Start it with: cd backend && python app.py\n")
    
    try:
        test_health_check()
        test_study_endpoint_normal()
        test_study_endpoint_math()
        test_study_endpoint_error()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection error: Make sure the backend server is running!")

