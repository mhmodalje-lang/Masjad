#!/usr/bin/env python3
"""
Backend API Testing Script - Review Request Specific
Test the backend API endpoints to verify the app is still working correctly after massive frontend translation changes.

Base URL: https://multilang-sync-3.preview.emergentagent.com

Test these endpoints:
1. GET /api/health - Should return 200
2. GET /api/quran/v4/chapters?language=ar - Should return 200 with Arabic chapters
3. GET /api/quran/v4/chapters?language=tr - Should return 200 with Turkish chapters  
4. GET /api/kids-learn/daily-games?locale=tr - Should return 200
5. GET /api/sohba/posts - Should return 200
6. GET /api/mosque-prayer-times/nearby?lat=48.8566&lng=2.3522 - Should return 200 (Paris mosque times)
7. GET /api/zakat/gold-price?currency=TRY - Should return 200
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, Any, List

# Base URL from frontend/.env
BASE_URL = "https://multilang-sync-3.preview.emergentagent.com"

class BackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    async def test_endpoint(self, method: str, endpoint: str, expected_status: int = 200, 
                          description: str = "", params: Dict = None, headers: Dict = None) -> Dict[str, Any]:
        """Test a single endpoint and return results"""
        self.total_tests += 1
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method.upper() == "GET":
                    response = await client.get(url, params=params, headers=headers)
                elif method.upper() == "POST":
                    response = await client.post(url, json=params, headers=headers)
                else:
                    response = await client.request(method, url, params=params, headers=headers)
                
                # Check status code
                status_ok = response.status_code == expected_status
                if status_ok:
                    self.passed_tests += 1
                
                # Try to parse JSON response
                try:
                    response_data = response.json()
                    data_preview = str(response_data)[:200] + "..." if len(str(response_data)) > 200 else str(response_data)
                except:
                    response_data = response.text
                    data_preview = response_data[:200] + "..." if len(response_data) > 200 else response_data
                
                result = {
                    "endpoint": endpoint,
                    "method": method.upper(),
                    "description": description,
                    "url": url,
                    "status_code": response.status_code,
                    "expected_status": expected_status,
                    "passed": status_ok,
                    "response_preview": data_preview,
                    "response_size": len(str(response_data)),
                    "headers": dict(response.headers),
                    "params": params or {}
                }
                
                # Additional validation for specific endpoints
                if status_ok and response.status_code == 200:
                    result["validation"] = self._validate_response(endpoint, response_data)
                
                self.results.append(result)
                return result
                
        except Exception as e:
            result = {
                "endpoint": endpoint,
                "method": method.upper(),
                "description": description,
                "url": url,
                "status_code": 0,
                "expected_status": expected_status,
                "passed": False,
                "error": str(e),
                "response_preview": f"ERROR: {str(e)}",
                "response_size": 0,
                "headers": {},
                "params": params or {}
            }
            self.results.append(result)
            return result
    
    def _validate_response(self, endpoint: str, data: Any) -> Dict[str, Any]:
        """Validate response data for specific endpoints"""
        validation = {"valid": True, "issues": []}
        
        try:
            if "/health" in endpoint:
                if isinstance(data, dict):
                    if "status" not in data:
                        validation["issues"].append("Missing 'status' field")
                    elif data.get("status") != "healthy":
                        validation["issues"].append(f"Status is '{data.get('status')}', expected 'healthy'")
                else:
                    validation["issues"].append("Response is not a JSON object")
            
            elif "/quran/v4/chapters" in endpoint:
                if isinstance(data, dict):
                    if "chapters" not in data:
                        validation["issues"].append("Missing 'chapters' field")
                    else:
                        chapters = data.get("chapters", [])
                        if not isinstance(chapters, list):
                            validation["issues"].append("'chapters' is not a list")
                        elif len(chapters) == 0:
                            validation["issues"].append("No chapters returned")
                        elif len(chapters) != 114:
                            validation["issues"].append(f"Expected 114 chapters, got {len(chapters)}")
                else:
                    validation["issues"].append("Response is not a JSON object")
            
            elif "/kids-learn/daily-games" in endpoint:
                if isinstance(data, dict):
                    if "success" not in data:
                        validation["issues"].append("Missing 'success' field")
                    elif not data.get("success"):
                        validation["issues"].append("Success is False")
                    if "games" not in data:
                        validation["issues"].append("Missing 'games' field")
                else:
                    validation["issues"].append("Response is not a JSON object")
            
            elif "/sohba/posts" in endpoint:
                if isinstance(data, dict):
                    if "posts" not in data:
                        validation["issues"].append("Missing 'posts' field")
                    else:
                        posts = data.get("posts", [])
                        if not isinstance(posts, list):
                            validation["issues"].append("'posts' is not a list")
                else:
                    validation["issues"].append("Response is not a JSON object")
            
            elif "/mosque-prayer-times/nearby" in endpoint or "/mosques/search" in endpoint:
                if isinstance(data, dict):
                    if "mosques" not in data:
                        validation["issues"].append("Missing 'mosques' field")
                    else:
                        mosques = data.get("mosques", [])
                        if not isinstance(mosques, list):
                            validation["issues"].append("'mosques' is not a list")
                else:
                    validation["issues"].append("Response is not a JSON object")
            
            elif "/zakat/gold-price" in endpoint:
                if isinstance(data, dict):
                    if "price" not in data and "gold_price" not in data:
                        validation["issues"].append("Missing price field")
                else:
                    validation["issues"].append("Response is not a JSON object")
            
            validation["valid"] = len(validation["issues"]) == 0
            
        except Exception as e:
            validation["valid"] = False
            validation["issues"].append(f"Validation error: {str(e)}")
        
        return validation
    
    async def run_review_request_tests(self):
        """Run all the tests specified in the review request"""
        print("🚀 Starting Backend API Testing - Review Request Specific")
        print(f"📍 Base URL: {self.base_url}")
        print(f"⏰ Test Time: {datetime.now().isoformat()}")
        print("=" * 80)
        
        # Test 1: Health Check
        await self.test_endpoint(
            "GET", "/api/health", 200,
            "Health check endpoint - should return healthy status"
        )
        
        # Test 2: Arabic Quran Chapters
        await self.test_endpoint(
            "GET", "/api/quran/v4/chapters", 200,
            "Get Arabic Quran chapters",
            params={"language": "ar"}
        )
        
        # Test 3: Turkish Quran Chapters
        await self.test_endpoint(
            "GET", "/api/quran/v4/chapters", 200,
            "Get Turkish Quran chapters",
            params={"language": "tr"}
        )
        
        # Test 4: Turkish Kids Daily Games
        await self.test_endpoint(
            "GET", "/api/kids-learn/daily-games", 200,
            "Get Turkish kids daily games",
            params={"locale": "tr"}
        )
        
        # Test 5: Sohba Posts
        await self.test_endpoint(
            "GET", "/api/sohba/posts", 200,
            "Get Sohba social posts"
        )
        
        # Test 6: Paris Mosque Prayer Times (try different endpoints)
        # First try the exact endpoint from review request
        await self.test_endpoint(
            "GET", "/api/mosque-prayer-times/nearby", 200,
            "Get Paris mosque prayer times (exact endpoint)",
            params={"lat": 48.8566, "lng": 2.3522}
        )
        
        # If that fails, try the mosque search endpoint we found in the code
        await self.test_endpoint(
            "GET", "/api/mosques/search", 200,
            "Search mosques near Paris (alternative endpoint)",
            params={"lat": 48.8566, "lon": 2.3522, "radius": 5000}
        )
        
        # Test 7: Zakat Gold Price (try different endpoints)
        # First try the exact endpoint from review request
        await self.test_endpoint(
            "GET", "/api/zakat/gold-price", 200,
            "Get gold price for Zakat in TRY (exact endpoint)",
            params={"currency": "TRY"}
        )
        
        # Additional tests for endpoints we know exist
        print("\n📋 Additional Backend Verification Tests:")
        
        # Test Quran global verse endpoint
        await self.test_endpoint(
            "GET", "/api/quran/v4/global-verse/1/1", 200,
            "Get first verse of Quran (Al-Fatiha 1:1)",
            params={"language": "en"}
        )
        
        # Test kids learn daily lesson
        await self.test_endpoint(
            "GET", "/api/kids-learn/daily-lesson", 200,
            "Get kids daily lesson",
            params={"locale": "en"}
        )
        
        # Test prayer times
        await self.test_endpoint(
            "GET", "/api/prayer-times", 200,
            "Get prayer times for Paris",
            params={"lat": 48.8566, "lon": 2.3522, "method": 3}
        )
        
        # Test sohba categories
        await self.test_endpoint(
            "GET", "/api/sohba/categories", 200,
            "Get Sohba categories"
        )
        
        print("\n" + "=" * 80)
        self.print_summary()
    
    def print_summary(self):
        """Print test results summary"""
        print(f"📊 TEST RESULTS SUMMARY")
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print("=" * 80)
        
        # Print detailed results
        for i, result in enumerate(self.results, 1):
            status_icon = "✅" if result["passed"] else "❌"
            print(f"{status_icon} Test {i}: {result['method']} {result['endpoint']}")
            print(f"   Description: {result['description']}")
            print(f"   Status: {result['status_code']} (expected {result['expected_status']})")
            
            if "error" in result:
                print(f"   Error: {result['error']}")
            elif result["passed"] and "validation" in result:
                validation = result["validation"]
                if validation["valid"]:
                    print(f"   ✅ Response validation passed")
                else:
                    print(f"   ⚠️  Response validation issues: {', '.join(validation['issues'])}")
            
            if result["passed"]:
                print(f"   Response size: {result['response_size']} chars")
                print(f"   Preview: {result['response_preview']}")
            
            print()
        
        # Summary by category
        failed_tests = [r for r in self.results if not r["passed"]]
        if failed_tests:
            print("❌ FAILED TESTS:")
            for test in failed_tests:
                error_msg = test.get('error', f"Status {test['status_code']}")
                print(f"   - {test['method']} {test['endpoint']}: {error_msg}")
        
        passed_tests = [r for r in self.results if r["passed"]]
        if passed_tests:
            print("✅ PASSED TESTS:")
            for test in passed_tests:
                print(f"   - {test['method']} {test['endpoint']}: Status {test['status_code']}")

async def main():
    """Main test runner"""
    tester = BackendTester()
    await tester.run_review_request_tests()

if __name__ == "__main__":
    asyncio.run(main())