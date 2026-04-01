#!/usr/bin/env python3
"""
Backend API Testing for أذان وحكاية
Tests critical backend APIs as specified in the review request
"""

import asyncio
import httpx
import json
from datetime import datetime
import sys

# Backend URL from frontend environment
BACKEND_URL = "https://bug-fix-tools.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    def log_result(self, test_name, success, details="", response_data=None):
        """Log test result"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
        
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"{status} - {test_name}")
        if details:
            print(f"    Details: {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()

    async def test_daily_islamic_content(self):
        """Test Daily Islamic Content APIs (FREE, no API key needed)"""
        print("🕌 Testing Daily Islamic Content APIs...")
        
        async with httpx.AsyncClient(timeout=30) as client:
            # Test verse-of-day
            try:
                response = await client.get(f"{BACKEND_URL}/ai/verse-of-day")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and "verse" in data:
                        verse = data["verse"]
                        if "text" in verse and "surah" in verse and "surah_number" in verse and "ayah" in verse:
                            self.log_result("GET /ai/verse-of-day", True, f"Returned verse from {verse['surah']} {verse['surah_number']}:{verse['ayah']}")
                        else:
                            self.log_result("GET /ai/verse-of-day", False, "Missing required verse fields", data)
                    else:
                        self.log_result("GET /ai/verse-of-day", False, "Invalid response format", data)
                else:
                    self.log_result("GET /ai/verse-of-day", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_result("GET /ai/verse-of-day", False, f"Exception: {str(e)}")

            # Test hadith-of-day
            try:
                response = await client.get(f"{BACKEND_URL}/ai/hadith-of-day")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and "hadith" in data:
                        hadith = data["hadith"]
                        if "text" in hadith and "narrator" in hadith and "source" in hadith:
                            self.log_result("GET /ai/hadith-of-day", True, f"Returned hadith from {hadith['source']}")
                        else:
                            self.log_result("GET /ai/hadith-of-day", False, "Missing required hadith fields", data)
                    else:
                        self.log_result("GET /ai/hadith-of-day", False, "Invalid response format", data)
                else:
                    self.log_result("GET /ai/hadith-of-day", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_result("GET /ai/hadith-of-day", False, f"Exception: {str(e)}")

            # Test daily-dua
            try:
                response = await client.get(f"{BACKEND_URL}/ai/daily-dua")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and "dua" in data:
                        dua = data["dua"]
                        if "text" in dua and "source" in dua:
                            self.log_result("GET /ai/daily-dua", True, f"Returned dua from {dua['source']}")
                        else:
                            self.log_result("GET /ai/daily-dua", False, "Missing required dua fields", data)
                    else:
                        self.log_result("GET /ai/daily-dua", False, "Invalid response format", data)
                else:
                    self.log_result("GET /ai/daily-dua", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_result("GET /ai/daily-dua", False, f"Exception: {str(e)}")

    async def test_prayer_times(self):
        """Test Prayer Times API (Aladhan API - FREE, global)"""
        print("🕌 Testing Prayer Times API...")
        
        test_locations = [
            {"name": "Berlin", "lat": 52.52, "lon": 13.405},
            {"name": "Mecca", "lat": 21.42, "lon": 39.82},
            {"name": "Jakarta", "lat": -6.2, "lon": 106.8}
        ]
        
        async with httpx.AsyncClient(timeout=30) as client:
            for location in test_locations:
                try:
                    response = await client.get(
                        f"{BACKEND_URL}/prayer-times",
                        params={"lat": location["lat"], "lon": location["lon"]}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("success") and "times" in data:
                            times = data["times"]
                            required_prayers = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]
                            if all(prayer in times for prayer in required_prayers):
                                self.log_result(f"GET /prayer-times ({location['name']})", True, f"All prayer times returned")
                            else:
                                missing = [p for p in required_prayers if p not in times]
                                self.log_result(f"GET /prayer-times ({location['name']})", False, f"Missing prayers: {missing}", data)
                        else:
                            self.log_result(f"GET /prayer-times ({location['name']})", False, "Invalid response format", data)
                    else:
                        self.log_result(f"GET /prayer-times ({location['name']})", False, f"HTTP {response.status_code}", response.text)
                except Exception as e:
                    self.log_result(f"GET /prayer-times ({location['name']})", False, f"Exception: {str(e)}")

    async def test_mosque_search(self):
        """Test Mosque Search API (Mawaqit/OpenStreetMap - FREE)"""
        print("🕌 Testing Mosque Search API...")
        
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                # Test Berlin mosque search
                response = await client.get(
                    f"{BACKEND_URL}/mosques/search",
                    params={"lat": 52.52, "lon": 13.405, "radius": 5}
                )
                if response.status_code == 200:
                    data = response.json()
                    if "mosques" in data:
                        mosques = data["mosques"]
                        if len(mosques) > 0:
                            # Check if mosques have required fields
                            first_mosque = mosques[0]
                            required_fields = ["name", "latitude", "longitude"]
                            if all(field in first_mosque for field in required_fields):
                                self.log_result("GET /mosques/search (Berlin)", True, f"Found {len(mosques)} mosques")
                            else:
                                missing = [f for f in required_fields if f not in first_mosque]
                                self.log_result("GET /mosques/search (Berlin)", False, f"Missing mosque fields: {missing}", data)
                        else:
                            self.log_result("GET /mosques/search (Berlin)", True, "No mosques found (acceptable for test location)")
                    else:
                        self.log_result("GET /mosques/search (Berlin)", False, "Missing 'mosques' field", data)
                else:
                    self.log_result("GET /mosques/search (Berlin)", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_result("GET /mosques/search (Berlin)", False, f"Exception: {str(e)}")

    async def test_stories_listing(self):
        """Test Stories listing with language filter"""
        print("📚 Testing Stories Listing API...")
        
        async with httpx.AsyncClient(timeout=30) as client:
            # Test Arabic stories
            try:
                response = await client.get(
                    f"{BACKEND_URL}/stories/list",
                    params={"category": "istighfar", "lang": "ar"}
                )
                if response.status_code == 200:
                    data = response.json()
                    if "stories" in data:
                        stories = data["stories"]
                        self.log_result("GET /stories/list (Arabic istighfar)", True, f"Found {len(stories)} Arabic stories")
                    else:
                        self.log_result("GET /stories/list (Arabic istighfar)", False, "Missing 'stories' field", data)
                else:
                    self.log_result("GET /stories/list (Arabic istighfar)", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_result("GET /stories/list (Arabic istighfar)", False, f"Exception: {str(e)}")

            # Test English stories
            try:
                response = await client.get(
                    f"{BACKEND_URL}/stories/list",
                    params={"category": "sahaba", "lang": "en"}
                )
                if response.status_code == 200:
                    data = response.json()
                    if "stories" in data:
                        stories = data["stories"]
                        self.log_result("GET /stories/list (English sahaba)", True, f"Found {len(stories)} English stories")
                    else:
                        self.log_result("GET /stories/list (English sahaba)", False, "Missing 'stories' field", data)
                else:
                    self.log_result("GET /stories/list (English sahaba)", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_result("GET /stories/list (English sahaba)", False, f"Exception: {str(e)}")

    async def test_active_ads(self):
        """Test Active Ads API for different placements"""
        print("📢 Testing Active Ads API...")
        
        placements = ["prayer", "quran", "stories"]
        
        async with httpx.AsyncClient(timeout=30) as client:
            for placement in placements:
                try:
                    response = await client.get(f"{BACKEND_URL}/ads/active", params={"placement": placement})
                    if response.status_code == 200:
                        data = response.json()
                        # The API might return empty ads list, which is acceptable
                        self.log_result(f"GET /ads/active (placement={placement})", True, f"API responded successfully")
                    else:
                        self.log_result(f"GET /ads/active (placement={placement})", False, f"HTTP {response.status_code}", response.text)
                except Exception as e:
                    self.log_result(f"GET /ads/active (placement={placement})", False, f"Exception: {str(e)}")

    async def test_health_endpoints(self):
        """Test basic health and status endpoints"""
        print("🔍 Testing Health Endpoints...")
        
        async with httpx.AsyncClient(timeout=30) as client:
            # Test root endpoint
            try:
                response = await client.get(f"{BACKEND_URL}/")
                if response.status_code == 200:
                    data = response.json()
                    if "message" in data and "version" in data:
                        self.log_result("GET /api/", True, f"API version {data.get('version')}")
                    else:
                        self.log_result("GET /api/", False, "Missing expected fields", data)
                else:
                    self.log_result("GET /api/", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_result("GET /api/", False, f"Exception: {str(e)}")

            # Test health endpoint
            try:
                response = await client.get(f"{BACKEND_URL}/health")
                if response.status_code == 200:
                    data = response.json()
                    if "status" in data:
                        self.log_result("GET /health", True, f"Status: {data.get('status')}")
                    else:
                        self.log_result("GET /health", False, "Missing status field", data)
                else:
                    self.log_result("GET /health", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_result("GET /health", False, f"Exception: {str(e)}")

    async def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting Backend API Tests for أذان وحكاية")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 60)
        
        # Run all test suites
        await self.test_health_endpoints()
        await self.test_daily_islamic_content()
        await self.test_prayer_times()
        await self.test_mosque_search()
        await self.test_stories_listing()
        await self.test_active_ads()
        
        # Print summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print()
        
        # Print failed tests details
        if self.failed_tests > 0:
            print("❌ FAILED TESTS:")
            for result in self.results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
            print()
        
        # Return results for further processing
        return {
            "total": self.total_tests,
            "passed": self.passed_tests,
            "failed": self.failed_tests,
            "success_rate": self.passed_tests/self.total_tests*100 if self.total_tests > 0 else 0,
            "results": self.results
        }

async def main():
    """Main test runner"""
    tester = BackendTester()
    results = await tester.run_all_tests()
    
    # Exit with error code if tests failed
    if results["failed"] > 0:
        sys.exit(1)
    else:
        print("🎉 All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())