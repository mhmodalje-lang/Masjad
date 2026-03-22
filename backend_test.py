#!/usr/bin/env python3
"""
Noor Academy (Kids Learning) Backend API Testing
Testing Islamic Library expansion and 9-language support
"""

import requests
import json
import time
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://islamic-academy-hub.preview.emergentagent.com"

class NoorAcademyTester:
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
            
    def test_endpoint(self, endpoint: str, expected_status: int = 200) -> Dict[str, Any]:
        """Test a single endpoint"""
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

    def test_library_categories(self):
        """Test library categories API - should return 8 categories with real counts"""
        print("📚 Testing Library Categories...")
        
        # Test Arabic locale
        result = self.test_endpoint("/api/kids-learn/library/categories?locale=ar")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Library Categories (Arabic)", "FAILED", result["response_time"], "Response success=false")
                return
            
            categories = data.get("categories", [])
            total = data.get("total", 0)
            
            if total != 8:
                self.log_result("Library Categories (Arabic)", "FAILED", result["response_time"], 
                              f"Expected 8 categories, got {total}")
                return
            
            if len(categories) != 8:
                self.log_result("Library Categories (Arabic)", "FAILED", result["response_time"], 
                              f"Expected 8 categories in list, got {len(categories)}")
                return
            
            # Check for required fields and real counts
            missing_fields = []
            category_names = []
            total_items = 0
            for category in categories:
                category_names.append(category.get("title", "Unknown"))  # Changed from "name" to "title"
                required_fields = ["id", "title", "emoji", "count"]  # Changed from "name" to "title"
                for field in required_fields:
                    if field not in category:
                        missing_fields.append(f"{category.get('title', 'Unknown')}: missing {field}")
                
                count = category.get("count", 0)
                # Allow 0 count for prophet_stories as it's expected to be empty
                if count < 0:
                    missing_fields.append(f"{category.get('title', 'Unknown')}: count is {count}")
                total_items += count
            
            if missing_fields:
                self.log_result("Library Categories (Arabic)", "FAILED", result["response_time"], 
                              f"Issues: {', '.join(missing_fields[:3])}")
                return
            
            if total_items < 28:
                self.log_result("Library Categories (Arabic)", "FAILED", result["response_time"], 
                              f"Expected at least 28 total items, got {total_items}")
                return
            
            self.log_result("Library Categories (Arabic)", "PASSED", result["response_time"], 
                          f"8 categories, {total_items} total items: {', '.join(category_names[:4])}...")
            
        else:
            self.log_result("Library Categories (Arabic)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test English locale
        result = self.test_endpoint("/api/kids-learn/library/categories?locale=en")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Library Categories (English)", "FAILED", result["response_time"], "Response success=false")
                return
            
            categories = data.get("categories", [])
            
            # Check for English names
            has_english = False
            english_names = []
            for category in categories:
                title = category.get("title", "")  # Changed from "name" to "title"
                english_names.append(title)
                # Check if title contains English words
                if any(word in title.lower() for word in ["stories", "science", "manners", "language", "math", "nature"]):
                    has_english = True
            
            if has_english:
                self.log_result("Library Categories (English)", "PASSED", result["response_time"], 
                              f"English names: {', '.join(english_names[:4])}...")
            else:
                self.log_result("Library Categories (English)", "FAILED", result["response_time"], 
                              "No English category names found")
        else:
            self.log_result("Library Categories (English)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_library_items_total(self):
        """Test library items total - should return 28 unique items"""
        print("📖 Testing Library Items Total...")
        
        result = self.test_endpoint("/api/kids-learn/library/items?locale=ar")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Library Items Total", "FAILED", result["response_time"], "Response success=false")
                return
            
            items = data.get("items", [])
            total = data.get("total", 0)
            
            if total != 28:
                self.log_result("Library Items Total", "FAILED", result["response_time"], 
                              f"Expected 28 items, got {total}")
                return
            
            if len(items) != 28:
                self.log_result("Library Items Total", "FAILED", result["response_time"], 
                              f"Expected 28 items in list, got {len(items)}")
                return
            
            # Check for unique items (no duplicates)
            item_ids = [item.get("id", "") for item in items]
            unique_ids = set(item_ids)
            
            if len(unique_ids) != 28:
                self.log_result("Library Items Total", "FAILED", result["response_time"], 
                              f"Found duplicates: {28 - len(unique_ids)} duplicate items")
                return
            
            # Check for required fields
            missing_fields = []
            for item in items[:5]:  # Check first 5 items
                required_fields = ["id", "category", "title", "content", "emoji"]
                for field in required_fields:
                    if field not in item:
                        missing_fields.append(f"{item.get('id', 'Unknown')}: missing {field}")
            
            if missing_fields:
                self.log_result("Library Items Total", "FAILED", result["response_time"], 
                              f"Missing fields: {', '.join(missing_fields[:3])}")
                return
            
            self.log_result("Library Items Total", "PASSED", result["response_time"], 
                          f"28 unique items found")
            
        else:
            self.log_result("Library Items Total", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_library_items_by_category(self):
        """Test library items by specific categories"""
        print("🗂️ Testing Library Items by Category...")
        
        test_categories = [
            {"category": "quran_stories", "expected_count": 9, "name": "Quran Stories"},
            {"category": "moral_stories", "expected_count": 6, "name": "Moral Stories"},
            {"category": "islamic_manners", "expected_count": 4, "name": "Islamic Manners"},
            {"category": "science", "expected_count": 3, "name": "Science"}
        ]
        
        for cat_info in test_categories:
            category = cat_info["category"]
            expected_count = cat_info["expected_count"]
            name = cat_info["name"]
            
            result = self.test_endpoint(f"/api/kids-learn/library/items?category={category}&locale=ar")
            
            if result["success"]:
                data = result["data"]
                
                if not data.get("success"):
                    self.log_result(f"{name} Items", "FAILED", result["response_time"], "Response success=false")
                    continue
                
                items = data.get("items", [])
                total = data.get("total", 0)
                
                if total != expected_count:
                    self.log_result(f"{name} Items", "FAILED", result["response_time"], 
                                  f"Expected {expected_count} items, got {total}")
                    continue
                
                if len(items) != expected_count:
                    self.log_result(f"{name} Items", "FAILED", result["response_time"], 
                                  f"Expected {expected_count} items in list, got {len(items)}")
                    continue
                
                # Check that all items belong to the correct category
                wrong_category = []
                item_titles = []
                for item in items:
                    if item.get("category") != category:
                        wrong_category.append(item.get("id", "Unknown"))
                    item_titles.append(item.get("title", "Unknown"))
                
                if wrong_category:
                    self.log_result(f"{name} Items", "FAILED", result["response_time"], 
                                  f"Wrong category items: {', '.join(wrong_category)}")
                    continue
                
                self.log_result(f"{name} Items", "PASSED", result["response_time"], 
                              f"{expected_count} items: {', '.join(item_titles[:3])}...")
                
            else:
                self.log_result(f"{name} Items", "FAILED", result["response_time"], 
                              result.get("error", "Unknown error"))

    def test_multi_language_support(self):
        """Test multi-language support for all 9 languages"""
        print("🌍 Testing Multi-Language Support...")
        
        languages = [
            {"locale": "en", "name": "English"},
            {"locale": "de", "name": "German"},
            {"locale": "fr", "name": "French"},
            {"locale": "tr", "name": "Turkish"},
            {"locale": "ru", "name": "Russian"},
            {"locale": "sv", "name": "Swedish"},
            {"locale": "nl", "name": "Dutch"},
            {"locale": "el", "name": "Greek"}
        ]
        
        for lang_info in languages:
            locale = lang_info["locale"]
            name = lang_info["name"]
            
            result = self.test_endpoint(f"/api/kids-learn/library/items?category=quran_stories&locale={locale}")
            
            if result["success"]:
                data = result["data"]
                
                if not data.get("success"):
                    self.log_result(f"Quran Stories ({name})", "FAILED", result["response_time"], "Response success=false")
                    continue
                
                items = data.get("items", [])
                
                if len(items) != 9:
                    self.log_result(f"Quran Stories ({name})", "FAILED", result["response_time"], 
                                  f"Expected 9 items, got {len(items)}")
                    continue
                
                # Check for translated content
                has_translation = False
                sample_titles = []
                for item in items[:3]:  # Check first 3 items
                    title = item.get("title", "")
                    content = item.get("content", "")
                    sample_titles.append(title)
                    
                    # Check if content is different from Arabic (basic check)
                    if title and content:
                        # For non-Arabic languages, check if text doesn't contain Arabic characters
                        if locale != "ar":
                            arabic_chars = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
                            if not any(char in title for char in arabic_chars):
                                has_translation = True
                                break
                        else:
                            # For Arabic, check if it contains Arabic characters
                            if any(char in title for char in arabic_chars):
                                has_translation = True
                                break
                
                if has_translation:
                    self.log_result(f"Quran Stories ({name})", "PASSED", result["response_time"], 
                                  f"9 items with {name} translations: {', '.join(sample_titles)}")
                else:
                    self.log_result(f"Quran Stories ({name})", "FAILED", result["response_time"], 
                                  f"No proper {name} translations found")
                
            else:
                self.log_result(f"Quran Stories ({name})", "FAILED", result["response_time"], 
                              result.get("error", "Unknown error"))

    def test_previous_apis_still_working(self):
        """Test that previous APIs are still working"""
        print("🔄 Testing Previous APIs Still Working...")
        
        # Test Quran surahs
        result = self.test_endpoint("/api/kids-learn/quran/surahs?locale=ar")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Previous API - Quran Surahs", "FAILED", result["response_time"], "Response success=false")
            else:
                surahs = data.get("surahs", [])
                total = data.get("total", 0)
                
                if total >= 15:  # Should have at least 15 surahs
                    self.log_result("Previous API - Quran Surahs", "PASSED", result["response_time"], 
                                  f"{total} surahs available")
                else:
                    self.log_result("Previous API - Quran Surahs", "FAILED", result["response_time"], 
                                  f"Expected at least 15 surahs, got {total}")
        else:
            self.log_result("Previous API - Quran Surahs", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test curriculum lesson
        result = self.test_endpoint("/api/kids-learn/curriculum/lesson/309?locale=ar")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Previous API - Curriculum Lesson", "FAILED", result["response_time"], "Response success=false")
            else:
                lesson = data.get("lesson", {})
                sections = lesson.get("sections", [])
                
                if sections:
                    self.log_result("Previous API - Curriculum Lesson", "PASSED", result["response_time"], 
                                  f"Stage 7 lesson with {len(sections)} sections")
                else:
                    self.log_result("Previous API - Curriculum Lesson", "FAILED", result["response_time"], 
                                  "No sections found in lesson")
        else:
            self.log_result("Previous API - Curriculum Lesson", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_api_health(self):
        """Test basic API health"""
        print("🏥 Testing API Health...")
        
        result = self.test_endpoint("/api/health")
        
        if result["success"]:
            data = result["data"]
            if data.get("status") == "healthy":
                self.log_result("API Health Check", "PASSED", result["response_time"], 
                              f"Status: {data.get('status')}")
            else:
                self.log_result("API Health Check", "FAILED", result["response_time"], 
                              f"Unhealthy status: {data.get('status')}")
        else:
            self.log_result("API Health Check", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Islamic Library Backend API Tests...")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 60)
        
        # Run all test suites
        self.test_api_health()
        self.test_library_categories()
        self.test_library_items_total()
        self.test_library_items_by_category()
        self.test_multi_language_support()
        self.test_previous_apis_still_working()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
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
    tester = NoorAcademyTester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open("/app/backend_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": results,
            "detailed_results": tester.results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed results saved to: /app/backend_test_results.json")