#!/usr/bin/env python3
"""
Instagram Reels-style Video Platform Backend API Testing
Tests the specific endpoints mentioned in the review request.
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend/.env
BACKEND_URL = "https://media-portal-164.preview.emergentagent.com"

def test_explore_endpoint():
    """Test GET /api/sohba/explore?limit=5 - Should return posts with engagement fields"""
    print("🧪 Testing GET /api/sohba/explore?limit=5...")
    
    url = f"{BACKEND_URL}/api/sohba/explore"
    params = {"limit": 5}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response keys: {list(data.keys())}")
            
            if "posts" in data and isinstance(data["posts"], list):
                posts = data["posts"]
                print(f"   Posts count: {len(posts)}")
                
                if posts:
                    first_post = posts[0]
                    print(f"   First post keys: {list(first_post.keys())}")
                    
                    # Check for required engagement fields
                    required_fields = ["likes_count", "comments_count", "shares_count", "saves_count", "liked", "saved"]
                    missing_fields = []
                    
                    for field in required_fields:
                        if field not in first_post:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        print(f"   ❌ FAIL: Missing required fields: {missing_fields}")
                        return False, None, None
                    else:
                        print("   ✅ PASS: All required engagement fields present")
                        # Return first post_id and user_id for other tests
                        post_id = first_post.get("id")
                        user_id = first_post.get("author_id")
                        return True, post_id, user_id
                else:
                    print("   ⚠️  WARNING: No posts returned, but endpoint works")
                    return True, None, None
            else:
                print("   ❌ FAIL: Response missing 'posts' array")
                return False, None, None
        else:
            print(f"   ❌ FAIL: Expected 200, got {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False, None, None
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False, None, None

def test_like_endpoint(post_id):
    """Test POST /api/sohba/posts/{post_id}/like - Should return 401 without auth"""
    print(f"🧪 Testing POST /api/sohba/posts/{post_id}/like...")
    
    url = f"{BACKEND_URL}/api/sohba/posts/{post_id}/like"
    
    try:
        response = requests.post(url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("   ✅ PASS: Correctly returns 401 without authentication")
            return True
        else:
            print(f"   ❌ FAIL: Expected 401, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_save_endpoint(post_id):
    """Test POST /api/sohba/posts/{post_id}/save - Should return 401 without auth"""
    print(f"🧪 Testing POST /api/sohba/posts/{post_id}/save...")
    
    url = f"{BACKEND_URL}/api/sohba/posts/{post_id}/save"
    
    try:
        response = requests.post(url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("   ✅ PASS: Correctly returns 401 without authentication")
            return True
        else:
            print(f"   ❌ FAIL: Expected 401, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_share_endpoint(post_id):
    """Test POST /api/sohba/posts/{post_id}/share - Should increment share count"""
    print(f"🧪 Testing POST /api/sohba/posts/{post_id}/share...")
    
    url = f"{BACKEND_URL}/api/sohba/posts/{post_id}/share"
    
    try:
        response = requests.post(url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            if "shared" in data and data["shared"]:
                print("   ✅ PASS: Share endpoint working correctly")
                return True
            else:
                print("   ❌ FAIL: Invalid response format")
                return False
        elif response.status_code == 404:
            print("   ❌ FAIL: Post not found")
            return False
        else:
            print(f"   ❌ FAIL: Expected 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_report_endpoint(post_id):
    """Test POST /api/sohba/posts/{post_id}/report - Should return 401 without auth"""
    print(f"🧪 Testing POST /api/sohba/posts/{post_id}/report...")
    
    url = f"{BACKEND_URL}/api/sohba/posts/{post_id}/report"
    payload = {"reason": "spam"}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("   ✅ PASS: Correctly returns 401 without authentication")
            return True
        else:
            print(f"   ❌ FAIL: Expected 401, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_not_interested_endpoint(post_id):
    """Test POST /api/sohba/posts/{post_id}/not-interested - Should return 401 without auth"""
    print(f"🧪 Testing POST /api/sohba/posts/{post_id}/not-interested...")
    
    url = f"{BACKEND_URL}/api/sohba/posts/{post_id}/not-interested"
    
    try:
        response = requests.post(url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("   ✅ PASS: Correctly returns 401 without authentication")
            return True
        else:
            print(f"   ❌ FAIL: Expected 401, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_view_endpoint(post_id):
    """Test POST /api/sohba/posts/{post_id}/view - Should track view count"""
    print(f"🧪 Testing POST /api/sohba/posts/{post_id}/view...")
    
    url = f"{BACKEND_URL}/api/sohba/posts/{post_id}/view"
    
    try:
        response = requests.post(url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            if "viewed" in data and data["viewed"]:
                print("   ✅ PASS: View tracking endpoint working correctly")
                return True
            else:
                print("   ❌ FAIL: Invalid response format")
                return False
        elif response.status_code == 404:
            print("   ❌ FAIL: Post not found")
            return False
        else:
            print(f"   ❌ FAIL: Expected 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_follow_endpoint(user_id):
    """Test POST /api/sohba/follow/{user_id} - Should return 401 without auth"""
    print(f"🧪 Testing POST /api/sohba/follow/{user_id}...")
    
    url = f"{BACKEND_URL}/api/sohba/follow/{user_id}"
    
    try:
        response = requests.post(url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("   ✅ PASS: Correctly returns 401 without authentication")
            return True
        else:
            print(f"   ❌ FAIL: Expected 401, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_comments_endpoint(post_id):
    """Test GET /api/sohba/posts/{post_id}/comments - Should get comments for a post"""
    print(f"🧪 Testing GET /api/sohba/posts/{post_id}/comments...")
    
    url = f"{BACKEND_URL}/api/sohba/posts/{post_id}/comments"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response keys: {list(data.keys())}")
            
            if "comments" in data and isinstance(data["comments"], list):
                comments = data["comments"]
                print(f"   Comments count: {len(comments)}")
                print("   ✅ PASS: Comments endpoint working correctly")
                return True
            else:
                print("   ❌ FAIL: Response missing 'comments' array")
                return False
        else:
            print(f"   ❌ FAIL: Expected 200, got {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_trending_users_endpoint():
    """Test GET /api/sohba/trending-users?limit=12 - Should get trending users for share sheet"""
    print("🧪 Testing GET /api/sohba/trending-users?limit=12...")
    
    url = f"{BACKEND_URL}/api/sohba/trending-users"
    params = {"limit": 12}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response keys: {list(data.keys())}")
            
            if "users" in data and isinstance(data["users"], list):
                users = data["users"]
                print(f"   Users count: {len(users)}")
                
                if users:
                    first_user = users[0]
                    print(f"   First user keys: {list(first_user.keys())}")
                    
                    # Check for required user fields
                    required_fields = ["id", "name", "followers_count"]
                    missing_fields = []
                    
                    for field in required_fields:
                        if field not in first_user:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        print(f"   ❌ FAIL: Missing required user fields: {missing_fields}")
                        return False
                    else:
                        print("   ✅ PASS: Trending users endpoint working correctly")
                        return True
                else:
                    print("   ⚠️  WARNING: No users returned, but endpoint works")
                    return True
            else:
                print("   ❌ FAIL: Response missing 'users' array")
                return False
        else:
            print(f"   ❌ FAIL: Expected 200, got {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def main():
    """Run all Instagram Reels-style backend API tests"""
    print("🚀 Starting Instagram Reels-style Backend API Tests")
    print(f"📍 Backend URL: {BACKEND_URL}")
    print("=" * 60)
    
    # Test 1: Get explore feed and extract post_id and user_id
    print(f"\n📋 Test 1: Explore Feed")
    print("-" * 40)
    success, post_id, user_id = test_explore_endpoint()
    
    if not success:
        print("❌ CRITICAL: Explore endpoint failed - cannot continue with other tests")
        return 1
    
    if not post_id or not user_id:
        print("⚠️  WARNING: No posts found in explore feed - some tests will be skipped")
        post_id = "dummy_post_id"  # Use dummy ID to test auth behavior
        user_id = "dummy_user_id"
    
    # Run all other tests
    tests = [
        ("Like Post (Auth Required)", lambda: test_like_endpoint(post_id)),
        ("Save Post (Auth Required)", lambda: test_save_endpoint(post_id)),
        ("Share Post", lambda: test_share_endpoint(post_id)),
        ("Report Post (Auth Required)", lambda: test_report_endpoint(post_id)),
        ("Not Interested (Auth Required)", lambda: test_not_interested_endpoint(post_id)),
        ("Track View", lambda: test_view_endpoint(post_id)),
        ("Follow User (Auth Required)", lambda: test_follow_endpoint(user_id)),
        ("Get Comments", lambda: test_comments_endpoint(post_id)),
        ("Trending Users", test_trending_users_endpoint),
    ]
    
    results = [("Explore Feed", success)]
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        success = test_func()
        results.append((test_name, success))
        print()
    
    # Summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Instagram Reels-style API tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed - check details above")
        return 1

if __name__ == "__main__":
    sys.exit(main())