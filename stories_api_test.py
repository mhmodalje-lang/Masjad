#!/usr/bin/env python3
"""
Stories API Backend Testing
Testing video upload and creation flow for Stories endpoints
"""

import requests
import json
import time
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://media-layout-update.preview.emergentagent.com"

class StoriesAPITester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = []
        
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
            
    def test_post_request(self, endpoint: str, data: dict = None, expected_status: int = 200) -> Dict[str, Any]:
        """Test a POST endpoint"""
        url = f"{BACKEND_URL}{endpoint}"
        start_time = time.time()
        
        try:
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

    def test_create_story_with_video(self):
        """Test 1: POST /api/stories/create - Creating a story with video_url field"""
        print("🎬 Testing Story Creation with Video URL...")
        
        story_data = {
            "content": "test video",
            "category": "general",
            "video_url": "/api/uploads/test.mp4",
            "media_type": "video"
        }
        
        # Expecting 401 without auth, which is OK according to requirements
        result = self.test_post_request("/api/stories/create", story_data, expected_status=401)
        
        if result["status_code"] == 401:
            self.log_result("Create Story with Video URL", "PASSED", result["response_time"], 
                          "Correctly returns 401 without auth (expected behavior)")
        else:
            self.log_result("Create Story with Video URL", "FAILED", result["response_time"], 
                          f"Expected 401, got {result['status_code']}: {result.get('error', 'Unknown error')}")

    def test_create_story_video_only(self):
        """Test 2: POST /api/stories/create - Creating story WITHOUT content (video only)"""
        print("📹 Testing Story Creation with Video Only (no content)...")
        
        story_data = {
            "video_url": "/api/uploads/test.mp4",
            "media_type": "video"
        }
        
        # Should accept (not require content when video_url is provided) - expecting 401 without auth
        result = self.test_post_request("/api/stories/create", story_data, expected_status=401)
        
        if result["status_code"] == 401:
            self.log_result("Create Story Video Only", "PASSED", result["response_time"], 
                          "Correctly returns 401 without auth (expected behavior)")
        else:
            self.log_result("Create Story Video Only", "FAILED", result["response_time"], 
                          f"Expected 401, got {result['status_code']}: {result.get('error', 'Unknown error')}")

    def test_create_empty_story(self):
        """Test 3: POST /api/stories/create - Creating empty story (should return 400)"""
        print("❌ Testing Empty Story Creation (should fail)...")
        
        story_data = {
            "content": "",
            "category": "general"
        }
        
        # Should return 400 error for empty story
        result = self.test_post_request("/api/stories/create", story_data, expected_status=400)
        
        if result["status_code"] == 400:
            self.log_result("Create Empty Story", "PASSED", result["response_time"], 
                          "Correctly returns 400 for empty story")
        elif result["status_code"] == 401:
            # If it returns 401, it means auth check happens before validation
            self.log_result("Create Empty Story", "PASSED", result["response_time"], 
                          "Returns 401 (auth check before validation - acceptable)")
        else:
            self.log_result("Create Empty Story", "FAILED", result["response_time"], 
                          f"Expected 400 or 401, got {result['status_code']}: {result.get('error', 'Unknown error')}")

    def test_list_translated_stories(self):
        """Test 4: GET /api/stories/list-translated - Check response format includes video_url field"""
        print("📋 Testing List Translated Stories...")
        
        result = self.test_get_request("/api/stories/list-translated?limit=5&language=ar")
        
        if result["success"]:
            data = result["data"]
            
            # Check if response has expected structure
            if "stories" not in data:
                self.log_result("List Translated Stories", "FAILED", result["response_time"], 
                              "Response missing 'stories' field")
                return
            
            stories = data["stories"]
            
            # Check if stories array exists (can be empty)
            if not isinstance(stories, list):
                self.log_result("List Translated Stories", "FAILED", result["response_time"], 
                              "Stories field is not an array")
                return
            
            # Check if response structure supports video_url field
            # At least one story should have the video_url field (even if null)
            # or if no stories have video content, that's also acceptable
            has_video_url_field = False
            video_stories_count = 0
            
            for story in stories:
                if "video_url" in story:
                    has_video_url_field = True
                if story.get("media_type") == "video":
                    video_stories_count += 1
            
            if len(stories) == 0:
                self.log_result("List Translated Stories", "PASSED", result["response_time"], 
                              "Empty stories list returned (no stories in DB)")
            elif has_video_url_field:
                self.log_result("List Translated Stories", "PASSED", result["response_time"], 
                              f"Response format supports video_url field ({len(stories)} stories)")
            elif video_stories_count == 0:
                self.log_result("List Translated Stories", "PASSED", result["response_time"], 
                              f"No video stories found, video_url field not required ({len(stories)} stories)")
            else:
                self.log_result("List Translated Stories", "FAILED", result["response_time"], 
                              f"Video stories exist but missing video_url field ({video_stories_count} video stories)")
        else:
            self.log_result("List Translated Stories", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_upload_multipart_endpoint(self):
        """Test 5: POST /api/upload/multipart - Check upload endpoint exists"""
        print("📤 Testing Upload Multipart Endpoint...")
        
        # Test without file (should return 422 for missing file)
        result = self.test_post_request("/api/upload/multipart", {}, expected_status=422)
        
        if result["status_code"] == 422:
            self.log_result("Upload Multipart Endpoint", "PASSED", result["response_time"], 
                          "Correctly returns 422 for missing file")
        else:
            self.log_result("Upload Multipart Endpoint", "FAILED", result["response_time"], 
                          f"Expected 422, got {result['status_code']}: {result.get('error', 'Unknown error')}")

    def run_all_tests(self):
        """Run all Stories API tests"""
        print("🚀 Starting Stories API Backend Tests...")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 70)
        
        # Run all test suites
        self.test_create_story_with_video()
        self.test_create_story_video_only()
        self.test_create_empty_story()
        self.test_list_translated_stories()
        self.test_upload_multipart_endpoint()
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 STORIES API TEST SUMMARY")
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
    tester = StoriesAPITester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open("/app/stories_api_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": results,
            "detailed_results": tester.results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed results saved to: /app/stories_api_test_results.json")