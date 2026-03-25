#!/usr/bin/env python3
"""
Noor Academy V2 API Backend Testing
===================================
Testing Noor Academy V2 API endpoints as requested in review:

Test 1: Academy Overview — All 9 Languages
Test 2: Track Detail
Test 3: Nooraniya Lessons
Test 4: Adab (Islamic Manners)
CRITICAL: Language purity check

Backend URL: https://fast-reload-app.preview.emergentagent.com
All API routes have /api prefix
"""

import asyncio
import aiohttp
import json
import sys
import re
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://fast-reload-app.preview.emergentagent.com"

class NoorAcademyTester:
    def __init__(self):
        self.session = None
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def log_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            print(f"✅ {test_name}: {status}")
        else:
            self.failed_tests += 1
            print(f"❌ {test_name}: {status}")
            if details:
                print(f"   Details: {details}")
        
        self.results.append({
            "test": test_name,
            "status": status,
            "details": details
        })

    def has_arabic_text(self, text: str) -> bool:
        """Check if text contains Arabic characters (Unicode 0x0600-0x06FF)"""
        if not text:
            return False
        return bool(re.search(r'[\u0600-\u06FF]', text))

    async def test_endpoint(self, endpoint: str, test_name: str = "") -> Dict[str, Any]:
        """Test a single endpoint"""
        try:
            url = f"{BACKEND_URL}/api{endpoint}"
            async with self.session.get(url) as response:
                if response.status != 200:
                    self.log_result(test_name, f"FAIL - HTTP {response.status}")
                    return {"status": "fail", "error": f"HTTP {response.status}"}
                
                try:
                    data = await response.json()
                except json.JSONDecodeError as e:
                    self.log_result(test_name, f"FAIL - Invalid JSON: {str(e)}")
                    return {"status": "fail", "error": f"Invalid JSON: {str(e)}"}
                
                self.log_result(test_name, "PASS")
                return {"status": "pass", "data": data}
                
        except Exception as e:
            self.log_result(test_name, f"FAIL - Exception: {str(e)}")
            return {"status": "fail", "error": str(e)}

    async def test_academy_overview_all_languages(self):
        """Test 1: Academy Overview — All 9 Languages"""
        print("\n🔸 Test 1: Academy Overview — All 9 Languages")
        print("=" * 60)
        
        locales = ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"]
        
        for locale in locales:
            endpoint = f"/kids-learn/academy/overview?locale={locale}"
            test_name = f"Academy Overview ({locale})"
            
            result = await self.test_endpoint(endpoint, test_name)
            
            if result["status"] == "pass":
                data = result["data"]
                
                # Verify success=true
                if not data.get("success", False):
                    self.log_result(f"{test_name} - Success Check", f"FAIL - success={data.get('success')}")
                else:
                    self.log_result(f"{test_name} - Success Check", "PASS")
                
                # Verify 5 tracks returned
                tracks = data.get("tracks", [])
                if len(tracks) != 5:
                    self.log_result(f"{test_name} - Track Count", f"FAIL - Expected 5 tracks, got {len(tracks)}")
                else:
                    self.log_result(f"{test_name} - Track Count", "PASS")
                
                # Verify badges exist
                badges = data.get("badges", [])
                if not badges:
                    self.log_result(f"{test_name} - Badges Check", "FAIL - No badges found")
                else:
                    self.log_result(f"{test_name} - Badges Check", "PASS")
                
                # Verify teaching_methods exist
                teaching_methods = data.get("teaching_methods", [])
                if not teaching_methods:
                    self.log_result(f"{test_name} - Teaching Methods Check", "FAIL - No teaching methods found")
                else:
                    self.log_result(f"{test_name} - Teaching Methods Check", "PASS")
                
                # CRITICAL: For non-Arabic locales, verify NO Arabic text
                if locale != "ar":
                    academy_name = data.get("academy_name", "")
                    tagline = data.get("tagline", "")
                    
                    if self.has_arabic_text(academy_name):
                        self.log_result(f"{test_name} - Arabic Text Check (academy_name)", f"FAIL - Arabic text found in academy_name: {academy_name}")
                    else:
                        self.log_result(f"{test_name} - Arabic Text Check (academy_name)", "PASS")
                    
                    if self.has_arabic_text(tagline):
                        self.log_result(f"{test_name} - Arabic Text Check (tagline)", f"FAIL - Arabic text found in tagline: {tagline}")
                    else:
                        self.log_result(f"{test_name} - Arabic Text Check (tagline)", "PASS")
                    
                    # Check track titles for Arabic text
                    for i, track in enumerate(tracks):
                        track_title = track.get("title", "")
                        if self.has_arabic_text(track_title):
                            self.log_result(f"{test_name} - Arabic Text Check (track {i+1} title)", f"FAIL - Arabic text found in track title: {track_title}")
                        else:
                            self.log_result(f"{test_name} - Arabic Text Check (track {i+1} title)", "PASS")
                
                # Verify each track has required fields
                for i, track in enumerate(tracks):
                    required_fields = ["id", "emoji", "color", "title", "description", "total_levels", "total_lessons"]
                    missing_fields = [field for field in required_fields if field not in track]
                    
                    if missing_fields:
                        self.log_result(f"{test_name} - Track {i+1} Structure", f"FAIL - Missing fields: {missing_fields}")
                    else:
                        self.log_result(f"{test_name} - Track {i+1} Structure", "PASS")

    async def test_track_detail(self):
        """Test 2: Track Detail"""
        print("\n🔸 Test 2: Track Detail")
        print("=" * 60)
        
        test_cases = [
            ("nooraniya", "en", 7, "levels"),
            ("aqeedah", "de", 5, "levels"),
            ("fiqh", "fr", 4, "levels"),
            ("seerah", "tr", 6, "levels"),
            ("adab", "ru", 10, "lessons"),
            ("invalid", "en", None, None)  # Error case
        ]
        
        for track_id, locale, expected_count, count_type in test_cases:
            endpoint = f"/kids-learn/academy/track/{track_id}?locale={locale}"
            test_name = f"Track Detail - {track_id} ({locale})"
            
            result = await self.test_endpoint(endpoint, test_name)
            
            if result["status"] == "pass":
                data = result["data"]
                
                if track_id == "invalid":
                    # Should be error response
                    if data.get("success", True):
                        self.log_result(f"{test_name} - Error Response Check", "FAIL - Expected error response for invalid track")
                    else:
                        self.log_result(f"{test_name} - Error Response Check", "PASS")
                else:
                    # Should be successful response
                    if not data.get("success", False):
                        self.log_result(f"{test_name} - Success Check", f"FAIL - success={data.get('success')}")
                    else:
                        self.log_result(f"{test_name} - Success Check", "PASS")
                    
                    # Check expected count
                    if count_type == "levels":
                        levels = data.get("levels", [])
                        if len(levels) != expected_count:
                            self.log_result(f"{test_name} - Level Count", f"FAIL - Expected {expected_count} levels, got {len(levels)}")
                        else:
                            self.log_result(f"{test_name} - Level Count", "PASS")
                        
                        # Verify each level has title and skills
                        for i, level in enumerate(levels):
                            if "title" not in level:
                                self.log_result(f"{test_name} - Level {i+1} Title", "FAIL - Missing title")
                            else:
                                self.log_result(f"{test_name} - Level {i+1} Title", "PASS")
                            
                            if "skills" not in level:
                                self.log_result(f"{test_name} - Level {i+1} Skills", "FAIL - Missing skills")
                            else:
                                self.log_result(f"{test_name} - Level {i+1} Skills", "PASS")
                    
                    elif count_type == "lessons":
                        lessons = data.get("lessons", [])
                        if len(lessons) != expected_count:
                            self.log_result(f"{test_name} - Lesson Count", f"FAIL - Expected {expected_count} lessons, got {len(lessons)}")
                        else:
                            self.log_result(f"{test_name} - Lesson Count", "PASS")

    async def test_nooraniya_lessons(self):
        """Test 3: Nooraniya Lessons"""
        print("\n🔸 Test 3: Nooraniya Lessons")
        print("=" * 60)
        
        test_cases = [
            (1, "ar", "Arabic content with quiz"),
            (4, "en", "Interactive diagram lesson"),
            (8, "sv", "Game-based lesson in Swedish"),
            (10, "el", "Assessment lesson"),
            (99, "en", "Error response")  # Invalid lesson
        ]
        
        for lesson_id, locale, description in test_cases:
            endpoint = f"/kids-learn/academy/nooraniya/lesson/{lesson_id}?locale={locale}"
            test_name = f"Nooraniya Lesson {lesson_id} ({locale}) - {description}"
            
            result = await self.test_endpoint(endpoint, test_name)
            
            if result["status"] == "pass":
                data = result["data"]
                
                if lesson_id == 99:
                    # Should be error response
                    if data.get("success", True):
                        self.log_result(f"{test_name} - Error Response Check", "FAIL - Expected error response for invalid lesson")
                    else:
                        self.log_result(f"{test_name} - Error Response Check", "PASS")
                else:
                    # Should be successful response
                    if not data.get("success", False):
                        self.log_result(f"{test_name} - Success Check", f"FAIL - success={data.get('success')}")
                    else:
                        self.log_result(f"{test_name} - Success Check", "PASS")
                    
                    # CRITICAL: For non-Arabic locales, verify NO Arabic text in title
                    if locale != "ar":
                        title = data.get("title", "")
                        if self.has_arabic_text(title):
                            self.log_result(f"{test_name} - Arabic Text Check (title)", f"FAIL - Arabic text found in title: {title}")
                        else:
                            self.log_result(f"{test_name} - Arabic Text Check (title)", "PASS")
                    
                    # Verify lesson content structure based on type
                    if lesson_id == 1 and locale == "ar":
                        # Should have quiz
                        if "quiz" not in data:
                            self.log_result(f"{test_name} - Quiz Check", "FAIL - Missing quiz content")
                        else:
                            self.log_result(f"{test_name} - Quiz Check", "PASS")
                    
                    elif lesson_id == 4 and locale == "en":
                        # Should be interactive diagram
                        lesson_type = data.get("type", "")
                        if "interactive" not in lesson_type.lower() and "diagram" not in lesson_type.lower():
                            self.log_result(f"{test_name} - Interactive Diagram Check", f"WARN - Expected interactive diagram, got type: {lesson_type}")
                        else:
                            self.log_result(f"{test_name} - Interactive Diagram Check", "PASS")
                    
                    elif lesson_id == 8 and locale == "sv":
                        # Should be game-based
                        lesson_type = data.get("type", "")
                        if "game" not in lesson_type.lower():
                            self.log_result(f"{test_name} - Game-based Check", f"WARN - Expected game-based lesson, got type: {lesson_type}")
                        else:
                            self.log_result(f"{test_name} - Game-based Check", "PASS")
                    
                    elif lesson_id == 10 and locale == "el":
                        # Should be assessment
                        lesson_type = data.get("type", "")
                        if "assessment" not in lesson_type.lower():
                            self.log_result(f"{test_name} - Assessment Check", f"WARN - Expected assessment lesson, got type: {lesson_type}")
                        else:
                            self.log_result(f"{test_name} - Assessment Check", "PASS")

    async def test_adab_islamic_manners(self):
        """Test 4: Adab (Islamic Manners)"""
        print("\n🔸 Test 4: Adab (Islamic Manners)")
        print("=" * 60)
        
        # Test adab list endpoint
        endpoint = "/kids-learn/academy/adab?locale=en"
        test_name = "Adab List (English)"
        
        result = await self.test_endpoint(endpoint, test_name)
        
        if result["status"] == "pass":
            data = result["data"]
            
            # Verify 10 lessons listed
            lessons = data.get("lessons", [])
            if len(lessons) != 10:
                self.log_result(f"{test_name} - Lesson Count", f"FAIL - Expected 10 lessons, got {len(lessons)}")
            else:
                self.log_result(f"{test_name} - Lesson Count", "PASS")
        
        # Test specific adab lessons
        test_cases = [
            (1, "ar", "Arabic eating etiquette with 5 rules + hadith"),
            (2, "nl", "Dutch mosque etiquette"),
            (9, "el", "Greek seeking knowledge etiquette")
        ]
        
        for lesson_id, locale, description in test_cases:
            endpoint = f"/kids-learn/academy/adab/{lesson_id}?locale={locale}"
            test_name = f"Adab Lesson {lesson_id} ({locale}) - {description}"
            
            result = await self.test_endpoint(endpoint, test_name)
            
            if result["status"] == "pass":
                data = result["data"]
                
                # Should be successful response
                if not data.get("success", False):
                    self.log_result(f"{test_name} - Success Check", f"FAIL - success={data.get('success')}")
                else:
                    self.log_result(f"{test_name} - Success Check", "PASS")
                
                # CRITICAL: For non-Arabic locales, verify NO Arabic text
                if locale != "ar":
                    # Check title
                    title = data.get("title", "")
                    if self.has_arabic_text(title):
                        self.log_result(f"{test_name} - Arabic Text Check (title)", f"FAIL - Arabic text found in title: {title}")
                    else:
                        self.log_result(f"{test_name} - Arabic Text Check (title)", "PASS")
                    
                    # Check description
                    description_text = data.get("description", "")
                    if self.has_arabic_text(description_text):
                        self.log_result(f"{test_name} - Arabic Text Check (description)", f"FAIL - Arabic text found in description: {description_text}")
                    else:
                        self.log_result(f"{test_name} - Arabic Text Check (description)", "PASS")
                    
                    # Check rules
                    rules = data.get("rules", [])
                    for i, rule in enumerate(rules):
                        if self.has_arabic_text(rule):
                            self.log_result(f"{test_name} - Arabic Text Check (rule {i+1})", f"FAIL - Arabic text found in rule: {rule}")
                        else:
                            self.log_result(f"{test_name} - Arabic Text Check (rule {i+1})", "PASS")
                    
                    # Check hadith
                    hadith = data.get("hadith", "")
                    if hadith and self.has_arabic_text(hadith):
                        self.log_result(f"{test_name} - Arabic Text Check (hadith)", f"FAIL - Arabic text found in hadith: {hadith}")
                    elif hadith:
                        self.log_result(f"{test_name} - Arabic Text Check (hadith)", "PASS")
                
                # Specific checks based on lesson
                if lesson_id == 1 and locale == "ar":
                    # Should have 5 rules + hadith
                    rules = data.get("rules", [])
                    if len(rules) != 5:
                        self.log_result(f"{test_name} - Rules Count", f"FAIL - Expected 5 rules, got {len(rules)}")
                    else:
                        self.log_result(f"{test_name} - Rules Count", "PASS")
                    
                    hadith = data.get("hadith", "")
                    if not hadith:
                        self.log_result(f"{test_name} - Hadith Check", "FAIL - Missing hadith")
                    else:
                        self.log_result(f"{test_name} - Hadith Check", "PASS")

    async def run_all_tests(self):
        """Run all Noor Academy V2 tests"""
        print("🚀 Starting Noor Academy V2 API Backend Testing")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print("Testing Noor Academy V2 API endpoints as per review request")
        print("=" * 80)
        
        # Run all test suites
        await self.test_academy_overview_all_languages()
        await self.test_track_detail()
        await self.test_nooraniya_lessons()
        await self.test_adab_islamic_manners()
        
        # Print summary
        print("\n" + "=" * 80)
        print("🏁 NOOR ACADEMY V2 TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%" if self.total_tests > 0 else "0%")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if result["status"] != "PASS":
                    print(f"  - {result['test']}: {result['status']}")
                    if result["details"]:
                        print(f"    {result['details']}")
        
        print("\n" + "=" * 80)
        return self.failed_tests == 0

async def main():
    """Main test runner"""
    async with NoorAcademyTester() as tester:
        success = await tester.run_all_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())