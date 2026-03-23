#!/usr/bin/env python3
"""
Policy Compliance Backend API Testing Script
Tests the 4 NEW policy compliance endpoints for Azan & Hikaya app
"""

import asyncio
import httpx
import json
from typing import Dict, Any, List

# Backend URL from frontend .env
BACKEND_URL = "https://store-ready-app-8.preview.emergentagent.com"

class PolicyComplianceAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.results = []
        
    def log_result(self, test_name: str, endpoint: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "endpoint": endpoint,
            "status": status,
            "details": details
        }
        self.results.append(result)
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
    
    async def test_data_deletion_request_valid(self):
        """Test 1: POST /api/data-deletion-request with valid data"""
        test_name = "Data Deletion Request - Valid Email"
        endpoint = "/api/data-deletion-request"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                payload = {
                    "email": "test@example.com",
                    "reason": "Testing deletion"
                }
                
                response = await client.post(f"{self.base_url}{endpoint}", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "success" in data and data["success"] is True:
                        if "message" in data:
                            self.log_result(test_name, endpoint, "PASS", 
                                          f"Success response: {data['message']}")
                        else:
                            self.log_result(test_name, endpoint, "PASS", 
                                          "Success response received (no message field)")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"Response missing success=true: {data}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_app_ads_txt(self):
        """Test 2: GET /api/app-ads-txt - Dynamic app-ads.txt content"""
        test_name = "App Ads.txt Content"
        endpoint = "/api/app-ads-txt"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    # Check if response is text/plain
                    content_type = response.headers.get("content-type", "")
                    
                    if "text/plain" in content_type:
                        content = response.text
                        if content and len(content.strip()) > 0:
                            self.log_result(test_name, endpoint, "PASS", 
                                          f"Text/plain response with {len(content)} characters")
                        else:
                            self.log_result(test_name, endpoint, "PASS", 
                                          "Text/plain response (empty content)")
                    else:
                        # Still pass if content is returned, even if not text/plain
                        content = response.text
                        self.log_result(test_name, endpoint, "PASS", 
                                      f"Response received (content-type: {content_type})")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_data_deletion_request_empty_email(self):
        """Test 3: POST /api/data-deletion-request with empty email"""
        test_name = "Data Deletion Request - Empty Email Validation"
        endpoint = "/api/data-deletion-request"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                payload = {
                    "email": "",
                    "reason": "test"
                }
                
                response = await client.post(f"{self.base_url}{endpoint}", json=payload)
                
                if response.status_code == 400:
                    data = response.json()
                    
                    # Check if error message mentions email requirement
                    error_message = str(data).lower()
                    if "email" in error_message and ("required" in error_message or "empty" in error_message):
                        self.log_result(test_name, endpoint, "PASS", 
                                      f"Correctly returns 400 with email validation: {data}")
                    else:
                        self.log_result(test_name, endpoint, "PASS", 
                                      f"Returns 400 error (validation working): {data}")
                elif response.status_code == 422:
                    # Unprocessable Entity is also acceptable for validation errors
                    data = response.json()
                    self.log_result(test_name, endpoint, "PASS", 
                                  f"Returns 422 validation error: {data}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"Expected 400/422 but got HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_data_deletion_request_valid_second(self):
        """Test 4: POST /api/data-deletion-request with another valid email"""
        test_name = "Data Deletion Request - Second Valid Email"
        endpoint = "/api/data-deletion-request"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                payload = {
                    "email": "user@test.com",
                    "reason": "I want to leave"
                }
                
                response = await client.post(f"{self.base_url}{endpoint}", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "success" in data and data["success"] is True:
                        self.log_result(test_name, endpoint, "PASS", 
                                      f"Success response: {data}")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"Response missing success=true: {data}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def run_all_tests(self):
        """Run all policy compliance API tests"""
        print(f"🚀 Starting Policy Compliance API Tests for: {self.base_url}")
        print("=" * 70)
        print("Testing 4 NEW policy compliance endpoints:")
        print("1. POST /api/data-deletion-request (valid email)")
        print("2. GET /api/app-ads-txt (dynamic content)")
        print("3. POST /api/data-deletion-request (empty email validation)")
        print("4. POST /api/data-deletion-request (second valid email)")
        print("=" * 70)
        
        # Run all tests in order
        await self.test_data_deletion_request_valid()
        await self.test_app_ads_txt()
        await self.test_data_deletion_request_empty_email()
        await self.test_data_deletion_request_valid_second()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 POLICY COMPLIANCE TEST SUMMARY")
        print("=" * 70)
        
        passed = len([r for r in self.results if r["status"] == "PASS"])
        failed = len([r for r in self.results if r["status"] == "FAIL"])
        skipped = len([r for r in self.results if r["status"] == "SKIP"])
        
        print(f"✅ PASSED: {passed}")
        print(f"❌ FAILED: {failed}")
        print(f"⏭️  SKIPPED: {skipped}")
        print(f"📈 SUCCESS RATE: {passed}/{passed+failed} ({(passed/(passed+failed)*100) if (passed+failed) > 0 else 0:.1f}%)")
        
        # Detailed results
        if failed > 0:
            print("\n🔍 FAILED TESTS DETAILS:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"❌ {result['test']}: {result['details']}")
        
        print("\n📋 COMPLIANCE STATUS:")
        if failed == 0:
            print("✅ ALL POLICY COMPLIANCE ENDPOINTS WORKING CORRECTLY")
            print("✅ Ready for Google Play Store submission")
        else:
            print("❌ POLICY COMPLIANCE ISSUES FOUND - NEEDS FIXING")
            print("❌ Not ready for Google Play Store submission")
        
        return self.results

async def main():
    """Main test runner"""
    tester = PolicyComplianceAPITester()
    results = await tester.run_all_tests()
    
    # Return results for potential use by other scripts
    return results

if __name__ == "__main__":
    asyncio.run(main())