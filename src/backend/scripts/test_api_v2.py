import requests
import json
import sys

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"

def print_result(name, success, data=None):
    symbol = "✅" if success else "❌"
    print(f"{symbol} {name}")
    if not success and data:
        print(f"   Error: {data}")
    if success and data:
        # Print summary of data if meaningful
        pass

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_result("Health Check", True)
            return True
        else:
            print_result("Health Check", False, response.text)
            return False
    except Exception as e:
        print_result("Health Check", False, str(e))
        return False

def test_login(email, password):
    url = f"{BASE_URL}{API_PREFIX}/auth/login"
    try:
        response = requests.post(url, json={"email": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            print_result(f"Login ({email})", True)
            return data["tokens"]["access_token"]
        else:
            print_result(f"Login ({email})", False, response.text)
            return None
    except Exception as e:
        print_result(f"Login ({email})", False, str(e))
        return None

def test_products():
    url = f"{BASE_URL}{API_PREFIX}/products"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            total = data.get("total", 0)
            print_result(f"Get Products (Total: {total})", True)
            return True
        else:
            print_result("Get Products", False, response.text)
            return False
    except Exception as e:
        print_result("Get Products", False, str(e))
        return False

def test_inventory(token):
    url = f"{BASE_URL}{API_PREFIX}/inventory/overview"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print_result(f"Inventory Overview (Products: {data.get('total_products')})", True)
            return True
        elif response.status_code == 403:
             print_result("Inventory Overview (Auth Check)", False, "Forbidden - Expected for non-admin/staff")
        else:
            print_result("Inventory Overview", False, response.text)
            return False
    except Exception as e:
        print_result("Inventory Overview", False, str(e))
        return False

def main():
    print("🚀 Starting API Verification...")
    
    if not test_health():
        print("⚠️ Backend might not be ready yet.")
        sys.exit(1)

    print("\n--- Public Endpoints ---")
    test_products()

    print("\n--- Authentication ---")
    # Admin
    admin_token = test_login("admin@shop.vn", "password123")
    
    # Customer
    customer_token = test_login("khach1@gmail.com", "password123")

    if admin_token:
        print("\n--- Protected Endpoints (Admin) ---")
        test_inventory(admin_token)

    if customer_token:
        print("\n--- Protected Endpoints (Customer) ---")
        # Try to access inventory (should fail or forbidden)
        # Note: In our implementation, maybe forbidden.
        pass

if __name__ == "__main__":
    main()
