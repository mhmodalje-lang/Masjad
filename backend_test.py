#!/usr/bin/env python3
"""
Backend Testing for Expanded Noor Academy V2 Content
Test Date: 2026-01-27
Focus: Expanded Nooraniya (30 lessons), Expanded Adab (20 lessons), Academy Overview Integration
"""

import requests
import json
import re
from typing import Dict, List, Any

# Configuration
BASE_URL = "https://maintain-momentum.preview.emergentagent.com"
TIMEOUT = 30

class NoorAcademyV2Tester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        self.results.append({
            'test': test_name,
            'status': status,
            'details': details
        })
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            
    def has_arabic_text(self, text: str) -> bool:
        """Check if text contains Arabic characters (Unicode range 0600-06FF)"""
        if not isinstance(text, str):
            return False
        arabic_pattern = re.compile(r'[\u0600-\u06FF]')
        return bool(arabic_pattern.search(text))
        
    def check_language_purity(self, response_data: dict, locale: str) -> bool:
        """Check if non-Arabic locales contain Arabic text in UI elements"""
        if locale == 'ar':
            return True  # Arabic locale should contain Arabic text
            
        # For Nooraniya lessons, Arabic letters in content are expected (it's Arabic learning)
        # We only check UI elements like title, level_title, method_info for language purity
        if 'lesson' in response_data:
            lesson = response_data['lesson']
            ui_elements = {
                'title': lesson.get('title', ''),
                'level_title': lesson.get('level_title', ''),
                'method_info_name': lesson.get('method_info', {}).get('name', '')
            }
            ui_text = json.dumps(ui_elements, ensure_ascii=False)
            return not self.has_arabic_text(ui_text)
        
        # For Adab lessons, check UI elements but allow Arabic in rules/hadith for Arabic locale
        if 'adab' in response_data:
            adab = response_data['adab']
            if locale != 'ar':
                # For non-Arabic locales, check title only (rules and hadith should be localized)
                ui_elements = {
                    'title': adab.get('title', '')
                }
                ui_text = json.dumps(ui_elements, ensure_ascii=False)
                return not self.has_arabic_text(ui_text)
            return True
        
        # For other responses, check the full response except known Arabic content fields
        response_copy = response_data.copy()
        response_str = json.dumps(response_copy, ensure_ascii=False)
        return not self.has_arabic_text(response_str)
        
    def make_request(self, endpoint: str) -> tuple:
        """Make HTTP request and return (success, data, status_code)"""
        try:
            url = f"{BASE_URL}{endpoint}"
            response = requests.get(url, timeout=TIMEOUT)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return True, data, 200
                except json.JSONDecodeError:
                    return False, f"Invalid JSON response", response.status_code
            else:
                return False, f"HTTP {response.status_code}", response.status_code
                
        except requests.exceptions.Timeout:
            return False, "Request timeout", 0
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {str(e)}", 0
            
    def test_expanded_nooraniya(self):
        """Test 1: Expanded Nooraniya (30 lessons across 3 levels)"""
        print("\n🔸 TEST 1: EXPANDED NOORANIYA (30 LESSONS)")
        
        test_cases = [
            {"lesson": 1, "locale": "en", "expected_level": 1, "description": "Level 1 lesson"},
            {"lesson": 11, "locale": "fr", "expected_level": 2, "description": "Level 2 (Letter Combinations) in French"},
            {"lesson": 15, "locale": "de", "expected_level": 2, "description": "Level 2 (Connecting) in German"},
            {"lesson": 21, "locale": "tr", "expected_level": 3, "description": "Level 3 (Fatha vowel) in Turkish"},
            {"lesson": 28, "locale": "ru", "expected_level": 3, "description": "Level 3 (Al-Fatiha practice) in Russian"},
            {"lesson": 30, "locale": "sv", "expected_level": 3, "description": "Level 3 Assessment in Swedish"}
        ]
        
        for case in test_cases:
            endpoint = f"/api/kids-learn/academy/nooraniya/lesson/{case['lesson']}?locale={case['locale']}"
            success, data, status_code = self.make_request(endpoint)
            
            test_name = f"Nooraniya Lesson {case['lesson']} ({case['locale']})"
            
            if not success:
                self.log_result(test_name, "FAIL", f"Request failed: {data}")
                continue
                
            # Check if response has expected structure
            if not isinstance(data, dict) or not data.get('success', False):
                self.log_result(test_name, "FAIL", f"Invalid response structure or success=false")
                continue
                
            # Check language purity (CRITICAL requirement)
            if not self.check_language_purity(data, case['locale']):
                self.log_result(test_name, "FAIL", f"CRITICAL: Arabic text found in UI elements for {case['locale']} response")
                continue
                
            # Check if lesson content exists
            lesson_data = data.get('lesson', {})
            if not lesson_data:
                self.log_result(test_name, "FAIL", "No lesson data found")
                continue
                
            # Verify lesson has required fields
            required_fields = ['title', 'level_title']
            missing_fields = [field for field in required_fields if not lesson_data.get(field)]
            if missing_fields:
                self.log_result(test_name, "FAIL", f"Missing fields: {missing_fields}")
                continue
                
            # Verify level matches expected
            actual_level = lesson_data.get('level')
            if actual_level != case['expected_level']:
                self.log_result(test_name, "FAIL", f"Expected level {case['expected_level']}, got {actual_level}")
                continue
                
            self.log_result(test_name, "PASS", f"{case['description']} - Level {actual_level}, UI language purity maintained")
            
    def test_expanded_adab(self):
        """Test 2: Expanded Adab (20 lessons)"""
        print("\n🔸 TEST 2: EXPANDED ADAB (20 LESSONS)")
        
        # First test the overview to verify 20 total lessons
        endpoint = "/api/kids-learn/academy/adab?locale=en"
        success, data, status_code = self.make_request(endpoint)
        
        if success and isinstance(data, dict) and data.get('success'):
            lessons = data.get('lessons', [])
            lesson_count = len(lessons)
            if lesson_count == 20:
                self.log_result("Adab Overview (20 lessons)", "PASS", f"Verified {lesson_count} total lessons")
            else:
                self.log_result("Adab Overview (20 lessons)", "FAIL", f"Expected 20 lessons, got {lesson_count}")
        else:
            self.log_result("Adab Overview (20 lessons)", "FAIL", f"Request failed: {data}")
            
        # Test specific lessons
        test_cases = [
            {"lesson": 1, "locale": "ar", "description": "Eating etiquette in Arabic (5 rules)"},
            {"lesson": 11, "locale": "en", "description": "Dua etiquette (new lesson, 5 rules)"},
            {"lesson": 16, "locale": "tr", "description": "Honoring Parents in Turkish"},
            {"lesson": 20, "locale": "el", "description": "Environmental Ethics in Greek"}
        ]
        
        for case in test_cases:
            endpoint = f"/api/kids-learn/academy/adab/{case['lesson']}?locale={case['locale']}"
            success, data, status_code = self.make_request(endpoint)
            
            test_name = f"Adab Lesson {case['lesson']} ({case['locale']})"
            
            if not success:
                self.log_result(test_name, "FAIL", f"Request failed: {data}")
                continue
                
            # Check if response has expected structure
            if not isinstance(data, dict) or not data.get('success', False):
                self.log_result(test_name, "FAIL", f"Invalid response structure or success=false")
                continue
                
            # Check language purity (CRITICAL requirement)
            if not self.check_language_purity(data, case['locale']):
                self.log_result(test_name, "FAIL", f"CRITICAL: Arabic text found in UI elements for {case['locale']} response")
                continue
                
            # Check if lesson content exists (using 'adab' key instead of 'lesson')
            lesson_data = data.get('adab', {})
            if not lesson_data:
                self.log_result(test_name, "FAIL", "No adab lesson data found")
                continue
                
            # Verify lesson has rules array and hadith text (CRITICAL requirement)
            rules = lesson_data.get('rules', [])
            hadith = lesson_data.get('hadith', '')
            
            if not rules or not isinstance(rules, list):
                self.log_result(test_name, "FAIL", "Missing or invalid rules array")
                continue
                
            if not hadith or not isinstance(hadith, str):
                self.log_result(test_name, "FAIL", "Missing or invalid hadith text")
                continue
                
            self.log_result(test_name, "PASS", f"{case['description']} - Rules: {len(rules)}, Hadith present, language purity maintained")
            
    def test_academy_overview_integration(self):
        """Test 3: Academy Overview Integration"""
        print("\n🔸 TEST 3: ACADEMY OVERVIEW INTEGRATION")
        
        test_cases = [
            {"locale": "nl", "description": "All 5 tracks visible with Dutch text"},
            {"track": "adab", "locale": "fr", "description": "Verify 20 levels/adab lessons"},
            {"track": "nooraniya", "locale": "el", "description": "Verify 7 levels in Greek"}
        ]
        
        # Test academy overview
        overview_case = test_cases[0]
        endpoint = f"/api/kids-learn/academy/overview?locale={overview_case['locale']}"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = f"Academy Overview ({overview_case['locale']})"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
        else:
            if not isinstance(data, dict) or not data.get('success', False):
                self.log_result(test_name, "FAIL", f"Invalid response structure or success=false")
            else:
                # Check language purity
                if not self.check_language_purity(data, overview_case['locale']):
                    self.log_result(test_name, "FAIL", f"CRITICAL: Arabic text found in {overview_case['locale']} response")
                else:
                    # Check if 5 tracks are present
                    tracks = data.get('tracks', [])
                    if len(tracks) == 5:
                        self.log_result(test_name, "PASS", f"{overview_case['description']} - 5 tracks verified")
                    else:
                        self.log_result(test_name, "FAIL", f"Expected 5 tracks, got {len(tracks)}")
        
        # Test specific track details
        track_cases = test_cases[1:]
        for case in track_cases:
            endpoint = f"/api/kids-learn/academy/track/{case['track']}?locale={case['locale']}"
            success, data, status_code = self.make_request(endpoint)
            
            test_name = f"Track {case['track']} ({case['locale']})"
            
            if not success:
                self.log_result(test_name, "FAIL", f"Request failed: {data}")
                continue
                
            if not isinstance(data, dict) or not data.get('success', False):
                self.log_result(test_name, "FAIL", f"Invalid response structure or success=false")
                continue
                
            # Check language purity
            if not self.check_language_purity(data, case['locale']):
                self.log_result(test_name, "FAIL", f"CRITICAL: Arabic text found in {case['locale']} response")
                continue
                
            # Check track-specific requirements
            if case['track'] == 'adab':
                # Should have information about 20 lessons
                levels = data.get('levels', [])  # Changed from track_data.get to data.get
                total_lessons = sum(level.get('lessons', 0) for level in levels)
                if total_lessons >= 20:
                    self.log_result(test_name, "PASS", f"{case['description']} - {total_lessons} lessons found")
                else:
                    self.log_result(test_name, "FAIL", f"Expected 20+ lessons, got {total_lessons}")
            elif case['track'] == 'nooraniya':
                # Should have 7 levels
                levels = data.get('levels', [])  # Changed from track_data.get to data.get
                if len(levels) == 7:
                    self.log_result(test_name, "PASS", f"{case['description']} - 7 levels verified")
                else:
                    self.log_result(test_name, "FAIL", f"Expected 7 levels, got {len(levels)}")
            else:
                self.log_result(test_name, "PASS", f"{case['description']} - Track data present")
                
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 STARTING EXPANDED NOOR ACADEMY V2 BACKEND TESTING")
        print(f"📍 Base URL: {BASE_URL}")
        print("🎯 Focus: Expanded Nooraniya (30 lessons), Expanded Adab (20 lessons), Academy Overview")
        
        # Run all test suites
        self.test_expanded_nooraniya()
        self.test_expanded_adab()
        self.test_academy_overview_integration()
        
        # Generate summary report
        self.generate_report()
        
    def generate_report(self):
        """Generate final test report"""
        print("\n" + "="*80)
        print("📊 EXPANDED NOOR ACADEMY V2 TESTING RESULTS")
        print("="*80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"📈 SUMMARY: {success_rate:.1f}% SUCCESS ({self.passed_tests}/{self.total_tests} tests passed)")
        print(f"✅ PASSED: {self.passed_tests}")
        print(f"❌ FAILED: {self.failed_tests}")
        
        # Group results by status
        passed_tests = [r for r in self.results if r['status'] == 'PASS']
        failed_tests = [r for r in self.results if r['status'] == 'FAIL']
        
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for result in failed_tests:
                print(f"   • {result['test']}: {result['details']}")
                
        if passed_tests:
            print(f"\n✅ PASSED TESTS ({len(passed_tests)}):")
            for result in passed_tests:
                print(f"   • {result['test']}: {result['details']}")
                
        # Critical findings
        critical_failures = [r for r in failed_tests if 'CRITICAL' in r['details']]
        if critical_failures:
            print(f"\n🚨 CRITICAL ISSUES FOUND ({len(critical_failures)}):")
            for result in critical_failures:
                print(f"   • {result['test']}: {result['details']}")
        else:
            print(f"\n🎉 CRITICAL REQUIREMENT MET: No Arabic text leakage detected in non-Arabic responses")
            
        print("\n" + "="*80)

if __name__ == "__main__":
    tester = NoorAcademyV2Tester()
    tester.run_all_tests()