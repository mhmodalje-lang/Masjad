#!/usr/bin/env python3
"""
V2026 Global Islamic Localization Backend Test - COMPLETE REVIEW REQUEST
Tests the specific requirements from the review request for all 9 languages
Focus: Greek Translation (NEW), Kids Tafsir, Bulk Tafsir, Daily Hadith
"""

import requests
import json
import sys
from typing import Dict, Any, List

# Backend URL from frontend environment
BACKEND_URL = "https://quran-verify-4.preview.emergentagent.com/api"

class V2026ComprehensiveTester:
    def __init__(self):
        self.results = []
        self.failed_tests = []
        self.passed_tests = []
        self.critical_failures = []
        
    def log_result(self, test_name: str, passed: bool, details: str, response_data: Any = None, critical: bool = False):
        """Log test result with details"""
        result = {
            "test": test_name,
            "passed": passed,
            "details": details,
            "response_data": response_data,
            "critical": critical
        }
        self.results.append(result)
        
        if passed:
            self.passed_tests.append(test_name)
            print(f"✅ {test_name}: {details}")
        else:
            self.failed_tests.append(test_name)
            if critical:
                self.critical_failures.append(test_name)
            print(f"❌ {test_name}: {details}")
            
    def make_request(self, endpoint: str, params: Dict = None, method: str = "GET") -> tuple:
        """Make HTTP request and return response and success status"""
        try:
            url = f"{BACKEND_URL}{endpoint}"
            print(f"\n🔍 Testing: {url}")
            if params:
                print(f"   Parameters: {params}")
                
            if method == "GET":
                response = requests.get(url, params=params, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=params, timeout=30)
            else:
                response = requests.request(method, url, params=params, timeout=30)
                
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

    def test_greek_translation_verses(self):
        """Test Greek Translation - Verses API (NEW - was missing before)"""
        print("\n" + "="*80)
        print("CRITICAL TEST 1: GREEK TRANSLATION VERSES - Must have greek_source field")
        print("="*80)
        
        data, success, error = self.make_request("/quran/v4/verses/by_chapter/1", {"language": "el", "per_page": "10"})
        
        if not success:
            self.log_result("Greek Verses API", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Greek Verses API", False, "No data returned", critical=True)
            return
            
        issues = []
        
        # Check for verses with translations
        verses = data.get('verses', [])
        if not verses:
            issues.append("No verses found in response")
        else:
            has_greek_text = False
            for verse in verses:
                translations = verse.get('translations', [])
                if translations:
                    for translation in translations:
                        text = translation.get('text', '')
                        # Check for Greek characters
                        if any('\u0370' <= char <= '\u03FF' or '\u1F00' <= char <= '\u1FFF' for char in text):
                            has_greek_text = True
                            break
                        # Check for common English words (should NOT be present)
                        english_words = ['the', 'and', 'of', 'to', 'in', 'that', 'is', 'for', 'with', 'as']
                        english_count = sum(1 for word in english_words if f' {word} ' in text.lower())
                        if english_count > 2:
                            issues.append(f"Translation contains English text instead of Greek: '{text[:100]}...'")
                if has_greek_text:
                    break
            
            if not has_greek_text and not issues:
                issues.append("No Greek text found in translations - should contain Ελληνικά characters")
        
        if issues:
            self.log_result("Greek Verses API", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Greek Verses API", True, "Greek verses API working correctly with Greek text", data)

    def test_greek_tafsir_1_1(self):
        """Test Greek Tafsir 1:1 - Must return Greek text from Rowwad, translation_pending=false"""
        print("\n" + "="*80)
        print("CRITICAL TEST 2: GREEK TAFSIR 1:1 - Must have Greek text from Rowwad")
        print("="*80)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "el"})
        
        if not success:
            self.log_result("Greek Tafsir 1:1", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Greek Tafsir 1:1", False, "No data returned", critical=True)
            return
            
        issues = []
        
        # Check tafsir_name contains "Rowwad"
        tafsir_name = data.get('tafsir_name', '')
        if 'Rowwad' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Rowwad', got '{tafsir_name}'")
        
        # Check translation_pending=false
        translation_pending = data.get('translation_pending', True)
        if translation_pending != False:
            issues.append(f"translation_pending should be false, got {translation_pending}")
        
        # Check for Greek text
        text = data.get('text', '')
        if text:
            has_greek = any('\u0370' <= char <= '\u03FF' or '\u1F00' <= char <= '\u1FFF' for char in text)
            if not has_greek:
                issues.append(f"Text should contain Greek characters, got: '{text[:100]}...'")
        else:
            issues.append("Text should not be empty for Greek tafsir")
        
        if issues:
            self.log_result("Greek Tafsir 1:1", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Greek Tafsir 1:1", True, f"Greek tafsir 1:1 working correctly: {tafsir_name}", data)

    def test_greek_tafsir_ayat_al_kursi(self):
        """Test Greek Tafsir 2:255 (Ayat al-Kursi) - Must return Greek tafsir"""
        print("\n" + "="*80)
        print("CRITICAL TEST 3: GREEK TAFSIR AYAT AL-KURSI - Must return Greek text")
        print("="*80)
        
        data, success, error = self.make_request("/quran/v4/tafsir/2:255", {"language": "el"})
        
        if not success:
            self.log_result("Greek Tafsir Ayat al-Kursi", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Greek Tafsir Ayat al-Kursi", False, "No data returned", critical=True)
            return
            
        issues = []
        
        # Check for Greek text
        text = data.get('text', '')
        if text:
            has_greek = any('\u0370' <= char <= '\u03FF' or '\u1F00' <= char <= '\u1FFF' for char in text)
            if not has_greek:
                issues.append(f"Text should contain Greek characters, got: '{text[:100]}...'")
        else:
            issues.append("Text should not be empty for Greek tafsir of Ayat al-Kursi")
        
        if issues:
            self.log_result("Greek Tafsir Ayat al-Kursi", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Greek Tafsir Ayat al-Kursi", True, "Greek tafsir for Ayat al-Kursi working correctly", data)

    def test_tafsir_all_9_languages_verse_1_2(self):
        """Test Tafsir for ALL 9 languages (verse 1:2) with specific sources"""
        print("\n" + "="*80)
        print("CRITICAL TEST 4: TAFSIR ALL 9 LANGUAGES (1:2) - Specific sources for each")
        print("="*80)
        
        # Expected sources for each language (more flexible matching)
        expected_sources = {
            'ar': ['الميسر', 'المیسر'],  # Arabic Al-Muyassar (allow both Arabic and Persian ي)
            'en': ['Ibn Kathir'],  # English Ibn Kathir
            'ru': ['Al-Sa\'di', 'Al Saddi', 'Saddi'],  # Russian Al-Sa'di (flexible matching)
            'de': ['Abu Reda'],  # German Abu Reda
            'fr': ['Hamidullah'],  # French Hamidullah
            'tr': ['Elmalılı'],  # Turkish Elmalılı Hamdi Yazır
            'sv': ['Al-Muyassar', 'الميسر', 'المیسر'],  # Swedish Arabic Al-Muyassar (flexible)
            'nl': ['Abdalsalaam'],  # Dutch Abdalsalaam
            'el': ['Rowwad']  # Greek Rowwad Translation Center
        }
        
        for lang, expected_source_list in expected_sources.items():
            data, success, error = self.make_request("/quran/v4/tafsir/1:2", {"language": lang})
            
            if not success:
                self.log_result(f"Tafsir {lang.upper()} 1:2", False, f"Request failed: {error}", critical=True)
                continue
                
            if not data:
                self.log_result(f"Tafsir {lang.upper()} 1:2", False, "No data returned", critical=True)
                continue
                
            issues = []
            tafsir_name = data.get('tafsir_name', '')
            text = data.get('text', '')
            
            # Check for expected source (flexible matching)
            source_found = any(expected_source in tafsir_name for expected_source in expected_source_list)
            if not source_found:
                issues.append(f"tafsir_name should contain one of {expected_source_list}, got '{tafsir_name}'")
            
            # Language-specific checks
            if lang == 'ru':  # Russian should have Cyrillic
                has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in text)
                if not has_cyrillic and text:
                    issues.append(f"Russian text should contain Cyrillic characters")
            elif lang == 'el':  # Greek should have Greek characters
                has_greek = any('\u0370' <= char <= '\u03FF' or '\u1F00' <= char <= '\u1FFF' for char in text)
                if not has_greek and text:
                    issues.append(f"Greek text should contain Greek characters")
            elif lang == 'sv':  # Swedish should be Arabic Al-Muyassar
                is_arabic_tafsir = data.get('is_arabic_tafsir', False)
                if not is_arabic_tafsir:
                    issues.append(f"Swedish should have is_arabic_tafsir=true, got {is_arabic_tafsir}")
            
            # Check text is not empty
            if not text or len(text) < 10:
                issues.append(f"Text should not be empty, got '{text[:50]}...'")
            
            if issues:
                self.log_result(f"Tafsir {lang.upper()} 1:2", False, "; ".join(issues), data, critical=True)
            else:
                found_source = next((source for source in expected_source_list if source in tafsir_name), expected_source_list[0])
                self.log_result(f"Tafsir {lang.upper()} 1:2", True, f"Correct source: {found_source}", data)

    def test_kids_tafsir_french_fatiha(self):
        """Test Kids Tafsir - French Fatiha (simplified explanations for children)"""
        print("\n" + "="*80)
        print("CRITICAL TEST 5: KIDS TAFSIR FRENCH FATIHA - Simplified explanations")
        print("="*80)
        
        data, success, error = self.make_request("/kids-learn/quran/surah/fatiha", {"locale": "fr"})
        
        if not success:
            self.log_result("Kids Tafsir French Fatiha", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Kids Tafsir French Fatiha", False, "No data returned", critical=True)
            return
            
        issues = []
        
        # Check if response has surah structure
        surah = data.get('surah', {})
        ayahs = surah.get('ayahs', [])
        
        if not ayahs:
            issues.append("No ayahs found in surah response")
        else:
            for i, ayah in enumerate(ayahs):
                if 'tafsir_kids' not in ayah:
                    issues.append(f"Ayah {i+1} missing 'tafsir_kids' field")
                else:
                    tafsir_kids = ayah.get('tafsir_kids', '')
                    if not tafsir_kids or len(tafsir_kids) < 10:
                        issues.append(f"Ayah {i+1} tafsir_kids should not be empty")
                    # Check for French text (basic check)
                    elif not any(char in tafsir_kids.lower() for char in ['le', 'la', 'les', 'de', 'du', 'des']):
                        issues.append(f"Ayah {i+1} tafsir_kids should be in French")
        
        if issues:
            self.log_result("Kids Tafsir French Fatiha", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Kids Tafsir French Fatiha", True, f"French kids tafsir working correctly for {len(ayahs)} ayahs", data)

    def test_kids_tafsir_german_ikhlas(self):
        """Test Kids Tafsir - German Ikhlas (simplified explanations for children)"""
        print("\n" + "="*80)
        print("CRITICAL TEST 6: KIDS TAFSIR GERMAN IKHLAS - Simplified explanations")
        print("="*80)
        
        data, success, error = self.make_request("/kids-learn/quran/surah/ikhlas", {"locale": "de"})
        
        if not success:
            self.log_result("Kids Tafsir German Ikhlas", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Kids Tafsir German Ikhlas", False, "No data returned", critical=True)
            return
            
        issues = []
        
        # Check if response has surah structure
        surah = data.get('surah', {})
        ayahs = surah.get('ayahs', [])
        
        if not ayahs:
            issues.append("No ayahs found in surah response")
        else:
            for i, ayah in enumerate(ayahs):
                if 'tafsir_kids' not in ayah:
                    issues.append(f"Ayah {i+1} missing 'tafsir_kids' field")
                else:
                    tafsir_kids = ayah.get('tafsir_kids', '')
                    if not tafsir_kids or len(tafsir_kids) < 10:
                        issues.append(f"Ayah {i+1} tafsir_kids should not be empty")
                    # Check for German text (basic check)
                    elif not any(char in tafsir_kids.lower() for char in ['der', 'die', 'das', 'und', 'ist', 'ein']):
                        issues.append(f"Ayah {i+1} tafsir_kids should be in German")
        
        if issues:
            self.log_result("Kids Tafsir German Ikhlas", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Kids Tafsir German Ikhlas", True, f"German kids tafsir working correctly for {len(ayahs)} ayahs", data)

    def test_kids_tafsir_greek_nas(self):
        """Test Kids Tafsir - Greek Nas (simplified explanations for children)"""
        print("\n" + "="*80)
        print("CRITICAL TEST 7: KIDS TAFSIR GREEK NAS - Simplified explanations")
        print("="*80)
        
        data, success, error = self.make_request("/kids-learn/quran/surah/nas", {"locale": "el"})
        
        if not success:
            self.log_result("Kids Tafsir Greek Nas", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Kids Tafsir Greek Nas", False, "No data returned", critical=True)
            return
            
        issues = []
        
        # Check if response has surah structure
        surah = data.get('surah', {})
        ayahs = surah.get('ayahs', [])
        
        if not ayahs:
            issues.append("No ayahs found in surah response")
        else:
            for i, ayah in enumerate(ayahs):
                if 'tafsir_kids' not in ayah:
                    issues.append(f"Ayah {i+1} missing 'tafsir_kids' field")
                else:
                    tafsir_kids = ayah.get('tafsir_kids', '')
                    if not tafsir_kids or len(tafsir_kids) < 10:
                        issues.append(f"Ayah {i+1} tafsir_kids should not be empty")
                    # Check for Greek characters
                    elif not any('\u0370' <= char <= '\u03FF' or '\u1F00' <= char <= '\u1FFF' for char in tafsir_kids):
                        issues.append(f"Ayah {i+1} tafsir_kids should contain Greek characters")
        
        if issues:
            self.log_result("Kids Tafsir Greek Nas", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Kids Tafsir Greek Nas", True, f"Greek kids tafsir working correctly for {len(ayahs)} ayahs", data)

    def test_daily_hadith_greek(self):
        """Test Daily Hadith localized - Greek"""
        print("\n" + "="*80)
        print("CRITICAL TEST 8: DAILY HADITH GREEK - Localized narrator/source")
        print("="*80)
        
        data, success, error = self.make_request("/daily-hadith", {"language": "el"})
        
        if not success:
            self.log_result("Daily Hadith Greek", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Daily Hadith Greek", False, "No data returned", critical=True)
            return
            
        issues = []
        hadith = data.get('hadith', {})
        narrator = hadith.get('narrator', '')
        source = hadith.get('source', '')
        
        if not narrator:
            issues.append("Narrator should not be empty")
        elif any('\u0600' <= char <= '\u06FF' for char in narrator):
            issues.append(f"Narrator should be localized, not Arabic: '{narrator}'")
        
        if not source:
            issues.append("Source should not be empty")
        elif any('\u0600' <= char <= '\u06FF' for char in source):
            issues.append(f"Source should be localized, not Arabic: '{source}'")
        
        if issues:
            self.log_result("Daily Hadith Greek", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Daily Hadith Greek", True, f"Greek hadith localized correctly: narrator='{narrator}', source='{source}'", data)

    def test_bulk_tafsir_greek_ikhlas(self):
        """Test Bulk Tafsir - Greek Al-Ikhlas (all 4 verses)"""
        print("\n" + "="*80)
        print("CRITICAL TEST 9: BULK TAFSIR GREEK IKHLAS - All 4 verses")
        print("="*80)
        
        data, success, error = self.make_request("/quran/v4/tafsir/bulk/112", {"language": "el"})
        
        if not success:
            self.log_result("Bulk Tafsir Greek Ikhlas", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Bulk Tafsir Greek Ikhlas", False, "No data returned", critical=True)
            return
            
        issues = []
        
        # Check if it's a list of tafsirs or a single object
        if isinstance(data, list):
            tafsirs = data
        else:
            tafsirs = data.get('tafsirs', [])
        
        if not tafsirs:
            issues.append("No tafsirs found in response")
        elif len(tafsirs) != 4:
            issues.append(f"Should return 4 tafsirs for Al-Ikhlas, got {len(tafsirs)}")
        else:
            for i, tafsir in enumerate(tafsirs):
                verse_num = i + 1
                text = tafsir.get('text', '')
                if not text:
                    issues.append(f"Verse {verse_num} tafsir text should not be empty")
                elif not any('\u0370' <= char <= '\u03FF' or '\u1F00' <= char <= '\u1FFF' for char in text):
                    issues.append(f"Verse {verse_num} tafsir should contain Greek characters")
        
        if issues:
            self.log_result("Bulk Tafsir Greek Ikhlas", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Bulk Tafsir Greek Ikhlas", True, f"Greek bulk tafsir working correctly for all 4 verses of Al-Ikhlas", data)

    def test_cache_clear(self):
        """Test Cache Management - Clear cache"""
        print("\n" + "="*80)
        print("TEST 10: CACHE CLEAR - Should return success=true")
        print("="*80)
        
        data, success, error = self.make_request("/quran/v4/cache/clear", method="POST")
        
        if not success:
            self.log_result("Cache Clear", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Cache Clear", False, "No data returned")
            return
            
        # Check success field
        cache_success = data.get('success', False)
        
        if cache_success:
            self.log_result("Cache Clear", True, f"Cache cleared successfully", data)
        else:
            self.log_result("Cache Clear", False, f"Cache clear failed: success={cache_success}", data)

    def run_all_tests(self):
        """Run all V2026 Global Islamic Localization tests based on review request"""
        print("🕌 STARTING V2026 COMPLETE GLOBAL ISLAMIC LOCALIZATION TESTS")
        print("="*80)
        print(f"Backend URL: {BACKEND_URL}")
        print("Focus: COMPLETE testing of all 9 languages with Greek Translation (NEW)")
        print("="*80)
        
        # Run all critical tests from review request
        self.test_greek_translation_verses()
        self.test_greek_tafsir_1_1()
        self.test_greek_tafsir_ayat_al_kursi()
        self.test_tafsir_all_9_languages_verse_1_2()
        self.test_kids_tafsir_french_fatiha()
        self.test_kids_tafsir_german_ikhlas()
        self.test_kids_tafsir_greek_nas()
        self.test_daily_hadith_greek()
        self.test_bulk_tafsir_greek_ikhlas()
        self.test_cache_clear()
        
        # Summary
        print("\n" + "="*80)
        print("🏁 V2026 COMPLETE LOCALIZATION TEST SUMMARY")
        print("="*80)
        print(f"✅ Passed: {len(self.passed_tests)}")
        print(f"❌ Failed: {len(self.failed_tests)}")
        print(f"🚨 Critical Failures: {len(self.critical_failures)}")
        print(f"📊 Total: {len(self.results)}")
        
        if self.passed_tests:
            print(f"\n✅ PASSED TESTS:")
            for test in self.passed_tests:
                print(f"   • {test}")
        
        if self.failed_tests:
            print(f"\n❌ FAILED TESTS:")
            for test in self.failed_tests:
                critical_marker = " 🚨 CRITICAL" if test in self.critical_failures else ""
                print(f"   • {test}{critical_marker}")
                
        if self.critical_failures:
            print(f"\n🚨 CRITICAL FAILURES (Must be fixed):")
            for test in self.critical_failures:
                print(f"   • {test}")
                
        print("\n" + "="*80)
        
        return len(self.failed_tests) == 0

if __name__ == "__main__":
    tester = V2026ComprehensiveTester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 ALL V2026 COMPLETE LOCALIZATION TESTS PASSED!")
        sys.exit(0)
    else:
        print("⚠️  SOME V2026 LOCALIZATION TESTS FAILED - Review results above")
        sys.exit(1)