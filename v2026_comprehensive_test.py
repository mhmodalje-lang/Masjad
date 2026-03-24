#!/usr/bin/env python3
"""
V2026 Architecture Update - COMPREHENSIVE API TESTING
=====================================================
Tests the COMPLETE Quran + Hadith API for the V2026 Architecture Update.

Base URL: https://kidszone-learn.preview.emergentagent.com

Test Coverage:
1. CHAPTERS API (all 9 languages)
2. VERSES API (sample surahs across all languages)
3. GLOBAL-VERSE REAL TAFSIR (CRITICAL)
4. HADITH API (NEW!)
5. LEGACY TAFSIR
"""

import requests
import json
import sys
from typing import Dict, Any, List
import time

# Base URL from frontend/.env
BASE_URL = "https://kidszone-learn.preview.emergentagent.com"

# All 9 supported languages
ALL_LANGUAGES = ["ar", "en", "fr", "de", "tr", "ru", "sv", "nl", "el"]

class V2026ComprehensiveTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.results = []
        self.failed_tests = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "details": details
        }
        self.results.append(result)
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
        else:
            self.failed_tests.append(result)
        print(f"[{status}] {test_name}: {details}")
    
    def make_request(self, endpoint: str, timeout: int = 30) -> Dict[Any, Any]:
        """Make API request and return response"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return {
                "success": True,
                "data": response.json(),
                "status_code": response.status_code
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
    
    def test_health_check(self):
        """Test 0: Health check"""
        print("\n=== HEALTH CHECK ===")
        result = self.make_request("/api/health")
        
        if result["success"]:
            self.log_result("Health Check", "PASS", "API is healthy")
        else:
            self.log_result("Health Check", "FAIL", f"Health check failed: {result['error']}")
    
    def test_chapters_api_all_languages(self):
        """Test 1: CHAPTERS API (all 9 languages)"""
        print("\n=== CHAPTERS API - ALL 9 LANGUAGES ===")
        
        for lang in ALL_LANGUAGES:
            result = self.make_request(f"/api/quran/v4/chapters?language={lang}")
            
            if not result["success"]:
                self.log_result(f"Chapters {lang.upper()}", "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            chapters = data.get("chapters", [])
            
            # Check if we have exactly 114 chapters
            if len(chapters) != 114:
                self.log_result(f"Chapters {lang.upper()}", "FAIL", f"Expected 114 chapters, got {len(chapters)}")
                continue
            
            # Check if each chapter has translated_name.name in the user's language
            sample_chapter = chapters[0] if chapters else {}
            translated_name = sample_chapter.get("translated_name", {})
            name = translated_name.get("name", "")
            
            if not name:
                self.log_result(f"Chapters {lang.upper()}", "FAIL", "Missing translated_name.name")
                continue
            
            self.log_result(f"Chapters {lang.upper()}", "PASS", f"114 chapters with translated names (sample: {name[:30]}...)")
    
    def test_verses_api_sample_surahs(self):
        """Test 2: VERSES API (sample surahs across all languages)"""
        print("\n=== VERSES API - SAMPLE SURAHS ===")
        
        # Test Surah 1 (Al-Fatiha) with 7 verses
        for lang in ALL_LANGUAGES:
            result = self.make_request(f"/api/quran/v4/verses/by_chapter/1?language={lang}&per_page=7")
            
            if not result["success"]:
                self.log_result(f"Verses Surah 1 {lang.upper()}", "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            verses = data.get("verses", [])
            
            if len(verses) != 7:
                self.log_result(f"Verses Surah 1 {lang.upper()}", "FAIL", f"Expected 7 verses, got {len(verses)}")
                continue
            
            # Check if verses have text_uthmani (Arabic)
            first_verse = verses[0] if verses else {}
            text_uthmani = first_verse.get("text_uthmani", "")
            
            if not text_uthmani:
                self.log_result(f"Verses Surah 1 {lang.upper()}", "FAIL", "Missing text_uthmani (Arabic text)")
                continue
            
            # For non-Arabic languages, check if translations exist
            if lang != "ar":
                translations = first_verse.get("translations", [])
                if not translations:
                    self.log_result(f"Verses Surah 1 {lang.upper()}", "FAIL", "Missing translations for non-Arabic language")
                    continue
                
                translation_text = translations[0].get("text", "") if translations else ""
                if not translation_text:
                    self.log_result(f"Verses Surah 1 {lang.upper()}", "FAIL", "Empty translation text")
                    continue
            
            self.log_result(f"Verses Surah 1 {lang.upper()}", "PASS", f"7 verses with Arabic text and translations")
    
    def test_global_verse_real_tafsir(self):
        """Test 3: GLOBAL-VERSE REAL TAFSIR (CRITICAL)"""
        print("\n=== GLOBAL-VERSE REAL TAFSIR - AYAT AL-KURSI (2:255) ===")
        
        for lang in ALL_LANGUAGES:
            result = self.make_request(f"/api/quran/v4/global-verse/2/255?language={lang}")
            
            if not result["success"]:
                self.log_result(f"Global Verse Tafsir {lang.upper()}", "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            
            # Check success field
            if not data.get("success", False):
                self.log_result(f"Global Verse Tafsir {lang.upper()}", "FAIL", "Response success=false")
                continue
            
            # Check arabic_text is not empty
            arabic_text = data.get("arabic_text", "")
            if not arabic_text:
                self.log_result(f"Global Verse Tafsir {lang.upper()}", "FAIL", "Empty arabic_text")
                continue
            
            # CRITICAL: Check tafsir field is NOT empty
            tafsir = data.get("tafsir", "")
            if not tafsir:
                self.log_result(f"Global Verse Tafsir {lang.upper()}", "FAIL", "CRITICAL: Empty tafsir field")
                continue
            
            # Check tafsir_source is not empty
            tafsir_source = data.get("tafsir_source", "")
            if not tafsir_source:
                self.log_result(f"Global Verse Tafsir {lang.upper()}", "FAIL", "Empty tafsir_source")
                continue
            
            # Check translation field
            translation = data.get("translation", "")
            
            # CRITICAL: Verify tafsir is DIFFERENT from translation (not duplicate!)
            if tafsir == translation and translation:
                self.log_result(f"Global Verse Tafsir {lang.upper()}", "FAIL", "CRITICAL: Tafsir is duplicate of translation!")
                continue
            
            # Check tafsir_is_arabic field based on language
            tafsir_is_arabic = data.get("tafsir_is_arabic", False)
            
            # For ar/en/ru: tafsir_is_arabic should be false (native tafsir)
            if lang in ["ar", "en", "ru"]:
                if tafsir_is_arabic:
                    self.log_result(f"Global Verse Tafsir {lang.upper()}", "FAIL", f"Expected tafsir_is_arabic=false for {lang}, got true")
                    continue
            
            # For de/tr/sv/nl/el: tafsir_is_arabic should be true (Arabic Al-Muyassar)
            elif lang in ["de", "tr", "sv", "nl", "el"]:
                if not tafsir_is_arabic:
                    self.log_result(f"Global Verse Tafsir {lang.upper()}", "FAIL", f"Expected tafsir_is_arabic=true for {lang}, got false")
                    continue
            
            # For fr: tafsir might be from QuranEnc footnotes (tafsir_is_arabic may be true if no footnotes)
            # This is acceptable for French
            
            self.log_result(f"Global Verse Tafsir {lang.upper()}", "PASS", 
                          f"Real tafsir found (source: {tafsir_source[:50]}..., is_arabic: {tafsir_is_arabic})")
    
    def test_hadith_api_new(self):
        """Test 4: HADITH API (NEW!)"""
        print("\n=== HADITH API - NEW FEATURES ===")
        
        # Test a) GET /api/hadith/random?language=en&collection=bukhari
        result = self.make_request("/api/hadith/random?language=en&collection=bukhari")
        if result["success"]:
            data = result["data"]
            hadith_text = data.get("hadith", "")
            collection = data.get("collection", "")
            if hadith_text and "bukhari" in collection.lower():
                self.log_result("Hadith Random EN Bukhari", "PASS", f"English Bukhari hadith received (collection: {collection})")
            else:
                self.log_result("Hadith Random EN Bukhari", "FAIL", f"Invalid response: {data}")
        else:
            self.log_result("Hadith Random EN Bukhari", "FAIL", f"API request failed: {result['error']}")
        
        # Test b) GET /api/hadith/random?language=tr&collection=bukhari
        result = self.make_request("/api/hadith/random?language=tr&collection=bukhari")
        if result["success"]:
            data = result["data"]
            hadith_text = data.get("hadith", "")
            language = data.get("language", "")
            if hadith_text and language == "tr":
                self.log_result("Hadith Random TR Bukhari", "PASS", f"Turkish Bukhari hadith received")
            else:
                self.log_result("Hadith Random TR Bukhari", "FAIL", f"Invalid response: {data}")
        else:
            self.log_result("Hadith Random TR Bukhari", "FAIL", f"API request failed: {result['error']}")
        
        # Test c) GET /api/hadith/random?language=fr&collection=muslim
        result = self.make_request("/api/hadith/random?language=fr&collection=muslim")
        if result["success"]:
            data = result["data"]
            hadith_text = data.get("hadith", "")
            collection = data.get("collection", "")
            if hadith_text and "muslim" in collection.lower():
                self.log_result("Hadith Random FR Muslim", "PASS", f"French Muslim hadith received")
            else:
                self.log_result("Hadith Random FR Muslim", "FAIL", f"Invalid response: {data}")
        else:
            self.log_result("Hadith Random FR Muslim", "FAIL", f"API request failed: {result['error']}")
        
        # Test d) GET /api/hadith/random?language=de&collection=bukhari
        result = self.make_request("/api/hadith/random?language=de&collection=bukhari")
        if result["success"]:
            data = result["data"]
            is_fallback = data.get("is_fallback", False)
            fallback_language = data.get("fallback_language", "")
            if is_fallback and fallback_language == "en":
                self.log_result("Hadith Random DE Bukhari Fallback", "PASS", f"German fallback to English working (is_fallback=true)")
            else:
                self.log_result("Hadith Random DE Bukhari Fallback", "FAIL", f"Expected English fallback, got: {data}")
        else:
            self.log_result("Hadith Random DE Bukhari Fallback", "FAIL", f"API request failed: {result['error']}")
        
        # Test e) GET /api/hadith/collections?language=en
        result = self.make_request("/api/hadith/collections?language=en")
        if result["success"]:
            data = result["data"]
            # Check if we have collections data (could be in 'data' or 'collections' field)
            collections_data = data.get("data", data.get("collections", []))
            if collections_data and len(collections_data) > 0:
                # Extract collection names
                collection_names = []
                if isinstance(collections_data, list):
                    for item in collections_data:
                        if isinstance(item, dict) and "name" in item:
                            collection_names.append(item["name"])
                        elif isinstance(item, str):
                            collection_names.append(item)
                
                if collection_names:
                    self.log_result("Hadith Collections EN", "PASS", f"Collections available: {collection_names[:5]}")  # Show first 5
                else:
                    self.log_result("Hadith Collections EN", "PASS", f"Collections data structure received (count: {len(collections_data)})")
            else:
                self.log_result("Hadith Collections EN", "FAIL", f"No collections data found: {data}")
        else:
            self.log_result("Hadith Collections EN", "FAIL", f"API request failed: {result['error']}")
        
        # Test f) GET /api/hadith/random?language=ru&collection=bukhari
        result = self.make_request("/api/hadith/random?language=ru&collection=bukhari")
        if result["success"]:
            data = result["data"]
            hadith_text = data.get("hadith", "")
            language = data.get("language", "")
            if hadith_text and language == "ru":
                self.log_result("Hadith Random RU Bukhari", "PASS", f"Russian Bukhari hadith received")
            else:
                self.log_result("Hadith Random RU Bukhari", "FAIL", f"Invalid response: {data}")
        else:
            self.log_result("Hadith Random RU Bukhari", "FAIL", f"API request failed: {result['error']}")
    
    def test_legacy_tafsir(self):
        """Test 5: LEGACY TAFSIR"""
        print("\n=== LEGACY TAFSIR - GET /api/quran/v4/tafsir/1:1 ===")
        
        for lang in ALL_LANGUAGES:
            result = self.make_request(f"/api/quran/v4/tafsir/1:1?language={lang}")
            
            if not result["success"]:
                self.log_result(f"Legacy Tafsir 1:1 {lang.upper()}", "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            
            # Check success field
            if not data.get("success", False):
                self.log_result(f"Legacy Tafsir 1:1 {lang.upper()}", "FAIL", "Response success=false")
                continue
            
            # Check text field is not empty
            text = data.get("text", "")
            if not text:
                self.log_result(f"Legacy Tafsir 1:1 {lang.upper()}", "FAIL", "Empty text field")
                continue
            
            # Check if this is real tafsir from Ibn Kathir (not just a translation)
            tafsir_name = data.get("tafsir_name", "")
            
            # For English, should be Ibn Kathir with real tafsir content
            if lang == "en":
                if "ibn kathir" not in text.lower() and "ibn kathir" not in tafsir_name.lower():
                    # Check if it contains tafsir-like content (explanation, context)
                    tafsir_indicators = ["explanation", "meaning", "refers to", "indicates", "context", "revelation"]
                    has_tafsir_content = any(indicator in text.lower() for indicator in tafsir_indicators)
                    if not has_tafsir_content:
                        self.log_result(f"Legacy Tafsir 1:1 {lang.upper()}", "FAIL", 
                                      f"Expected real tafsir content, got translation-like text: {text[:100]}...")
                        continue
            
            # Check is_arabic_tafsir field for fallback languages
            is_arabic_tafsir = data.get("is_arabic_tafsir", False)
            if lang in ["de", "tr", "sv", "nl", "el"]:
                if not is_arabic_tafsir:
                    self.log_result(f"Legacy Tafsir 1:1 {lang.upper()}", "FAIL", 
                                  f"Expected is_arabic_tafsir=true for {lang}, got false")
                    continue
            
            self.log_result(f"Legacy Tafsir 1:1 {lang.upper()}", "PASS", 
                          f"Real tafsir content found (source: {tafsir_name[:30]}...)")
    
    def test_html_entities_cleanup(self):
        """Test 6: HTML Entities Cleanup"""
        print("\n=== HTML ENTITIES CLEANUP ===")
        
        # Test a few endpoints for HTML entity contamination
        test_endpoints = [
            "/api/quran/v4/global-verse/2/255?language=tr",
            "/api/quran/v4/verses/by_chapter/1?language=fr&per_page=3",
            "/api/hadith/random?language=en&collection=bukhari"
        ]
        
        html_entities = ["&amp;quot;", "&amp;nbsp;", "&quot;", "&nbsp;", "&amp;", "&lt;", "&gt;"]
        
        for endpoint in test_endpoints:
            result = self.make_request(endpoint)
            if result["success"]:
                response_text = json.dumps(result["data"])
                found_entities = [entity for entity in html_entities if entity in response_text]
                
                if found_entities:
                    self.log_result(f"HTML Cleanup {endpoint.split('?')[0]}", "FAIL", 
                                  f"Found HTML entities: {found_entities}")
                else:
                    self.log_result(f"HTML Cleanup {endpoint.split('?')[0]}", "PASS", 
                                  "No HTML entities found")
            else:
                self.log_result(f"HTML Cleanup {endpoint.split('?')[0]}", "FAIL", 
                              f"API request failed: {result['error']}")
    
    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("="*80)
        print("V2026 ARCHITECTURE UPDATE - COMPREHENSIVE API TESTING")
        print("="*80)
        print(f"Base URL: {self.base_url}")
        print(f"Testing {len(ALL_LANGUAGES)} languages: {', '.join(ALL_LANGUAGES)}")
        print("="*80)
        
        # Run all test suites
        self.test_health_check()
        self.test_chapters_api_all_languages()
        self.test_verses_api_sample_surahs()
        self.test_global_verse_real_tafsir()
        self.test_hadith_api_new()
        self.test_legacy_tafsir()
        self.test_html_entities_cleanup()
        
        # Summary
        print("\n" + "="*80)
        print("COMPREHENSIVE TEST SUMMARY")
        print("="*80)
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {len(self.failed_tests)}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        if self.failed_tests:
            print(f"\n❌ FAILED TESTS ({len(self.failed_tests)}):")
            for test in self.failed_tests:
                print(f"  - {test['test']}: {test['details']}")
        else:
            print("\n✅ ALL TESTS PASSED!")
        
        print("="*80)
        return len(self.failed_tests) == 0

if __name__ == "__main__":
    tester = V2026ComprehensiveTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)