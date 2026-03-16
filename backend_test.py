#!/usr/bin/env python3
"""
Backend API Test Suite for Islamic Social App (أذاني) - Review Request Testing
Testing specific endpoints mentioned in review request with exact test data.
"""

import requests
import json
import sys
import time
from typing import Optional, Dict, Any

# Backend URL from frontend .env configuration
BASE_URL = "https://viral-shorts-96.preview.emergentagent.com/api"

# Test data exactly as specified in review request
REGISTER_DATA = {
    "email": "testfinal@test.com",
    "password": "test123456", 
    "name": "مستخدم تجريبي"
}

UPDATE_PROFILE_DATA = {
    "name": "اسم جديد محدث",
    "avatar": "/api/uploads/test.jpg"
}

POST_DATA = {
    "content": "منشور تجريبي جديد",
    "category": "general"
}

COMMENT_DATA = {
    "content": "تعليق تجريبي"
}

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
        if headers is None:
            headers = {}
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            headers["Content-Type"] = "application/json"
            response = requests.post(url, json=data, headers=headers, timeout=timeout)
        elif method.upper() == "PUT":
            headers["Content-Type"] = "application/json"
            response = requests.put(url, json=data, headers=headers, timeout=timeout)
        else:
            return False, None, f"Unsupported HTTP method: {method}"
        
        # Parse response
        try:
            response_data = response.json()
        except:
            response_data = {"raw_response": response.text}
        
        success = 200 <= response.status_code < 300
        details = f"Status {response.status_code}"
        
        if not success:
            details += f": {response_data.get('detail', response.text[:100])}"
        
        return success, response_data, details
        
    except requests.exceptions.Timeout:
        return False, None, f"Request timeout after {timeout}s"
    except requests.exceptions.ConnectionError:
        return False, None, "Connection error"
    except Exception as e:
        return False, None, f"Request error: {str(e)}"

class ReviewRequestTester:
    """Test the specific endpoints from review request"""
    
    def __init__(self):
        self.auth_token = None
        self.user_data = None
        self.test_post_id = None
        self.results = TestResults()
    
    def test_register(self):
        """1. POST /api/auth/register - Register with Arabic name"""
        print("🔍 1. Testing user registration with Arabic name...")
        
        success, response, details = make_request("POST", "/auth/register", REGISTER_DATA)
        
        if success and response.get("access_token"):
            self.auth_token = response["access_token"]
            self.user_data = response.get("user", {})
            self.results.add_result("Register User", True, f"User registered: {self.user_data.get('name', 'Unknown')}")
            print(f"   ✅ Registered user: {self.user_data.get('name')}")
            print(f"   ✅ Got auth token: {self.auth_token[:20]}...")
        elif "البريد الإلكتروني مسجل مسبقاً" in str(response) or "email" in str(response):
            # User already exists, try to login instead
            self.results.add_result("Register User", True, "User already exists (proceeding to login)")
            print("   ℹ️ User already exists, will login instead")
        else:
            self.results.add_result("Register User", False, f"Registration failed: {details}")
            print(f"   ❌ Registration failed: {details}")
    
    def test_login(self):
        """2. POST /api/auth/login - Login with same credentials"""
        print("🔍 2. Testing user login...")
        
        login_data = {
            "email": REGISTER_DATA["email"],
            "password": REGISTER_DATA["password"]
        }
        
        success, response, details = make_request("POST", "/auth/login", login_data)
        
        if success and response.get("access_token"):
            self.auth_token = response["access_token"]
            self.user_data = response.get("user", {})
            self.results.add_result("Login User", True, f"Login successful: {self.user_data.get('name', 'Unknown')}")
            print(f"   ✅ Login successful: {self.user_data.get('name')}")
            print(f"   ✅ Got auth token: {self.auth_token[:20]}...")
        else:
            self.results.add_result("Login User", False, f"Login failed: {details}")
            print(f"   ❌ Login failed: {details}")
    
    def test_update_profile(self):
        """3. PUT /api/auth/update-profile - Update profile with Arabic name and avatar"""
        print("🔍 3. Testing profile update with Arabic name...")
        
        if not self.auth_token:
            self.results.add_result("Update Profile", False, "No auth token available")
            print("   ❌ No auth token available")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        success, response, details = make_request("PUT", "/auth/update-profile", UPDATE_PROFILE_DATA, headers)
        
        if success:
            self.results.add_result("Update Profile", True, "Profile updated successfully")
            print(f"   ✅ Profile updated successfully")
        else:
            self.results.add_result("Update Profile", False, f"Update failed: {details}")
            print(f"   ❌ Update failed: {details}")
    
    def test_create_post(self):
        """4. POST /api/sohba/posts - Create post with Arabic content"""
        print("🔍 4. Testing post creation with Arabic content...")
        
        if not self.auth_token:
            self.results.add_result("Create Post", False, "No auth token available")
            print("   ❌ No auth token available")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        success, response, details = make_request("POST", "/sohba/posts", POST_DATA, headers)
        
        if success and "post" in response:
            self.test_post_id = response["post"]["id"]
            self.results.add_result("Create Post", True, f"Post created with ID: {self.test_post_id}")
            print(f"   ✅ Post created with ID: {self.test_post_id}")
        else:
            self.results.add_result("Create Post", False, f"Post creation failed: {details}")
            print(f"   ❌ Post creation failed: {details}")
    
    def test_get_posts(self):
        """5. GET /api/sohba/posts?category=all&limit=10 - Get all posts"""
        print("🔍 5. Testing get all posts...")
        
        success, response, details = make_request("GET", "/sohba/posts?category=all&limit=10")
        
        if success and "posts" in response:
            posts_count = len(response["posts"])
            self.results.add_result("Get Posts", True, f"Retrieved {posts_count} posts")
            print(f"   ✅ Retrieved {posts_count} posts")
            
            # If we don't have a post ID for testing, use an existing one
            if not self.test_post_id and posts_count > 0:
                self.test_post_id = response["posts"][0]["id"]
                print(f"   ℹ️ Using existing post ID for testing: {self.test_post_id}")
        else:
            self.results.add_result("Get Posts", False, f"Get posts failed: {details}")
            print(f"   ❌ Get posts failed: {details}")
    
    def test_search(self):
        """6. GET /api/sohba/search?q=سبحان&type=all - Search Arabic text"""
        print("🔍 6. Testing search with Arabic text...")
        
        success, response, details = make_request("GET", "/sohba/search?q=سبحان&type=all")
        
        if success:
            posts_found = len(response.get("posts", []))
            users_found = len(response.get("users", []))
            total = response.get("total", 0)
            self.results.add_result("Search Posts", True, f"Search returned {posts_found} posts, {users_found} users (total: {total})")
            print(f"   ✅ Search returned {posts_found} posts, {users_found} users")
        else:
            self.results.add_result("Search Posts", False, f"Search failed: {details}")
            print(f"   ❌ Search failed: {details}")
    
    def test_explore(self):
        """7. GET /api/sohba/explore?limit=10 - Explore feed"""
        print("🔍 7. Testing explore feed...")
        
        success, response, details = make_request("GET", "/sohba/explore?limit=10")
        
        if success and "posts" in response:
            posts_count = len(response["posts"])
            total = response.get("total", 0)
            self.results.add_result("Explore Feed", True, f"Explore returned {posts_count} posts (total: {total})")
            print(f"   ✅ Explore returned {posts_count} posts")
        else:
            self.results.add_result("Explore Feed", False, f"Explore failed: {details}")
            print(f"   ❌ Explore failed: {details}")
    
    def test_like_post(self):
        """8. POST /api/sohba/posts/{post_id}/like - Like a post"""
        print("🔍 8. Testing post like...")
        
        if not self.auth_token:
            self.results.add_result("Like Post", False, "No auth token available")
            print("   ❌ No auth token available")
            return
            
        if not self.test_post_id:
            self.results.add_result("Like Post", False, "No post ID available for testing")
            print("   ❌ No post ID available for testing")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        success, response, details = make_request("POST", f"/sohba/posts/{self.test_post_id}/like", {}, headers)
        
        if success and "liked" in response:
            liked_status = response["liked"]
            self.results.add_result("Like Post", True, f"Post like toggled: {liked_status}")
            print(f"   ✅ Post like toggled: {liked_status}")
        else:
            self.results.add_result("Like Post", False, f"Like failed: {details}")
            print(f"   ❌ Like failed: {details}")
    
    def test_comment(self):
        """9. POST /api/sohba/posts/{post_id}/comments - Comment with Arabic text"""
        print("🔍 9. Testing comment with Arabic text...")
        
        if not self.auth_token:
            self.results.add_result("Comment Post", False, "No auth token available")
            print("   ❌ No auth token available")
            return
            
        if not self.test_post_id:
            self.results.add_result("Comment Post", False, "No post ID available for testing")
            print("   ❌ No post ID available for testing")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        success, response, details = make_request("POST", f"/sohba/posts/{self.test_post_id}/comments", COMMENT_DATA, headers)
        
        if success and "comment" in response:
            comment_id = response["comment"]["id"]
            self.results.add_result("Comment Post", True, f"Comment created: {comment_id}")
            print(f"   ✅ Comment created: {comment_id}")
        else:
            self.results.add_result("Comment Post", False, f"Comment failed: {details}")
            print(f"   ❌ Comment failed: {details}")
    
    def test_gifts_list(self):
        """10. GET /api/gifts/list - Get gifts list"""
        print("🔍 10. Testing gifts list...")
        
        success, response, details = make_request("GET", "/gifts/list")
        
        if success and "gifts" in response:
            gifts_count = len(response["gifts"])
            self.results.add_result("Get Gifts", True, f"Retrieved {gifts_count} gifts")
            print(f"   ✅ Retrieved {gifts_count} gifts")
            if gifts_count > 0:
                sample_gift = response["gifts"][0]
                print(f"   ✅ Sample gift: {sample_gift['name']} {sample_gift['emoji']} - {sample_gift['price_credits']} credits")
        else:
            self.results.add_result("Get Gifts", False, f"Get gifts failed: {details}")
            print(f"   ❌ Get gifts failed: {details}")
    
    def run_all_tests(self):
        """Run all tests in the exact order specified in review request"""
        print("🕌 Islamic App Backend API Testing - Review Request Endpoints")
        print(f"Testing against: {BASE_URL}")
        print("=" * 80)
        
        # Run tests in exact order from review request
        self.test_register()
        self.test_login()  
        self.test_update_profile()
        self.test_create_post()
        self.test_get_posts()
        self.test_search()
        self.test_explore()
        self.test_like_post()
        self.test_comment()
        self.test_gifts_list()
        
        # Show summary
        self.results.summary()
        
        # Check critical systems
        auth_passed = any(r['test'] in ['Register User', 'Login User'] and r['success'] for r in self.results.results)
        social_passed = any(r['test'] in ['Create Post', 'Get Posts', 'Like Post'] and r['success'] for r in self.results.results)
        
        print(f"🔑 Authentication System: {'✅ Working' if auth_passed else '❌ Failed'}")
        print(f"📱 Social Features: {'✅ Working' if social_passed else '❌ Failed'}")
        print(f"🎁 Gifts System: {'✅ Working' if any(r['test'] == 'Get Gifts' and r['success'] for r in self.results.results) else '❌ Failed'}")
        
        return self.results.failed == 0

def main():
    """Main test runner for review request endpoints"""
    tester = ReviewRequestTester()
    success = tester.run_all_tests()
    
    if success:
        print(f"\n🎉 All review request endpoints are working correctly!")
        sys.exit(0)
    else:
        print(f"\n⚠️ Some endpoints failed. Check details above.")
        sys.exit(1)

if __name__ == "__main__":
    main()