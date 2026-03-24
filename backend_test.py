#!/usr/bin/env python3
"""
Arabic Course Engine & App UI Rebuild - Comprehensive Backend Testing
Testing all endpoints for the new Arabic & Quran Course system
"""
import requests
import json
import sys
from datetime import datetime

# Base URL from environment
BASE_URL = "https://hadith-cards.preview.emergentagent.com"

# Test configuration
LANGUAGES = ["ar", "en", "fr", "de", "tr", "ru", "sv", "nl", "el"]
EXPECTED_LEVELS = 6
EXPECTED_LETTERS = 28
EXPECTED_TOTAL_LESSONS = 216  # Foundation=40, A1=34, A2=34, B1=36, B2=36, C1=36

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def log_pass(self, test_name):
        print(f"✅ {test_name}")
        self.passed += 1
        
    def log_fail(self, test_name, error):
        print(f"❌ {test_name}: {error}")
        self.failed += 1
        self.errors.append(f"{test_name}: {error}")
        
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY: {self.passed}/{total} PASSED")
        if self.failed > 0:
            print(f"FAILED TESTS:")
            for error in self.errors:
                print(f"  - {error}")
        print(f"{'='*60}")
        return self.failed == 0

def test_health_endpoint():
    """Test basic health endpoint"""
    results = TestResults()
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                results.log_pass("Health endpoint working")
            else:
                results.log_fail("Health endpoint", f"Status not healthy: {data}")
        else:
            results.log_fail("Health endpoint", f"HTTP {response.status_code}")
    except Exception as e:
        results.log_fail("Health endpoint", str(e))
    return results

def test_course_overview():
    """Test course overview for all 9 languages"""
    results = TestResults()
    
    for lang in LANGUAGES:
        try:
            response = requests.get(f"{BASE_URL}/api/kids-learn/course/overview?locale={lang}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    levels = data.get("levels", [])
                    total_levels = data.get("total_levels", 0)
                    
                    # Verify 6 levels
                    if total_levels == EXPECTED_LEVELS and len(levels) == EXPECTED_LEVELS:
                        # Verify each level has 6 units
                        all_units_valid = True
                        total_lessons = 0
                        for level in levels:
                            units = level.get("units", [])
                            if len(units) != 6:
                                all_units_valid = False
                                break
                            total_lessons += level.get("total_lessons", 0)
                        
                        if all_units_valid:
                            if total_lessons == EXPECTED_TOTAL_LESSONS:
                                results.log_pass(f"Course overview ({lang}) - {EXPECTED_LEVELS} levels, 6 units each, {total_lessons} total lessons")
                            else:
                                results.log_fail(f"Course overview ({lang})", f"Expected {EXPECTED_TOTAL_LESSONS} lessons, got {total_lessons}")
                        else:
                            results.log_fail(f"Course overview ({lang})", "Not all levels have 6 units")
                    else:
                        results.log_fail(f"Course overview ({lang})", f"Expected {EXPECTED_LEVELS} levels, got {total_levels}")
                else:
                    results.log_fail(f"Course overview ({lang})", f"Success=false: {data}")
            else:
                results.log_fail(f"Course overview ({lang})", f"HTTP {response.status_code}")
        except Exception as e:
            results.log_fail(f"Course overview ({lang})", str(e))
    
    return results

def test_arabic_alphabet():
    """Test Arabic alphabet endpoint"""
    results = TestResults()
    
    try:
        response = requests.get(f"{BASE_URL}/api/kids-learn/course/alphabet?locale=en", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                letters = data.get("letters", [])
                total = data.get("total", 0)
                
                if total == EXPECTED_LETTERS and len(letters) == EXPECTED_LETTERS:
                    # Verify each letter has required fields
                    all_valid = True
                    for letter in letters:
                        required_fields = ["letter", "name", "sound", "forms", "emoji", "word_ar", "word_en"]
                        for field in required_fields:
                            if field not in letter or not letter[field]:
                                all_valid = False
                                break
                        if not all_valid:
                            break
                    
                    if all_valid:
                        results.log_pass(f"Arabic alphabet - {EXPECTED_LETTERS} letters with all required fields")
                    else:
                        results.log_fail("Arabic alphabet", "Some letters missing required fields")
                else:
                    results.log_fail("Arabic alphabet", f"Expected {EXPECTED_LETTERS} letters, got {total}")
            else:
                results.log_fail("Arabic alphabet", f"Success=false: {data}")
        else:
            results.log_fail("Arabic alphabet", f"HTTP {response.status_code}")
    except Exception as e:
        results.log_fail("Arabic alphabet", str(e))
    
    return results

def test_letter_lessons():
    """Test letter lesson endpoints with games"""
    results = TestResults()
    
    # Test boundary cases and specific examples
    test_cases = [
        (0, "en", "Alif lesson (first letter)"),
        (27, "en", "Ya lesson (last letter)"),
        (5, "sv", "Swedish locale test"),
    ]
    
    for index, locale, description in test_cases:
        try:
            response = requests.get(f"{BASE_URL}/api/kids-learn/course/alphabet/{index}?locale={locale}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    lesson = data.get("lesson", {})
                    games = data.get("games", [])
                    
                    # Verify lesson has required fields
                    lesson_fields = ["letter", "name", "forms", "emoji", "example_word", "example_translation"]
                    lesson_valid = all(field in lesson for field in lesson_fields)
                    
                    # Verify games array
                    games_valid = len(games) >= 3  # Should have at least 3 games
                    game_types = [game.get("type") for game in games]
                    has_quiz = "quiz" in game_types
                    has_memory = "memory" in game_types
                    
                    # Check for Swedish locale - no Arabic in instructions
                    swedish_valid = True
                    if locale == "sv":
                        for game in games:
                            title = game.get("title", "")
                            question = game.get("question", "")
                            # Check for Arabic characters (basic check)
                            if any('\u0600' <= char <= '\u06FF' for char in title + question):
                                swedish_valid = False
                                break
                    
                    if lesson_valid and games_valid and has_quiz and has_memory and swedish_valid:
                        results.log_pass(f"{description} - lesson + {len(games)} games (quiz, memory)")
                    else:
                        issues = []
                        if not lesson_valid:
                            issues.append("lesson fields missing")
                        if not games_valid:
                            issues.append(f"only {len(games)} games")
                        if not has_quiz:
                            issues.append("no quiz game")
                        if not has_memory:
                            issues.append("no memory game")
                        if not swedish_valid:
                            issues.append("Arabic text in Swedish instructions")
                        results.log_fail(description, ", ".join(issues))
                else:
                    results.log_fail(description, f"Success=false: {data}")
            else:
                results.log_fail(description, f"HTTP {response.status_code}")
        except Exception as e:
            results.log_fail(description, str(e))
    
    return results

def test_previous_endpoints():
    """Test that previous endpoints still work"""
    results = TestResults()
    
    # Test daily games endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/kids-learn/daily-games?locale=en", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                games = data.get("games", [])
                total_xp = data.get("total_xp", 0)
                if len(games) == 4 and total_xp == 60:
                    results.log_pass("Daily games endpoint - 4 games, 60 XP")
                else:
                    results.log_fail("Daily games endpoint", f"Expected 4 games/60 XP, got {len(games)} games/{total_xp} XP")
            else:
                results.log_fail("Daily games endpoint", f"Success=false: {data}")
        else:
            results.log_fail("Daily games endpoint", f"HTTP {response.status_code}")
    except Exception as e:
        results.log_fail("Daily games endpoint", str(e))
    
    # Test digital shield endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/kids-learn/digital-shield?locale=en&theme=all", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                lessons = data.get("lessons", [])
                total = data.get("total", 0)
                if total == 30 and len(lessons) == 30:
                    results.log_pass("Digital shield endpoint - 30 lessons")
                else:
                    results.log_fail("Digital shield endpoint", f"Expected 30 lessons, got {total}")
            else:
                results.log_fail("Digital shield endpoint", f"Success=false: {data}")
        else:
            results.log_fail("Digital shield endpoint", f"HTTP {response.status_code}")
    except Exception as e:
        results.log_fail("Digital shield endpoint", str(e))
    
    return results

def main():
    """Run all tests"""
    print("🧪 ARABIC COURSE ENGINE & APP UI REBUILD - BACKEND TESTING")
    print(f"Base URL: {BASE_URL}")
    print(f"Test Time: {datetime.now().isoformat()}")
    print("="*60)
    
    all_results = TestResults()
    
    # Run all test suites
    test_suites = [
        ("Health Check", test_health_endpoint),
        ("Course Overview (9 languages)", test_course_overview),
        ("Arabic Alphabet (28 letters)", test_arabic_alphabet),
        ("Letter Lessons + Games", test_letter_lessons),
        ("Previous Endpoints", test_previous_endpoints),
    ]
    
    for suite_name, test_func in test_suites:
        print(f"\n📋 {suite_name}")
        print("-" * 40)
        suite_results = test_func()
        all_results.passed += suite_results.passed
        all_results.failed += suite_results.failed
        all_results.errors.extend(suite_results.errors)
    
    # Final summary
    success = all_results.summary()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! Arabic Course Engine is fully functional.")
    else:
        print(f"\n⚠️  {all_results.failed} TESTS FAILED. See details above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())