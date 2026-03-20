#!/usr/bin/env python3
"""
Backend API Testing for Islamic App
Tests the requested endpoints from the review request
"""
import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, List

# Base URL from frontend environment
BASE_URL = "https://app-stability-check-1.preview.emergentagent.com/api"

class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_endpoint(self, method: str, endpoint: str, expected_keys: List[str] = None, description: str = "") -> Dict[str, Any]:
        """Test a single endpoint and return results"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            async with self.session.request(method, url) as response:
                duration = time.time() - start_time
                
                # Get response data
                if response.content_type == 'application/json':
                    data = await response.json()
                else:
                    text_data = await response.text()
                    try:
                        data = json.loads(text_data)
                    except:
                        data = {"response_text": text_data}
                
                result = {
                    "endpoint": endpoint,
                    "method": method,
                    "url": url,
                    "status_code": response.status,
                    "success": response.status == 200,
                    "duration": round(duration, 3),
                    "description": description,
                    "content_type": response.content_type,
                    "response_size": len(str(data)),
                    "has_data": bool(data),
                    "issues": [],
                    "validation_notes": []
                }
                
                # Status code validation
                if response.status != 200:
                    result["issues"].append(f"Non-200 status code: {response.status}")
                
                # Empty response check
                if not data:
                    result["issues"].append("Empty response body")
                
                # Expected keys check
                if expected_keys and isinstance(data, dict):
                    missing_keys = [key for key in expected_keys if key not in data]
                    if missing_keys:
                        result["issues"].append(f"Missing expected keys: {missing_keys}")
                
                # Special validation for daily-hadith multilingual API
                if "/daily-hadith" in endpoint and response.status == 200:
                    self._validate_hadith_response(endpoint, data, result)
                
                # Special validation for store and ruqyah items
                if "/store/items" in endpoint and response.status == 200:
                    self._validate_items_response("store", data, result)
                elif "/ruqyah" in endpoint and response.status == 200:
                    self._validate_items_response("ruqyah", data, result)
                
                # Store sample data for verification
                if isinstance(data, dict):
                    result["sample_keys"] = list(data.keys())[:10]  # First 10 keys
                    if "data" in data:
                        result["data_type"] = type(data["data"]).__name__
                        if isinstance(data["data"], list):
                            result["data_count"] = len(data["data"])
                        elif isinstance(data["data"], dict):
                            result["data_sample_keys"] = list(data["data"].keys())[:5]
                    if "items" in data:
                        result["data_type"] = type(data["items"]).__name__
                        if isinstance(data["items"], list):
                            result["data_count"] = len(data["items"])
                elif isinstance(data, list):
                    result["data_count"] = len(data)
                    result["data_type"] = "list"
                
                return result
                
        except asyncio.TimeoutError:
            return {
                "endpoint": endpoint,
                "method": method,
                "url": url,
                "status_code": "TIMEOUT",
                "success": False,
                "duration": time.time() - start_time,
                "description": description,
                "issues": ["Request timeout (30s)"]
            }
        except Exception as e:
            return {
                "endpoint": endpoint,
                "method": method,
                "url": url,
                "status_code": "ERROR",
                "success": False,
                "duration": time.time() - start_time,
                "description": description,
                "issues": [f"Request error: {str(e)}"]
            }
    
    def _validate_hadith_response(self, endpoint: str, data: dict, result: dict):
        """Validate hadith API response based on language parameter"""
        if not isinstance(data, dict) or "hadith" not in data:
            result["issues"].append("Invalid hadith response structure")
            return
            
        hadith = data["hadith"]
        if not isinstance(hadith, dict):
            result["issues"].append("Hadith field is not a dictionary")
            return
            
        # Check success field
        if not data.get("success"):
            result["issues"].append("Response does not indicate success=true")
        
        # Required hadith fields
        required_fields = ["text", "narrator", "source"]
        missing_fields = [field for field in required_fields if field not in hadith]
        if missing_fields:
            result["issues"].append(f"Missing hadith fields: {missing_fields}")
        
        # Language-specific validation
        if "language=en" in endpoint:
            # English request should have arabic_text field
            if "arabic_text" not in hadith:
                result["issues"].append("English hadith request missing arabic_text field")
            else:
                result["validation_notes"].append("✓ English hadith contains arabic_text field")
                
        elif "language=ar" in endpoint or endpoint == "/daily-hadith":
            # Arabic request should NOT have arabic_text field
            if "arabic_text" in hadith:
                result["issues"].append("Arabic hadith request should not contain arabic_text field")
            else:
                result["validation_notes"].append("✓ Arabic hadith correctly excludes arabic_text field")
                
        elif "language=de" in endpoint:
            # German request should return Arabic text (no translation available)
            if "arabic_text" in hadith:
                result["issues"].append("German hadith should return Arabic text without arabic_text field")
            else:
                result["validation_notes"].append("✓ German hadith correctly returns Arabic text (no German translation)")
    
    def _validate_items_response(self, api_type: str, data: dict, result: dict):
        """Validate items response structure"""
        if "items" not in data:
            result["issues"].append(f"{api_type} API missing 'items' key")
            return
            
        items = data["items"]
        if not isinstance(items, list):
            result["issues"].append(f"{api_type} items is not a list")
            return
            
        if len(items) == 0:
            result["validation_notes"].append(f"⚠️ {api_type} returned empty items list")
        else:
            result["validation_notes"].append(f"✓ {api_type} returned {len(items)} items")
    
    async def run_tests(self):
        """Run all the requested API tests"""
        print("🕌 Starting Islamic App Backend API Tests...")
        print(f"Base URL: {self.base_url}")
        print("-" * 60)
        
        # Test cases based on review request - focusing on multilingual hadith API
        test_cases = [
            {
                "method": "GET",
                "endpoint": "/health",
                "expected_keys": ["status"],
                "description": "General health check - should return healthy status"
            },
            {
                "method": "GET",
                "endpoint": "/daily-hadith",
                "expected_keys": ["success", "hadith"],
                "description": "Default daily hadith - should return Arabic hadith without arabic_text field"
            },
            {
                "method": "GET",
                "endpoint": "/daily-hadith?language=ar",
                "expected_keys": ["success", "hadith"],
                "description": "Arabic daily hadith - should return Arabic hadith without arabic_text field"
            },
            {
                "method": "GET",
                "endpoint": "/daily-hadith?language=en", 
                "expected_keys": ["success", "hadith"],
                "description": "English daily hadith - should return English translation with arabic_text field"
            },
            {
                "method": "GET",
                "endpoint": "/daily-hadith?language=de",
                "expected_keys": ["success", "hadith"],
                "description": "German daily hadith - should return Arabic text (German not available)"
            },
            {
                "method": "GET",
                "endpoint": "/ruqyah",
                "expected_keys": ["items"],
                "description": "Ruqyah API - should return items list"
            },
            {
                "method": "GET",
                "endpoint": "/store/items", 
                "expected_keys": ["items"],
                "description": "Store API - should return items list"
            }
        ]
        
        # Run tests
        for i, test_case in enumerate(test_cases, 1):
            print(f"Test {i}/{len(test_cases)}: {test_case['description']}")
            result = await self.test_endpoint(**test_case)
            self.results.append(result)
            
            # Print immediate result
            status_icon = "✅" if result["success"] else "❌"
            print(f"  {status_icon} {result['endpoint']} - Status: {result['status_code']} ({result['duration']}s)")
            
            if result["issues"]:
                for issue in result["issues"]:
                    print(f"    ❌ {issue}")
            
            if result.get("validation_notes"):
                for note in result["validation_notes"]:
                    print(f"    {note}")
            
            print()
        
        return self.results
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate test summary"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        
        summary = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": round((passed_tests / total_tests) * 100, 1) if total_tests > 0 else 0,
            "total_duration": round(sum(r["duration"] for r in self.results), 3),
            "avg_response_time": round(sum(r["duration"] for r in self.results) / total_tests, 3) if total_tests > 0 else 0,
            "critical_issues": []
        }
        
        # Identify critical issues
        for result in self.results:
            if not result["success"]:
                summary["critical_issues"].append({
                    "endpoint": result["endpoint"],
                    "issues": result["issues"]
                })
        
        return summary
    
    def print_detailed_report(self):
        """Print detailed test report"""
        summary = self.generate_summary()
        
        print("=" * 60)
        print("🎯 BACKEND API TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']} ✅")
        print(f"Failed: {summary['failed']} ❌")
        print(f"Success Rate: {summary['success_rate']}%")
        print(f"Total Duration: {summary['total_duration']}s")
        print(f"Avg Response Time: {summary['avg_response_time']}s")
        print()
        
        if summary["critical_issues"]:
            print("🚨 CRITICAL ISSUES FOUND:")
            for issue in summary["critical_issues"]:
                print(f"  ❌ {issue['endpoint']}")
                for detail in issue["issues"]:
                    print(f"     - {detail}")
            print()
        
        print("📋 DETAILED RESULTS:")
        for result in self.results:
            status_icon = "✅" if result["success"] else "❌"
            print(f"{status_icon} {result['method']} {result['endpoint']}")
            print(f"    Status: {result['status_code']}")
            print(f"    Duration: {result['duration']}s")
            print(f"    Description: {result['description']}")
            
            if "sample_keys" in result:
                print(f"    Response Keys: {result['sample_keys']}")
            
            if "data_count" in result:
                print(f"    Data Items: {result['data_count']}")
            
            if result.get("validation_notes"):
                print(f"    Validation: {result['validation_notes']}")
            
            if result["issues"]:
                print(f"    Issues: {result['issues']}")
            
            print()

async def main():
    """Main test runner"""
    try:
        async with APITester(BASE_URL) as tester:
            results = await tester.run_tests()
            tester.print_detailed_report()
            
            # Return summary for potential use by other tools
            summary = tester.generate_summary()
            return {
                "summary": summary,
                "results": results
            }
    
    except Exception as e:
        print(f"❌ Testing failed with error: {e}")
        return {
            "summary": {"total_tests": 0, "passed": 0, "failed": 0, "success_rate": 0},
            "results": [],
            "error": str(e)
        }

if __name__ == "__main__":
    asyncio.run(main())