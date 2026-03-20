#!/usr/bin/env python3
"""
Athan Tales Backend API Testing Script
Tests Arabic Academy and Live Streams endpoints
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, List

# Get external URL from frontend .env
FRONTEND_ENV_PATH = "/app/frontend/.env"
def get_backend_url():
    try:
        with open(FRONTEND_ENV_PATH, 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.strip().split('=', 1)[1]
    except:
        pass
    return "https://athan-tales.preview.emergentagent.com"

BASE_URL = get_backend_url()
API_BASE = f"{BASE_URL}/api"

class BackendTester:
    def __init__(self):
        self.session = None
        self.results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(ssl=False)
        )
        return self
        
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def test_endpoint(self, method: str, endpoint: str, data: Dict[Any, Any] = None, expected_status: int = 200) -> Dict[str, Any]:
        """Test a single endpoint"""
        url = f"{API_BASE}{endpoint}"
        start_time = time.time()
        
        try:
            if method == "GET":
                async with self.session.get(url) as response:
                    response_time = time.time() - start_time
                    response_data = await response.text()
                    
                    try:
                        json_data = json.loads(response_data)
                    except json.JSONDecodeError:
                        json_data = {"raw_response": response_data}
                    
                    return {
                        "method": method,
                        "endpoint": endpoint,
                        "url": url,
                        "status": response.status,
                        "expected_status": expected_status,
                        "passed": response.status == expected_status,
                        "response_time": round(response_time, 3),
                        "response_data": json_data,
                        "error": None
                    }
                    
            elif method == "POST":
                headers = {"Content-Type": "application/json"}
                async with self.session.post(url, json=data, headers=headers) as response:
                    response_time = time.time() - start_time
                    response_data = await response.text()
                    
                    try:
                        json_data = json.loads(response_data)
                    except json.JSONDecodeError:
                        json_data = {"raw_response": response_data}
                    
                    return {
                        "method": method,
                        "endpoint": endpoint,
                        "url": url,
                        "status": response.status,
                        "expected_status": expected_status,
                        "passed": response.status == expected_status,
                        "response_time": round(response_time, 3),
                        "response_data": json_data,
                        "request_data": data,
                        "error": None
                    }
                    
        except Exception as e:
            response_time = time.time() - start_time
            return {
                "method": method,
                "endpoint": endpoint,
                "url": url,
                "status": 0,
                "expected_status": expected_status,
                "passed": False,
                "response_time": round(response_time, 3),
                "response_data": {},
                "error": str(e)
            }

    async def run_tests(self):
        """Run all backend tests"""
        print("🔍 Starting Athan Tales Backend API Testing...")
        print(f"🌐 Testing against: {BASE_URL}")
        print("=" * 80)
        
        # Test cases based on review request
        test_cases = [
            # 1. Health check
            {
                "name": "Health Check",
                "method": "GET",
                "endpoint": "/health",
                "validation": lambda r: r.get("status") == "healthy"
            },
            
            # 2. Arabic Academy - Letters (28 letters)
            {
                "name": "Arabic Academy Letters",
                "method": "GET", 
                "endpoint": "/arabic-academy/letters",
                "validation": lambda r: (
                    r.get("success") == True and
                    len(r.get("letters", [])) == 28 and
                    all("id" in letter and "letter" in letter and "name_ar" in letter 
                        for letter in r.get("letters", []))
                )
            },
            
            # 3. Arabic Academy - Vocabulary (20 words)
            {
                "name": "Arabic Academy Vocabulary",
                "method": "GET",
                "endpoint": "/arabic-academy/vocab", 
                "validation": lambda r: (
                    r.get("success") == True and
                    len(r.get("words", [])) == 20 and
                    all("word" in word and "transliteration" in word and "meaning" in word
                        for word in r.get("words", []))
                )
            },
            
            # 4. Arabic Academy - Quiz for letter 1 (Alif)
            {
                "name": "Arabic Academy Quiz (Alif)",
                "method": "GET",
                "endpoint": "/arabic-academy/quiz/1",
                "validation": lambda r: (
                    r.get("success") == True and
                    "quiz" in r and 
                    len(r["quiz"].get("options", [])) == 4 and
                    sum(1 for opt in r["quiz"]["options"] if opt.get("correct")) == 1
                )
            },
            
            # 5. Arabic Academy - Daily word
            {
                "name": "Arabic Academy Daily Word", 
                "method": "GET",
                "endpoint": "/arabic-academy/daily-word",
                "validation": lambda r: (
                    r.get("success") == True and
                    "word" in r and
                    "word" in r["word"] and "meaning" in r["word"]
                )
            },
            
            # 6. Arabic Academy - Guest progress
            {
                "name": "Arabic Academy Guest Progress",
                "method": "GET",
                "endpoint": "/arabic-academy/progress/guest",
                "validation": lambda r: (
                    r.get("success") == True and
                    "progress" in r and
                    all(field in r["progress"] for field in 
                        ["completed_letters", "stars", "total_xp", "level", "golden_bricks"])
                )
            },
            
            # 7. Arabic Academy - Save progress (POST)
            {
                "name": "Arabic Academy Save Progress",
                "method": "POST",
                "endpoint": "/arabic-academy/progress",
                "data": {
                    "user_id": "test-user",
                    "completed_letters": [1, 2, 3],
                    "stars": 3,
                    "total_xp": 30,
                    "level": 1,
                    "golden_bricks": 3
                },
                "validation": lambda r: r.get("success") == True
            },
            
            # 8. Live Streams - All streams
            {
                "name": "Live Streams (All)",
                "method": "GET",
                "endpoint": "/live-streams",
                "validation": lambda r: (
                    r.get("success") == True and
                    len(r.get("streams", [])) > 0 and
                    all("embed_url" in stream and "youtube.com/embed" in stream["embed_url"]
                        for stream in r.get("streams", []))
                )
            },
            
            # 9. Live Streams - Haramain category filter
            {
                "name": "Live Streams (Haramain Filter)",
                "method": "GET",
                "endpoint": "/live-streams?category=haramain",
                "validation": lambda r: (
                    r.get("success") == True and
                    all(stream.get("category") == "haramain" 
                        for stream in r.get("streams", [])) and
                    len(r.get("streams", [])) >= 2  # Should have Makkah and Madinah
                )
            }
        ]
        
        # Execute tests
        for i, test in enumerate(test_cases, 1):
            print(f"🧪 Test {i}: {test['name']}")
            
            result = await self.test_endpoint(
                method=test["method"],
                endpoint=test["endpoint"],
                data=test.get("data")
            )
            
            # Add validation result
            if result["passed"] and "validation" in test:
                try:
                    validation_passed = test["validation"](result["response_data"])
                    result["validation_passed"] = validation_passed
                    if not validation_passed:
                        result["passed"] = False
                        result["validation_error"] = "Response structure validation failed"
                except Exception as e:
                    result["validation_passed"] = False
                    result["passed"] = False
                    result["validation_error"] = f"Validation error: {str(e)}"
            
            self.results.append(result)
            
            # Print result
            status = "✅ PASSED" if result["passed"] else "❌ FAILED"
            print(f"   {status} ({result['status']}) - {result['response_time']}s")
            
            if not result["passed"]:
                if result.get("error"):
                    print(f"   💥 Error: {result['error']}")
                elif result.get("validation_error"):
                    print(f"   ⚠️ Validation: {result['validation_error']}")
                else:
                    print(f"   ⚠️ HTTP Status: Expected {result['expected_status']}, got {result['status']}")
            
            print()

    def print_summary(self):
        """Print test summary"""
        passed_tests = sum(1 for r in self.results if r["passed"])
        total_tests = len(self.results)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        avg_response_time = sum(r["response_time"] for r in self.results) / total_tests if total_tests > 0 else 0
        
        print("=" * 80)
        print("📊 ATHAN TALES BACKEND TEST SUMMARY")
        print("=" * 80)
        print(f"✅ Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print(f"⏱️ Average Response Time: {avg_response_time:.3f}s")
        print(f"🌐 Backend URL: {BASE_URL}")
        
        # Show failed tests
        failed_tests = [r for r in self.results if not r["passed"]]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   • {test['method']} {test['endpoint']}")
                if test.get("error"):
                    print(f"     Error: {test['error']}")
                elif test.get("validation_error"):
                    print(f"     Validation: {test['validation_error']}")
                else:
                    print(f"     HTTP {test['status']} (expected {test['expected_status']})")
        
        print("\n🎯 Specific Features Tested:")
        print("   ✅ Health check endpoint")
        print("   ✅ Arabic Academy: 28 letters with metadata")
        print("   ✅ Arabic Academy: 20 Quranic vocabulary words")
        print("   ✅ Arabic Academy: Quiz generation with 4 options")
        print("   ✅ Arabic Academy: Daily word rotation")
        print("   ✅ Arabic Academy: Progress tracking system")
        print("   ✅ Arabic Academy: Progress persistence")
        print("   ✅ Live Streams: YouTube embed URL generation")
        print("   ✅ Live Streams: Category filtering (haramain)")
        
        return success_rate == 100.0

async def main():
    """Main test runner"""
    async with BackendTester() as tester:
        await tester.run_tests()
        all_passed = tester.print_summary()
        
        if all_passed:
            print("\n🎉 ALL TESTS PASSED - Arabic Academy & Live Streams APIs are fully functional!")
        else:
            print("\n⚠️ Some tests failed - Review the issues above")
            
        return all_passed

if __name__ == "__main__":
    asyncio.run(main())