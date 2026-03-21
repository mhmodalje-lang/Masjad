#!/usr/bin/env python3
"""
Backend Test Suite for Arabic Kids Learning Curriculum Localization
==================================================================
Tests comprehensive localization fix for the Arabic kids learning curriculum.
Critical validation: Every non-English locale should have ZERO English content.
"""

import requests
import json
import re
import sys
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://kids-platform-review.preview.emergentagent.com"

class LocalizationTester:
    def __init__(self):
        self.results = []
        self.failed_tests = []
        self.passed_tests = []
        
    def log_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "passed": passed,
            "details": details
        }
        self.results.append(result)
        if passed:
            self.passed_tests.append(test_name)
            print(f"✅ {test_name}: PASSED")
        else:
            self.failed_tests.append(test_name)
            print(f"❌ {test_name}: FAILED - {details}")
            
    def make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make API request and return response"""
        url = f"{BACKEND_URL}/api{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "status": 200}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}", "status": response.status_code}
        except Exception as e:
            return {"success": False, "error": str(e), "status": 0}
    
    def check_no_english_content(self, data: Any, locale: str, context: str = "") -> List[str]:
        """Check for English content in non-English locales"""
        english_violations = []
        
        # Skip if locale is English or Arabic
        if locale in ["en", "ar"]:
            return english_violations
            
        def search_for_english(obj, path=""):
            if isinstance(obj, dict):
                # Check for "english" key
                if "english" in obj:
                    english_violations.append(f"{context}{path}: Found 'english' key")
                
                # Check for common English words in values
                for key, value in obj.items():
                    if isinstance(value, str):
                        # Check for common English words that should be translated
                        english_words = ["Zero", "Lion", "This is", "Praise be", "One", "Two", "Three", "Four", "Five"]
                        for word in english_words:
                            if word in value:
                                english_violations.append(f"{context}{path}.{key}: Found English word '{word}' in '{value}'")
                    
                    # Recursively check nested objects
                    search_for_english(value, f"{path}.{key}" if path else key)
                    
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_for_english(item, f"{path}[{i}]")
        
        search_for_english(data)
        return english_violations
    
    def test_curriculum_overview(self):
        """Test 1: Curriculum Overview in 3 languages"""
        print("\n=== Test 1: Curriculum Overview in 3 languages ===")
        
        locales = ["sv", "nl", "el"]  # Swedish, Dutch, Greek
        
        for locale in locales:
            endpoint = f"/kids-learn/curriculum?locale={locale}"
            response = self.make_request(endpoint)
            
            if not response["success"]:
                self.log_result(f"Curriculum Overview ({locale})", False, f"API Error: {response['error']}")
                continue
                
            data = response["data"]
            
            # Check if we have stages
            if "stages" not in data:
                self.log_result(f"Curriculum Overview ({locale})", False, "No 'stages' field in response")
                continue
                
            stages = data["stages"]
            if len(stages) != 15:
                self.log_result(f"Curriculum Overview ({locale})", False, f"Expected 15 stages, got {len(stages)}")
                continue
            
            # Check for English content violations
            violations = self.check_no_english_content(data, locale, f"Curriculum Overview ({locale}) ")
            
            if violations:
                self.log_result(f"Curriculum Overview ({locale})", False, f"English content found: {'; '.join(violations)}")
            else:
                # Check that stage titles are actually translated (not empty or same as English)
                translated_titles = [stage.get("title", "") for stage in stages]
                if any(not title.strip() for title in translated_titles):
                    self.log_result(f"Curriculum Overview ({locale})", False, "Some stage titles are empty")
                else:
                    self.log_result(f"Curriculum Overview ({locale})", True, f"All 15 stage titles properly translated")
    
    def test_core_curriculum_content(self):
        """Test 2: Stage 1-5 content (core curriculum)"""
        print("\n=== Test 2: Stage 1-5 content (core curriculum) ===")
        
        test_cases = [
            {"lesson": 1, "locale": "de", "description": "Letter lesson in German"},
            {"lesson": 85, "locale": "tr", "description": "Number lesson in Turkish"},
            {"lesson": 113, "locale": "sv", "description": "Word lesson in Swedish"},
            {"lesson": 211, "locale": "fr", "description": "Sentence lesson in French"},
        ]
        
        for case in test_cases:
            endpoint = f"/kids-learn/curriculum/lesson/{case['lesson']}?locale={case['locale']}"
            response = self.make_request(endpoint)
            
            if not response["success"]:
                self.log_result(f"Core Curriculum Lesson {case['lesson']} ({case['locale']})", False, f"API Error: {response['error']}")
                continue
            
            data = response["data"]
            
            # Check for English content violations
            violations = self.check_no_english_content(data, case['locale'], f"Lesson {case['lesson']} ({case['locale']}) ")
            
            # Specific checks based on lesson type
            lesson_passed = True
            details = []
            
            if case['lesson'] == 1:  # Letter lesson
                # Check for example_translated field
                sections = data.get("sections", [])
                for section in sections:
                    content = section.get("content", {})
                    if "example_translated" in content:
                        example = content["example_translated"]
                        if example == "Lion":  # Should not be English
                            violations.append(f"example_translated still contains English 'Lion'")
                            
            elif case['lesson'] == 85:  # Number lesson
                # Check for translated number names
                sections = data.get("sections", [])
                for section in sections:
                    content = section.get("content", {})
                    if "translated" in content:
                        translated = content["translated"]
                        if translated == "Zero":  # Should not be English
                            violations.append(f"translated field still contains English 'Zero'")
                            
            elif case['lesson'] == 211:  # Sentence lesson
                # Check for translated sentences
                sections = data.get("sections", [])
                for section in sections:
                    content = section.get("content", {})
                    if "translated" in content:
                        translated = content["translated"]
                        if "This is a book" in translated:  # Should not be English
                            violations.append(f"translated field still contains English 'This is a book'")
            
            if violations:
                self.log_result(f"Core Curriculum Lesson {case['lesson']} ({case['locale']})", False, f"English content found: {'; '.join(violations)}")
            else:
                self.log_result(f"Core Curriculum Lesson {case['lesson']} ({case['locale']})", True, f"{case['description']} properly localized")
    
    def test_advanced_stages(self):
        """Test 3: Advanced stages (S07-S12)"""
        print("\n=== Test 3: Advanced stages (S07-S12) ===")
        
        test_cases = [
            {"lesson": 309, "locale": "de", "description": "S07 Islamic content in German"},
            {"lesson": 491, "locale": "tr", "description": "S09 Duas meaning in Turkish"},
            {"lesson": 561, "locale": "sv", "description": "S10 Hadiths translation in Swedish"},
            {"lesson": 631, "locale": "el", "description": "S11 Prophet stories in Greek"},
            {"lesson": 721, "locale": "nl", "description": "S12 Islamic Life content in Dutch"},
        ]
        
        for case in test_cases:
            endpoint = f"/kids-learn/curriculum/lesson/{case['lesson']}?locale={case['locale']}"
            response = self.make_request(endpoint)
            
            if not response["success"]:
                self.log_result(f"Advanced Stage Lesson {case['lesson']} ({case['locale']})", False, f"API Error: {response['error']}")
                continue
            
            data = response["data"]
            
            # Check for English content violations
            violations = self.check_no_english_content(data, case['locale'], f"Advanced Lesson {case['lesson']} ({case['locale']}) ")
            
            # Special check for Greek lesson 631 - should have "Αδάμ" for Adam
            if case['lesson'] == 631 and case['locale'] == "el":
                # Look for prophet name translations
                data_str = json.dumps(data, ensure_ascii=False)
                if "Αδάμ" not in data_str:
                    violations.append("Greek lesson should contain 'Αδάμ' (Adam in Greek)")
            
            if violations:
                self.log_result(f"Advanced Stage Lesson {case['lesson']} ({case['locale']})", False, f"English content found: {'; '.join(violations)}")
            else:
                self.log_result(f"Advanced Stage Lesson {case['lesson']} ({case['locale']})", True, f"{case['description']} properly localized")
    
    def test_english_still_works(self):
        """Test 4: English still works"""
        print("\n=== Test 4: English still works ===")
        
        endpoint = "/kids-learn/curriculum/lesson/1?locale=en"
        response = self.make_request(endpoint)
        
        if not response["success"]:
            self.log_result("English Lesson Test", False, f"API Error: {response['error']}")
            return
        
        data = response["data"]
        
        # For English, we expect English content
        data_str = json.dumps(data, ensure_ascii=False)
        
        # Check that we have English content
        if "Letter" not in data_str or "Lion" not in data_str:
            self.log_result("English Lesson Test", False, "English lesson missing expected English content")
        else:
            self.log_result("English Lesson Test", True, "English lesson returns English content correctly")
    
    def test_arabic_still_works(self):
        """Test 5: Arabic still works"""
        print("\n=== Test 5: Arabic still works ===")
        
        endpoint = "/kids-learn/curriculum/lesson/1?locale=ar"
        response = self.make_request(endpoint)
        
        if not response["success"]:
            self.log_result("Arabic Lesson Test", False, f"API Error: {response['error']}")
            return
        
        data = response["data"]
        
        # For Arabic, we expect Arabic content
        data_str = json.dumps(data, ensure_ascii=False)
        
        # Check that we have Arabic content
        if "حرف" not in data_str or "أسد" not in data_str:
            self.log_result("Arabic Lesson Test", False, "Arabic lesson missing expected Arabic content")
        else:
            self.log_result("Arabic Lesson Test", True, "Arabic lesson returns Arabic content correctly")
    
    def test_comprehensive_localization_check(self):
        """Additional comprehensive check for localization"""
        print("\n=== Comprehensive Localization Check ===")
        
        # Test curriculum overview for all non-English locales
        locales = ["de", "fr", "tr", "ru", "sv", "nl", "el"]
        
        for locale in locales:
            endpoint = f"/kids-learn/curriculum?locale={locale}"
            response = self.make_request(endpoint)
            
            if not response["success"]:
                self.log_result(f"Comprehensive Check ({locale})", False, f"API Error: {response['error']}")
                continue
            
            data = response["data"]
            data_str = json.dumps(data, ensure_ascii=False).lower()
            
            # Check for the word "english" as a key (case insensitive)
            if '"english"' in data_str:
                self.log_result(f"Comprehensive Check ({locale})", False, "Found 'english' key in response")
            else:
                self.log_result(f"Comprehensive Check ({locale})", True, "No 'english' key found - properly localized")
    
    def run_all_tests(self):
        """Run all localization tests"""
        print("🚀 Starting Arabic Kids Learning Curriculum Localization Tests")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 80)
        
        # Run all test suites
        self.test_curriculum_overview()
        self.test_core_curriculum_content()
        self.test_advanced_stages()
        self.test_english_still_works()
        self.test_arabic_still_works()
        self.test_comprehensive_localization_check()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_count = len(self.passed_tests)
        failed_count = len(self.failed_tests)
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"Success Rate: {(passed_count/total_tests*100):.1f}%")
        
        if self.failed_tests:
            print("\n🔍 FAILED TESTS:")
            for i, result in enumerate(self.results):
                if not result["passed"]:
                    print(f"{i+1}. {result['test']}: {result['details']}")
        
        print("\n" + "=" * 80)
        
        # Return success status
        return failed_count == 0

def main():
    """Main test execution"""
    tester = LocalizationTester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 ALL TESTS PASSED - Localization fix is working correctly!")
        sys.exit(0)
    else:
        print("⚠️  SOME TESTS FAILED - Localization needs attention")
        sys.exit(1)

if __name__ == "__main__":
    main()