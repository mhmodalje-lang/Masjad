#!/usr/bin/env python3
"""
Backend Test Suite: Strict Localization Fix for Noor Academy Arabic Learning App
Testing all 9 locales for proper localization without English text leakage
Base URL: https://kidszone-learn.preview.emergentagent.com
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Base URL from frontend/.env
BASE_URL = "https://kidszone-learn.preview.emergentagent.com"

# All 9 supported locales
LOCALES = ["ar", "en", "fr", "de", "tr", "ru", "sv", "nl", "el"]

# Expected localized letter names for key locales
EXPECTED_LETTER_NAMES = {
    "ar": "ألف",  # Should be Arabic, NOT "Alif"
    "ru": "Алиф",  # Should be Russian, NOT "Alif"
    "fr": "Alif",  # Same in French
    "tr": "Elif",  # Turkish
    "de": "Alif",  # German
    "el": "Αλίφ",  # Greek
}

# Expected word translations for "Lion" (first letter example)
EXPECTED_WORD_TRANSLATIONS = {
    "ar": "أسد",
    "ru": "Лев",  # Should be Russian, NOT "Lion"
    "fr": "Lion",  # Same in French
    "tr": "Aslan",  # Should be Turkish, NOT "Lion"
    "de": "Löwe",  # Should be German, NOT "Lion"
    "el": "Λιοντάρι",  # Greek
}

# Expected memory game form labels (localized)
EXPECTED_FORM_LABELS = {
    "ar": ["معزول", "بداية", "وسط", "نهاية"],
    "ru": ["Отдельная", "Начальная", "Средняя", "Конечная"],
    "tr": ["Tek", "Başta", "Ortada", "Sonda"],
    "de": ["Isoliert", "Anfang", "Mitte", "Ende"],
    "sv": ["Isolerad", "Början", "Mitten", "Slutet"],
    "el": ["Μεμονωμένο", "Αρχικό", "Μεσαίο", "Τελικό"],
}

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.failures = []
    
    def add_pass(self, test_name: str):
        self.passed += 1
        print(f"✅ PASS: {test_name}")
    
    def add_fail(self, test_name: str, error: str):
        self.failed += 1
        self.failures.append(f"{test_name}: {error}")
        print(f"❌ FAIL: {test_name} - {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY: {self.passed}/{total} PASSED")
        print(f"{'='*60}")
        if self.failures:
            print("FAILURES:")
            for failure in self.failures:
                print(f"  - {failure}")
        return self.failed == 0

def make_request(endpoint: str, params: Dict = None) -> Dict[str, Any]:
    """Make HTTP request with error handling."""
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}"}

def test_health_check(results: TestResults):
    """Test 1: Health Check"""
    print("\n🔍 Testing Health Check...")
    data = make_request("/api/health")
    
    if "error" in data:
        results.add_fail("Health Check", data["error"])
        return
    
    if data.get("status") == "healthy":
        results.add_pass("Health Check")
    else:
        results.add_fail("Health Check", f"Expected healthy status, got: {data}")

def test_alphabet_lesson_localization(results: TestResults):
    """Test 2: Alphabet Letter Lesson - ALL 9 LOCALES (MOST CRITICAL)"""
    print("\n🔍 Testing Alphabet Letter Lesson Localization (Index 0 - Alif)...")
    
    for locale in LOCALES:
        test_name = f"Alphabet Lesson Localization - {locale.upper()}"
        data = make_request("/api/kids-learn/course/alphabet/0", {"locale": locale})
        
        if "error" in data:
            results.add_fail(test_name, data["error"])
            continue
        
        if not data.get("success"):
            results.add_fail(test_name, f"API returned success=false: {data}")
            continue
        
        lesson = data.get("lesson", {})
        games = data.get("games", [])
        
        # Check lesson name is localized (NOT English for non-English locales)
        lesson_name = lesson.get("name", "")
        if locale in EXPECTED_LETTER_NAMES:
            expected_name = EXPECTED_LETTER_NAMES[locale]
            if lesson_name != expected_name:
                results.add_fail(test_name, f"Letter name should be '{expected_name}', got '{lesson_name}'")
                continue
        elif locale == "en":
            if lesson_name != "Alif":
                results.add_fail(test_name, f"English letter name should be 'Alif', got '{lesson_name}'")
                continue
        
        # Check example_translation is localized (NOT English)
        example_translation = lesson.get("example_translation", "")
        if locale in EXPECTED_WORD_TRANSLATIONS:
            expected_word = EXPECTED_WORD_TRANSLATIONS[locale]
            if example_translation != expected_word:
                results.add_fail(test_name, f"Word translation should be '{expected_word}', got '{example_translation}'")
                continue
        elif locale == "en":
            if example_translation != "Lion":
                results.add_fail(test_name, f"English word should be 'Lion', got '{example_translation}'")
                continue
        
        # Check memory game form labels are localized
        memory_game = None
        for game in games:
            if game.get("type") == "memory":
                memory_game = game
                break
        
        if memory_game:
            cards = memory_game.get("cards", [])
            text_cards = [card["content"] for card in cards if card.get("type") == "text"]
            
            if locale in EXPECTED_FORM_LABELS:
                expected_labels = EXPECTED_FORM_LABELS[locale]
                for expected_label in expected_labels:
                    if expected_label not in text_cards:
                        results.add_fail(test_name, f"Missing localized form label '{expected_label}' in memory game")
                        break
                else:
                    # Check for English leakage in non-English locales
                    if locale != "en":
                        english_labels = ["Isolated", "Initial", "Medial", "Final"]
                        for eng_label in english_labels:
                            if eng_label in text_cards:
                                results.add_fail(test_name, f"Found English form label '{eng_label}' in {locale} locale")
                                break
                        else:
                            results.add_pass(test_name)
                    else:
                        results.add_pass(test_name)
            else:
                # For locales not in our expected list, just check no obvious English leakage
                if locale != "en":
                    english_labels = ["Isolated", "Initial", "Medial", "Final"]
                    for eng_label in english_labels:
                        if eng_label in text_cards:
                            results.add_fail(test_name, f"Found English form label '{eng_label}' in {locale} locale")
                            break
                    else:
                        results.add_pass(test_name)
                else:
                    results.add_pass(test_name)
        else:
            results.add_fail(test_name, "No memory game found in games array")

def test_alphabet_list_localization(results: TestResults):
    """Test 3: Alphabet List - Localized words"""
    print("\n🔍 Testing Alphabet List Localization...")
    
    test_locales = ["ar", "ru", "tr"]  # Key locales to test
    
    for locale in test_locales:
        test_name = f"Alphabet List Localization - {locale.upper()}"
        data = make_request("/api/kids-learn/course/alphabet", {"locale": locale})
        
        if "error" in data:
            results.add_fail(test_name, data["error"])
            continue
        
        if not data.get("success"):
            results.add_fail(test_name, f"API returned success=false: {data}")
            continue
        
        letters = data.get("letters", [])
        if not letters:
            results.add_fail(test_name, "No letters returned")
            continue
        
        # Check first letter (Alif) word translation
        first_letter = letters[0]
        word_translation = first_letter.get("word_en", "")  # This field should contain localized word
        
        if locale in EXPECTED_WORD_TRANSLATIONS:
            expected_word = EXPECTED_WORD_TRANSLATIONS[locale]
            if word_translation == expected_word:
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"word_en should be '{expected_word}', got '{word_translation}'")
        else:
            results.add_pass(test_name)  # Pass for other locales

def test_boundary_letter_lesson(results: TestResults):
    """Test 4: Letter Lesson at last index (boundary test)"""
    print("\n🔍 Testing Boundary Letter Lesson (Index 27 - Ya)...")
    
    test_name = "Boundary Letter Lesson (Index 27) - Russian"
    data = make_request("/api/kids-learn/course/alphabet/27", {"locale": "ru"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
        return
    
    if not data.get("success"):
        results.add_fail(test_name, f"API returned success=false: {data}")
        return
    
    lesson = data.get("lesson", {})
    if lesson.get("letter") == "ي" and lesson.get("name") == "Йа":
        results.add_pass(test_name)
    else:
        results.add_fail(test_name, f"Expected letter 'ي' with name 'Йа', got letter '{lesson.get('letter')}' with name '{lesson.get('name')}'")

def test_quiz_questions_localization(results: TestResults):
    """Test 5: Quiz questions localization"""
    print("\n🔍 Testing Quiz Questions Localization...")
    
    # Test Arabic locale
    test_name = "Quiz Questions - Arabic Locale"
    data = make_request("/api/kids-learn/course/alphabet/0", {"locale": "ar"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    elif not data.get("success"):
        results.add_fail(test_name, f"API returned success=false: {data}")
    else:
        games = data.get("games", [])
        quiz_game = None
        for game in games:
            if game.get("type") == "quiz":
                quiz_game = game
                break
        
        if quiz_game:
            question = quiz_game.get("question", "")
            if "ألف" in question:  # Should contain Arabic letter name
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"Quiz question should contain 'ألف', got: {question}")
        else:
            results.add_fail(test_name, "No quiz game found")
    
    # Test Russian locale
    test_name = "Quiz Questions - Russian Locale"
    data = make_request("/api/kids-learn/course/alphabet/0", {"locale": "ru"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    elif not data.get("success"):
        results.add_fail(test_name, f"API returned success=false: {data}")
    else:
        games = data.get("games", [])
        quiz_game = None
        for game in games:
            if game.get("type") == "quiz":
                quiz_game = game
                break
        
        if quiz_game:
            question = quiz_game.get("question", "")
            if "Алиф" in question:  # Should contain Russian letter name
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"Quiz question should contain 'Алиф', got: {question}")
        else:
            results.add_fail(test_name, "No quiz game found")

def test_regression_endpoints(results: TestResults):
    """Test 6: Regression Tests - Existing endpoints still working"""
    print("\n🔍 Testing Regression - Existing Endpoints...")
    
    # Test daily games
    test_name = "Regression - Daily Games"
    data = make_request("/api/kids-learn/daily-games", {"locale": "en"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    elif not data.get("success"):
        results.add_fail(test_name, f"Daily games API returned success=false: {data}")
    else:
        games = data.get("games", [])
        total_xp = data.get("total_xp", 0)
        if len(games) == 4 and total_xp == 60:
            results.add_pass(test_name)
        else:
            results.add_fail(test_name, f"Expected 4 games with 60 XP, got {len(games)} games with {total_xp} XP")
    
    # Test digital shield
    test_name = "Regression - Digital Shield"
    data = make_request("/api/kids-learn/digital-shield", {"locale": "en", "theme": "all"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    elif not data.get("success"):
        results.add_fail(test_name, f"Digital shield API returned success=false: {data}")
    else:
        lessons = data.get("lessons", [])
        if len(lessons) == 30:
            results.add_pass(test_name)
        else:
            results.add_fail(test_name, f"Expected 30 lessons, got {len(lessons)}")
    
    # Test course overview
    test_name = "Regression - Course Overview (English)"
    data = make_request("/api/kids-learn/course/overview", {"locale": "en"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    elif not data.get("success"):
        results.add_fail(test_name, f"Course overview API returned success=false: {data}")
    else:
        levels = data.get("levels", [])
        if len(levels) == 6:
            results.add_pass(test_name)
        else:
            results.add_fail(test_name, f"Expected 6 levels, got {len(levels)}")
    
    # Test course overview Arabic
    test_name = "Regression - Course Overview (Arabic)"
    data = make_request("/api/kids-learn/course/overview", {"locale": "ar"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    elif not data.get("success"):
        results.add_fail(test_name, f"Course overview Arabic API returned success=false: {data}")
    else:
        levels = data.get("levels", [])
        if len(levels) == 6:
            # Check if Arabic names are present
            first_level = levels[0]
            if "التمهيدي" in first_level.get("name", ""):
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"Expected Arabic level names, got: {first_level.get('name')}")
        else:
            results.add_fail(test_name, f"Expected 6 levels, got {len(levels)}")

def main():
    """Run all tests for Strict Localization Fix."""
    print("🚀 Starting Backend Tests: Strict Localization Fix")
    print(f"Base URL: {BASE_URL}")
    print(f"Testing {len(LOCALES)} locales: {', '.join(LOCALES)}")
    
    results = TestResults()
    
    # Run all test suites
    test_health_check(results)
    test_alphabet_lesson_localization(results)
    test_alphabet_list_localization(results)
    test_boundary_letter_lesson(results)
    test_quiz_questions_localization(results)
    test_regression_endpoints(results)
    
    # Print final summary
    success = results.summary()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! Strict Localization Fix is working correctly.")
        sys.exit(0)
    else:
        print(f"\n💥 {results.failed} TESTS FAILED! Issues found with localization.")
        sys.exit(1)

if __name__ == "__main__":
    main()