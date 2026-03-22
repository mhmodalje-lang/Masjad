#!/usr/bin/env python3
"""
Backend API Testing for Redesigned Frontend
Testing specific endpoints used by the redesigned video/content platform
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

# Backend URL from frontend/.env
BACKEND_URL = "https://video-hub-pro-4.preview.emergentagent.com"

class BackendTester:
    def __init__(self):
        self.session = None
        self.results = []
        self.auth_token = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_result(self, endpoint: str, status: str, details: str, response_data: Any = None):
        """Log test result"""
        result = {
            "endpoint": endpoint,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.results.append(result)
        
        # Print result
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {endpoint}: {details}")
        
    async def test_endpoint(self, method: str, endpoint: str, expected_keys: List[str], 
                          headers: Optional[Dict] = None, params: Optional[Dict] = None) -> bool:
        """Test a single endpoint"""
        url = f"{BACKEND_URL}{endpoint}"
        
        try:
            async with self.session.request(method, url, headers=headers, params=params) as response:
                status_code = response.status
                
                if status_code != 200:
                    self.log_result(endpoint, "FAIL", f"Status code: {status_code}")
                    return False
                
                try:
                    data = await response.json()
                except Exception as e:
                    self.log_result(endpoint, "FAIL", f"Invalid JSON response: {e}")
                    return False
                
                # Check for expected keys in response
                missing_keys = []
                for key in expected_keys:
                    if key not in data:
                        missing_keys.append(key)
                
                if missing_keys:
                    self.log_result(endpoint, "FAIL", f"Missing keys: {missing_keys}", data)
                    return False
                
                # Additional validation based on endpoint
                validation_result = self.validate_response_content(endpoint, data)
                if not validation_result["valid"]:
                    self.log_result(endpoint, "FAIL", validation_result["message"], data)
                    return False
                
                self.log_result(endpoint, "PASS", f"Status: {status_code}, Response valid", data)
                return True
                
        except Exception as e:
            self.log_result(endpoint, "FAIL", f"Request failed: {e}")
            return False
    
    def validate_response_content(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        """Validate response content based on endpoint"""
        
        if "/sohba/explore" in endpoint:
            if "posts" not in data or not isinstance(data["posts"], list):
                return {"valid": False, "message": "posts should be an array"}
            return {"valid": True, "message": f"Found {len(data['posts'])} posts"}
            
        elif "/sohba/feed/videos" in endpoint:
            if "posts" not in data or not isinstance(data["posts"], list):
                return {"valid": False, "message": "posts should be an array"}
            return {"valid": True, "message": f"Found {len(data['posts'])} video posts"}
            
        elif "/stories/categories" in endpoint:
            if "categories" not in data or not isinstance(data["categories"], list):
                return {"valid": False, "message": "categories should be an array"}
            return {"valid": True, "message": f"Found {len(data['categories'])} categories"}
            
        elif "/stories/list-translated" in endpoint:
            if "stories" not in data or not isinstance(data["stories"], list):
                return {"valid": False, "message": "stories should be an array"}
            return {"valid": True, "message": f"Found {len(data['stories'])} stories"}
            
        elif "/sohba/recommended-users" in endpoint:
            if "users" not in data or not isinstance(data["users"], list):
                return {"valid": False, "message": "users should be an array"}
            return {"valid": True, "message": f"Found {len(data['users'])} recommended users"}
            
        elif "/sohba/feed/following" in endpoint:
            if "posts" not in data or not isinstance(data["posts"], list):
                return {"valid": False, "message": "posts should be an array"}
            return {"valid": True, "message": f"Found {len(data['posts'])} following posts"}
        
        return {"valid": True, "message": "Response structure valid"}
    
    async def test_health_endpoint(self):
        """Test basic health endpoint first"""
        print("\n🔍 Testing Backend Health...")
        await self.test_endpoint("GET", "/api/health", ["status"])
    
    async def test_redesign_endpoints(self):
        """Test all endpoints used by the redesigned frontend"""
        
        print("\n🎯 Testing Redesigned Frontend API Endpoints...")
        
        # Test endpoints that don't require authentication
        endpoints_no_auth = [
            {
                "endpoint": "/api/sohba/explore",
                "params": {"limit": 5},
                "expected_keys": ["posts"]
            },
            {
                "endpoint": "/api/sohba/feed/videos", 
                "params": {"limit": 5},
                "expected_keys": ["posts"]
            },
            {
                "endpoint": "/api/stories/categories",
                "params": None,
                "expected_keys": ["categories"]
            },
            {
                "endpoint": "/api/stories/list-translated",
                "params": {"limit": 5, "language": "ar"},
                "expected_keys": ["stories"]
            },
            {
                "endpoint": "/api/sohba/recommended-users",
                "params": {"limit": 5},
                "expected_keys": ["users"]
            }
        ]
        
        # Test endpoints without auth
        for test_case in endpoints_no_auth:
            await self.test_endpoint(
                "GET", 
                test_case["endpoint"], 
                test_case["expected_keys"],
                params=test_case["params"]
            )
        
        # Test endpoint that requires auth (expect 401 without auth)
        print("\n🔐 Testing Authentication-Required Endpoints...")
        await self.test_auth_required_endpoint("/api/sohba/feed/following", {"limit": 5})
    
    async def test_auth_required_endpoint(self, endpoint: str, params: Optional[Dict] = None):
        """Test endpoint that requires authentication - expect 401 without auth"""
        url = f"{BACKEND_URL}{endpoint}"
        
        try:
            async with self.session.request("GET", url, params=params) as response:
                status_code = response.status
                
                if status_code == 401:
                    self.log_result(endpoint, "PASS", "Correctly requires authentication (401)")
                    return True
                elif status_code == 200:
                    # If it returns 200, check if it has the expected structure
                    try:
                        data = await response.json()
                        if "posts" in data and isinstance(data["posts"], list):
                            self.log_result(endpoint, "PASS", f"Status: {status_code}, Response valid (works without auth)")
                            return True
                        else:
                            self.log_result(endpoint, "FAIL", f"Status: {status_code}, Invalid response structure")
                            return False
                    except Exception as e:
                        self.log_result(endpoint, "FAIL", f"Status: {status_code}, Invalid JSON: {e}")
                        return False
                else:
                    self.log_result(endpoint, "FAIL", f"Unexpected status code: {status_code}")
                    return False
                
        except Exception as e:
            self.log_result(endpoint, "FAIL", f"Request failed: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Backend API Tests for Redesigned Frontend")
        print(f"🌐 Backend URL: {BACKEND_URL}")
        print("=" * 60)
        
        # Test health first
        await self.test_health_endpoint()
        
        # Test redesign endpoints
        await self.test_redesign_endpoints()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.results if r["status"] == "FAIL"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"  • {result['endpoint']}: {result['details']}")
        
        print("\n" + "=" * 60)
        
        # Save detailed results
        with open("/app/backend_test_redesign_results.json", "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        print("📄 Detailed results saved to: backend_test_redesign_results.json")

async def main():
    """Main test runner"""
    async with BackendTester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())