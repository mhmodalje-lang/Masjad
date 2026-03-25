#!/usr/bin/env python3
"""
Backend Test Suite: Quran Page Rebuild API Testing
Testing all Quran API endpoints for the rebuilt Quran page
Base URL: https://backend-localization.preview.emergentagent.com
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Base URL from the review request
BASE_URL = "https://backend-localization.preview.emergentagent.com"

# Test languages
TEST_LANGUAGES = ["ru", "ar", "fr", "tr", "en"]

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

def test_chapters_multiple_languages(results: TestResults):
    """Test 1: Chapter List (All Surahs) — Multiple languages"""
    print("\n🔍 Testing Chapter List in Multiple Languages...")
    
    for language in TEST_LANGUAGES:
        test_name = f"Chapters List - {language.upper()}"
        data = make_request("/api/quran/v4/chapters", {"language": language})
        
        if "error" in data:
            results.add_fail(test_name, data["error"])
            continue
        
        # Check if we have chapters array
        chapters = data.get("chapters", [])
        if not chapters:
            results.add_fail(test_name, "No chapters array found in response")
            continue
        
        # Should return exactly 114 surahs
        if len(chapters) != 114:
            results.add_fail(test_name, f"Expected 114 chapters, got {len(chapters)}")
            continue
        
        # Check first surah structure
        first_surah = chapters[0]
        required_fields = ["id", "name_arabic", "translated_name"]
        
        for field in required_fields:
            if field not in first_surah:
                results.add_fail(test_name, f"Missing required field: {field}")
                break
        else:
            # Check if translated_name has proper structure
            translated_name = first_surah.get("translated_name", {})
            if not isinstance(translated_name, dict) or "name" not in translated_name:
                results.add_fail(test_name, "translated_name should be object with 'name' field")
                continue
            
            # For Russian, check if we have Russian translated name
            if language == "ru":
                name = translated_name.get("name", "")
                if not name or name == first_surah.get("name_arabic", ""):
                    results.add_fail(test_name, "Russian translated name should be different from Arabic name")
                    continue
            
            results.add_pass(test_name)

def test_chapter_info(results: TestResults):
    """Test 2: Chapter Info"""
    print("\n🔍 Testing Chapter Info...")
    
    # Test Al-Fatihah with Russian
    test_name = "Chapter Info - Al-Fatihah (Russian)"
    data = make_request("/api/quran/v4/chapters/1", {"language": "ru"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        chapter = data.get("chapter", {})
        if not chapter:
            results.add_fail(test_name, "No chapter object found in response")
        else:
            # Check if we have translated name
            translated_name = chapter.get("translated_name", {})
            if translated_name.get("name") == "Открывающая Коран":
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"Expected Russian name 'Открывающая Коран', got: {translated_name.get('name')}")
    
    # Test An-Nas with French
    test_name = "Chapter Info - An-Nas (French)"
    data = make_request("/api/quran/v4/chapters/114", {"language": "fr"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        chapter = data.get("chapter", {})
        if not chapter:
            results.add_fail(test_name, "No chapter object found in response")
        else:
            # Check if we have French translated name
            translated_name = chapter.get("translated_name", {})
            name = translated_name.get("name", "")
            if name and name != chapter.get("name_arabic", ""):
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"Expected French translated name, got: {name}")

def test_verses_with_translation(results: TestResults):
    """Test 3: Verses with Translation"""
    print("\n🔍 Testing Verses with Translation...")
    
    # Test Russian translation
    test_name = "Verses - Al-Fatihah (Russian)"
    data = make_request("/api/quran/v4/verses/by_chapter/1", {"language": "ru", "per_page": "10"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        verses = data.get("verses", [])
        if len(verses) != 7:
            results.add_fail(test_name, f"Expected 7 verses for Al-Fatihah, got {len(verses)}")
        else:
            # Check first verse has Russian translation
            first_verse = verses[0]
            translations = first_verse.get("translations", [])
            if not translations:
                results.add_fail(test_name, "No translations found in verse")
            else:
                translation_text = translations[0].get("text", "")
                if translation_text and translation_text != first_verse.get("text_uthmani", ""):
                    results.add_pass(test_name)
                else:
                    results.add_fail(test_name, "Russian translation text should be different from Arabic text")
    
    # Test French translation
    test_name = "Verses - Al-Fatihah (French)"
    data = make_request("/api/quran/v4/verses/by_chapter/1", {"language": "fr", "per_page": "10"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        verses = data.get("verses", [])
        if len(verses) != 7:
            results.add_fail(test_name, f"Expected 7 verses for Al-Fatihah, got {len(verses)}")
        else:
            # Check first verse has French translation
            first_verse = verses[0]
            translations = first_verse.get("translations", [])
            if translations and translations[0].get("text"):
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, "No French translation text found")
    
    # Test Arabic (should have text_uthmani but no separate translation)
    test_name = "Verses - Al-Fatihah (Arabic)"
    data = make_request("/api/quran/v4/verses/by_chapter/1", {"language": "ar", "per_page": "10"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        verses = data.get("verses", [])
        if len(verses) != 7:
            results.add_fail(test_name, f"Expected 7 verses for Al-Fatihah, got {len(verses)}")
        else:
            # Check first verse has Arabic text
            first_verse = verses[0]
            text_uthmani = first_verse.get("text_uthmani", "")
            if text_uthmani:
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, "No Arabic text_uthmani found")

def test_tafsir_critical(results: TestResults):
    """Test 4: Tafsir (Most Critical)"""
    print("\n🔍 Testing Tafsir (MOST CRITICAL)...")
    
    # Test Russian tafsir
    test_name = "Tafsir - Russian (As-Sa'di)"
    data = make_request("/api/quran/v4/global-verse/1/1", {"language": "ru"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        if not data.get("success"):
            results.add_fail(test_name, f"API returned success=false: {data}")
        else:
            tafsir = data.get("tafsir", "")
            tafsir_is_arabic = data.get("tafsir_is_arabic", True)
            
            if not tafsir:
                results.add_fail(test_name, "Tafsir text is empty")
            elif tafsir_is_arabic:
                results.add_fail(test_name, "tafsir_is_arabic should be false for Russian")
            else:
                results.add_pass(test_name)
    
    # Test Arabic tafsir
    test_name = "Tafsir - Arabic (Al-Muyassar)"
    data = make_request("/api/quran/v4/global-verse/1/1", {"language": "ar"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        if not data.get("success"):
            results.add_fail(test_name, f"API returned success=false: {data}")
        else:
            tafsir = data.get("tafsir", "")
            if tafsir:
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, "Arabic tafsir text is empty")
    
    # Test English tafsir
    test_name = "Tafsir - English (Ibn Kathir)"
    data = make_request("/api/quran/v4/global-verse/1/1", {"language": "en"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        if not data.get("success"):
            results.add_fail(test_name, f"API returned success=false: {data}")
        else:
            tafsir = data.get("tafsir", "")
            tafsir_is_arabic = data.get("tafsir_is_arabic", True)
            
            if not tafsir:
                results.add_fail(test_name, "English tafsir text is empty")
            elif tafsir_is_arabic:
                results.add_fail(test_name, "tafsir_is_arabic should be false for English")
            else:
                results.add_pass(test_name)
    
    # Test Turkish tafsir (should fallback to Arabic)
    test_name = "Tafsir - Turkish (Arabic fallback)"
    data = make_request("/api/quran/v4/global-verse/1/1", {"language": "tr"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        if not data.get("success"):
            results.add_fail(test_name, f"API returned success=false: {data}")
        else:
            tafsir = data.get("tafsir", "")
            tafsir_is_arabic = data.get("tafsir_is_arabic", False)
            
            if not tafsir:
                results.add_fail(test_name, "Turkish tafsir text is empty")
            elif not tafsir_is_arabic:
                results.add_fail(test_name, "tafsir_is_arabic should be true for Turkish (Arabic fallback)")
            else:
                results.add_pass(test_name)

def test_regression_endpoints(results: TestResults):
    """Test 5: Regression Tests"""
    print("\n🔍 Testing Regression Endpoints...")
    
    # Test daily games
    test_name = "Regression - Daily Games"
    data = make_request("/api/kids-learn/daily-games", {"locale": "en"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        if not data.get("success"):
            results.add_fail(test_name, f"Daily games API returned success=false: {data}")
        else:
            games = data.get("games", [])
            if len(games) == 4:
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"Expected 4 games, got {len(games)}")
    
    # Test Arabic course alphabet
    test_name = "Regression - Arabic Course Alphabet"
    data = make_request("/api/kids-learn/course/alphabet/0", {"locale": "ru"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        if not data.get("success"):
            results.add_fail(test_name, f"Alphabet API returned success=false: {data}")
        else:
            lesson = data.get("lesson", {})
            letter_name = lesson.get("name", "")
            if letter_name == "Алиф":
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"Expected Russian letter name 'Алиф', got '{letter_name}'")
    
    # Test digital shield
    test_name = "Regression - Digital Shield"
    data = make_request("/api/kids-learn/digital-shield", {"locale": "fr", "theme": "all"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    else:
        if not data.get("success"):
            results.add_fail(test_name, f"Digital shield API returned success=false: {data}")
        else:
            lessons = data.get("lessons", [])
            if len(lessons) == 30:
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"Expected 30 lessons, got {len(lessons)}")

def main():
    """Run all tests for Quran Page Rebuild."""
    print("🚀 Starting Backend Tests: Quran Page Rebuild API Testing")
    print(f"Base URL: {BASE_URL}")
    print(f"Testing languages: {', '.join(TEST_LANGUAGES)}")
    
    results = TestResults()
    
    # Run all test suites
    test_chapters_multiple_languages(results)
    test_chapter_info(results)
    test_verses_with_translation(results)
    test_tafsir_critical(results)
    test_regression_endpoints(results)
    
    # Print final summary
    success = results.summary()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! Quran Page Rebuild API is working correctly.")
        sys.exit(0)
    else:
        print(f"\n💥 {results.failed} TESTS FAILED! Issues found with Quran API endpoints.")
        sys.exit(1)

if __name__ == "__main__":
    main()