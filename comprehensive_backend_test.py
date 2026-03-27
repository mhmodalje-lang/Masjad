#!/usr/bin/env python3
"""
Comprehensive Backend API Testing
Testing all major endpoint groups as requested in the review
"""

import requests
import json
import time
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://mobile-deploy-23.preview.emergentagent.com"

class ComprehensiveAPITester:
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

    def test_core_endpoints(self):
        """Test core API endpoints"""
        print("🔧 Testing Core Endpoints...")
        
        # Test 1: Root API endpoint
        result = self.test_get_request("/api/")
        if result["success"]:
            data = result["data"]
            if data.get("message") and data.get("version") and data.get("status"):
                self.log_result("Core API Root", "PASSED", result["response_time"], 
                              f"Message: {data.get('message')}, Version: {data.get('version')}")
            else:
                self.log_result("Core API Root", "FAILED", result["response_time"], 
                              "Missing required fields in response")
        else:
            self.log_result("Core API Root", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 2: Health endpoint
        result = self.test_get_request("/api/health")
        if result["success"]:
            data = result["data"]
            if data.get("status") == "healthy":
                self.log_result("Health Check", "PASSED", result["response_time"], 
                              f"Status: {data.get('status')}")
            else:
                self.log_result("Health Check", "FAILED", result["response_time"], 
                              f"Unhealthy status: {data.get('status')}")
        else:
            self.log_result("Health Check", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_stories_endpoints(self):
        """Test Stories endpoints"""
        print("📚 Testing Stories Endpoints...")
        
        # Test 1: Story Categories
        result = self.test_get_request("/api/stories/categories")
        if result["success"]:
            data = result["data"]
            categories = data.get("categories", [])
            if len(categories) > 0:
                # Check category structure
                first_cat = categories[0]
                required_fields = ["key", "label", "emoji", "color"]
                missing_fields = [field for field in required_fields if field not in first_cat]
                if missing_fields:
                    self.log_result("Stories Categories", "FAILED", result["response_time"], 
                                  f"Missing fields: {', '.join(missing_fields)}")
                else:
                    self.log_result("Stories Categories", "PASSED", result["response_time"], 
                                  f"Found {len(categories)} categories")
            else:
                self.log_result("Stories Categories", "FAILED", result["response_time"], 
                              "No categories returned")
        else:
            self.log_result("Stories Categories", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 2: Stories List
        result = self.test_get_request("/api/stories/list?page=1&limit=5")
        if result["success"]:
            data = result["data"]
            stories = data.get("stories", [])
            total = data.get("total", 0)
            self.log_result("Stories List", "PASSED", result["response_time"], 
                          f"Found {len(stories)} stories, total: {total}")
        else:
            self.log_result("Stories List", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_ai_endpoints(self):
        """Test AI endpoints"""
        print("🤖 Testing AI Endpoints...")
        
        # Test 1: Verse of Day (Arabic)
        result = self.test_get_request("/api/ai/verse-of-day?language=ar")
        if result["success"]:
            data = result["data"]
            verse = data.get("verse", {})
            if verse.get("text") and verse.get("surah"):
                self.log_result("AI Verse of Day (AR)", "PASSED", result["response_time"], 
                              f"Verse from {verse.get('surah')}")
            else:
                self.log_result("AI Verse of Day (AR)", "FAILED", result["response_time"], 
                              "Missing verse text or surah")
        else:
            self.log_result("AI Verse of Day (AR)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 2: Hadith of Day (Arabic)
        result = self.test_get_request("/api/ai/hadith-of-day?language=ar")
        if result["success"]:
            data = result["data"]
            hadith = data.get("hadith", {})
            if hadith.get("text") and hadith.get("source"):
                self.log_result("AI Hadith of Day (AR)", "PASSED", result["response_time"], 
                              f"Hadith from {hadith.get('source')}")
            else:
                self.log_result("AI Hadith of Day (AR)", "FAILED", result["response_time"], 
                              "Missing hadith text or source")
        else:
            self.log_result("AI Hadith of Day (AR)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 3: Daily Dua
        result = self.test_get_request("/api/ai/daily-dua")
        if result["success"]:
            data = result["data"]
            dua = data.get("dua", {})
            if dua.get("text") and dua.get("source"):
                self.log_result("AI Daily Dua", "PASSED", result["response_time"], 
                              f"Dua from {dua.get('source')}")
            else:
                self.log_result("AI Daily Dua", "FAILED", result["response_time"], 
                              "Missing dua text or source")
        else:
            self.log_result("AI Daily Dua", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_prayer_endpoints(self):
        """Test Prayer endpoints"""
        print("🕌 Testing Prayer Endpoints...")
        
        # Test Prayer Times (Mecca coordinates)
        result = self.test_get_request("/api/prayer-times?lat=21.42&lon=39.82")
        if result["success"]:
            data = result["data"]
            if data.get("success") and data.get("times"):
                times = data.get("times", {})
                prayer_names = ["fajr", "dhuhr", "asr", "maghrib", "isha"]
                found_prayers = [name for name in prayer_names if name in times]
                if len(found_prayers) >= 5:
                    self.log_result("Prayer Times", "PASSED", result["response_time"], 
                                  f"Found {len(found_prayers)} prayer times")
                else:
                    self.log_result("Prayer Times", "FAILED", result["response_time"], 
                                  f"Only found {len(found_prayers)} prayer times")
            else:
                self.log_result("Prayer Times", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Prayer Times", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_quran_endpoints(self):
        """Test Quran endpoints"""
        print("📖 Testing Quran Endpoints...")
        
        # Test 1: Quran Chapters
        result = self.test_get_request("/api/quran/v4/chapters")
        if result["success"]:
            data = result["data"]
            chapters = data.get("chapters", [])
            if len(chapters) > 0:
                first_chapter = chapters[0]
                if first_chapter.get("name_simple") and first_chapter.get("id"):
                    self.log_result("Quran Chapters", "PASSED", result["response_time"], 
                                  f"Found {len(chapters)} chapters")
                else:
                    self.log_result("Quran Chapters", "FAILED", result["response_time"], 
                                  "Missing chapter fields")
            else:
                self.log_result("Quran Chapters", "FAILED", result["response_time"], 
                              "No chapters returned")
        else:
            self.log_result("Quran Chapters", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 2: Verses by Chapter (Al-Fatiha)
        result = self.test_get_request("/api/quran/v4/verses/by_chapter/1")
        if result["success"]:
            data = result["data"]
            verses = data.get("verses", [])
            if len(verses) > 0:
                self.log_result("Quran Verses by Chapter", "PASSED", result["response_time"], 
                              f"Found {len(verses)} verses in chapter 1")
            else:
                self.log_result("Quran Verses by Chapter", "FAILED", result["response_time"], 
                              "No verses returned")
        else:
            self.log_result("Quran Verses by Chapter", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 3: Surah endpoint
        result = self.test_get_request("/api/quran/surah/1")
        if result["success"]:
            data = result["data"]
            if data.get("data") and data.get("data", {}).get("name"):
                surah_data = data.get("data", {})
                if surah_data.get("name") and surah_data.get("ayahs"):
                    self.log_result("Quran Surah", "PASSED", result["response_time"], 
                                  f"Surah: {surah_data.get('name')}")
                else:
                    self.log_result("Quran Surah", "FAILED", result["response_time"], 
                                  "Missing surah fields")
            else:
                self.log_result("Quran Surah", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Quran Surah", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_hadith_endpoints(self):
        """Test Hadith endpoints"""
        print("📜 Testing Hadith Endpoints...")
        
        # Test 1: Daily Hadith (Arabic)
        result = self.test_get_request("/api/daily-hadith?language=ar")
        if result["success"]:
            data = result["data"]
            if data.get("success") and data.get("hadith"):
                hadith = data.get("hadith", {})
                if hadith.get("text") and hadith.get("source"):
                    self.log_result("Daily Hadith (AR)", "PASSED", result["response_time"], 
                                  f"Hadith from {hadith.get('source')}")
                else:
                    self.log_result("Daily Hadith (AR)", "FAILED", result["response_time"], 
                                  "Missing hadith fields")
            else:
                self.log_result("Daily Hadith (AR)", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Daily Hadith (AR)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 2: Daily Hadith (English)
        result = self.test_get_request("/api/daily-hadith?language=en")
        if result["success"]:
            data = result["data"]
            if data.get("success") and data.get("hadith"):
                hadith = data.get("hadith", {})
                if hadith.get("text") and hadith.get("source"):
                    self.log_result("Daily Hadith (EN)", "PASSED", result["response_time"], 
                                  f"Hadith from {hadith.get('source')}")
                else:
                    self.log_result("Daily Hadith (EN)", "FAILED", result["response_time"], 
                                  "Missing hadith fields")
            else:
                self.log_result("Daily Hadith (EN)", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Daily Hadith (EN)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_kids_zone_endpoints(self):
        """Test Kids Zone endpoints"""
        print("👶 Testing Kids Zone Endpoints...")
        
        # Test 1: Kids Journey
        result = self.test_get_request("/api/kids-zone/journey?user_id=test")
        if result["success"]:
            data = result["data"]
            if data.get("success") and data.get("worlds"):
                worlds = data.get("worlds", [])
                self.log_result("Kids Zone Journey", "PASSED", result["response_time"], 
                              f"Found {len(worlds)} worlds")
            else:
                self.log_result("Kids Zone Journey", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Kids Zone Journey", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 2: Kids Mosque
        result = self.test_get_request("/api/kids-zone/mosque?user_id=test")
        if result["success"]:
            data = result["data"]
            if data.get("success") and data.get("mosque"):
                mosque = data.get("mosque", {})
                if mosque.get("current_stage") and "stages" in mosque:
                    self.log_result("Kids Zone Mosque", "PASSED", result["response_time"], 
                                  f"Mosque stage: {mosque.get('current_stage', {}).get('stage', 'unknown')}")
                else:
                    self.log_result("Kids Zone Mosque", "FAILED", result["response_time"], 
                                  "Missing mosque fields")
            else:
                self.log_result("Kids Zone Mosque", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Kids Zone Mosque", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 3: Kids Learn Curriculum
        result = self.test_get_request("/api/kids-learn/curriculum")
        if result["success"]:
            data = result["data"]
            if data.get("success") and data.get("stages"):
                stages = data.get("stages", [])
                self.log_result("Kids Learn Curriculum", "PASSED", result["response_time"], 
                              f"Found {len(stages)} curriculum stages")
            else:
                self.log_result("Kids Learn Curriculum", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Kids Learn Curriculum", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 4: Kids Learn Alphabet
        result = self.test_get_request("/api/kids-learn/alphabet")
        if result["success"]:
            data = result["data"]
            if data.get("success") and data.get("letters"):
                letters = data.get("letters", [])
                total = data.get("total", len(letters))
                self.log_result("Kids Learn Alphabet", "PASSED", result["response_time"], 
                              f"Found {total} alphabet letters")
            else:
                self.log_result("Kids Learn Alphabet", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Kids Learn Alphabet", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_baraka_market_endpoints(self):
        """Test Baraka Market endpoints"""
        print("💰 Testing Baraka Market Endpoints...")
        
        # Test 1: Wallet
        result = self.test_get_request("/api/baraka/wallet/test_user")
        if result["success"]:
            data = result["data"]
            if data.get("success") and data.get("wallet"):
                wallet = data.get("wallet", {})
                if "blessing_coins" in wallet and "golden_bricks" in wallet:
                    self.log_result("Baraka Wallet", "PASSED", result["response_time"], 
                                  f"Coins: {wallet.get('blessing_coins')}, Bricks: {wallet.get('golden_bricks')}")
                else:
                    self.log_result("Baraka Wallet", "FAILED", result["response_time"], 
                                  "Missing wallet fields")
            else:
                self.log_result("Baraka Wallet", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Baraka Wallet", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 2: Leaderboard
        result = self.test_get_request("/api/baraka/leaderboard")
        if result["success"]:
            data = result["data"]
            if data.get("success") and data.get("leaderboard"):
                leaderboard = data.get("leaderboard", [])
                self.log_result("Baraka Leaderboard", "PASSED", result["response_time"], 
                              f"Found {len(leaderboard)} users")
            else:
                self.log_result("Baraka Leaderboard", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Baraka Leaderboard", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 3: Transactions
        result = self.test_get_request("/api/baraka/transactions/test_user")
        if result["success"]:
            data = result["data"]
            if data.get("success"):
                transactions = data.get("transactions", [])
                self.log_result("Baraka Transactions", "PASSED", result["response_time"], 
                              f"Found {len(transactions)} transactions")
            else:
                self.log_result("Baraka Transactions", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Baraka Transactions", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_social_endpoints(self):
        """Test Social endpoints"""
        print("👥 Testing Social Endpoints...")
        
        # Test 1: Sohba Feed Videos
        result = self.test_get_request("/api/sohba/feed/videos")
        if result["success"]:
            data = result["data"]
            if "posts" in data and "total" in data:
                posts = data.get("posts", [])
                total = data.get("total", 0)
                self.log_result("Sohba Feed Videos", "PASSED", result["response_time"], 
                              f"Found {total} videos/posts")
            else:
                self.log_result("Sohba Feed Videos", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Sohba Feed Videos", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 2: Sohba Posts
        result = self.test_get_request("/api/sohba/posts")
        if result["success"]:
            data = result["data"]
            if "posts" in data and "total" in data:
                posts = data.get("posts", [])
                total = data.get("total", 0)
                self.log_result("Sohba Posts", "PASSED", result["response_time"], 
                              f"Found {total} posts")
            else:
                self.log_result("Sohba Posts", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Sohba Posts", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_ads_endpoints(self):
        """Test Ads endpoints"""
        print("📺 Testing Ads Endpoints...")
        
        # Test 1: Ads Content
        result = self.test_get_request("/api/ads/content?placement=main&locale=ar")
        if result["success"]:
            data = result["data"]
            if data.get("success"):
                self.log_result("Ads Content", "PASSED", result["response_time"], 
                              "Ads content retrieved successfully")
            else:
                self.log_result("Ads Content", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Ads Content", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 2: Ad Config
        result = self.test_get_request("/api/ad-config")
        if result["success"]:
            data = result["data"]
            if "ads_enabled" in data and "ad_tier" in data:
                self.log_result("Ad Config", "PASSED", result["response_time"], 
                              f"Config retrieved with ads_enabled: {data.get('ads_enabled')}")
            else:
                self.log_result("Ad Config", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Ad Config", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_store_endpoints(self):
        """Test Store endpoints"""
        print("🛒 Testing Store Endpoints...")
        
        # Test 1: Store Items
        result = self.test_get_request("/api/store/items")
        if result["success"]:
            data = result["data"]
            if "items" in data:
                items = data.get("items", [])
                self.log_result("Store Items", "PASSED", result["response_time"], 
                              f"Found {len(items)} store items")
            else:
                self.log_result("Store Items", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Store Items", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 2: Marketplace Products
        result = self.test_get_request("/api/marketplace/products")
        if result["success"]:
            data = result["data"]
            if "products" in data:
                products = data.get("products", [])
                self.log_result("Marketplace Products", "PASSED", result["response_time"], 
                              f"Found {len(products)} products")
            else:
                self.log_result("Marketplace Products", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("Marketplace Products", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_99_names_endpoint(self):
        """Test 99 Names endpoint"""
        print("🕌 Testing 99 Names Endpoint...")
        
        result = self.test_get_request("/api/asma-al-husna")
        if result["success"]:
            data = result["data"]
            if data.get("names") and data.get("total"):
                names = data.get("names", [])
                total = data.get("total", 0)
                if total >= 99:
                    self.log_result("99 Names (Asma Al-Husna)", "PASSED", result["response_time"], 
                                  f"Found {total} names")
                else:
                    self.log_result("99 Names (Asma Al-Husna)", "FAILED", result["response_time"], 
                                  f"Expected 99+ names, found {total}")
            else:
                self.log_result("99 Names (Asma Al-Husna)", "FAILED", result["response_time"], 
                              "Invalid response structure")
        else:
            self.log_result("99 Names (Asma Al-Husna)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def run_comprehensive_audit(self):
        """Run comprehensive backend API audit"""
        print("🚀 Starting Comprehensive Backend API Audit...")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 80)
        
        # Run all test suites
        self.test_core_endpoints()
        self.test_stories_endpoints()
        self.test_ai_endpoints()
        self.test_prayer_endpoints()
        self.test_quran_endpoints()
        self.test_hadith_endpoints()
        self.test_kids_zone_endpoints()
        self.test_baraka_market_endpoints()
        self.test_social_endpoints()
        self.test_ads_endpoints()
        self.test_store_endpoints()
        self.test_99_names_endpoint()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE API AUDIT SUMMARY")
        print("=" * 80)
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
    tester = ComprehensiveAPITester()
    results = tester.run_comprehensive_audit()
    
    # Save results to file
    with open("/app/comprehensive_api_audit_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": results,
            "detailed_results": tester.results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed results saved to: /app/comprehensive_api_audit_results.json")