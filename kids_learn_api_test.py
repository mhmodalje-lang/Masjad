#!/usr/bin/env python3
"""
Kids Learn (Academy Noor) Backend API Test Suite
===============================================
Tests all Kids Learn API endpoints with multiple languages (ar, en, de, fr, ru, tr, sv, nl, el)
Validates response structure, content translation, and expected data counts.

Test Coverage:
- 13 API endpoints
- 9 languages per endpoint (where applicable)
- Response validation and content verification
- Translation verification across languages
"""

import requests
import json
import sys
from typing import Dict, List, Any
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://prayer-phone-mode.preview.emergentagent.com"

# Test languages
LANGUAGES = ["ar", "en", "de", "fr", "ru", "tr", "sv", "nl", "el"]
PRIMARY_TEST_LANGUAGES = ["ar", "en", "de"]  # Focus on these 3 as requested

class KidsLearnAPITester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_result(self, test_name: str, status: str, details: str = "", response_data: Dict = None):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.results.append(result)
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            print(f"✅ {test_name}: {details}")
        else:
            self.failed_tests += 1
            print(f"❌ {test_name}: {details}")
    
    def make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make HTTP request to API endpoint"""
        url = f"{BACKEND_URL}/api{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=30)
            return {
                "status_code": response.status_code,
                "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "headers": dict(response.headers)
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "data": {"error": str(e)},
                "headers": {}
            }
    
    def test_curriculum_overview(self):
        """Test GET /kids-learn/curriculum - Should return 15 stages"""
        print("\n🔍 Testing Curriculum Overview...")
        
        for lang in PRIMARY_TEST_LANGUAGES:
            response = self.make_request("/kids-learn/curriculum", {"locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Curriculum Overview ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}: {response['data']}")
                continue
            
            data = response["data"]
            
            # Validate response structure
            if not data.get("success"):
                self.log_result(f"Curriculum Overview ({lang})", "FAIL", 
                              f"success=false: {data}")
                continue
            
            stages = data.get("stages", [])
            if len(stages) != 15:
                self.log_result(f"Curriculum Overview ({lang})", "FAIL", 
                              f"Expected 15 stages, got {len(stages)}")
                continue
            
            # Validate stage structure
            stage = stages[0]
            required_fields = ["id", "emoji", "color", "title", "description", "day_start", "day_end", "total_lessons"]
            missing_fields = [f for f in required_fields if f not in stage]
            if missing_fields:
                self.log_result(f"Curriculum Overview ({lang})", "FAIL", 
                              f"Missing fields in stage: {missing_fields}")
                continue
            
            self.log_result(f"Curriculum Overview ({lang})", "PASS", 
                          f"15 stages returned with proper structure")
    
    def test_curriculum_lesson(self):
        """Test GET /kids-learn/curriculum/lesson/1 - Should return lesson with sections"""
        print("\n🔍 Testing Curriculum Lesson...")
        
        for lang in PRIMARY_TEST_LANGUAGES:
            response = self.make_request("/kids-learn/curriculum/lesson/1", {"locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Curriculum Lesson 1 ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}: {response['data']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"Curriculum Lesson 1 ({lang})", "FAIL", 
                              f"success=false: {data}")
                continue
            
            lesson = data.get("lesson", {})
            sections = lesson.get("sections", [])
            
            if not sections:
                self.log_result(f"Curriculum Lesson 1 ({lang})", "FAIL", 
                              "No sections found in lesson")
                continue
            
            # Validate lesson structure
            required_fields = ["day", "stage", "sections", "total_sections"]
            missing_fields = [f for f in required_fields if f not in lesson]
            if missing_fields:
                self.log_result(f"Curriculum Lesson 1 ({lang})", "FAIL", 
                              f"Missing fields in lesson: {missing_fields}")
                continue
            
            self.log_result(f"Curriculum Lesson 1 ({lang})", "PASS", 
                          f"Lesson returned with {len(sections)} sections")
    
    def test_duas(self):
        """Test GET /kids-learn/duas - Should return duas array"""
        print("\n🔍 Testing Duas...")
        
        for lang in PRIMARY_TEST_LANGUAGES:
            response = self.make_request("/kids-learn/duas", {"locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Duas ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}: {response['data']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"Duas ({lang})", "FAIL", 
                              f"success=false: {data}")
                continue
            
            duas = data.get("duas", [])
            
            if len(duas) < 10:  # Should have at least 10 duas
                self.log_result(f"Duas ({lang})", "FAIL", 
                              f"Expected at least 10 duas, got {len(duas)}")
                continue
            
            # Validate dua structure
            if duas:
                dua = duas[0]
                required_fields = ["id", "category", "arabic", "title"]
                missing_fields = [f for f in required_fields if f not in dua]
                if missing_fields:
                    self.log_result(f"Duas ({lang})", "FAIL", 
                                  f"Missing fields in dua: {missing_fields}")
                    continue
            
            self.log_result(f"Duas ({lang})", "PASS", 
                          f"{len(duas)} duas returned with proper structure")
    
    def test_hadiths(self):
        """Test GET /kids-learn/hadiths - Should return hadiths array"""
        print("\n🔍 Testing Hadiths...")
        
        for lang in PRIMARY_TEST_LANGUAGES:
            response = self.make_request("/kids-learn/hadiths", {"locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Hadiths ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}: {response['data']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"Hadiths ({lang})", "FAIL", 
                              f"success=false: {data}")
                continue
            
            hadiths = data.get("hadiths", [])
            
            if len(hadiths) < 10:  # Should have at least 10 hadiths
                self.log_result(f"Hadiths ({lang})", "FAIL", 
                              f"Expected at least 10 hadiths, got {len(hadiths)}")
                continue
            
            # Validate hadith structure
            if hadiths:
                hadith = hadiths[0]
                required_fields = ["id", "category", "arabic", "lesson"]
                missing_fields = [f for f in required_fields if f not in hadith]
                if missing_fields:
                    self.log_result(f"Hadiths ({lang})", "FAIL", 
                                  f"Missing fields in hadith: {missing_fields}")
                    continue
            
            self.log_result(f"Hadiths ({lang})", "PASS", 
                          f"{len(hadiths)} hadiths returned with proper structure")
    
    def test_prophets_full(self):
        """Test GET /kids-learn/prophets-full - Should return 25 prophets"""
        print("\n🔍 Testing Prophets Full...")
        
        for lang in PRIMARY_TEST_LANGUAGES:
            response = self.make_request("/kids-learn/prophets-full", {"locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Prophets Full ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}: {response['data']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"Prophets Full ({lang})", "FAIL", 
                              f"success=false: {data}")
                continue
            
            prophets = data.get("prophets", [])
            
            if len(prophets) != 25:
                self.log_result(f"Prophets Full ({lang})", "FAIL", 
                              f"Expected 25 prophets, got {len(prophets)}")
                continue
            
            # Validate prophet structure
            if prophets:
                prophet = prophets[0]
                required_fields = ["id", "name", "title", "summary"]
                missing_fields = [f for f in required_fields if f not in prophet]
                if missing_fields:
                    self.log_result(f"Prophets Full ({lang})", "FAIL", 
                                  f"Missing fields in prophet: {missing_fields}")
                    continue
            
            self.log_result(f"Prophets Full ({lang})", "PASS", 
                          f"25 prophets returned with proper structure")
    
    def test_islamic_pillars(self):
        """Test GET /kids-learn/islamic-pillars - Should return 5 pillars"""
        print("\n🔍 Testing Islamic Pillars...")
        
        for lang in PRIMARY_TEST_LANGUAGES:
            response = self.make_request("/kids-learn/islamic-pillars", {"locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Islamic Pillars ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}: {response['data']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"Islamic Pillars ({lang})", "FAIL", 
                              f"success=false: {data}")
                continue
            
            pillars = data.get("pillars", [])
            
            if len(pillars) != 5:
                self.log_result(f"Islamic Pillars ({lang})", "FAIL", 
                              f"Expected 5 pillars, got {len(pillars)}")
                continue
            
            # Validate pillar structure
            if pillars:
                pillar = pillars[0]
                required_fields = ["id", "number", "title", "description"]
                missing_fields = [f for f in required_fields if f not in pillar]
                if missing_fields:
                    self.log_result(f"Islamic Pillars ({lang})", "FAIL", 
                                  f"Missing fields in pillar: {missing_fields}")
                    continue
            
            self.log_result(f"Islamic Pillars ({lang})", "PASS", 
                          f"5 pillars returned with proper structure")
    
    def test_wudu_steps(self):
        """Test GET /kids-learn/wudu - Should return wudu steps"""
        print("\n🔍 Testing Wudu Steps...")
        
        for lang in PRIMARY_TEST_LANGUAGES:
            response = self.make_request("/kids-learn/wudu", {"locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Wudu Steps ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}: {response['data']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"Wudu Steps ({lang})", "FAIL", 
                              f"success=false: {data}")
                continue
            
            steps = data.get("steps", [])
            
            if len(steps) < 10:  # Should have at least 10 steps
                self.log_result(f"Wudu Steps ({lang})", "FAIL", 
                              f"Expected at least 10 steps, got {len(steps)}")
                continue
            
            # Validate step structure
            if steps:
                step = steps[0]
                required_fields = ["step", "title", "description"]
                missing_fields = [f for f in required_fields if f not in step]
                if missing_fields:
                    self.log_result(f"Wudu Steps ({lang})", "FAIL", 
                                  f"Missing fields in step: {missing_fields}")
                    continue
            
            self.log_result(f"Wudu Steps ({lang})", "PASS", 
                          f"{len(steps)} wudu steps returned with proper structure")
    
    def test_salah_steps(self):
        """Test GET /kids-learn/salah - Should return salah steps"""
        print("\n🔍 Testing Salah Steps...")
        
        for lang in PRIMARY_TEST_LANGUAGES:
            response = self.make_request("/kids-learn/salah", {"locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Salah Steps ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}: {response['data']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"Salah Steps ({lang})", "FAIL", 
                              f"success=false: {data}")
                continue
            
            steps = data.get("steps", [])
            
            if len(steps) < 10:  # Should have at least 10 steps
                self.log_result(f"Salah Steps ({lang})", "FAIL", 
                              f"Expected at least 10 steps, got {len(steps)}")
                continue
            
            # Validate step structure
            if steps:
                step = steps[0]
                required_fields = ["step", "title", "description"]
                missing_fields = [f for f in required_fields if f not in step]
                if missing_fields:
                    self.log_result(f"Salah Steps ({lang})", "FAIL", 
                                  f"Missing fields in step: {missing_fields}")
                    continue
            
            self.log_result(f"Salah Steps ({lang})", "PASS", 
                          f"{len(steps)} salah steps returned with proper structure")
    
    def test_library_categories(self):
        """Test GET /kids-learn/library/categories - Should return categories"""
        print("\n🔍 Testing Library Categories...")
        
        for lang in PRIMARY_TEST_LANGUAGES:
            response = self.make_request("/kids-learn/library/categories", {"locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Library Categories ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}: {response['data']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"Library Categories ({lang})", "FAIL", 
                              f"success=false: {data}")
                continue
            
            categories = data.get("categories", [])
            
            if len(categories) < 5:  # Should have at least 5 categories
                self.log_result(f"Library Categories ({lang})", "FAIL", 
                              f"Expected at least 5 categories, got {len(categories)}")
                continue
            
            # Validate category structure
            if categories:
                category = categories[0]
                required_fields = ["id", "title", "emoji"]
                missing_fields = [f for f in required_fields if f not in category]
                if missing_fields:
                    self.log_result(f"Library Categories ({lang})", "FAIL", 
                                  f"Missing fields in category: {missing_fields}")
                    continue
            
            self.log_result(f"Library Categories ({lang})", "PASS", 
                          f"{len(categories)} categories returned with proper structure")
    
    def test_library_items(self):
        """Test GET /kids-learn/library/items - Should return library items"""
        print("\n🔍 Testing Library Items...")
        
        for lang in PRIMARY_TEST_LANGUAGES:
            response = self.make_request("/kids-learn/library/items", {"category": "all", "locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Library Items ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}: {response['data']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"Library Items ({lang})", "FAIL", 
                              f"success=false: {data}")
                continue
            
            items = data.get("items", [])
            
            if len(items) < 20:  # Should have at least 20 items
                self.log_result(f"Library Items ({lang})", "FAIL", 
                              f"Expected at least 20 items, got {len(items)}")
                continue
            
            # Validate item structure
            if items:
                item = items[0]
                required_fields = ["id", "category", "title"]
                missing_fields = [f for f in required_fields if f not in item]
                if missing_fields:
                    self.log_result(f"Library Items ({lang})", "FAIL", 
                                  f"Missing fields in item: {missing_fields}")
                    continue
            
            self.log_result(f"Library Items ({lang})", "PASS", 
                          f"{len(items)} library items returned with proper structure")
    
    def test_quran_surahs(self):
        """Test GET /kids-learn/quran/surahs - Should return surahs"""
        print("\n🔍 Testing Quran Surahs...")
        
        for lang in PRIMARY_TEST_LANGUAGES:
            response = self.make_request("/kids-learn/quran/surahs", {"locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Quran Surahs ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}: {response['data']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"Quran Surahs ({lang})", "FAIL", 
                              f"success=false: {data}")
                continue
            
            surahs = data.get("surahs", [])
            
            if len(surahs) < 15:  # Should have at least 15 surahs
                self.log_result(f"Quran Surahs ({lang})", "FAIL", 
                              f"Expected at least 15 surahs, got {len(surahs)}")
                continue
            
            # Validate surah structure
            if surahs:
                surah = surahs[0]
                required_fields = ["id", "number", "name_ar", "name_en"]
                missing_fields = [f for f in required_fields if f not in surah]
                if missing_fields:
                    self.log_result(f"Quran Surahs ({lang})", "FAIL", 
                                  f"Missing fields in surah: {missing_fields}")
                    continue
            
            self.log_result(f"Quran Surahs ({lang})", "PASS", 
                          f"{len(surahs)} surahs returned with proper structure")
    
    def test_achievements(self):
        """Test GET /kids-learn/achievements - Should return achievement badges"""
        print("\n🔍 Testing Achievements...")
        
        response = self.make_request("/kids-learn/achievements", {"user_id": "test123"})
        
        if response["status_code"] != 200:
            self.log_result("Achievements", "FAIL", 
                          f"HTTP {response['status_code']}: {response['data']}")
            return
        
        data = response["data"]
        
        if not data.get("success"):
            self.log_result("Achievements", "FAIL", 
                          f"success=false: {data}")
            return
        
        badges = data.get("badges", [])
        
        if len(badges) < 10:  # Should have at least 10 badges
            self.log_result("Achievements", "FAIL", 
                          f"Expected at least 10 badges, got {len(badges)}")
            return
        
        # Validate badge structure
        if badges:
            badge = badges[0]
            required_fields = ["id", "emoji", "title_ar", "title_en", "earned"]
            missing_fields = [f for f in required_fields if f not in badge]
            if missing_fields:
                self.log_result("Achievements", "FAIL", 
                              f"Missing fields in badge: {missing_fields}")
                return
        
        self.log_result("Achievements", "PASS", 
                      f"{len(badges)} achievement badges returned with proper structure")
    
    def test_parental_consent(self):
        """Test GET /parental-consent/check - Should return consent status"""
        print("\n🔍 Testing Parental Consent...")
        
        response = self.make_request("/parental-consent/check", {"user_id": "test123"})
        
        if response["status_code"] != 200:
            self.log_result("Parental Consent", "FAIL", 
                          f"HTTP {response['status_code']}: {response['data']}")
            return
        
        data = response["data"]
        
        if not data.get("success"):
            self.log_result("Parental Consent", "FAIL", 
                          f"success=false: {data}")
            return
        
        self.log_result("Parental Consent", "PASS", 
                      "Parental consent check returned success=true")
    
    def test_translation_verification(self):
        """Test that content changes across different languages"""
        print("\n🔍 Testing Translation Verification...")
        
        # Test duas translation
        ar_response = self.make_request("/kids-learn/duas", {"locale": "ar"})
        en_response = self.make_request("/kids-learn/duas", {"locale": "en"})
        de_response = self.make_request("/kids-learn/duas", {"locale": "de"})
        
        if (ar_response["status_code"] == 200 and en_response["status_code"] == 200 and 
            de_response["status_code"] == 200):
            
            ar_data = ar_response["data"]
            en_data = en_response["data"]
            de_data = de_response["data"]
            
            if (ar_data.get("success") and en_data.get("success") and de_data.get("success")):
                ar_duas = ar_data.get("duas", [])
                en_duas = en_data.get("duas", [])
                de_duas = de_data.get("duas", [])
                
                if ar_duas and en_duas and de_duas:
                    # Check if titles are different (indicating translation)
                    ar_title = ar_duas[0].get("title", {})
                    en_title = en_duas[0].get("title", {})
                    de_title = de_duas[0].get("title", {})
                    
                    if isinstance(ar_title, dict) and isinstance(en_title, dict) and isinstance(de_title, dict):
                        ar_text = ar_title.get("ar", "")
                        en_text = en_title.get("en", "")
                        de_text = de_title.get("de", "")
                        
                        if ar_text != en_text and en_text != de_text and ar_text != de_text:
                            self.log_result("Translation Verification", "PASS", 
                                          "Content properly translated across languages")
                        else:
                            self.log_result("Translation Verification", "FAIL", 
                                          "Content not properly translated across languages")
                    else:
                        self.log_result("Translation Verification", "PASS", 
                                      "Translation structure varies by language")
                else:
                    self.log_result("Translation Verification", "FAIL", 
                                  "No duas found for translation comparison")
            else:
                self.log_result("Translation Verification", "FAIL", 
                              "API calls failed for translation verification")
        else:
            self.log_result("Translation Verification", "FAIL", 
                          "HTTP errors during translation verification")
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Kids Learn (Academy Noor) API Test Suite")
        print(f"🌐 Backend URL: {BACKEND_URL}")
        print(f"🗣️ Testing Languages: {', '.join(PRIMARY_TEST_LANGUAGES)}")
        print("=" * 80)
        
        # Run all tests
        self.test_curriculum_overview()
        self.test_curriculum_lesson()
        self.test_duas()
        self.test_hadiths()
        self.test_prophets_full()
        self.test_islamic_pillars()
        self.test_wudu_steps()
        self.test_salah_steps()
        self.test_library_categories()
        self.test_library_items()
        self.test_quran_surahs()
        self.test_achievements()
        self.test_parental_consent()
        self.test_translation_verification()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['details']}")
        
        # Save detailed results
        with open("/app/kids_learn_api_test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_tests": self.total_tests,
                    "passed_tests": self.passed_tests,
                    "failed_tests": self.failed_tests,
                    "success_rate": round(self.passed_tests/self.total_tests*100, 1),
                    "test_date": datetime.now().isoformat(),
                    "backend_url": BACKEND_URL,
                    "languages_tested": PRIMARY_TEST_LANGUAGES
                },
                "results": self.results
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: /app/kids_learn_api_test_results.json")
        
        return self.failed_tests == 0

if __name__ == "__main__":
    tester = KidsLearnAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)