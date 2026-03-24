#!/usr/bin/env python3
"""
Comprehensive Quran API Testing Suite
Tests all endpoints across all 9 languages as requested in the review
"""

import requests
import json
import sys
import re
from typing import Dict, Any, List

# Base URL from frontend/.env
BASE_URL = "https://quran-114-surahs.preview.emergentagent.com"

# All 9 languages to test
LANGUAGES = ["ar", "en", "fr", "de", "tr", "ru", "sv", "nl", "el"]

# Test surahs for verses endpoint
TEST_SURAHS = [1, 36, 112, 114]

class ComprehensiveQuranTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.results = []
        self.failed_tests = []
        self.languages = LANGUAGES
        
    def log_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "details": details
        }
        self.results.append(result)
        if status == "FAIL":
            self.failed_tests.append(result)
        print(f"[{status}] {test_name}: {details}")
    
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
            r'&amp;',
            r'&quot;',
            r'&nbsp;',
            r'&lt;',
            r'&gt;',
            r'&apos;'
        ]
        
        for pattern in patterns:
            if re.search(pattern, text):
                html_entities.append(pattern)
        
        return html_entities
    
    def test_chapters_endpoint(self):
        """Test 1: GET /api/quran/v4/chapters?language={lang} for all 9 languages"""
        print("\n=== TESTING CHAPTERS ENDPOINT ===")
        
        for lang in self.languages:
            endpoint = f"/api/quran/v4/chapters?language={lang}"
            result = self.make_request(endpoint)
            
            if not result["success"]:
                self.log_result(f"Chapters {lang.upper()}", "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            
            # Check if it's a list or has chapters key
            chapters = data if isinstance(data, list) else data.get("chapters", [])
            
            # Verify exactly 114 chapters
            if len(chapters) != 114:
                self.log_result(f"Chapters {lang.upper()}", "FAIL", f"Expected 114 chapters, got {len(chapters)}")
                continue
            
            # Check first few chapters have required fields
            missing_fields = []
            for i, chapter in enumerate(chapters[:3]):  # Check first 3 chapters
                if not chapter.get("name_arabic"):
                    missing_fields.append(f"Chapter {i+1} missing name_arabic")
                
                translated_name = chapter.get("translated_name")
                if not translated_name or not translated_name.get("name"):
                    missing_fields.append(f"Chapter {i+1} missing translated_name.name")
            
            if missing_fields:
                self.log_result(f"Chapters {lang.upper()}", "FAIL", f"Missing fields: {', '.join(missing_fields)}")
                continue
            
            self.log_result(f"Chapters {lang.upper()}", "PASS", f"114 chapters with required fields")
    
    def test_verses_endpoint(self):
        """Test 2: GET /api/quran/v4/verses/by_chapter/{surah}?language={lang}&per_page=10"""
        print("\n=== TESTING VERSES ENDPOINT ===")
        
        for lang in self.languages:
            for surah in TEST_SURAHS:
                endpoint = f"/api/quran/v4/verses/by_chapter/{surah}?language={lang}&per_page=10"
                result = self.make_request(endpoint)
                
                test_name = f"Verses {lang.upper()} Surah {surah}"
                
                if not result["success"]:
                    self.log_result(test_name, "FAIL", f"API request failed: {result['error']}")
                    continue
                
                data = result["data"]
                verses = data.get("verses", [])
                
                if not verses:
                    self.log_result(test_name, "FAIL", "No verses returned")
                    continue
                
                # Check first verse has required fields
                first_verse = verses[0]
                
                # Check for text_uthmani (Arabic text)
                if not first_verse.get("text_uthmani"):
                    self.log_result(test_name, "FAIL", "Missing text_uthmani (Arabic text)")
                    continue
                
                # For non-Arabic languages, check for translations
                if lang != "ar":
                    translations = first_verse.get("translations", [])
                    if not translations:
                        self.log_result(test_name, "FAIL", "Missing translations for non-Arabic language")
                        continue
                    
                    # Check first translation has text
                    if not translations[0].get("text"):
                        self.log_result(test_name, "FAIL", "Translation missing text field")
                        continue
                
                self.log_result(test_name, "PASS", f"Returned {len(verses)} verses with required fields")
    
    def test_global_verse_endpoint(self):
        """Test 3: GET /api/quran/v4/global-verse/{surah}/{ayah}?language={lang} for verse 2:255"""
        print("\n=== TESTING GLOBAL VERSE ENDPOINT (2:255) ===")
        
        for lang in self.languages:
            endpoint = f"/api/quran/v4/global-verse/2/255?language={lang}"
            result = self.make_request(endpoint)
            
            test_name = f"Global Verse {lang.upper()} 2:255"
            
            if not result["success"]:
                self.log_result(test_name, "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            
            # Check success=true
            if not data.get("success", False):
                self.log_result(test_name, "FAIL", "Response success is not true")
                continue
            
            # Check arabic_text (not empty)
            arabic_text = data.get("arabic_text", "")
            if not arabic_text or not arabic_text.strip():
                self.log_result(test_name, "FAIL", "arabic_text is empty")
                continue
            
            # Check tafsir (not empty) - THIS IS CRITICAL
            tafsir = data.get("tafsir", "")
            if not tafsir or not tafsir.strip():
                self.log_result(test_name, "FAIL", "tafsir is empty - CRITICAL ISSUE")
                continue
            
            # Check tafsir_source (not empty)
            tafsir_source = data.get("tafsir_source", "")
            if not tafsir_source or not tafsir_source.strip():
                self.log_result(test_name, "FAIL", "tafsir_source is empty")
                continue
            
            # Check for HTML entities
            html_entities = self.check_html_entities(tafsir)
            if html_entities:
                self.log_result(test_name, "FAIL", f"HTML entities found: {', '.join(html_entities)}")
                continue
            
            self.log_result(test_name, "PASS", f"All fields present, source: {tafsir_source[:50]}...")
    
    def test_tafsir_endpoint(self):
        """Test 4: GET /api/quran/v4/tafsir/1:1?language={lang} for all 9 languages"""
        print("\n=== TESTING TAFSIR ENDPOINT (1:1) ===")
        
        for lang in self.languages:
            endpoint = f"/api/quran/v4/tafsir/1:1?language={lang}"
            result = self.make_request(endpoint)
            
            test_name = f"Tafsir {lang.upper()} 1:1"
            
            if not result["success"]:
                self.log_result(test_name, "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            
            # Check success=true
            if not data.get("success", False):
                self.log_result(test_name, "FAIL", "Response success is not true")
                continue
            
            # Check text (not empty for all languages)
            text = data.get("text", "")
            if not text or not text.strip():
                self.log_result(test_name, "FAIL", "text field is empty")
                continue
            
            # Check tafsir_name with Islamic source attribution
            tafsir_name = data.get("tafsir_name", "")
            if not tafsir_name or not tafsir_name.strip():
                self.log_result(test_name, "FAIL", "tafsir_name is empty")
                continue
            
            self.log_result(test_name, "PASS", f"Text present, source: {tafsir_name[:50]}...")
    
    def test_html_entities_turkish(self):
        """Test 5: Verify no HTML entities, specifically test Turkish language for verse 114:1"""
        print("\n=== TESTING HTML ENTITIES (Turkish 114:1) ===")
        
        endpoint = "/api/quran/v4/global-verse/114/1?language=tr"
        result = self.make_request(endpoint)
        
        if not result["success"]:
            self.log_result("HTML Entities Turkish", "FAIL", f"API request failed: {result['error']}")
            return
        
        data = result["data"]
        
        # Check all text fields for HTML entities
        fields_to_check = ["tafsir", "arabic_text", "translation"]
        html_entities_found = []
        
        for field in fields_to_check:
            field_value = data.get(field, "")
            if field_value:
                entities = self.check_html_entities(str(field_value))
                if entities:
                    html_entities_found.extend([f"{field}: {entity}" for entity in entities])
        
        if html_entities_found:
            self.log_result("HTML Entities Turkish", "FAIL", f"HTML entities found: {', '.join(html_entities_found)}")
        else:
            self.log_result("HTML Entities Turkish", "PASS", "No HTML entities found in Turkish 114:1")
    
    def test_source_verification(self):
        """Test 6: Verify tafsir_source for each language is an Islamic scholarly source"""
        print("\n=== TESTING SOURCE VERIFICATION ===")
        
        # Expected Islamic sources (partial matches)
        expected_sources = {
            "ar": ["التفسير الميسر", "مجمع الملك فهد"],
            "en": ["Abdel Haleem", "Oxford"],
            "fr": ["Fondation Islamique Montada", "Montada"],
            "de": ["Abu Reda Muhammad ibn Ahmad", "Abu Reda"],
            "tr": ["Elmalılı", "Hamdi Yazır"],
            "ru": ["Кулиев", "Эльмир", "Тафсир"],
            "sv": ["Knut Bernström", "Bernström"],
            "nl": ["Malak Faris Abdalsalaam", "Abdalsalaam"],
            "el": ["مركز رواد الترجمة", "رواد الترجمة"]
        }
        
        for lang in self.languages:
            endpoint = f"/api/quran/v4/global-verse/2/255?language={lang}"
            result = self.make_request(endpoint)
            
            test_name = f"Source Verification {lang.upper()}"
            
            if not result["success"]:
                self.log_result(test_name, "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            tafsir_source = data.get("tafsir_source", "")
            
            if not tafsir_source:
                # Some languages might not have tafsir (ar, sv, el)
                if lang in ["ar", "sv", "el"]:
                    self.log_result(test_name, "PASS", "No tafsir source (expected for this language)")
                else:
                    self.log_result(test_name, "FAIL", "tafsir_source is empty")
                continue
            
            # Check if source matches expected Islamic sources
            expected = expected_sources.get(lang, [])
            source_matches = any(exp.lower() in tafsir_source.lower() for exp in expected)
            
            if expected and not source_matches:
                self.log_result(test_name, "FAIL", f"Source '{tafsir_source}' doesn't match expected Islamic sources: {expected}")
            else:
                self.log_result(test_name, "PASS", f"Islamic source verified: {tafsir_source}")
    
    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("Starting Comprehensive Quran API Testing Suite...")
        print(f"Base URL: {self.base_url}")
        print(f"Testing {len(self.languages)} languages: {', '.join(self.languages)}")
        
        # Run all tests
        self.test_chapters_endpoint()
        self.test_verses_endpoint()
        self.test_global_verse_endpoint()
        self.test_tafsir_endpoint()
        self.test_html_entities_turkish()
        self.test_source_verification()
        
        # Summary
        print("\n" + "="*60)
        print("COMPREHENSIVE TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["status"] == "PASS"])
        failed_tests = len(self.failed_tests)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        
        if self.failed_tests:
            print("\nFAILED TESTS:")
            for test in self.failed_tests:
                print(f"- {test['test']}: {test['details']}")
        else:
            print("\n🎉 ALL TESTS PASSED!")
        
        return failed_tests == 0

if __name__ == "__main__":
    tester = ComprehensiveQuranTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)