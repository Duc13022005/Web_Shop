
import urllib.request
import json
import urllib.error

def verify_external():
    print("🚀 TESTING EXTERNAL LOGIN (Host -> Docker)...")
    url = "http://localhost:8000/api/v1/auth/login"
    payload = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        url, 
        data=data, 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"✅ STATUS: {response.getcode()}")
            body = response.read().decode('utf-8')
            if "access_token" in body:
                print("🎉 SUCCESS: Token received!")
            else:
                print("⚠️  WARNING: No token in response.")
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    verify_external()
