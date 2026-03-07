"""
Test script for Lung Disease Detection API
Tests the FastAPI backend locally before Hugging Face deployment
"""

import requests
import json
import sys
from pathlib import Path
import time

BASE_URL = "http://localhost:8000"  # Change to 7860 if testing app.py

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed!")
            print(f"  - Status: {data.get('status')}")
            print(f"  - Model loaded: {data.get('model_loaded')}")
            print(f"  - Device: {data.get('device')}")
            print(f"  - Model type: {data.get('model_type')}")
            print(f"  - Number of classes: {data.get('num_classes')}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error connecting to API: {str(e)}")
        print("  Make sure the backend is running!")
        return False


def test_root_endpoint():
    """Test the root endpoint"""
    print("\n" + "="*60)
    print("Testing Root Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Root endpoint working!")
            print(f"  - Message: {data.get('message')}")
            print(f"  - Version: {data.get('version')}")
            print(f"  - Model: {data.get('model')}")
            print(f"  - Classes: {', '.join(data.get('classes', []))}")
            return True
        else:
            print(f"✗ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_chat_endpoint():
    """Test the chat endpoint"""
    print("\n" + "="*60)
    print("Testing Chat Endpoint")
    print("="*60)
    
    test_messages = [
        "What is COVID-19?",
        "Symptoms of pneumonia",
        "How does your model work?",
        "What should I do after diagnosis?"
    ]
    
    all_passed = True
    for message in test_messages:
        print(f"\n📨 Testing: '{message}'")
        
        try:
            payload = {
                "message": message,
                "history": []
            }
            
            response = requests.post(
                f"{BASE_URL}/api/chat",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '')
                print(f"✓ Response received ({len(response_text)} chars)")
                print(f"  Preview: {response_text[:100]}...")
            else:
                print(f"✗ Failed: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            all_passed = False
    
    return all_passed


def test_prediction_endpoint(image_path=None):
    """Test the prediction endpoint"""
    print("\n" + "="*60)
    print("Testing Prediction Endpoint")
    print("="*60)
    
    if image_path is None:
        print("⚠ No image provided. Skipping prediction test.")
        print("  To test predictions, run:")
        print(f"  python {Path(__file__).name} path/to/xray_image.jpg")
        return None
    
    image_file = Path(image_path)
    
    if not image_file.exists():
        print(f"✗ Image file not found: {image_path}")
        return False
    
    print(f"📤 Uploading image: {image_file.name}")
    print(f"   Size: {image_file.stat().st_size / 1024:.1f} KB")
    
    try:
        with open(image_file, 'rb') as f:
            files = {'file': (image_file.name, f, 'image/jpeg')}
            
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/predict",
                files=files,
                timeout=30
            )
            elapsed_time = time.time() - start_time
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Prediction successful!")
            print(f"\n🔬 Results:")
            print(f"  Prediction: {data.get('prediction')}")
            print(f"  Confidence: {data.get('confidence')*100:.2f}%")
            print(f"  Inference time: {data.get('inference_time')} seconds")
            print(f"  Total request time: {elapsed_time:.3f} seconds")
            print(f"  Model: {data.get('model')}")
            
            print(f"\n📊 Class Probabilities:")
            probs = data.get('probabilities', {})
            for class_name, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True):
                bar = '█' * int(prob * 50)
                print(f"  {class_name:25s} {prob*100:6.2f}% {bar}")
            
            return True
        else:
            print(f"✗ Prediction failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def run_all_tests(image_path=None):
    """Run all tests"""
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*15 + "API TEST SUITE" + " "*29 + "║")
    print("║" + " "*10 + "Lung Disease Detection API" + " "*22 + "║")
    print("╚" + "═"*58 + "╝")
    
    print(f"\nBase URL: {BASE_URL}")
    print(f"Testing Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'health': test_health_check(),
        'root': test_root_endpoint(),
        'chat': test_chat_endpoint(),
        'prediction': test_prediction_endpoint(image_path)
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result is True else "✗ FAILED" if result is False else "⊘ SKIPPED"
        print(f"{test_name.upper():15s}: {status}")
    
    print(f"\nTotal: {total} | Passed: {passed} | Failed: {failed} | Skipped: {skipped}")
    
    if failed == 0 and passed > 0:
        print("\n✅ All tests passed! Backend is ready for deployment.")
        return True
    elif failed > 0:
        print(f"\n⚠️  {failed} test(s) failed. Please fix before deploying.")
        return False
    else:
        print("\n⚠️  No tests completed. Check if backend is running.")
        return False


if __name__ == "__main__":
    # Check if image path provided
    image_path = None
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    
    # Run tests
    success = run_all_tests(image_path)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
