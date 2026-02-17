"""
Quick test script for the FastAPI backend.
Run this after starting the API server with: uvicorn api:app --reload
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint."""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_basic_query():
    """Test basic query endpoint."""
    print("\n=== Testing Basic Query ===")
    payload = {
        "question": "Who is the CEO of Bhavna corp?",
        "top_k": 3
    }
    response = requests.post(f"{API_BASE_URL}/api/query/basic", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_advanced_query():
    """Test advanced query endpoint."""
    print("\n=== Testing Advanced Query ===")
    payload = {
        "question": "Who is the CEO of Bhavna corp?",
        "top_k": 3,
        "min_score": 0.0,
        "stream": False,
        "summarize": True
    }
    response = requests.post(f"{API_BASE_URL}/api/query/advanced", json=payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Question: {result.get('question')}")
    print(f"Answer: {result.get('answer')[:200]}...")
    print(f"Sources: {len(result.get('sources', []))} documents")
    print(f"Summary: {result.get('summary')}")
    return response.status_code == 200

def test_history():
    """Test history endpoints."""
    print("\n=== Testing History ===")
    
    # Get history
    response = requests.get(f"{API_BASE_URL}/api/history")
    print(f"Get History Status: {response.status_code}")
    history_data = response.json()
    print(f"History Count: {history_data.get('count')}")
    
    return response.status_code == 200

if __name__ == "__main__":
    print("=" * 60)
    print("FastAPI Backend Test Suite")
    print("=" * 60)
    print(f"Testing API at: {API_BASE_URL}")
    print("Make sure the API server is running!")
    print("Start with: uvicorn api:app --reload")
    print("=" * 60)
    
    try:
        results = []
        results.append(("Health Check", test_health()))
        results.append(("Basic Query", test_basic_query()))
        results.append(("Advanced Query", test_advanced_query()))
        results.append(("History", test_history()))
        
        print("\n" + "=" * 60)
        print("Test Results Summary")
        print("=" * 60)
        for test_name, passed in results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        all_passed = all(result[1] for result in results)
        if all_passed:
            print("\n🎉 All tests passed!")
        else:
            print("\n⚠️  Some tests failed. Check the output above.")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server!")
        print("Make sure the server is running with: uvicorn api:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
