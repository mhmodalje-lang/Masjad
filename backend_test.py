#!/usr/bin/env python3
"""
Noor Academy (Kids Learning) Backend API Testing
Testing enriched content for stages 6-15 and expanded Quran surahs
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

    def test_curriculum_lessons(self):
        """Test curriculum lessons for advanced stages (S06-S15)"""
        print("🎓 Testing Curriculum Lessons for Advanced Stages...")
        
        # Test specific lesson IDs for each stage
        test_lessons = [
            {"day": 267, "stage": "S06", "name": "Reading Practice", "expected_sections": 4, "section_types": ["read", "listen", "quiz", "write"]},
            {"day": 309, "stage": "S07", "name": "Islamic Foundations", "expected_sections": 3, "section_types": ["learn", "memorize", "quiz"]},
            {"day": 385, "stage": "S08", "name": "Quran", "expected_sections": 4, "section_types": ["quran", "listen", "memorize", "quiz"]},
            {"day": 500, "stage": "S09", "name": "Duas", "expected_sections": 4, "section_types": ["dua", "memorize", "listen", "quiz"]},
            {"day": 570, "stage": "S10", "name": "Hadiths", "expected_sections": 3, "section_types": ["hadith", "reflect", "quiz"]},
            {"day": 640, "stage": "S11", "name": "Prophet Stories", "expected_sections": 3, "section_types": ["story", "lesson", "quiz"]},
            {"day": 725, "stage": "S12", "name": "Islamic Life", "expected_sections": 3, "section_types": ["learn", "practice", "quiz"]},
            {"day": 815, "stage": "S13", "name": "Advanced Arabic", "expected_sections": 3, "section_types": ["grammar", "practice", "quiz"]},
            {"day": 910, "stage": "S14", "name": "Advanced Quran", "expected_sections": 3, "section_types": ["quran", "tajweed", "memorize"]},
            {"day": 965, "stage": "S15", "name": "Mastery", "expected_sections": 3, "section_types": ["review", "quiz", "memorize"]}
        ]
        
        for lesson_info in test_lessons:
            day = lesson_info["day"]
            stage = lesson_info["stage"]
            name = lesson_info["name"]
            
            # Test Arabic locale
            result = self.test_endpoint(f"/api/kids-learn/curriculum/lesson/{day}?locale=ar")
            
            if result["success"]:
                data = result["data"]
                
                # Check basic structure
                if not data.get("success"):
                    self.log_result(f"Lesson {day} ({stage} - {name}) - Arabic", "FAILED", 
                                  result["response_time"], "Response success=false")
                    continue
                
                lesson = data.get("lesson", {})
                sections = lesson.get("sections", [])
                
                # Check if lesson has content
                if not sections:
                    self.log_result(f"Lesson {day} ({stage} - {name}) - Arabic", "FAILED", 
                                  result["response_time"], "No sections found in lesson")
                    continue
                
                # Check minimum sections (at least 2)
                if len(sections) < 2:
                    self.log_result(f"Lesson {day} ({stage} - {name}) - Arabic", "FAILED", 
                                  result["response_time"], f"Only {len(sections)} sections, expected at least 2")
                    continue
                
                # Check for meaningful content in sections
                has_content = False
                section_details = []
                for section in sections:
                    section_type = section.get("type", "unknown")
                    section_title = section.get("title", "")
                    section_content = section.get("content", {})
                    
                    section_details.append(f"{section_type}: {section_title}")
                    
                    # Check if section has meaningful content
                    if section_content and (
                        section_content.get("arabic") or 
                        section_content.get("text") or 
                        section_content.get("question") or
                        section_content.get("tip") or
                        section_content.get("surah") or
                        section_content.get("story")
                    ):
                        has_content = True
                
                if not has_content:
                    self.log_result(f"Lesson {day} ({stage} - {name}) - Arabic", "FAILED", 
                                  result["response_time"], "No meaningful content found in sections")
                    continue
                
                # Check for Arabic content
                has_arabic = False
                for section in sections:
                    content = section.get("content", {})
                    if content.get("arabic") or any("ا" in str(v) or "ب" in str(v) or "ت" in str(v) for v in content.values() if isinstance(v, str)):
                        has_arabic = True
                        break
                
                if not has_arabic:
                    self.log_result(f"Lesson {day} ({stage} - {name}) - Arabic", "FAILED", 
                                  result["response_time"], "No Arabic content found")
                    continue
                
                self.log_result(f"Lesson {day} ({stage} - {name}) - Arabic", "PASSED", 
                              result["response_time"], 
                              f"{len(sections)} sections: {', '.join(section_details)}")
                
            else:
                self.log_result(f"Lesson {day} ({stage} - {name}) - Arabic", "FAILED", 
                              result["response_time"], result.get("error", "Unknown error"))

    def test_quran_surahs_list(self):
        """Test Quran surahs list - should return 15 surahs total"""
        print("📖 Testing Quran Surahs List...")
        
        result = self.test_endpoint("/api/kids-learn/quran/surahs?locale=ar")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Quran Surahs List", "FAILED", result["response_time"], "Response success=false")
                return
            
            surahs = data.get("surahs", [])
            total = data.get("total", 0)
            
            if total != 15:
                self.log_result("Quran Surahs List", "FAILED", result["response_time"], 
                              f"Expected 15 surahs, got {total}")
                return
            
            if len(surahs) != 15:
                self.log_result("Quran Surahs List", "FAILED", result["response_time"], 
                              f"Expected 15 surahs in list, got {len(surahs)}")
                return
            
            # Check for required fields in each surah
            missing_fields = []
            surah_names = []
            for surah in surahs:
                surah_names.append(surah.get("name_ar", "Unknown"))
                required_fields = ["id", "number", "name_ar", "name_en", "total_ayahs"]
                for field in required_fields:
                    if field not in surah:
                        missing_fields.append(f"{surah.get('name_ar', 'Unknown')}: missing {field}")
            
            if missing_fields:
                self.log_result("Quran Surahs List", "FAILED", result["response_time"], 
                              f"Missing fields: {', '.join(missing_fields[:3])}")
                return
            
            self.log_result("Quran Surahs List", "PASSED", result["response_time"], 
                          f"15 surahs found: {', '.join(surah_names[:5])}...")
            
        else:
            self.log_result("Quran Surahs List", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_new_surah_details(self):
        """Test new surah details (fil, kafiroon, zilzal)"""
        print("🕌 Testing New Surah Details...")
        
        test_surahs = [
            {"id": "fil", "name": "Al-Fil", "expected_ayahs": 5},
            {"id": "kafiroon", "name": "Al-Kafiroon", "expected_ayahs": 6},
            {"id": "zilzal", "name": "Az-Zilzal", "expected_ayahs": 8}
        ]
        
        for surah_info in test_surahs:
            surah_id = surah_info["id"]
            name = surah_info["name"]
            expected_ayahs = surah_info["expected_ayahs"]
            
            result = self.test_endpoint(f"/api/kids-learn/quran/surah/{surah_id}?locale=ar")
            
            if result["success"]:
                data = result["data"]
                
                if not data.get("success"):
                    self.log_result(f"Surah {name} ({surah_id})", "FAILED", result["response_time"], 
                                  "Response success=false")
                    continue
                
                surah = data.get("surah", {})
                ayahs = surah.get("ayahs", [])
                
                if len(ayahs) != expected_ayahs:
                    self.log_result(f"Surah {name} ({surah_id})", "FAILED", result["response_time"], 
                                  f"Expected {expected_ayahs} ayahs, got {len(ayahs)}")
                    continue
                
                # Check ayah structure
                missing_fields = []
                has_arabic = False
                for i, ayah in enumerate(ayahs):
                    if "arabic" not in ayah:
                        missing_fields.append(f"ayah {i+1}: missing arabic")
                    elif ayah["arabic"] and any(char in ayah["arabic"] for char in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"):
                        has_arabic = True
                    
                    if "translation" not in ayah:
                        missing_fields.append(f"ayah {i+1}: missing translation")
                
                if missing_fields:
                    self.log_result(f"Surah {name} ({surah_id})", "FAILED", result["response_time"], 
                                  f"Missing fields: {', '.join(missing_fields[:3])}")
                    continue
                
                if not has_arabic:
                    self.log_result(f"Surah {name} ({surah_id})", "FAILED", result["response_time"], 
                                  "No Arabic text found in ayahs")
                    continue
                
                self.log_result(f"Surah {name} ({surah_id})", "PASSED", result["response_time"], 
                              f"{len(ayahs)} ayahs with Arabic and translations")
                
            else:
                self.log_result(f"Surah {name} ({surah_id})", "FAILED", result["response_time"], 
                              result.get("error", "Unknown error"))

    def test_english_locale_support(self):
        """Test English locale support"""
        print("🌍 Testing English Locale Support...")
        
        # Test curriculum lesson in English
        result = self.test_endpoint("/api/kids-learn/curriculum/lesson/310?locale=en")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("English Curriculum Lesson", "FAILED", result["response_time"], 
                              "Response success=false")
            else:
                lesson = data.get("lesson", {})
                sections = lesson.get("sections", [])
                
                if not sections:
                    self.log_result("English Curriculum Lesson", "FAILED", result["response_time"], 
                                  "No sections found")
                else:
                    # Check for English content
                    has_english = False
                    for section in sections:
                        content = section.get("content", {})
                        title = section.get("title", "")
                        
                        # Look for English text (contains common English words)
                        english_indicators = ["the", "and", "of", "to", "in", "is", "you", "that", "it", "with", "for", "as", "was", "on", "are", "this"]
                        text_to_check = f"{title} {str(content)}".lower()
                        
                        if any(word in text_to_check for word in english_indicators):
                            has_english = True
                            break
                    
                    if has_english:
                        self.log_result("English Curriculum Lesson", "PASSED", result["response_time"], 
                                      f"{len(sections)} sections with English content")
                    else:
                        self.log_result("English Curriculum Lesson", "FAILED", result["response_time"], 
                                      "No English content found")
        else:
            self.log_result("English Curriculum Lesson", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test surah in English
        result = self.test_endpoint("/api/kids-learn/quran/surah/fil?locale=en")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("English Surah Al-Fil", "FAILED", result["response_time"], 
                              "Response success=false")
            else:
                surah = data.get("surah", {})
                ayahs = surah.get("ayahs", [])
                
                if not ayahs:
                    self.log_result("English Surah Al-Fil", "FAILED", result["response_time"], 
                                  "No ayahs found")
                else:
                    # Check for English translations
                    has_english_translation = False
                    for ayah in ayahs:
                        translation = ayah.get("translation", "")
                        if translation and any(char.isalpha() and ord(char) < 128 for char in translation):
                            has_english_translation = True
                            break
                    
                    if has_english_translation:
                        self.log_result("English Surah Al-Fil", "PASSED", result["response_time"], 
                                      f"{len(ayahs)} ayahs with English translations")
                    else:
                        self.log_result("English Surah Al-Fil", "FAILED", result["response_time"], 
                                      "No English translations found")
        else:
            self.log_result("English Surah Al-Fil", "FAILED", result["response_time"], 
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
        print("🚀 Starting Noor Academy Backend API Tests...")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 60)
        
        # Run all test suites
        self.test_api_health()
        self.test_curriculum_lessons()
        self.test_quran_surahs_list()
        self.test_new_surah_details()
        self.test_english_locale_support()
        
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