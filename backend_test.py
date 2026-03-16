#!/usr/bin/env python3
"""
Islamic App Backend API Testing
Tests all backend API endpoints mentioned in the review request.
"""

import requests
import json
import sys
import time
from typing import Optional, Dict, Any

# Backend URL from frontend .env configuration
BASE_URL = "https://viral-shorts-96.preview.emergentagent.com/api"

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
        
    def add_result(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        self.results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'response_data': response_data
        })
        if success:
            self.passed += 1
        else:
            self.failed += 1
            
    def summary(self):
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY: {self.passed} passed, {self.failed} failed")
        print(f"{'='*60}")
        
        for result in self.results:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"{status}: {result['test']}")
            if result['details']:
                print(f"    Details: {result['details']}")
        print()

def make_request(method: str, endpoint: str, data: dict = None, headers: dict = None, timeout: int = 30) -> tuple:
    """Make HTTP request and return (success, response, details)"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=data, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=timeout)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=timeout)
        else:
            return False, None, f"Unsupported method: {method}"
            
        return True, response, f"Status: {response.status_code}"
        
    except requests.exceptions.Timeout:
        return False, None, f"Request timeout after {timeout}s"
    except requests.exceptions.ConnectionError:
        return False, None, "Connection error - backend might be down"
    except Exception as e:
        return False, None, f"Request failed: {str(e)}"

def test_root_endpoint(results: TestResults):
    """Test GET /api/ endpoint"""
    print("🔍 Testing root endpoint...")
    
    success, response, details = make_request("GET", "/")
    
    if not success:
        results.add_result("Root API Endpoint", False, details)
        return
        
    if response.status_code == 200:
        try:
            data = response.json()
            expected_version = "2.0"
            
            if (data.get("version") == expected_version and 
                "message" in data):
                results.add_result("Root API Endpoint", True, 
                                 f"API running: {data}")
            else:
                results.add_result("Root API Endpoint", False, 
                                 f"Unexpected response: {data}")
        except json.JSONDecodeError:
            results.add_result("Root API Endpoint", False, 
                             "Invalid JSON response")
    else:
        results.add_result("Root API Endpoint", False, 
                         f"HTTP {response.status_code}: {response.text}")

def test_user_registration(results: TestResults) -> Optional[str]:
    """Test POST /api/auth/register endpoint"""
    print("🔍 Testing user registration...")
    
    # Use test credentials from review request
    user_data = {
        "email": "test_search@test.com",
        "password": "test123456",
        "name": "TestUser"
    }
    
    success, response, details = make_request("POST", "/auth/register", user_data)
    
    if not success:
        results.add_result("User Registration", False, details)
        return None
        
    if response.status_code == 200:
        try:
            data = response.json()
            if "access_token" in data and "user" in data:
                access_token = data["access_token"]
                user_info = data["user"]
                results.add_result("User Registration", True, 
                                 f"User registered: {user_info.get('email')}, token received")
                return access_token
            else:
                results.add_result("User Registration", False, 
                                 f"Missing required fields in response: {data}")
                return None
        except json.JSONDecodeError:
            results.add_result("User Registration", False, 
                             "Invalid JSON response")
            return None
    elif response.status_code == 400:
        # User might already exist, try login instead
        results.add_result("User Registration", True, 
                         "User already exists (expected for repeated tests)")
        return test_user_login_direct(results, user_data["email"], user_data["password"])
    else:
        results.add_result("User Registration", False, 
                         f"HTTP {response.status_code}: {response.text}")
        return None

def test_user_login_direct(results: TestResults, email: str, password: str) -> Optional[str]:
    """Direct login helper function"""
    login_data = {"email": email, "password": password}
    
    success, response, details = make_request("POST", "/auth/login", login_data)
    
    if not success:
        return None
        
    if response.status_code == 200:
        try:
            data = response.json()
            if "access_token" in data:
                return data["access_token"]
        except json.JSONDecodeError:
            pass
    return None

def test_user_login(results: TestResults) -> Optional[str]:
    """Test POST /api/auth/login endpoint"""
    print("🔍 Testing user login...")
    
    login_data = {
        "email": "test_search@test.com",
        "password": "test123456"
    }
    
    success, response, details = make_request("POST", "/auth/login", login_data)
    
    if not success:
        results.add_result("User Login", False, details)
        return None
        
    if response.status_code == 200:
        try:
            data = response.json()
            if "access_token" in data and "user" in data:
                access_token = data["access_token"]
                user_info = data["user"]
                results.add_result("User Login", True, 
                                 f"Login successful for: {user_info.get('email')}")
                return access_token
            else:
                results.add_result("User Login", False, 
                                 f"Missing required fields in response: {data}")
                return None
        except json.JSONDecodeError:
            results.add_result("User Login", False, 
                             "Invalid JSON response")
            return None
    else:
        results.add_result("User Login", False, 
                         f"HTTP {response.status_code}: {response.text}")
        return None

def test_auth_me(results: TestResults, access_token: str):
    """Test GET /api/auth/me endpoint"""
    print("🔍 Testing auth/me endpoint...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    success, response, details = make_request("GET", "/auth/me", headers=headers)
    
    if not success:
        results.add_result("Auth Me Endpoint", False, details)
        return
        
    if response.status_code == 200:
        try:
            data = response.json()
            required_fields = ["id", "email", "name"]
            if all(field in data for field in required_fields):
                results.add_result("Auth Me Endpoint", True, 
                                 f"User info retrieved: {data.get('email')}")
            else:
                results.add_result("Auth Me Endpoint", False, 
                                 f"Missing required fields in response: {data}")
        except json.JSONDecodeError:
            results.add_result("Auth Me Endpoint", False, 
                             "Invalid JSON response")
    else:
        results.add_result("Auth Me Endpoint", False, 
                         f"HTTP {response.status_code}: {response.text}")

def test_prayer_times(results: TestResults):
    """Test GET /api/prayer-times endpoint"""
    print("🔍 Testing prayer times endpoint...")
    
    # Riyadh, Saudi Arabia coordinates
    params = {
        "lat": 24.68,
        "lon": 46.72
    }
    
    success, response, details = make_request("GET", "/prayer-times", params)
    
    if not success:
        results.add_result("Prayer Times API", False, details)
        return
        
    if response.status_code == 200:
        try:
            data = response.json()
            if (data.get("success") == True and 
                "source" in data and
                "times" in data):
                times = data["times"]
                required_prayers = ["fajr", "dhuhr", "asr", "maghrib", "isha"]
                if all(prayer in times for prayer in required_prayers):
                    results.add_result("Prayer Times API", True, 
                                     f"Prayer times retrieved with source: {data.get('source')}")
                else:
                    results.add_result("Prayer Times API", False, 
                                     f"Missing prayer times in response: {times}")
            else:
                results.add_result("Prayer Times API", False, 
                                 f"Unexpected response structure: {data}")
        except json.JSONDecodeError:
            results.add_result("Prayer Times API", False, 
                             "Invalid JSON response")
    else:
        results.add_result("Prayer Times API", False, 
                         f"HTTP {response.status_code}: {response.text}")

def test_mosque_search(results: TestResults):
    """Test GET /api/mosques/search endpoint"""
    print("🔍 Testing mosque search endpoint...")
    
    # Riyadh, Saudi Arabia coordinates
    params = {
        "lat": 24.68,
        "lon": 46.72,
        "radius": 5000
    }
    
    success, response, details = make_request("GET", "/mosques/search", params)
    
    if not success:
        results.add_result("Mosque Search API", False, details)
        return
        
    if response.status_code == 200:
        try:
            data = response.json()
            if "mosques" in data and "count" in data:
                mosques = data["mosques"]
                count = data["count"]
                
                if isinstance(mosques, list) and count >= 0:
                    if count > 0 and len(mosques) > 0:
                        # Check first mosque structure
                        mosque = mosques[0]
                        required_fields = ["osm_id", "name", "latitude", "longitude", "address"]
                        if all(field in mosque for field in required_fields):
                            results.add_result("Mosque Search API", True, 
                                             f"Found {count} mosques, first: {mosque.get('name')}")
                        else:
                            results.add_result("Mosque Search API", False, 
                                             f"Mosque object missing required fields: {mosque}")
                    else:
                        results.add_result("Mosque Search API", True, 
                                         f"Search completed successfully, found {count} mosques")
                else:
                    results.add_result("Mosque Search API", False, 
                                     f"Invalid response structure: {data}")
            else:
                results.add_result("Mosque Search API", False, 
                                 f"Missing required fields in response: {data}")
        except json.JSONDecodeError:
            results.add_result("Mosque Search API", False, 
                             "Invalid JSON response")
    else:
        results.add_result("Mosque Search API", False, 
                         f"HTTP {response.status_code}: {response.text}")

def test_mosque_prayer_times(results: TestResults):
    """Test POST /api/mosques/prayer-times endpoint"""
    print("🔍 Testing mosque prayer times endpoint...")
    
    mosque_data = {
        "mosqueName": "الحرم المكي الشريف",  # Grand Mosque of Mecca
        "latitude": 24.68,
        "longitude": 46.72
    }
    
    success, response, details = make_request("POST", "/mosques/prayer-times", mosque_data)
    
    if not success:
        results.add_result("Mosque Prayer Times API", False, details)
        return
        
    if response.status_code == 200:
        try:
            data = response.json()
            if (data.get("success") == True and 
                "source" in data and
                "times" in data):
                times = data["times"]
                source = data["source"]
                required_prayers = ["fajr", "dhuhr", "asr", "maghrib", "isha"]
                if all(prayer in times for prayer in required_prayers):
                    results.add_result("Mosque Prayer Times API", True, 
                                     f"Mosque prayer times retrieved with source: {source}")
                else:
                    results.add_result("Mosque Prayer Times API", False, 
                                     f"Missing prayer times in response: {times}")
            else:
                results.add_result("Mosque Prayer Times API", False, 
                                 f"Unexpected response structure: {data}")
        except json.JSONDecodeError:
            results.add_result("Mosque Prayer Times API", False, 
                             "Invalid JSON response")
    else:
        results.add_result("Mosque Prayer Times API", False, 
                         f"HTTP {response.status_code}: {response.text}")

# ========== NEW SEARCH & EXPLORE ENDPOINTS TESTS ==========

def test_sohba_search_arabic(results: TestResults, access_token: str):
    """Test GET /api/sohba/search with Arabic text"""
    print("🔍 Testing sohba search with Arabic text...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": "سبحان", "type": "all"}
    
    success, response, details = make_request("GET", "/sohba/search", params, headers)
    
    if not success:
        results.add_result("Sohba Search (Arabic)", False, details)
        return
        
    if response.status_code == 200:
        try:
            data = response.json()
            required_fields = ["posts", "users", "hashtags", "total"]
            if all(field in data for field in required_fields):
                results.add_result("Sohba Search (Arabic)", True, 
                                 f"Search completed: {data.get('total')} total results")
            else:
                results.add_result("Sohba Search (Arabic)", False, 
                                 f"Missing required fields in response: {data}")
        except json.JSONDecodeError:
            results.add_result("Sohba Search (Arabic)", False, 
                             "Invalid JSON response")
    else:
        results.add_result("Sohba Search (Arabic)", False, 
                         f"HTTP {response.status_code}: {response.text}")

def test_sohba_search_users(results: TestResults, access_token: str):
    """Test GET /api/sohba/search for users"""
    print("🔍 Testing sohba search for users...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": "Ahmed", "type": "users"}
    
    success, response, details = make_request("GET", "/sohba/search", params, headers)
    
    if not success:
        results.add_result("Sohba Search (Users)", False, details)
        return
        
    if response.status_code == 200:
        try:
            data = response.json()
            required_fields = ["posts", "users", "hashtags", "total"]
            if all(field in data for field in required_fields):
                users = data.get("users", [])
                if isinstance(users, list):
                    results.add_result("Sohba Search (Users)", True, 
                                     f"User search completed: found {len(users)} users")
                else:
                    results.add_result("Sohba Search (Users)", False, 
                                     f"Users field is not a list: {type(users)}")
            else:
                results.add_result("Sohba Search (Users)", False, 
                                 f"Missing required fields in response: {data}")
        except json.JSONDecodeError:
            results.add_result("Sohba Search (Users)", False, 
                             "Invalid JSON response")
    else:
        results.add_result("Sohba Search (Users)", False, 
                         f"HTTP {response.status_code}: {response.text}")

def test_sohba_explore(results: TestResults, access_token: str):
    """Test GET /api/sohba/explore endpoint"""
    print("🔍 Testing sohba explore feed...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"limit": 10}
    
    success, response, details = make_request("GET", "/sohba/explore", params, headers)
    
    if not success:
        results.add_result("Sohba Explore Feed", False, details)
        return
        
    if response.status_code == 200:
        try:
            data = response.json()
            required_fields = ["posts", "total", "page", "has_more"]
            if all(field in data for field in required_fields):
                posts = data.get("posts", [])
                total = data.get("total", 0)
                results.add_result("Sohba Explore Feed", True, 
                                 f"Explore feed loaded: {len(posts)} posts, {total} total")
            else:
                results.add_result("Sohba Explore Feed", False, 
                                 f"Missing required fields in response: {data}")
        except json.JSONDecodeError:
            results.add_result("Sohba Explore Feed", False, 
                             "Invalid JSON response")
    else:
        results.add_result("Sohba Explore Feed", False, 
                         f"HTTP {response.status_code}: {response.text}")

def test_sohba_trending_users(results: TestResults, access_token: str):
    """Test GET /api/sohba/trending-users endpoint"""
    print("🔍 Testing sohba trending users...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"limit": 5}
    
    success, response, details = make_request("GET", "/sohba/trending-users", params, headers)
    
    if not success:
        results.add_result("Sohba Trending Users", False, details)
        return
        
    if response.status_code == 200:
        try:
            data = response.json()
            if "users" in data:
                users = data.get("users", [])
                if isinstance(users, list):
                    results.add_result("Sohba Trending Users", True, 
                                     f"Trending users loaded: {len(users)} users")
                else:
                    results.add_result("Sohba Trending Users", False, 
                                     f"Users field is not a list: {type(users)}")
            else:
                results.add_result("Sohba Trending Users", False, 
                                 f"Missing 'users' field in response: {data}")
        except json.JSONDecodeError:
            results.add_result("Sohba Trending Users", False, 
                             "Invalid JSON response")
    else:
        results.add_result("Sohba Trending Users", False, 
                         f"HTTP {response.status_code}: {response.text}")

def test_sohba_posts(results: TestResults, access_token: str):
    """Test GET /api/sohba/posts endpoint"""
    print("🔍 Testing existing sohba posts endpoint...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"category": "all", "limit": 5}
    
    success, response, details = make_request("GET", "/sohba/posts", params, headers)
    
    if not success:
        results.add_result("Sohba Posts (Existing)", False, details)
        return
        
    if response.status_code == 200:
        try:
            data = response.json()
            required_fields = ["posts", "total", "page", "has_more"]
            if all(field in data for field in required_fields):
                posts = data.get("posts", [])
                total = data.get("total", 0)
                results.add_result("Sohba Posts (Existing)", True, 
                                 f"Posts loaded: {len(posts)} posts, {total} total")
            else:
                results.add_result("Sohba Posts (Existing)", False, 
                                 f"Missing required fields in response: {data}")
        except json.JSONDecodeError:
            results.add_result("Sohba Posts (Existing)", False, 
                             "Invalid JSON response")
    else:
        results.add_result("Sohba Posts (Existing)", False, 
                         f"HTTP {response.status_code}: {response.text}")

def test_sohba_categories(results: TestResults):
    """Test GET /api/sohba/categories endpoint"""
    print("🔍 Testing existing sohba categories endpoint...")
    
    success, response, details = make_request("GET", "/sohba/categories")
    
    if not success:
        results.add_result("Sohba Categories (Existing)", False, details)
        return
        
    if response.status_code == 200:
        try:
            data = response.json()
            if "categories" in data:
                categories = data.get("categories", [])
                if isinstance(categories, list) and len(categories) > 0:
                    results.add_result("Sohba Categories (Existing)", True, 
                                     f"Categories loaded: {len(categories)} categories")
                else:
                    results.add_result("Sohba Categories (Existing)", False, 
                                     f"Categories field is empty or invalid: {categories}")
            else:
                results.add_result("Sohba Categories (Existing)", False, 
                                 f"Missing 'categories' field in response: {data}")
        except json.JSONDecodeError:
            results.add_result("Sohba Categories (Existing)", False, 
                             "Invalid JSON response")
    else:
        results.add_result("Sohba Categories (Existing)", False, 
                         f"HTTP {response.status_code}: {response.text}")

def main():
    """Run all backend API tests"""
    print(f"🕌 Islamic App Backend API Testing - NEW SEARCH & EXPLORE ENDPOINTS")
    print(f"Testing against: {BASE_URL}")
    print("="*80)
    
    results = TestResults()
    
    # Test basic endpoints first
    test_root_endpoint(results)
    
    # Test authentication flow - CRITICAL for search & explore endpoints
    access_token = test_user_registration(results)
    if not access_token:
        access_token = test_user_login(results)
    
    if access_token:
        test_auth_me(results, access_token)
        print("\n" + "="*50)
        print("🆕 TESTING NEW SEARCH & EXPLORE ENDPOINTS")
        print("="*50)
        
        # NEW SEARCH & EXPLORE ENDPOINTS (Primary Focus)
        test_sohba_search_arabic(results, access_token)
        test_sohba_search_users(results, access_token)
        test_sohba_explore(results, access_token)
        test_sohba_trending_users(results, access_token)
        
        print("\n" + "="*40)
        print("✅ TESTING EXISTING SOHBA ENDPOINTS")
        print("="*40)
        
        # EXISTING SOHBA ENDPOINTS (Verification)
        test_sohba_posts(results, access_token)
        test_sohba_categories(results)
        
    else:
        results.add_result("Auth System", False, 
                         "CRITICAL: No valid access token - cannot test authenticated endpoints")
        # Still test public endpoints
        test_sohba_categories(results)
    
    print("\n" + "="*40)
    print("🕌 TESTING EXISTING PRAYER/MOSQUE APIs")
    print("="*40)
    
    # Test existing prayer and mosque APIs
    test_prayer_times(results)
    test_mosque_search(results)
    test_mosque_prayer_times(results)
    
    # Print summary
    results.summary()
    
    # Special focus on new search endpoints
    print("🎯 NEW SEARCH & EXPLORE ENDPOINTS FOCUS:")
    search_tests = [r for r in results.results if 'Search' in r['test'] or 'Explore' in r['test'] or 'Trending' in r['test']]
    for test in search_tests:
        status = "✅" if test['success'] else "❌"
        print(f"  {status} {test['test']}")
    
    # Return exit code based on results
    return 0 if results.failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())