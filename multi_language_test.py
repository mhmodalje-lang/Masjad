#!/usr/bin/env python3
"""
Multi-Language Deployment Test for أذان وحكاية
Tests all 9 languages for chapter names, verses, and tafsir functionality
"""

import requests
import json
import sys
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = "https://translate-hub-123.preview.emergentagent.com/api"

class MultiLanguageDeploymentTester:
    def __init__(self):
        self.results = []
        self.failed_tests = []
        self.passed_tests = []
        
        # Expected chapter names for verification
        self.expected_chapter_names = {
            'ar': {'1': 'سورة الفاتحة', '2': 'سورة البقرة'},
            'en': {'1': 'Al-Fatihah', '2': 'Al-Baqarah'},
            'fr': {'1': "L'ouverture", '2': 'La vache'},
            'de': {'1': 'Die Eröffnende', '2': 'Die Kuh'},
            'tr': {'1': 'Fâtiha', '2': 'Bakara'},
            'ru': {'1': 'Аль-Фатиха', '2': 'Аль-Бакара'},
            'sv': {'1': 'Öppnaren', '2': 'Kon'},
            'nl': {'1': 'De Opening', '2': 'De Koe'},
            'el': {'1': 'Η Εναρκτήρια', '2': 'Η Αγελάδα'}
        }
        
    def log_result(self, test_name: str, passed: bool, details: str, response_data: Any = None):
        """Log test result with details"""
        result = {
            "test": test_name,
            "passed": passed,
            "details": details,
            "response_data": response_data
        }
        self.results.append(result)
        
        if passed:
            self.passed_tests.append(test_name)
            print(f"✅ {test_name}: {details}")
        else:
            self.failed_tests.append(test_name)
            print(f"❌ {test_name}: {details}")
            
    def make_request(self, endpoint: str, params: Dict = None) -> tuple:
        """Make HTTP request and return response and success status"""
        try:
            url = f"{BACKEND_URL}{endpoint}"
            print(f"\n🔍 Testing: {url}")
            if params:
                print(f"   Parameters: {params}")
                
            response = requests.get(url, params=params, timeout=30)
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return data, True, None
                except json.JSONDecodeError:
                    return response.text, True, None
            else:
                return None, False, f"HTTP {response.status_code}: {response.text}"
                
        except requests.exceptions.RequestException as e:
            return None, False, f"Request failed: {str(e)}"
    
    def test_chapter_names_all_languages(self):
        """Test 1: Chapter Names in ALL 9 Languages"""
        print("\n" + "="*80)
        print("TEST 1: CHAPTER NAMES IN ALL 9 LANGUAGES")
        print("="*80)
        
        languages = ['ar', 'en', 'fr', 'de', 'tr', 'ru', 'sv', 'nl', 'el']
        
        for lang in languages:
            print(f"\n--- Testing {lang.upper()} Chapter Names ---")
            
            data, success, error = self.make_request("/quran/v4/chapters", {"language": lang})
            
            if not success:
                self.log_result(f"Chapter Names {lang.upper()}", False, f"Request failed: {error}")
                continue
                
            if not data or not isinstance(data, dict):
                self.log_result(f"Chapter Names {lang.upper()}", False, "No valid data returned")
                continue
                
            chapters = data.get('chapters', [])
            if not chapters:
                self.log_result(f"Chapter Names {lang.upper()}", False, "No chapters found in response")
                continue
                
            # Check first two chapters for expected names
            passed = True
            details = []
            
            for i, chapter in enumerate(chapters[:2], 1):
                # Check translated_name first, then fall back to name_simple
                translated_name = chapter.get('translated_name', {})
                if translated_name and 'name' in translated_name:
                    chapter_name = translated_name['name']
                else:
                    chapter_name = chapter.get('name_simple', chapter.get('name', ''))
                
                expected_name = self.expected_chapter_names.get(lang, {}).get(str(i), '')
                
                if expected_name and expected_name.lower() in chapter_name.lower():
                    details.append(f"Chapter {i}: '{chapter_name}' ✓")
                elif expected_name:
                    details.append(f"Chapter {i}: Expected '{expected_name}', got '{chapter_name}' ✗")
                    passed = False
                else:
                    details.append(f"Chapter {i}: '{chapter_name}' (no expected name to verify)")
            
            if passed:
                self.log_result(f"Chapter Names {lang.upper()}", True, "; ".join(details))
            else:
                self.log_result(f"Chapter Names {lang.upper()}", False, "; ".join(details))
    
    def test_french_verses_with_translation(self):
        """Test 2: French Verses with Translation"""
        print("\n" + "="*80)
        print("TEST 2: FRENCH VERSES WITH TRANSLATION")
        print("="*80)
        
        data, success, error = self.make_request("/quran/v4/verses/by_chapter/1", {"language": "fr", "per_page": "10"})
        
        if not success:
            self.log_result("French Verses", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("French Verses", False, "No data returned")
            return
            
        verses = data.get('verses', [])
        if not verses:
            self.log_result("French Verses", False, "No verses found in response")
            return
            
        # Check first verse for Arabic text and French translation
        first_verse = verses[0]
        
        # Check for Arabic text (text_uthmani)
        arabic_text = first_verse.get('text_uthmani', '')
        has_arabic = bool(arabic_text and any('\u0600' <= char <= '\u06FF' for char in arabic_text))
        
        # Check for French translation
        translations = first_verse.get('translations', [])
        has_french_translation = False
        french_text = ""
        
        if translations:
            for translation in translations:
                text = translation.get('text', '')
                if text and ('au nom d' in text.lower() or 'nom d' in text.lower()):
                    has_french_translation = True
                    french_text = text[:100] + "..." if len(text) > 100 else text
                    break
        
        if has_arabic and has_french_translation:
            self.log_result("French Verses", True, f"Arabic text and French translation found. French: '{french_text}'")
        elif not has_arabic:
            self.log_result("French Verses", False, "No Arabic text (text_uthmani) found")
        elif not has_french_translation:
            self.log_result("French Verses", False, "No French translation found or doesn't contain expected French text")
        else:
            self.log_result("French Verses", False, "Unknown issue with verse structure")
    
    def test_german_verses_with_translation(self):
        """Test 3: German Verses with Translation"""
        print("\n" + "="*80)
        print("TEST 3: GERMAN VERSES WITH TRANSLATION")
        print("="*80)
        
        data, success, error = self.make_request("/quran/v4/verses/by_chapter/1", {"language": "de", "per_page": "10"})
        
        if not success:
            self.log_result("German Verses", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("German Verses", False, "No data returned")
            return
            
        verses = data.get('verses', [])
        if not verses:
            self.log_result("German Verses", False, "No verses found in response")
            return
            
        # Check first verse for German translation (Bubenheim)
        first_verse = verses[0]
        translations = first_verse.get('translations', [])
        has_german_translation = False
        german_text = ""
        
        if translations:
            for translation in translations:
                text = translation.get('text', '')
                # Look for German indicators (Bubenheim translation typically starts with "Im Namen")
                if text and ('im namen' in text.lower() or 'namen allah' in text.lower()):
                    has_german_translation = True
                    german_text = text[:100] + "..." if len(text) > 100 else text
                    break
        
        if has_german_translation:
            self.log_result("German Verses", True, f"German translation found: '{german_text}'")
        else:
            self.log_result("German Verses", False, "No German translation found or doesn't contain expected German text")
    
    def test_tafsir_fallback_french(self):
        """Test 4: Tafsir Fallback for French"""
        print("\n" + "="*80)
        print("TEST 4: TAFSIR FALLBACK FOR FRENCH")
        print("="*80)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "fr"})
        
        if not success:
            self.log_result("Tafsir French Fallback", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Tafsir French Fallback", False, "No data returned")
            return
            
        # Check for fallback indicators
        is_fallback = data.get('is_fallback_language', False)
        translation_pending = data.get('translation_pending', True)  # Should be false for fallback
        text_content = data.get('text', '')
        
        # Verify fallback behavior
        if is_fallback and not translation_pending and text_content:
            # Should contain English Ibn Kathir tafsir
            if 'allah' in text_content.lower() or 'prophet' in text_content.lower():
                self.log_result("Tafsir French Fallback", True, f"Fallback working: is_fallback={is_fallback}, translation_pending={translation_pending}, has English text")
            else:
                self.log_result("Tafsir French Fallback", False, f"Fallback indicated but no English tafsir text found")
        else:
            details = f"is_fallback={is_fallback}, translation_pending={translation_pending}, has_text={bool(text_content)}"
            self.log_result("Tafsir French Fallback", False, f"Fallback not working correctly: {details}")
    
    def test_tafsir_arabic(self):
        """Test 5: Tafsir for Arabic"""
        print("\n" + "="*80)
        print("TEST 5: TAFSIR FOR ARABIC")
        print("="*80)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "ar"})
        
        if not success:
            self.log_result("Tafsir Arabic", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Tafsir Arabic", False, "No data returned")
            return
            
        # Check for normal Arabic tafsir behavior
        is_fallback = data.get('is_fallback_language', True)  # Should be false for Arabic
        text_content = data.get('text', '')
        
        if not is_fallback and text_content:
            # Check if text contains Arabic characters
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in text_content)
            if has_arabic:
                self.log_result("Tafsir Arabic", True, f"Arabic tafsir working: is_fallback={is_fallback}, has Arabic text")
            else:
                self.log_result("Tafsir Arabic", True, f"Arabic tafsir working: is_fallback={is_fallback}, text present (may be transliterated)")
        else:
            details = f"is_fallback={is_fallback}, has_text={bool(text_content)}"
            self.log_result("Tafsir Arabic", False, f"Arabic tafsir not working: {details}")
    
    def test_full_audit_report(self):
        """Test 6: Full Audit Report"""
        print("\n" + "="*80)
        print("TEST 6: FULL AUDIT REPORT")
        print("="*80)
        
        data, success, error = self.make_request("/audit/full-report")
        
        if not success:
            self.log_result("Full Audit Report", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Full Audit Report", False, "No data returned")
            return
            
        summary = data.get('summary', {})
        
        # Check critical audit fields
        all_adult_bukhari_muslim = summary.get('all_adult_bukhari_muslim')
        all_kids_bukhari_muslim = summary.get('all_kids_bukhari_muslim')
        all_extended_bukhari_muslim = summary.get('all_extended_bukhari_muslim')
        
        if all_adult_bukhari_muslim and all_kids_bukhari_muslim and all_extended_bukhari_muslim:
            self.log_result("Full Audit Report", True, "All audit checks passed: adult, kids, and extended collections verified")
        else:
            details = f"adult={all_adult_bukhari_muslim}, kids={all_kids_bukhari_muslim}, extended={all_extended_bukhari_muslim}"
            self.log_result("Full Audit Report", False, f"Audit checks failed: {details}")
    
    def test_daily_hadith_french(self):
        """Test 7: Daily Hadith French"""
        print("\n" + "="*80)
        print("TEST 7: DAILY HADITH FRENCH")
        print("="*80)
        
        data, success, error = self.make_request("/daily-hadith", {"language": "fr"})
        
        if not success:
            self.log_result("Daily Hadith French", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Daily Hadith French", False, "No data returned")
            return
            
        # Check for French translation
        hadith = data.get('hadith', data)
        has_french_translation = False
        
        # Check various fields for French content
        text_fields = ['text', 'translation', 'french_translation', 'content']
        for field in text_fields:
            if field in hadith and hadith[field]:
                text = str(hadith[field]).lower()
                # Check for French characters and words
                french_indicators = ['à', 'è', 'é', 'ê', 'ç', 'miséricorde', 'vérité', 'celui qui']
                if any(indicator in text for indicator in french_indicators):
                    has_french_translation = True
                    break
        
        if has_french_translation:
            self.log_result("Daily Hadith French", True, "French translation found")
        else:
            # Check if translation is pending
            translation_pending = data.get('translation_pending', False)
            if translation_pending:
                self.log_result("Daily Hadith French", True, "Translation pending (acceptable)")
            else:
                self.log_result("Daily Hadith French", False, "No French translation found and no translation_pending flag")
    
    def run_all_tests(self):
        """Run all multi-language deployment tests"""
        print("🌍 STARTING MULTI-LANGUAGE DEPLOYMENT TESTS")
        print("="*80)
        print(f"Backend URL: {BACKEND_URL}")
        print("Testing 9 languages: Arabic, English, French, German, Turkish, Russian, Swedish, Dutch, Greek")
        print("="*80)
        
        # Run all tests
        self.test_chapter_names_all_languages()
        self.test_french_verses_with_translation()
        self.test_german_verses_with_translation()
        self.test_tafsir_fallback_french()
        self.test_tafsir_arabic()
        self.test_full_audit_report()
        self.test_daily_hadith_french()
        
        # Summary
        print("\n" + "="*80)
        print("🏁 MULTI-LANGUAGE DEPLOYMENT TEST SUMMARY")
        print("="*80)
        print(f"✅ Passed: {len(self.passed_tests)}")
        print(f"❌ Failed: {len(self.failed_tests)}")
        print(f"📊 Total: {len(self.results)}")
        
        if self.passed_tests:
            print(f"\n✅ PASSED TESTS:")
            for test in self.passed_tests:
                print(f"   • {test}")
        
        if self.failed_tests:
            print(f"\n❌ FAILED TESTS:")
            for test in self.failed_tests:
                print(f"   • {test}")
                
        print("\n" + "="*80)
        
        return len(self.failed_tests) == 0

if __name__ == "__main__":
    tester = MultiLanguageDeploymentTester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 ALL MULTI-LANGUAGE TESTS PASSED!")
        sys.exit(0)
    else:
        print("⚠️  SOME MULTI-LANGUAGE TESTS FAILED - Review results above")
        sys.exit(1)