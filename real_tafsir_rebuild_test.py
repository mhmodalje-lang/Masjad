#!/usr/bin/env python3
"""
REAL TAFSIR REBUILD - Comprehensive Testing Suite
Tests all Quran API endpoints as specified in the review request
Focus: Verify REAL tafsir content (not duplicate translations)
"""

import requests
import json
import sys
import re
from typing import Dict, Any, List

# Base URL from review request
BASE_URL = "https://mobile-deploy-23.preview.emergentagent.com"

# All 9 languages to test
LANGUAGES = ["ar", "en", "fr", "de", "tr", "ru", "sv", "nl", "el"]

class RealTafsirTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.results = []
        self.failed_tests = []
        self.languages = LANGUAGES
        self.critical_failures = []
        
    def log_result(self, test_name: str, status: str, details: str = "", is_critical: bool = False):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "critical": is_critical
        }
        self.results.append(result)
        if status == "FAIL":
            self.failed_tests.append(result)
            if is_critical:
                self.critical_failures.append(result)
        
        status_icon = "❌" if status == "FAIL" else "✅"
        critical_marker = " [CRITICAL]" if is_critical else ""
        print(f"{status_icon} {test_name}{critical_marker}: {details}")
    
    def make_request(self, endpoint: str) -> Dict[Any, Any]:
        """Make API request and return response"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return {
                "success": True,
                "data": response.json(),
                "status_code": response.status_code,
                "url": url
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
                "url": url
            }
    
    def check_html_entities(self, text: str) -> List[str]:
        """Check for HTML entities in text"""
        html_entities = []
        patterns = [
            r'&amp;quot;',
            r'&amp;nbsp;',
            r'&quot;',
            r'&nbsp;',
            r'&amp;',
            r'&lt;',
            r'&gt;',
            r'&apos;'
        ]
        
        for pattern in patterns:
            if re.search(pattern, text):
                html_entities.append(pattern)
        
        return html_entities
    
    def test_chapters_all_languages(self):
        """Test 1: Chapters in all 9 languages - GET /api/quran/v4/chapters?language={lang}"""
        print("\n🔍 TEST 1: CHAPTERS IN ALL 9 LANGUAGES")
        print("=" * 60)
        
        for lang in self.languages:
            endpoint = f"/api/quran/v4/chapters?language={lang}"
            result = self.make_request(endpoint)
            
            test_name = f"Chapters {lang.upper()}"
            
            if not result["success"]:
                self.log_result(test_name, "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            chapters = data if isinstance(data, list) else data.get("chapters", [])
            
            # Should return exactly 114 chapters
            if len(chapters) != 114:
                self.log_result(test_name, "FAIL", f"Expected 114 chapters, got {len(chapters)}")
                continue
            
            # Check that chapters have translated_name.name (in user's language, NOT Arabic)
            first_chapter = chapters[0] if chapters else {}
            translated_name = first_chapter.get("translated_name", {})
            name = translated_name.get("name", "")
            
            if not name:
                self.log_result(test_name, "FAIL", "Missing translated_name.name")
                continue
            
            # For non-Arabic languages, the name should not be purely Arabic
            if lang != "ar" and self._is_arabic_text(name):
                self.log_result(test_name, "FAIL", f"translated_name.name is in Arabic for {lang}: {name}")
                continue
            
            self.log_result(test_name, "PASS", f"114 chapters, first chapter name: {name[:30]}...")
    
    def _is_arabic_text(self, text: str) -> bool:
        """Check if text contains primarily Arabic characters"""
        arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        return arabic_chars > len(text) * 0.7
    
    def test_verses_surah_1_all_languages(self):
        """Test 2: Verses for Surah 1 in all 9 languages - GET /api/quran/v4/verses/by_chapter/1?language={lang}&per_page=7"""
        print("\n🔍 TEST 2: VERSES FOR SURAH 1 IN ALL 9 LANGUAGES")
        print("=" * 60)
        
        for lang in self.languages:
            endpoint = f"/api/quran/v4/verses/by_chapter/1?language={lang}&per_page=7"
            result = self.make_request(endpoint)
            
            test_name = f"Verses Surah 1 {lang.upper()}"
            
            if not result["success"]:
                self.log_result(test_name, "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            verses = data.get("verses", [])
            
            # Should return 7 verses (Al-Fatiha has 7 verses)
            if len(verses) != 7:
                self.log_result(test_name, "FAIL", f"Expected 7 verses, got {len(verses)}")
                continue
            
            # Check that verses have text_uthmani
            first_verse = verses[0] if verses else {}
            text_uthmani = first_verse.get("text_uthmani", "")
            
            if not text_uthmani:
                self.log_result(test_name, "FAIL", "Missing text_uthmani")
                continue
            
            # For non-Arabic languages, should have translations
            if lang != "ar":
                translations = first_verse.get("translations", [])
                if not translations:
                    self.log_result(test_name, "FAIL", "Missing translations for non-Arabic language")
                    continue
                
                translation_text = translations[0].get("text", "") if translations else ""
                if not translation_text:
                    self.log_result(test_name, "FAIL", "Translation text is empty")
                    continue
            
            self.log_result(test_name, "PASS", f"7 verses with text_uthmani and translations")
    
    def test_real_tafsir_critical(self):
        """Test 3: REAL TAFSIR test (CRITICAL) - GET /api/quran/v4/global-verse/2/255?language={lang}"""
        print("\n🔍 TEST 3: REAL TAFSIR TEST (CRITICAL) - AYAT AL-KURSI 2:255")
        print("=" * 60)
        
        # Expected tafsir sources for verification
        expected_tafsir_sources = {
            "ar": "التفسير الميسر",  # Arabic scholarly tafsir
            "en": "Ibn Kathir",      # Real tafsir with explanation about virtues, hadith, etc.
            "ru": "ас-Саади",       # Real Russian tafsir
            "fr": "QuranEnc",       # Explanatory footnotes from QuranEnc
            # For de, tr, sv, nl, el: tafsir should be in Arabic (التفسير الميسر)
        }
        
        for lang in self.languages:
            endpoint = f"/api/quran/v4/global-verse/2/255?language={lang}"
            result = self.make_request(endpoint)
            
            test_name = f"REAL TAFSIR {lang.upper()}"
            
            if not result["success"]:
                self.log_result(test_name, "FAIL", f"API request failed: {result['error']}", is_critical=True)
                continue
            
            data = result["data"]
            
            # Check tafsir field is NOT empty
            tafsir = data.get("tafsir", "")
            if not tafsir or not tafsir.strip():
                self.log_result(test_name, "FAIL", "tafsir field is empty", is_critical=True)
                continue
            
            # Get translation for comparison
            translation = data.get("translation", "")
            
            # Check tafsir is DIFFERENT from translation (not a duplicate!)
            if tafsir.strip() == translation.strip():
                self.log_result(test_name, "FAIL", "tafsir is identical to translation (duplicate!)", is_critical=True)
                continue
            
            # Check tafsir source
            tafsir_source = data.get("tafsir_source", "")
            tafsir_is_arabic = data.get("tafsir_is_arabic", False)
            
            # Verify specific requirements per language
            if lang == "ar":
                if "التفسير الميسر" not in tafsir_source:
                    self.log_result(test_name, "FAIL", f"Arabic tafsir should be from التفسير الميسر, got: {tafsir_source}", is_critical=True)
                    continue
            elif lang == "en":
                if "Ibn Kathir" not in tafsir_source:
                    self.log_result(test_name, "FAIL", f"English tafsir should be from Ibn Kathir, got: {tafsir_source}", is_critical=True)
                    continue
                # Check if it's real tafsir with explanation (should be longer and more detailed)
                if len(tafsir) < 100:
                    self.log_result(test_name, "FAIL", f"Ibn Kathir tafsir too short ({len(tafsir)} chars), might not be real tafsir", is_critical=True)
                    continue
            elif lang == "ru":
                if "ас-Саади" not in tafsir_source:
                    self.log_result(test_name, "FAIL", f"Russian tafsir should be from ас-Саади, got: {tafsir_source}", is_critical=True)
                    continue
            elif lang == "fr":
                if "QuranEnc" not in tafsir_source:
                    self.log_result(test_name, "FAIL", f"French tafsir should be from QuranEnc, got: {tafsir_source}", is_critical=True)
                    continue
            elif lang in ["de", "tr", "sv", "nl", "el"]:
                # These should have Arabic tafsir (التفسير الميسر) and tafsir_is_arabic=true
                if not tafsir_is_arabic:
                    self.log_result(test_name, "FAIL", f"tafsir_is_arabic should be true for {lang}", is_critical=True)
                    continue
                if "التفسير الميسر" not in tafsir_source:
                    self.log_result(test_name, "FAIL", f"Tafsir should be Arabic التفسير الميسر for {lang}, got: {tafsir_source}", is_critical=True)
                    continue
            
            # Check for HTML entities
            html_entities = self.check_html_entities(tafsir)
            if html_entities:
                self.log_result(test_name, "FAIL", f"HTML entities found: {', '.join(html_entities)}", is_critical=True)
                continue
            
            self.log_result(test_name, "PASS", f"Real tafsir verified, source: {tafsir_source}, length: {len(tafsir)} chars")
    
    def test_legacy_tafsir_endpoint(self):
        """Test 4: Legacy tafsir endpoint - GET /api/quran/v4/tafsir/1:1?language={lang}"""
        print("\n🔍 TEST 4: LEGACY TAFSIR ENDPOINT")
        print("=" * 60)
        
        for lang in self.languages:
            endpoint = f"/api/quran/v4/tafsir/1:1?language={lang}"
            result = self.make_request(endpoint)
            
            test_name = f"Legacy Tafsir {lang.upper()}"
            
            if not result["success"]:
                self.log_result(test_name, "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            
            # All 9 languages should return non-empty text
            text = data.get("text", "")
            if not text or not text.strip():
                self.log_result(test_name, "FAIL", "text field is empty")
                continue
            
            # For de, tr, sv, nl, el: is_arabic_tafsir should be true
            if lang in ["de", "tr", "sv", "nl", "el"]:
                is_arabic_tafsir = data.get("is_arabic_tafsir", False)
                if not is_arabic_tafsir:
                    self.log_result(test_name, "FAIL", f"is_arabic_tafsir should be true for {lang}")
                    continue
            
            tafsir_name = data.get("tafsir_name", "")
            self.log_result(test_name, "PASS", f"Text present, source: {tafsir_name[:40]}...")
    
    def test_no_html_entities(self):
        """Test 5: No HTML entities - Check responses for &amp;quot; &amp;nbsp; etc."""
        print("\n🔍 TEST 5: NO HTML ENTITIES CHECK")
        print("=" * 60)
        
        # Test multiple endpoints for HTML entities
        test_endpoints = [
            ("/api/quran/v4/global-verse/2/255?language=tr", "Turkish Global Verse"),
            ("/api/quran/v4/verses/by_chapter/1?language=fr&per_page=1", "French Verses"),
            ("/api/quran/v4/tafsir/1:1?language=de", "German Tafsir")
        ]
        
        for endpoint, test_desc in test_endpoints:
            result = self.make_request(endpoint)
            
            test_name = f"HTML Entities {test_desc}"
            
            if not result["success"]:
                self.log_result(test_name, "FAIL", f"API request failed: {result['error']}")
                continue
            
            # Convert entire response to string and check for HTML entities
            response_text = json.dumps(result["data"])
            html_entities = self.check_html_entities(response_text)
            
            if html_entities:
                self.log_result(test_name, "FAIL", f"HTML entities found: {', '.join(html_entities)}")
            else:
                self.log_result(test_name, "PASS", "No HTML entities found")
    
    def run_all_tests(self):
        """Run all tests as specified in the review request"""
        print("🚀 REAL TAFSIR REBUILD - COMPREHENSIVE TESTING SUITE")
        print(f"📍 Base URL: {self.base_url}")
        print(f"🌍 Testing {len(self.languages)} languages: {', '.join(self.languages)}")
        print("=" * 80)
        
        # Run all tests in order
        self.test_chapters_all_languages()
        self.test_verses_surah_1_all_languages()
        self.test_real_tafsir_critical()
        self.test_legacy_tafsir_endpoint()
        self.test_no_html_entities()
        
        # Final Summary
        print("\n" + "=" * 80)
        print("📊 FINAL TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["status"] == "PASS"])
        failed_tests = len(self.failed_tests)
        critical_failures = len(self.critical_failures)
        
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"🚨 Critical Failures: {critical_failures}")
        
        if self.critical_failures:
            print("\n🚨 CRITICAL FAILURES (MUST BE FIXED):")
            for test in self.critical_failures:
                print(f"   ❌ {test['test']}: {test['details']}")
        
        if self.failed_tests and not self.critical_failures:
            print("\n⚠️  NON-CRITICAL FAILURES:")
            for test in self.failed_tests:
                if not test.get("critical", False):
                    print(f"   ⚠️  {test['test']}: {test['details']}")
        
        if failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! REAL TAFSIR REBUILD IS WORKING CORRECTLY!")
        elif critical_failures == 0:
            print("\n✅ CRITICAL TESTS PASSED! Minor issues found but core functionality works.")
        else:
            print("\n🚨 CRITICAL ISSUES FOUND! REAL TAFSIR FUNCTIONALITY IS BROKEN!")
        
        return failed_tests == 0, critical_failures == 0

if __name__ == "__main__":
    tester = RealTafsirTester()
    all_passed, critical_passed = tester.run_all_tests()
    
    # Exit with appropriate code
    if all_passed:
        sys.exit(0)  # All tests passed
    elif critical_passed:
        sys.exit(1)  # Minor failures only
    else:
        sys.exit(2)  # Critical failures