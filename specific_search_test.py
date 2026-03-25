#!/usr/bin/env python3
"""
Specific Search & Explore API Testing
Tests the exact endpoints mentioned in the review request
"""

import requests
import json

BASE_URL = "https://fast-reload-app.preview.emergentagent.com/api"

def get_auth_token():
    """Get auth token for test user"""
    # First try to register
    register_data = {
        "email": "test_search@test.com",
        "password": "test123456", 
        "name": "TestUser"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data, timeout=30)
        if response.status_code == 200:
            return response.json().get("access_token")
    except Exception:
        pass
    
    # If register fails, try login
    login_data = {
        "email": "test_search@test.com",
        "password": "test123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=30)
        if response.status_code == 200:
            return response.json().get("access_token")
    except Exception:
        pass
    
    return None

def test_specific_endpoints():
    """Test the exact endpoints from the review request"""
    print("🔍 Testing Specific Search & Explore Endpoints as per Review Request")
    print("="*70)
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("❌ FAILED: Could not get auth token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    test_cases = [
        {
            "name": "1. Search Arabic text in posts",
            "method": "GET",
            "endpoint": "/sohba/search",
            "params": {"q": "سبحان", "type": "all"}
        },
        {
            "name": "2. Search for users", 
            "method": "GET",
            "endpoint": "/sohba/search",
            "params": {"q": "Admin", "type": "users"}
        },
        {
            "name": "3. Get explore/trending posts",
            "method": "GET", 
            "endpoint": "/sohba/explore",
            "params": {"limit": 10}
        },
        {
            "name": "4. Get trending users",
            "method": "GET",
            "endpoint": "/sohba/trending-users", 
            "params": {"limit": 5}
        },
        {
            "name": "5. Get posts (existing)",
            "method": "GET",
            "endpoint": "/sohba/posts",
            "params": {"category": "all", "limit": 5}
        },
        {
            "name": "6. Get categories (existing)",
            "method": "GET", 
            "endpoint": "/sohba/categories",
            "params": {}
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}")
        print(f"Testing: {test_case['method']} {test_case['endpoint']}")
        
        try:
            url = f"{BASE_URL}{test_case['endpoint']}"
            response = requests.get(url, params=test_case['params'], headers=headers, timeout=30)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Analyze response based on endpoint
                    if "/search" in test_case['endpoint']:
                        total = data.get('total', 0)
                        posts = len(data.get('posts', []))
                        users = len(data.get('users', []))
                        print(f"✅ SUCCESS: Total results: {total}, Posts: {posts}, Users: {users}")
                        
                    elif "/explore" in test_case['endpoint']:
                        posts = len(data.get('posts', []))
                        total = data.get('total', 0)
                        print(f"✅ SUCCESS: Explore posts: {posts}, Total: {total}")
                        
                    elif "/trending-users" in test_case['endpoint']:
                        users = len(data.get('users', []))
                        print(f"✅ SUCCESS: Trending users: {users}")
                        
                    elif "/posts" in test_case['endpoint']:
                        posts = len(data.get('posts', []))
                        total = data.get('total', 0)
                        print(f"✅ SUCCESS: Posts loaded: {posts}, Total: {total}")
                        
                    elif "/categories" in test_case['endpoint']:
                        categories = len(data.get('categories', []))
                        print(f"✅ SUCCESS: Categories loaded: {categories}")
                        
                    results.append({"test": test_case['name'], "status": "PASS", "response": data})
                    
                except json.JSONDecodeError:
                    print(f"❌ FAILED: Invalid JSON response")
                    results.append({"test": test_case['name'], "status": "FAIL", "error": "Invalid JSON"})
            else:
                print(f"❌ FAILED: HTTP {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error: {error_data}")
                except:
                    print(f"Error: {response.text}")
                results.append({"test": test_case['name'], "status": "FAIL", "error": f"HTTP {response.status_code}"})
                
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            results.append({"test": test_case['name'], "status": "FAIL", "error": str(e)})
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY OF SPECIFIC ENDPOINT TESTS")
    print("="*70)
    
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    
    for result in results:
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        print(f"{status_icon} {result['test']} - {result['status']}")
    
    print(f"\nFINAL RESULT: {passed} passed, {failed} failed")
    print("="*70)

if __name__ == "__main__":
    test_specific_endpoints()