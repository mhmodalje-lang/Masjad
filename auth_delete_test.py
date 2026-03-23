#!/usr/bin/env python3
"""
Auth Delete Account Endpoint Testing
Testing DELETE /api/auth/delete-account endpoint authentication and responses
"""

import requests
import json
import time
from typing import Dict, Any

# Backend URL from review request
BACKEND_URL = "https://multilang-app-fix.preview.emergentagent.com"

class AuthDeleteTester:
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
            
    def test_delete_request(self, endpoint: str, headers: dict = None, expected_status: int = 401) -> Dict[str, Any]:
        """Test a DELETE endpoint"""
        url = f"{BACKEND_URL}{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.delete(url, headers=headers or {}, timeout=15)
            response_time = time.time() - start_time
            
            result = {
                "success": response.status_code == expected_status,
                "status_code": response.status_code,
                "response_time": response_time,
                "response_text": response.text[:500] if response.text else "No response text"
            }
            
            if response.status_code != expected_status:
                result["error"] = f"Expected {expected_status}, got {response.status_code}"
            
            # Try to parse JSON response
            try:
                result["data"] = response.json()
            except json.JSONDecodeError:
                result["data"] = None
                
            return result
                
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return {
                "success": False,
                "status_code": 0,
                "response_time": response_time,
                "error": f"Request failed: {str(e)}"
            }

    def test_delete_account_no_auth(self):
        """Test DELETE /api/auth/delete-account without authentication token"""
        print("🔒 Testing DELETE /api/auth/delete-account without auth token...")
        
        result = self.test_delete_request("/api/auth/delete-account", expected_status=401)
        
        if result["success"]:
            # Check if response contains expected error message
            response_data = result.get("data")
            if response_data and "detail" in response_data:
                detail = response_data["detail"]
                if "غير مصادق" in detail or "unauthorized" in detail.lower() or "not authenticated" in detail.lower():
                    self.log_result("DELETE without auth token", "PASSED", result["response_time"], 
                                  f"Correctly returned 401 with message: {detail}")
                else:
                    self.log_result("DELETE without auth token", "PASSED", result["response_time"], 
                                  f"Correctly returned 401, message: {detail}")
            else:
                self.log_result("DELETE without auth token", "PASSED", result["response_time"], 
                              f"Correctly returned 401 status code")
        else:
            self.log_result("DELETE without auth token", "FAILED", result["response_time"], 
                          result.get("error", f"Expected 401, got {result['status_code']}"))

    def test_delete_account_invalid_auth(self):
        """Test DELETE /api/auth/delete-account with invalid authentication token"""
        print("🔐 Testing DELETE /api/auth/delete-account with invalid auth token...")
        
        # Use an invalid Bearer token
        headers = {
            "Authorization": "Bearer invalid_token_12345"
        }
        
        result = self.test_delete_request("/api/auth/delete-account", headers=headers, expected_status=401)
        
        if result["success"]:
            response_data = result.get("data")
            if response_data and "detail" in response_data:
                detail = response_data["detail"]
                self.log_result("DELETE with invalid token", "PASSED", result["response_time"], 
                              f"Correctly returned 401 with message: {detail}")
            else:
                self.log_result("DELETE with invalid token", "PASSED", result["response_time"], 
                              f"Correctly returned 401 status code")
        else:
            self.log_result("DELETE with invalid token", "FAILED", result["response_time"], 
                          result.get("error", f"Expected 401, got {result['status_code']}"))

    def test_delete_account_malformed_auth(self):
        """Test DELETE /api/auth/delete-account with malformed authentication header"""
        print("🔓 Testing DELETE /api/auth/delete-account with malformed auth header...")
        
        # Use a malformed Authorization header
        headers = {
            "Authorization": "InvalidFormat token123"
        }
        
        result = self.test_delete_request("/api/auth/delete-account", headers=headers, expected_status=401)
        
        if result["success"]:
            response_data = result.get("data")
            if response_data and "detail" in response_data:
                detail = response_data["detail"]
                self.log_result("DELETE with malformed auth", "PASSED", result["response_time"], 
                              f"Correctly returned 401 with message: {detail}")
            else:
                self.log_result("DELETE with malformed auth", "PASSED", result["response_time"], 
                              f"Correctly returned 401 status code")
        else:
            self.log_result("DELETE with malformed auth", "FAILED", result["response_time"], 
                          result.get("error", f"Expected 401, got {result['status_code']}"))

    def test_endpoint_exists(self):
        """Test that the DELETE /api/auth/delete-account endpoint exists (not 404)"""
        print("📍 Testing that DELETE /api/auth/delete-account endpoint exists...")
        
        result = self.test_delete_request("/api/auth/delete-account", expected_status=401)
        
        if result["status_code"] == 404:
            self.log_result("Endpoint existence", "FAILED", result["response_time"], 
                          "Endpoint not found (404) - endpoint does not exist")
        elif result["status_code"] == 405:
            self.log_result("Endpoint existence", "FAILED", result["response_time"], 
                          "Method not allowed (405) - DELETE method not supported")
        elif result["status_code"] == 401:
            self.log_result("Endpoint existence", "PASSED", result["response_time"], 
                          "Endpoint exists and correctly requires authentication")
        else:
            self.log_result("Endpoint existence", "PASSED", result["response_time"], 
                          f"Endpoint exists (status: {result['status_code']})")

    def run_all_tests(self):
        """Run all auth delete account tests"""
        print("🚀 Starting DELETE /api/auth/delete-account Endpoint Tests...")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 70)
        
        # Run all test suites
        self.test_endpoint_exists()
        self.test_delete_account_no_auth()
        self.test_delete_account_invalid_auth()
        self.test_delete_account_malformed_auth()
        
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
    tester = AuthDeleteTester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open("/app/auth_delete_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "endpoint": "DELETE /api/auth/delete-account",
            "backend_url": BACKEND_URL,
            "summary": results,
            "detailed_results": tester.results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed results saved to: /app/auth_delete_test_results.json")