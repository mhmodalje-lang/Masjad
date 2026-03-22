#!/usr/bin/env python3
"""
TikTok-Style Stories Backend API Testing
Testing the new TikTok-style Stories page API endpoints
"""

import requests
import json
import time
import uuid
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://video-hub-pro-4.preview.emergentagent.com"

class TikTokStoriesAPITester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = []
        self.test_post_id = None  # Will be set when we find a post
        
    def log_result(self, test_name: str, status: str, response_time: float, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "response_time": f"{response_time:.3f}s",
            "details": details
        }
        self.results.append(result)
        self.total_tests += 1
        if status == "PASSED":
            self.passed_tests += 1
        else:
            self.failed_tests.append(result)
            
    def test_get_request(self, endpoint: str, expected_status: int = 200) -> Dict[str, Any]:
        """Test a GET endpoint"""
        url = f"{BACKEND_URL}{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code != expected_status:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "error": f"Expected {expected_status}, got {response.status_code}",
                    "response_text": response.text[:500] if response.text else "No response text"
                }
                
            try:
                data = response.json()
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "data": data
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "error": "Invalid JSON response",
                    "response_text": response.text[:500]
                }
                
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return {
                "success": False,
                "status_code": 0,
                "response_time": response_time,
                "error": f"Request failed: {str(e)}"
            }

    def test_post_request(self, endpoint: str, data: dict = None, expected_status: int = 200, headers: dict = None) -> Dict[str, Any]:
        """Test a POST endpoint"""
        url = f"{BACKEND_URL}{endpoint}"
        start_time = time.time()
        
        try:
            if headers is None:
                headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=data, headers=headers, timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code != expected_status:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "error": f"Expected {expected_status}, got {response.status_code}",
                    "response_text": response.text[:500] if response.text else "No response text"
                }
                
            try:
                response_data = response.json()
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "data": response_data
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "error": "Invalid JSON response",
                    "response_text": response.text[:500]
                }
                
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return {
                "success": False,
                "status_code": 0,
                "response_time": response_time,
                "error": f"Request failed: {str(e)}"
            }

    def test_api_health(self):
        """Test basic API health"""
        print("🏥 Testing API Health...")
        
        result = self.test_get_request("/api/health")
        
        if result["success"]:
            data = result["data"]
            if data.get("status") == "healthy":
                self.log_result("API Health Check", "PASSED", result["response_time"], 
                              f"Status: {data.get('status')}")
            else:
                self.log_result("API Health Check", "FAILED", result["response_time"], 
                              f"Unhealthy status: {data.get('status')}")
        else:
            self.log_result("API Health Check", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_sohba_explore_feed(self):
        """Test GET /api/sohba/explore?limit=10 - Should return posts array for 'For You' feed"""
        print("🔍 Testing Sohba Explore Feed...")
        
        result = self.test_get_request("/api/sohba/explore?limit=10")
        
        if result["success"]:
            data = result["data"]
            
            # Check if response has posts array
            if "posts" not in data:
                self.log_result("Sohba Explore Feed", "FAILED", result["response_time"], 
                              "Response missing 'posts' array")
                return
            
            posts = data["posts"]
            
            # Check if posts is a list
            if not isinstance(posts, list):
                self.log_result("Sohba Explore Feed", "FAILED", result["response_time"], 
                              f"'posts' should be array, got {type(posts)}")
                return
            
            # Check if we have posts and store first post ID for later tests
            if len(posts) > 0:
                self.test_post_id = posts[0].get("id")
                
                # Verify post structure
                first_post = posts[0]
                required_fields = ["id", "author_id", "content", "created_at"]
                missing_fields = [field for field in required_fields if field not in first_post]
                
                if missing_fields:
                    self.log_result("Sohba Explore Feed", "FAILED", result["response_time"], 
                                  f"Post missing fields: {', '.join(missing_fields)}")
                    return
                
                self.log_result("Sohba Explore Feed", "PASSED", result["response_time"], 
                              f"Returned {len(posts)} posts with proper structure")
            else:
                self.log_result("Sohba Explore Feed", "PASSED", result["response_time"], 
                              "Returned empty posts array (no content yet)")
            
        else:
            self.log_result("Sohba Explore Feed", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_sohba_following_feed_unauthorized(self):
        """Test GET /api/sohba/feed/following?limit=10 - Should return 401 (needs auth)"""
        print("👥 Testing Sohba Following Feed (Unauthorized)...")
        
        result = self.test_get_request("/api/sohba/feed/following?limit=10", expected_status=401)
        
        if result["success"]:
            self.log_result("Sohba Following Feed (401)", "PASSED", result["response_time"], 
                          "Correctly returned 401 Unauthorized")
        else:
            if result["status_code"] == 401:
                self.log_result("Sohba Following Feed (401)", "PASSED", result["response_time"], 
                              "Correctly returned 401 Unauthorized")
            else:
                self.log_result("Sohba Following Feed (401)", "FAILED", result["response_time"], 
                              f"Expected 401, got {result['status_code']}: {result.get('error', 'Unknown error')}")

    def test_stories_categories(self):
        """Test GET /api/stories/categories - Should return categories array"""
        print("📚 Testing Stories Categories...")
        
        result = self.test_get_request("/api/stories/categories")
        
        if result["success"]:
            data = result["data"]
            
            # Check if response has categories array
            if "categories" not in data:
                self.log_result("Stories Categories", "FAILED", result["response_time"], 
                              "Response missing 'categories' array")
                return
            
            categories = data["categories"]
            
            # Check if categories is a list
            if not isinstance(categories, list):
                self.log_result("Stories Categories", "FAILED", result["response_time"], 
                              f"'categories' should be array, got {type(categories)}")
                return
            
            # Check if we have categories
            if len(categories) > 0:
                # Verify category structure
                first_category = categories[0]
                required_fields = ["key", "label", "emoji"]
                missing_fields = [field for field in required_fields if field not in first_category]
                
                if missing_fields:
                    self.log_result("Stories Categories", "FAILED", result["response_time"], 
                                  f"Category missing fields: {', '.join(missing_fields)}")
                    return
                
                self.log_result("Stories Categories", "PASSED", result["response_time"], 
                              f"Returned {len(categories)} categories with proper structure")
            else:
                self.log_result("Stories Categories", "FAILED", result["response_time"], 
                              "Returned empty categories array")
            
        else:
            self.log_result("Stories Categories", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_post_like_unauthorized(self):
        """Test POST /api/sohba/posts/{id}/like - Should return 401 (needs auth)"""
        print("❤️ Testing Post Like (Unauthorized)...")
        
        # Use test post ID if available, otherwise use a dummy ID
        post_id = self.test_post_id or "dummy-post-id"
        
        result = self.test_post_request(f"/api/sohba/posts/{post_id}/like", expected_status=401)
        
        if result["success"]:
            self.log_result("Post Like (401)", "PASSED", result["response_time"], 
                          "Correctly returned 401 Unauthorized")
        else:
            if result["status_code"] == 401:
                self.log_result("Post Like (401)", "PASSED", result["response_time"], 
                              "Correctly returned 401 Unauthorized")
            else:
                self.log_result("Post Like (401)", "FAILED", result["response_time"], 
                              f"Expected 401, got {result['status_code']}: {result.get('error', 'Unknown error')}")

    def test_post_save_unauthorized(self):
        """Test POST /api/sohba/posts/{id}/save - Should return 401 (needs auth)"""
        print("🔖 Testing Post Save (Unauthorized)...")
        
        # Use test post ID if available, otherwise use a dummy ID
        post_id = self.test_post_id or "dummy-post-id"
        
        result = self.test_post_request(f"/api/sohba/posts/{post_id}/save", expected_status=401)
        
        if result["success"]:
            self.log_result("Post Save (401)", "PASSED", result["response_time"], 
                          "Correctly returned 401 Unauthorized")
        else:
            if result["status_code"] == 401:
                self.log_result("Post Save (401)", "PASSED", result["response_time"], 
                              "Correctly returned 401 Unauthorized")
            else:
                self.log_result("Post Save (401)", "FAILED", result["response_time"], 
                              f"Expected 401, got {result['status_code']}: {result.get('error', 'Unknown error')}")

    def test_post_share(self):
        """Test POST /api/sohba/posts/{id}/share - Test share count increment"""
        print("📤 Testing Post Share...")
        
        # Use test post ID if available, otherwise use a dummy ID
        post_id = self.test_post_id or "dummy-post-id"
        
        result = self.test_post_request(f"/api/sohba/posts/{post_id}/share")
        
        if result["success"]:
            data = result["data"]
            
            # Check if response indicates successful share
            if data.get("shared") is True:
                self.log_result("Post Share", "PASSED", result["response_time"], 
                              "Successfully incremented share count")
            else:
                self.log_result("Post Share", "FAILED", result["response_time"], 
                              f"Share response: {data}")
        else:
            if result["status_code"] == 404:
                self.log_result("Post Share", "PASSED", result["response_time"], 
                              "Post not found (expected with dummy ID)")
            else:
                self.log_result("Post Share", "FAILED", result["response_time"], 
                              result.get("error", "Unknown error"))

    def test_post_comments(self):
        """Test GET /api/sohba/posts/{id}/comments - Get comments for a post"""
        print("💬 Testing Post Comments...")
        
        # Use test post ID if available, otherwise use a dummy ID
        post_id = self.test_post_id or "dummy-post-id"
        
        result = self.test_get_request(f"/api/sohba/posts/{post_id}/comments")
        
        if result["success"]:
            data = result["data"]
            
            # Check if response has comments array
            if "comments" not in data:
                self.log_result("Post Comments", "FAILED", result["response_time"], 
                              "Response missing 'comments' array")
                return
            
            comments = data["comments"]
            
            # Check if comments is a list
            if not isinstance(comments, list):
                self.log_result("Post Comments", "FAILED", result["response_time"], 
                              f"'comments' should be array, got {type(comments)}")
                return
            
            self.log_result("Post Comments", "PASSED", result["response_time"], 
                          f"Returned {len(comments)} comments")
            
        else:
            if result["status_code"] == 404:
                self.log_result("Post Comments", "PASSED", result["response_time"], 
                              "Post not found (expected with dummy ID)")
            else:
                self.log_result("Post Comments", "FAILED", result["response_time"], 
                              result.get("error", "Unknown error"))

    def test_follow_user_unauthorized(self):
        """Test POST /api/sohba/follow/{target_id} - Should return 401 (needs auth)"""
        print("👤 Testing Follow User (Unauthorized)...")
        
        # Use a dummy target ID
        target_id = "dummy-user-id"
        
        result = self.test_post_request(f"/api/sohba/follow/{target_id}", expected_status=401)
        
        if result["success"]:
            self.log_result("Follow User (401)", "PASSED", result["response_time"], 
                          "Correctly returned 401 Unauthorized")
        else:
            if result["status_code"] == 401:
                self.log_result("Follow User (401)", "PASSED", result["response_time"], 
                              "Correctly returned 401 Unauthorized")
            else:
                self.log_result("Follow User (401)", "FAILED", result["response_time"], 
                              f"Expected 401, got {result['status_code']}: {result.get('error', 'Unknown error')}")

    def test_upload_multipart_endpoint(self):
        """Test POST /api/upload/multipart - Upload endpoint exists"""
        print("📁 Testing Upload Multipart Endpoint...")
        
        # Test with empty request to see if endpoint exists
        result = self.test_post_request("/api/upload/multipart", expected_status=422)  # Expect validation error
        
        if result["success"] or result["status_code"] == 422:
            # 422 means endpoint exists but validation failed (expected)
            self.log_result("Upload Multipart Endpoint", "PASSED", result["response_time"], 
                          "Endpoint exists (422 validation error expected)")
        else:
            if result["status_code"] == 404:
                self.log_result("Upload Multipart Endpoint", "FAILED", result["response_time"], 
                              "Endpoint not found (404)")
            else:
                self.log_result("Upload Multipart Endpoint", "FAILED", result["response_time"], 
                              result.get("error", "Unknown error"))

    def test_stories_create_unauthorized(self):
        """Test POST /api/stories/create - Should return 401 (needs auth)"""
        print("✍️ Testing Stories Create (Unauthorized)...")
        
        story_data = {
            "content": "Test story content",
            "category": "general"
        }
        
        result = self.test_post_request("/api/stories/create", story_data, expected_status=401)
        
        if result["success"]:
            self.log_result("Stories Create (401)", "PASSED", result["response_time"], 
                          "Correctly returned 401 Unauthorized")
        else:
            if result["status_code"] == 401:
                self.log_result("Stories Create (401)", "PASSED", result["response_time"], 
                              "Correctly returned 401 Unauthorized")
            else:
                self.log_result("Stories Create (401)", "FAILED", result["response_time"], 
                              f"Expected 401, got {result['status_code']}: {result.get('error', 'Unknown error')}")

    def run_all_tests(self):
        """Run all TikTok Stories API tests"""
        print("🚀 Starting TikTok-Style Stories Backend API Tests...")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 70)
        
        # Run all test suites
        self.test_api_health()
        self.test_sohba_explore_feed()
        self.test_sohba_following_feed_unauthorized()
        self.test_stories_categories()
        self.test_post_like_unauthorized()
        self.test_post_save_unauthorized()
        self.test_post_share()
        self.test_post_comments()
        self.test_follow_user_unauthorized()
        self.test_upload_multipart_endpoint()
        self.test_stories_create_unauthorized()
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in self.failed_tests:
                print(f"  • {test['test']}: {test['details']}")
        
        print("\n✅ PASSED TESTS:")
        for result in self.results:
            if result["status"] == "PASSED":
                print(f"  • {result['test']}: {result['details']}")
        
        return {
            "total": self.total_tests,
            "passed": self.passed_tests,
            "failed": self.total_tests - self.passed_tests,
            "success_rate": self.passed_tests/self.total_tests*100 if self.total_tests > 0 else 0,
            "failed_tests": self.failed_tests
        }

if __name__ == "__main__":
    tester = TikTokStoriesAPITester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open("/app/tiktok_stories_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": results,
            "detailed_results": tester.results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed results saved to: /app/tiktok_stories_test_results.json")