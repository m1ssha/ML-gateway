import requests
import json
import time

def test_health():
    print("Testing /health...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        assert response.json()["model_loaded"] is True
    except Exception as e:
        print(f"Health check failed: {e}")

def test_predict():
    print("\nTesting /predict...")
    payload = {
        "session_id": "test-uuid",
        "context": "USER: Привет! Помоги мне с вопросом про DevOps?\nASSISTANT: Конечно, я сразу тебе с этим помогу!."
    }
    try:
        start_time = time.time()
        response = requests.post("http://localhost:8000/predict", json=payload)
        end_time = time.time()
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            assert "is_attack" in data
            assert "risk_score" in data
            print(f"Total round-trip time: {(end_time - start_time)*1000:.2f}ms")
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Predict failed: {e}")

if __name__ == "__main__":
    # Wait for server to be ready
    print("Waiting for server to start...")
    for i in range(10):
        try:
            requests.get("http://localhost:8000/health")
            print("Server is up!")
            break
        except:
            time.sleep(2)
    
    test_health()
    test_predict()
