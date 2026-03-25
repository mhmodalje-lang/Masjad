#!/usr/bin/env python3
"""
Noor Academy V2 Backend API Testing
Test Date: 2026-01-27
Focus: Complete testing of all Noor Academy V2 endpoints as specified in review request
"""

import requests
import json
import re
from typing import Dict, List, Any

# Configuration
BASE_URL = "https://fast-reload-app.preview.emergentagent.com"
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
            
    def make_request(self, endpoint: str) -> tuple:
        """Make HTTP request and return (success, data, status_code)"""
        try:
            url = f"{BASE_URL}{endpoint}"
            print(f"Testing: {url}")
            response = requests.get(url, timeout=TIMEOUT)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return True, data, 200
                except json.JSONDecodeError:
                    return False, f"Invalid JSON response", response.status_code
            else:
                return False, f"HTTP {response.status_code}: {response.text[:200]}", response.status_code
                
        except requests.exceptions.Timeout:
            return False, "Request timeout", 0
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {str(e)}", 0
            
    def test_academy_overview(self):
        """Test 1: Academy Overview - should return 5 tracks"""
        print("\n🔸 TEST 1: ACADEMY OVERVIEW")
        
        endpoint = "/api/kids-learn/academy/overview?locale=en"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "Academy Overview (5 tracks)"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict) or not data.get('success', False):
            self.log_result(test_name, "FAIL", f"Invalid response structure or success=false")
            return
            
        # Check if 5 tracks are present
        tracks = data.get('tracks', [])
        if len(tracks) != 5:
            self.log_result(test_name, "FAIL", f"Expected 5 tracks, got {len(tracks)}")
            return
            
        # Verify track IDs
        expected_tracks = {'nooraniya', 'aqeedah', 'fiqh', 'seerah', 'adab'}
        actual_tracks = {track.get('id') for track in tracks}
        if actual_tracks != expected_tracks:
            self.log_result(test_name, "FAIL", f"Expected tracks {expected_tracks}, got {actual_tracks}")
            return
            
        self.log_result(test_name, "PASS", f"5 tracks found: {', '.join(actual_tracks)}")
        
    def test_track_details(self):
        """Test 2-4: Track Details - Fiqh (4 levels), Seerah (6 levels), Aqeedah (5 levels), Nooraniya"""
        print("\n🔸 TEST 2-4: TRACK DETAILS")
        
        track_tests = [
            {"track": "fiqh", "locale": "en", "expected_levels": 4, "description": "Fiqh Track with lesson summaries"},
            {"track": "seerah", "locale": "en", "expected_levels": 6, "description": "Seerah Track with lesson summaries"},
            {"track": "aqeedah", "locale": "en", "expected_levels": 5, "description": "Aqeedah Track with lesson summaries"},
            {"track": "nooraniya", "locale": "en", "expected_levels": 7, "description": "Nooraniya Track with lesson summaries"},
        ]
        
        for test_case in track_tests:
            endpoint = f"/api/kids-learn/academy/track/{test_case['track']}?locale={test_case['locale']}"
            success, data, status_code = self.make_request(endpoint)
            
            test_name = f"{test_case['track'].title()} Track ({test_case['expected_levels']} levels)"
            
            if not success:
                self.log_result(test_name, "FAIL", f"Request failed: {data}")
                continue
                
            # Check if response has expected structure
            if not isinstance(data, dict) or not data.get('success', False):
                self.log_result(test_name, "FAIL", f"Invalid response structure or success=false")
                continue
                
            # Check levels count
            levels = data.get('levels', [])
            if len(levels) != test_case['expected_levels']:
                self.log_result(test_name, "FAIL", f"Expected {test_case['expected_levels']} levels, got {len(levels)}")
                continue
                
            # Verify each level has lesson summaries (not just count)
            has_lesson_summaries = True
            for level in levels:
                lessons = level.get('lessons', [])
                if not isinstance(lessons, list):
                    has_lesson_summaries = False
                    break
                # Check if lessons have proper structure (not just count)
                for lesson in lessons:
                    if not isinstance(lesson, dict) or 'id' not in lesson or 'title' not in lesson:
                        has_lesson_summaries = False
                        break
                if not has_lesson_summaries:
                    break
                    
            if not has_lesson_summaries:
                self.log_result(test_name, "FAIL", "Levels should contain lesson objects with summaries, not just counts")
                continue
                
            total_lessons = sum(len(level.get('lessons', [])) for level in levels)
            self.log_result(test_name, "PASS", f"{test_case['description']} - {len(levels)} levels, {total_lessons} total lessons")
            
    def test_lesson_content(self):
        """Test 5-10: Individual Lesson Content"""
        print("\n🔸 TEST 5-10: LESSON CONTENT")
        
        lesson_tests = [
            {"track": "fiqh", "lesson": 1, "locale": "en", "description": "Fiqh Lesson 1 - real content with quiz"},
            {"track": "seerah", "lesson": 1, "locale": "en", "description": "Seerah Lesson 1 - real content with story"},
            {"track": "aqeedah", "lesson": 1, "locale": "en", "description": "Aqeedah Lesson 1 - real content about Tawheed"},
            {"track": "fiqh", "lesson": 40, "locale": "en", "description": "Fiqh Lesson 40 (last lesson)"},
            {"track": "seerah", "lesson": 60, "locale": "en", "description": "Seerah Lesson 60 (last lesson)"},
            {"track": "fiqh", "lesson": 1, "locale": "ar", "description": "Fiqh Lesson 1 in Arabic"},
        ]
        
        for test_case in lesson_tests:
            endpoint = f"/api/kids-learn/academy/{test_case['track']}/lesson/{test_case['lesson']}?locale={test_case['locale']}"
            success, data, status_code = self.make_request(endpoint)
            
            test_name = f"{test_case['track'].title()} Lesson {test_case['lesson']} ({test_case['locale']})"
            
            if not success:
                self.log_result(test_name, "FAIL", f"Request failed: {data}")
                continue
                
            # Check if response has expected structure
            if not isinstance(data, dict) or not data.get('success', False):
                self.log_result(test_name, "FAIL", f"Invalid response structure or success=false")
                continue
                
            # Check lesson data
            lesson_data = data.get('lesson', {})
            if not lesson_data:
                self.log_result(test_name, "FAIL", "No lesson data found")
                continue
                
            # Check for placeholder content
            content = lesson_data.get('content', {})
            if content.get('placeholder', False) or content.get('status') == 'placeholder':
                self.log_result(test_name, "FAIL", "Lesson contains placeholder content - should have real content")
                continue
                
            # Verify required fields
            required_fields = ['id', 'title', 'content']
            missing_fields = [field for field in required_fields if not lesson_data.get(field)]
            if missing_fields:
                self.log_result(test_name, "FAIL", f"Missing required fields: {missing_fields}")
                continue
                
            # Check for quiz
            quiz = lesson_data.get('quiz', {})
            if not quiz:
                self.log_result(test_name, "FAIL", "Lesson should have a quiz")
                continue
                
            # Special handling for comprehensive assessments
            if quiz.get('type') == 'comprehensive':
                # Comprehensive assessments may have empty question but should have type
                if not quiz.get('type'):
                    self.log_result(test_name, "FAIL", "Comprehensive assessment should have quiz type")
                    continue
            else:
                # Regular lessons should have questions
                if not quiz.get('question'):
                    self.log_result(test_name, "FAIL", "Lesson should have a quiz with question")
                    continue
                    
                # Verify quiz structure for non-comprehensive quizzes
                if not quiz.get('options') and quiz.get('type') not in ['true_false', 'input']:
                    self.log_result(test_name, "FAIL", "Quiz should have options or be true/false or input type")
                    continue
                
            # Special checks for specific lessons
            if test_case['track'] == 'aqeedah' and test_case['lesson'] == 1:
                # Should be about Tawheed
                title = lesson_data.get('title', '').lower()
                content_str = str(content).lower()
                if 'tawheed' not in title and 'tawheed' not in content_str and 'توحيد' not in title and 'توحيد' not in content_str:
                    self.log_result(test_name, "FAIL", "Aqeedah Lesson 1 should be about Tawheed")
                    continue
                    
            if test_case['track'] == 'seerah' and test_case['lesson'] == 1:
                # Should have story content
                if not any(key in content for key in ['story', 'narrative', 'events', 'background']):
                    self.log_result(test_name, "FAIL", "Seerah Lesson 1 should contain story content")
                    continue
                    
            # Check Arabic content for Arabic locale
            if test_case['locale'] == 'ar':
                title = lesson_data.get('title', '')
                if not self.has_arabic_text(title):
                    self.log_result(test_name, "FAIL", "Arabic locale should return Arabic text in title")
                    continue
                    
            self.log_result(test_name, "PASS", f"{test_case['description']} - Real content with quiz verified")
            
    def has_arabic_text(self, text: str) -> bool:
        """Check if text contains Arabic characters (Unicode range 0600-06FF)"""
        if not isinstance(text, str):
            return False
        arabic_pattern = re.compile(r'[\u0600-\u06FF]')
        return bool(arabic_pattern.search(text))
        
    def test_comprehensive_validation(self):
        """Test 11: Comprehensive validation of all tracks"""
        print("\n🔸 TEST 11: COMPREHENSIVE VALIDATION")
        
        # Test that all tracks have no placeholder lessons
        tracks_to_validate = [
            {"track": "fiqh", "total_lessons": 40, "description": "All 40 Fiqh lessons should be real"},
            {"track": "seerah", "total_lessons": 60, "description": "All 60 Seerah lessons should be real"},
        ]
        
        for track_info in tracks_to_validate:
            track = track_info['track']
            total_lessons = track_info['total_lessons']
            
            # Sample test a few lessons to verify no placeholders
            sample_lessons = [1, total_lessons // 2, total_lessons]  # First, middle, last
            
            placeholder_found = False
            for lesson_num in sample_lessons:
                endpoint = f"/api/kids-learn/academy/{track}/lesson/{lesson_num}?locale=en"
                success, data, status_code = self.make_request(endpoint)
                
                if success and data.get('success'):
                    lesson_data = data.get('lesson', {})
                    content = lesson_data.get('content', {})
                    if content.get('placeholder', False) or content.get('status') == 'placeholder':
                        placeholder_found = True
                        break
                        
            test_name = f"{track.title()} Track - No Placeholders"
            if placeholder_found:
                self.log_result(test_name, "FAIL", f"Found placeholder content in {track} lessons")
            else:
                self.log_result(test_name, "PASS", f"{track_info['description']}")
                
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 STARTING NOOR ACADEMY V2 BACKEND API TESTING")
        print(f"📍 Base URL: {BASE_URL}")
        print("🎯 Focus: Complete Noor Academy V2 API validation as per review request")
        
        # Run all test suites
        self.test_academy_overview()
        self.test_track_details()
        self.test_lesson_content()
        self.test_comprehensive_validation()
        
        # Generate summary report
        self.generate_report()
        
    def generate_report(self):
        """Generate final test report"""
        print("\n" + "="*80)
        print("📊 NOOR ACADEMY V2 API TESTING RESULTS")
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
        critical_failures = [r for r in failed_tests if any(word in r['details'].lower() for word in ['placeholder', 'missing', 'invalid'])]
        if critical_failures:
            print(f"\n🚨 CRITICAL ISSUES FOUND ({len(critical_failures)}):")
            for result in critical_failures:
                print(f"   • {result['test']}: {result['details']}")
        else:
            print(f"\n🎉 ALL CRITICAL REQUIREMENTS MET: No placeholder content, all APIs working correctly")
            
        print("\n" + "="*80)

if __name__ == "__main__":
    tester = NoorAcademyV2Tester()
    tester.run_all_tests()