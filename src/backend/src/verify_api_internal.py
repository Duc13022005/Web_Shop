
import asyncio
import sys
import json
import urllib.request
import urllib.error

async def verify_api():
    print("🚀 STARTING INTERNAL API VERIFICATION (PRODUCTS)")
    
    url = "http://localhost:8000/api/v1/products"
    
    print(f"📡 Sending GET request to: {url}")
    
    req = urllib.request.Request(
        url, 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"✅ API Response Code: {response.getcode()}")
            body = response.read().decode('utf-8')
            print(f"📄 Response Body: {body[:100]}...")
            
            if "access_token" in body:
                print("🎉 SUCCESS: Access Token received!")
            else:
                print("⚠️  WARNING: Response 200 OK but no token found (check body).")
                
    except urllib.error.HTTPError as e:
        print(f"❌ API Request Failed: {e.code} {e.reason}")
        print(f"📄 Error Body: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify_api())
