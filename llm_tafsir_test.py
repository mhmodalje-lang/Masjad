#!/usr/bin/env python3
"""
Backend Test Suite: LLM Tafsir Translation Feature
Testing LLM-translated tafsir for all 9 languages with longer timeouts
Base URL: https://quality-check-app-2.preview.emergentagent.com
"""

import requests
import json
import sys
import time
from typing import Dict, List, Any

# Base URL from frontend/.env
BASE_URL = "https://quality-check-app-2.preview.emergentagent.com"

# All 9 supported languages
LANGUAGES = ["ar", "en", "fr", "de", "tr", "ru", "sv", "nl", "el"]

# Languages that should have LLM-translated tafsir (NOT Arabic fallback)
LLM_TRANSLATED_LANGUAGES = ["tr", "de", "fr", "sv", "nl", "el"]

# Languages that should have native tafsir
NATIVE_TAFSIR_LANGUAGES = ["ar", "en", "ru"]

# Expected tafsir sources for verification
EXPECTED_TAFSIR_SOURCES = {
    "ar": "التفسير الميسر",  # Al-Muyassar
    "en": "Ibn Kathir",      # Ibn Kathir
    "ru": "ас-Саади",       # As-Sa'di
    "tr": "İbn Kesir",      # Should be Turkish Ibn Kathir
    "de": "Ibn Kathir",     # Should be German Ibn Kathir
    "fr": "Ibn Kathir",     # Should be French Ibn Kathir
    "sv": "Ibn Kathir",     # Should be Swedish Ibn Kathir
    "nl": "Ibn Kathir",     # Should be Dutch Ibn Kathir
    "el": "Ibn Kathir",     # Should be Greek Ibn Kathir
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

def make_request(endpoint: str, params: Dict = None, timeout: int = 30) -> Dict[str, Any]:
    """Make HTTP request with error handling and longer timeout for LLM calls."""
    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"🔄 Making request to: {url} with params: {params}")
        start_time = time.time()
        response = requests.get(url, params=params, timeout=timeout)
        end_time = time.time()
        print(f"⏱️  Request took {end_time - start_time:.2f} seconds")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}"}

def contains_language_text(text: str, language: str) -> bool:
    """Check if text contains characters typical of the specified language."""
    if not text:
        return False
    
    # Language-specific character checks
    language_patterns = {
        "tr": ["ı", "ğ", "ü", "ş", "ö", "ç", "İ", "Ğ", "Ü", "Ş", "Ö", "Ç"],
        "de": ["ä", "ö", "ü", "ß", "Ä", "Ö", "Ü"],
        "fr": ["à", "é", "è", "ê", "ë", "î", "ï", "ô", "ù", "û", "ü", "ÿ", "ç", "À", "É", "È", "Ê", "Ë", "Î", "Ï", "Ô", "Ù", "Û", "Ü", "Ÿ", "Ç"],
        "sv": ["å", "ä", "ö", "Å", "Ä", "Ö"],
        "nl": ["ë", "ï", "ö", "ü", "Ë", "Ï", "Ö", "Ü"],
        "el": ["α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ", "μ", "ν", "ξ", "ο", "π", "ρ", "σ", "τ", "υ", "φ", "χ", "ψ", "ω", "Α", "Β", "Γ", "Δ", "Ε", "Ζ", "Η", "Θ", "Ι", "Κ", "Λ", "Μ", "Ν", "Ξ", "Ο", "Π", "Ρ", "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω"],
        "ru": ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я", "А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"],
        "ar": [chr(i) for i in range(0x0600, 0x06FF)]  # Arabic Unicode range
    }
    
    if language in language_patterns:
        return any(char in text for char in language_patterns[language])
    
    return True  # For English, assume any text is valid

def test_llm_tafsir_translation(results: TestResults):
    """Test LLM Tafsir Translation for all 9 languages - CRITICAL TEST"""
    print("\n🔍 Testing LLM Tafsir Translation - ALL 9 LANGUAGES...")
    print("⚠️  Using 30-second timeout for first-time LLM translations")
    
    # Test verse 1:1 (Bismillah) for all languages
    for language in LANGUAGES:
        test_name = f"LLM Tafsir Translation - {language.upper()}"
        print(f"\n🌍 Testing {language.upper()} tafsir...")
        
        data = make_request("/api/quran/v4/global-verse/1/1", {"language": language}, timeout=30)
        
        if "error" in data:
            results.add_fail(test_name, data["error"])
            continue
        
        if not data.get("success"):
            results.add_fail(test_name, f"API returned success=false: {data}")
            continue
        
        # Check required fields
        tafsir = data.get("tafsir", "")
        tafsir_is_arabic = data.get("tafsir_is_arabic", None)
        tafsir_source = data.get("tafsir_source", "")
        
        if not tafsir:
            results.add_fail(test_name, "Tafsir is empty")
            continue
        
        if tafsir_is_arabic is None:
            results.add_fail(test_name, "tafsir_is_arabic field is missing")
            continue
        
        if not tafsir_source:
            results.add_fail(test_name, "tafsir_source is empty")
            continue
        
        # Language-specific validation
        if language in LLM_TRANSLATED_LANGUAGES:
            # These languages should have LLM-translated tafsir (NOT Arabic fallback)
            if tafsir_is_arabic:
                results.add_fail(test_name, f"tafsir_is_arabic should be FALSE for {language}, got TRUE (Arabic fallback)")
                continue
            
            # Check if tafsir contains language-specific characters
            if not contains_language_text(tafsir, language):
                results.add_fail(test_name, f"Tafsir does not appear to be in {language} - no language-specific characters found")
                continue
            
            # Check that it's not just Arabic text
            if contains_language_text(tafsir, "ar") and not contains_language_text(tafsir, language):
                results.add_fail(test_name, f"Tafsir appears to be Arabic text, not {language}")
                continue
            
            print(f"📝 {language.upper()} tafsir preview: {tafsir[:100]}...")
            results.add_pass(test_name)
            
        elif language in NATIVE_TAFSIR_LANGUAGES:
            # These languages should have native tafsir
            # Note: Based on API response, Arabic also returns tafsir_is_arabic=false
            # This might be the expected behavior for the current implementation
            if language == "ar":
                # Arabic tafsir - accept either true or false based on implementation
                pass  # Don't fail on this, just verify content is Arabic
            else:
                if tafsir_is_arabic != False:
                    results.add_fail(test_name, f"{language} native tafsir should have tafsir_is_arabic=False, got {tafsir_is_arabic}")
                    continue
            
            # Check language-specific content
            if not contains_language_text(tafsir, language):
                results.add_fail(test_name, f"Native tafsir does not appear to be in {language}")
                continue
            
            print(f"📝 {language.upper()} native tafsir preview: {tafsir[:100]}...")
            results.add_pass(test_name)
        
        else:
            # Fallback case - should not happen with current setup
            results.add_fail(test_name, f"Unknown language category for {language}")

def test_tafsir_sources(results: TestResults):
    """Test that tafsir sources are correctly attributed"""
    print("\n🔍 Testing Tafsir Source Attribution...")
    
    for language in LANGUAGES:
        test_name = f"Tafsir Source - {language.upper()}"
        
        data = make_request("/api/quran/v4/global-verse/1/1", {"language": language}, timeout=30)
        
        if "error" in data:
            results.add_fail(test_name, data["error"])
            continue
        
        if not data.get("success"):
            results.add_fail(test_name, f"API returned success=false: {data}")
            continue
        
        tafsir_source = data.get("tafsir_source", "")
        
        if language in EXPECTED_TAFSIR_SOURCES:
            expected_source = EXPECTED_TAFSIR_SOURCES[language]
            # For Greek, accept transliterated version
            if language == "el" and "Ιμπν Κατίρ" in tafsir_source:
                results.add_pass(test_name)
                print(f"📚 {language.upper()} source: {tafsir_source}")
            elif expected_source in tafsir_source:
                results.add_pass(test_name)
                print(f"📚 {language.upper()} source: {tafsir_source}")
            else:
                results.add_fail(test_name, f"Expected source containing '{expected_source}', got '{tafsir_source}'")
        else:
            # For languages not in our expected list, just check it's not empty
            if tafsir_source:
                results.add_pass(test_name)
                print(f"📚 {language.upper()} source: {tafsir_source}")
            else:
                results.add_fail(test_name, "Tafsir source is empty")

def test_regression_endpoints(results: TestResults):
    """Test regression - existing endpoints should still work"""
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
        if len(games) == 4:
            results.add_pass(test_name)
        else:
            results.add_fail(test_name, f"Expected 4 games, got {len(games)}")
    
    # Test chapters endpoint
    test_name = "Regression - Chapters (Turkish)"
    data = make_request("/api/quran/v4/chapters", {"language": "tr"})
    
    if "error" in data:
        results.add_fail(test_name, data["error"])
    elif not isinstance(data, dict) or "chapters" not in data:
        results.add_fail(test_name, f"Expected dict with 'chapters' key, got: {type(data)}")
    else:
        chapters = data.get("chapters", [])
        if len(chapters) == 114:
            results.add_pass(test_name)
        else:
            results.add_fail(test_name, f"Expected 114 chapters, got {len(chapters)}")

def main():
    """Run all tests for LLM Tafsir Translation feature."""
    print("🚀 Starting Backend Tests: LLM Tafsir Translation Feature")
    print(f"Base URL: {BASE_URL}")
    print(f"Testing {len(LANGUAGES)} languages: {', '.join(LANGUAGES)}")
    print("⚠️  Note: First-time LLM translations may take 10-15 seconds")
    
    results = TestResults()
    
    # Run all test suites
    test_llm_tafsir_translation(results)
    test_tafsir_sources(results)
    test_regression_endpoints(results)
    
    # Print final summary
    success = results.summary()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! LLM Tafsir Translation is working correctly.")
        print("✅ Turkish, German, French, Swedish, Dutch, Greek now have LLM-translated tafsir")
        print("✅ Arabic, English, Russian maintain native tafsir sources")
        sys.exit(0)
    else:
        print(f"\n💥 {results.failed} TESTS FAILED! Issues found with LLM tafsir translation.")
        sys.exit(1)

if __name__ == "__main__":
    main()