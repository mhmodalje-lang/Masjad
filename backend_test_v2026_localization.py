#!/usr/bin/env python3
"""
V2026 Global Islamic Localization Backend Test
Tests the specific requirements for Quran/Hadith backend APIs
Focus: Each language gets its OWN content (no English fallback)
"""

import requests
import json
import sys
from typing import Dict, Any, List

# Backend URL from frontend environment
BACKEND_URL = "https://bug-fix-tools.preview.emergentagent.com/api"

class V2026LocalizationTester:
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

    def test_tafsir_arabic(self):
        """Test Tafsir API - Arabic (should contain الميسر)"""
        print("\n" + "="*60)
        print("TEST 1: TAFSIR ARABIC - Should contain الميسر")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "ar"})
        
        if not success:
            self.log_result("Tafsir Arabic 1:1", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Arabic 1:1", False, "No data returned", critical=True)
            return
            
        # Check required fields
        fallback_to_english = data.get('fallback_to_english', True)  # Should be False
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if fallback_to_english != False:
            issues.append(f"fallback_to_english should be false, got {fallback_to_english}")
            
        if 'الميسر' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'الميسر', got '{tafsir_name}'")
            
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Arabic 1:1", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Arabic 1:1", True, f"Arabic tafsir correct: {tafsir_name}", data)

    def test_tafsir_english(self):
        """Test Tafsir API - English (should contain Ibn Kathir)"""
        print("\n" + "="*60)
        print("TEST 2: TAFSIR ENGLISH - Should contain Ibn Kathir")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "en"})
        
        if not success:
            self.log_result("Tafsir English 1:1", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir English 1:1", False, "No data returned", critical=True)
            return
            
        # Check required fields
        fallback_to_english = data.get('fallback_to_english', True)  # Should be False
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if fallback_to_english != False:
            issues.append(f"fallback_to_english should be false, got {fallback_to_english}")
            
        if 'Ibn Kathir' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Ibn Kathir', got '{tafsir_name}'")
            
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir English 1:1", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir English 1:1", True, f"English tafsir correct: {tafsir_name}", data)

    def test_tafsir_russian(self):
        """Test Tafsir API - Russian (should be Cyrillic)"""
        print("\n" + "="*60)
        print("TEST 3: TAFSIR RUSSIAN - Should be Cyrillic")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "ru"})
        
        if not success:
            self.log_result("Tafsir Russian 1:1", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Russian 1:1", False, "No data returned", critical=True)
            return
            
        # Check required fields
        fallback_to_english = data.get('fallback_to_english', True)  # Should be False
        text = data.get('text', '')
        
        issues = []
        
        if fallback_to_english != False:
            issues.append(f"fallback_to_english should be false, got {fallback_to_english}")
            
        # Check for Cyrillic characters
        has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in text)
        if not has_cyrillic and text:
            issues.append(f"text should contain Cyrillic characters, got '{text[:50]}...'")
            
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Russian 1:1", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Russian 1:1", True, f"Russian tafsir correct with Cyrillic text", data)

    def test_tafsir_german(self):
        """Test Tafsir API - German (should contain Bubenheim, NOT English)"""
        print("\n" + "="*60)
        print("TEST 4: TAFSIR GERMAN - Should contain Bubenheim, NOT English")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "de"})
        
        if not success:
            self.log_result("Tafsir German 1:1", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir German 1:1", False, "No data returned", critical=True)
            return
            
        # Check required fields
        fallback_to_english = data.get('fallback_to_english', True)  # Should be False
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if fallback_to_english != False:
            issues.append(f"fallback_to_english should be false, got {fallback_to_english}")
            
        if 'Bubenheim' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Bubenheim', got '{tafsir_name}'")
            
        # Check that text is NOT English
        if text:
            english_words = ['the', 'and', 'of', 'to', 'in', 'that', 'is', 'for', 'with', 'as']
            english_count = sum(1 for word in english_words if f' {word} ' in text.lower())
            if english_count > 2:  # Allow some false positives
                issues.append(f"text appears to be English, not German: '{text[:100]}...'")
                
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir German 1:1", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir German 1:1", True, f"German tafsir correct: {tafsir_name}", data)

    def test_tafsir_french(self):
        """Test Tafsir API - French (should contain Montada, NOT English)"""
        print("\n" + "="*60)
        print("TEST 5: TAFSIR FRENCH - Should contain Montada, NOT English")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "fr"})
        
        if not success:
            self.log_result("Tafsir French 1:1", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir French 1:1", False, "No data returned", critical=True)
            return
            
        # Check required fields
        fallback_to_english = data.get('fallback_to_english', True)  # Should be False
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if fallback_to_english != False:
            issues.append(f"fallback_to_english should be false, got {fallback_to_english}")
            
        if 'Montada' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Montada', got '{tafsir_name}'")
            
        # Check that text is NOT English
        if text:
            english_words = ['the', 'and', 'of', 'to', 'in', 'that', 'is', 'for', 'with', 'as']
            english_count = sum(1 for word in english_words if f' {word} ' in text.lower())
            if english_count > 2:  # Allow some false positives
                issues.append(f"text appears to be English, not French: '{text[:100]}...'")
                
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir French 1:1", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir French 1:1", True, f"French tafsir correct: {tafsir_name}", data)

    def test_tafsir_turkish(self):
        """Test Tafsir API - Turkish (should contain Diyanet, NOT English)"""
        print("\n" + "="*60)
        print("TEST 6: TAFSIR TURKISH - Should contain Diyanet, NOT English")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "tr"})
        
        if not success:
            self.log_result("Tafsir Turkish 1:1", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Turkish 1:1", False, "No data returned", critical=True)
            return
            
        # Check required fields
        fallback_to_english = data.get('fallback_to_english', True)  # Should be False
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if fallback_to_english != False:
            issues.append(f"fallback_to_english should be false, got {fallback_to_english}")
            
        if 'Diyanet' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Diyanet', got '{tafsir_name}'")
            
        # Check that text is NOT English
        if text:
            english_words = ['the', 'and', 'of', 'to', 'in', 'that', 'is', 'for', 'with', 'as']
            english_count = sum(1 for word in english_words if f' {word} ' in text.lower())
            if english_count > 2:  # Allow some false positives
                issues.append(f"text appears to be English, not Turkish: '{text[:100]}...'")
                
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Turkish 1:1", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Turkish 1:1", True, f"Turkish tafsir correct: {tafsir_name}", data)

    def test_tafsir_swedish(self):
        """Test Tafsir API - Swedish (should contain Bernström, NOT English)"""
        print("\n" + "="*60)
        print("TEST 7: TAFSIR SWEDISH - Should contain Bernström, NOT English")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "sv"})
        
        if not success:
            self.log_result("Tafsir Swedish 1:1", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Swedish 1:1", False, "No data returned", critical=True)
            return
            
        # Check required fields
        fallback_to_english = data.get('fallback_to_english', True)  # Should be False
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if fallback_to_english != False:
            issues.append(f"fallback_to_english should be false, got {fallback_to_english}")
            
        if 'Bernström' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Bernström', got '{tafsir_name}'")
            
        # Check that text is NOT English
        if text:
            english_words = ['the', 'and', 'of', 'to', 'in', 'that', 'is', 'for', 'with', 'as']
            english_count = sum(1 for word in english_words if f' {word} ' in text.lower())
            if english_count > 2:  # Allow some false positives
                issues.append(f"text appears to be English, not Swedish: '{text[:100]}...'")
                
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Swedish 1:1", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Swedish 1:1", True, f"Swedish tafsir correct: {tafsir_name}", data)

    def test_tafsir_dutch(self):
        """Test Tafsir API - Dutch (should contain Siregar, NOT English)"""
        print("\n" + "="*60)
        print("TEST 8: TAFSIR DUTCH - Should contain Siregar, NOT English")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "nl"})
        
        if not success:
            self.log_result("Tafsir Dutch 1:1", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Dutch 1:1", False, "No data returned", critical=True)
            return
            
        # Check required fields
        fallback_to_english = data.get('fallback_to_english', True)  # Should be False
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if fallback_to_english != False:
            issues.append(f"fallback_to_english should be false, got {fallback_to_english}")
            
        if 'Siregar' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Siregar', got '{tafsir_name}'")
            
        # Check that text is NOT English
        if text:
            english_words = ['the', 'and', 'of', 'to', 'in', 'that', 'is', 'for', 'with', 'as']
            english_count = sum(1 for word in english_words if f' {word} ' in text.lower())
            if english_count > 2:  # Allow some false positives
                issues.append(f"text appears to be English, not Dutch: '{text[:100]}...'")
                
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Dutch 1:1", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Dutch 1:1", True, f"Dutch tafsir correct: {tafsir_name}", data)

    def test_tafsir_greek(self):
        """Test Tafsir API - Greek (should have translation_pending=true, NO English)"""
        print("\n" + "="*60)
        print("TEST 9: TAFSIR GREEK - Should have translation_pending=true, NO English")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "el"})
        
        if not success:
            self.log_result("Tafsir Greek 1:1", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Greek 1:1", False, "No data returned", critical=True)
            return
            
        # Check required fields
        translation_pending = data.get('translation_pending', False)  # Should be True
        text = data.get('text', '')
        
        issues = []
        
        if translation_pending != True:
            issues.append(f"translation_pending should be true, got {translation_pending}")
            
        if text and len(text) > 0:
            # Check that there's NO English text
            english_words = ['the', 'and', 'of', 'to', 'in', 'that', 'is', 'for', 'with', 'as']
            english_count = sum(1 for word in english_words if f' {word} ' in text.lower())
            if english_count > 1:
                issues.append(f"text should be empty when translation_pending=true, got English text: '{text[:100]}...'")
            
        if issues:
            self.log_result("Tafsir Greek 1:1", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Greek 1:1", True, f"Greek tafsir correct: translation_pending=true, no English fallback", data)

    def test_quran_verses_greek(self):
        """Test Quran Verses API - Greek handling"""
        print("\n" + "="*60)
        print("TEST 10: QURAN VERSES GREEK - Should have translation_pending=true")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/verses/by_chapter/1", {"language": "el", "per_page": "10"})
        
        if not success:
            self.log_result("Quran Verses Greek", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Quran Verses Greek", False, "No data returned", critical=True)
            return
            
        # Check required fields
        translation_pending = data.get('translation_pending', False)  # Should be True
        pending_language = data.get('pending_language', '')
        
        issues = []
        
        if translation_pending != True:
            issues.append(f"translation_pending should be true, got {translation_pending}")
            
        if pending_language != 'el':
            issues.append(f"pending_language should be 'el', got '{pending_language}'")
            
        if issues:
            self.log_result("Quran Verses Greek", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Quran Verses Greek", True, f"Greek verses correct: translation_pending=true", data)

    def test_daily_hadith_german(self):
        """Test Daily Hadith - German (should have German narrator/source, NOT Arabic strings)"""
        print("\n" + "="*60)
        print("TEST 11: DAILY HADITH GERMAN - German narrator/source, NOT Arabic")
        print("="*60)
        
        data, success, error = self.make_request("/daily-hadith", {"language": "de"})
        
        if not success:
            self.log_result("Daily Hadith German", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Daily Hadith German", False, "No data returned", critical=True)
            return
            
        hadith = data.get('hadith', {})
        narrator = hadith.get('narrator', '')
        source = hadith.get('source', '')
        
        issues = []
        
        # Check that narrator and source are NOT Arabic
        if narrator:
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in narrator)
            if has_arabic:
                issues.append(f"narrator should be German, not Arabic: '{narrator}'")
                
        if source:
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in source)
            if has_arabic:
                issues.append(f"source should be German, not Arabic: '{source}'")
                
        if not narrator or not source:
            issues.append(f"narrator and source should not be empty: narrator='{narrator}', source='{source}'")
            
        if issues:
            self.log_result("Daily Hadith German", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Daily Hadith German", True, f"German hadith correct: narrator='{narrator}', source='{source}'", data)

    def test_daily_hadith_turkish(self):
        """Test Daily Hadith - Turkish (should have Turkish narrator/source)"""
        print("\n" + "="*60)
        print("TEST 12: DAILY HADITH TURKISH - Turkish narrator/source")
        print("="*60)
        
        data, success, error = self.make_request("/daily-hadith", {"language": "tr"})
        
        if not success:
            self.log_result("Daily Hadith Turkish", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Daily Hadith Turkish", False, "No data returned", critical=True)
            return
            
        hadith = data.get('hadith', {})
        narrator = hadith.get('narrator', '')
        source = hadith.get('source', '')
        
        issues = []
        
        # Check that narrator and source are NOT Arabic
        if narrator:
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in narrator)
            if has_arabic:
                issues.append(f"narrator should be Turkish, not Arabic: '{narrator}'")
                
        if source:
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in source)
            if has_arabic:
                issues.append(f"source should be Turkish, not Arabic: '{source}'")
                
        if not narrator or not source:
            issues.append(f"narrator and source should not be empty: narrator='{narrator}', source='{source}'")
            
        if issues:
            self.log_result("Daily Hadith Turkish", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Daily Hadith Turkish", True, f"Turkish hadith correct: narrator='{narrator}', source='{source}'", data)

    def test_daily_hadith_russian(self):
        """Test Daily Hadith - Russian (should have Russian narrator/source in Cyrillic)"""
        print("\n" + "="*60)
        print("TEST 13: DAILY HADITH RUSSIAN - Russian narrator/source (Cyrillic)")
        print("="*60)
        
        data, success, error = self.make_request("/daily-hadith", {"language": "ru"})
        
        if not success:
            self.log_result("Daily Hadith Russian", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Daily Hadith Russian", False, "No data returned", critical=True)
            return
            
        hadith = data.get('hadith', {})
        narrator = hadith.get('narrator', '')
        source = hadith.get('source', '')
        
        issues = []
        
        # Check for Cyrillic characters in narrator and source
        if narrator:
            has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in narrator)
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in narrator)
            if has_arabic:
                issues.append(f"narrator should be Russian, not Arabic: '{narrator}'")
            elif not has_cyrillic:
                issues.append(f"narrator should contain Cyrillic characters: '{narrator}'")
                
        if source:
            has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in source)
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in source)
            if has_arabic:
                issues.append(f"source should be Russian, not Arabic: '{source}'")
            elif not has_cyrillic:
                issues.append(f"source should contain Cyrillic characters: '{source}'")
                
        if not narrator or not source:
            issues.append(f"narrator and source should not be empty: narrator='{narrator}', source='{source}'")
            
        if issues:
            self.log_result("Daily Hadith Russian", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Daily Hadith Russian", True, f"Russian hadith correct: narrator='{narrator}', source='{source}'", data)

    def test_cache_clear(self):
        """Test Cache Management - Clear cache"""
        print("\n" + "="*60)
        print("TEST 14: CACHE CLEAR - Should return success=true")
        print("="*60)
        
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

    def test_tafsir_ayat_al_kursi_french(self):
        """Test Tafsir for verse 2:255 (Ayat al-Kursi) in French - Should be French, NOT English"""
        print("\n" + "="*60)
        print("TEST 15: TAFSIR AYAT AL-KURSI FRENCH - Should be French, NOT English")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/2:255", {"language": "fr"})
        
        if not success:
            self.log_result("Tafsir Ayat al-Kursi French", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Ayat al-Kursi French", False, "No data returned", critical=True)
            return
            
        # Check required fields
        fallback_to_english = data.get('fallback_to_english', True)  # Should be False
        text = data.get('text', '')
        
        issues = []
        
        if fallback_to_english != False:
            issues.append(f"fallback_to_english should be false, got {fallback_to_english}")
            
        # Check that text is NOT English
        if text:
            english_words = ['the', 'and', 'of', 'to', 'in', 'that', 'is', 'for', 'with', 'as', 'allah', 'god']
            english_count = sum(1 for word in english_words if f' {word} ' in text.lower())
            if english_count > 3:  # Allow some false positives
                issues.append(f"text appears to be English, not French: '{text[:100]}...'")
                
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Ayat al-Kursi French", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Ayat al-Kursi French", True, f"French Ayat al-Kursi tafsir correct", data)

    def test_tafsir_ayat_al_kursi_turkish(self):
        """Test Tafsir for verse 2:255 (Ayat al-Kursi) in Turkish - Should be Turkish, NOT English"""
        print("\n" + "="*60)
        print("TEST 16: TAFSIR AYAT AL-KURSI TURKISH - Should be Turkish, NOT English")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/2:255", {"language": "tr"})
        
        if not success:
            self.log_result("Tafsir Ayat al-Kursi Turkish", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Ayat al-Kursi Turkish", False, "No data returned", critical=True)
            return
            
        # Check required fields
        fallback_to_english = data.get('fallback_to_english', True)  # Should be False
        text = data.get('text', '')
        
        issues = []
        
        if fallback_to_english != False:
            issues.append(f"fallback_to_english should be false, got {fallback_to_english}")
            
        # Check that text is NOT English
        if text:
            english_words = ['the', 'and', 'of', 'to', 'in', 'that', 'is', 'for', 'with', 'as', 'allah', 'god']
            english_count = sum(1 for word in english_words if f' {word} ' in text.lower())
            if english_count > 3:  # Allow some false positives
                issues.append(f"text appears to be English, not Turkish: '{text[:100]}...'")
                
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Ayat al-Kursi Turkish", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Ayat al-Kursi Turkish", True, f"Turkish Ayat al-Kursi tafsir correct", data)

    def run_all_tests(self):
        """Run all V2026 Global Islamic Localization tests"""
        print("🕌 STARTING V2026 GLOBAL ISLAMIC LOCALIZATION TESTS")
        print("="*80)
        print(f"Backend URL: {BACKEND_URL}")
        print("Focus: Each language gets its OWN content (no English fallback)")
        print("="*80)
        
        # Run all tests in order
        self.test_tafsir_arabic()
        self.test_tafsir_english()
        self.test_tafsir_russian()
        self.test_tafsir_german()
        self.test_tafsir_french()
        self.test_tafsir_turkish()
        self.test_tafsir_swedish()
        self.test_tafsir_dutch()
        self.test_tafsir_greek()
        self.test_quran_verses_greek()
        self.test_daily_hadith_german()
        self.test_daily_hadith_turkish()
        self.test_daily_hadith_russian()
        self.test_cache_clear()
        self.test_tafsir_ayat_al_kursi_french()
        self.test_tafsir_ayat_al_kursi_turkish()
        
        # Summary
        print("\n" + "="*80)
        print("🏁 V2026 LOCALIZATION TEST SUMMARY")
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
    tester = V2026LocalizationTester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 ALL V2026 LOCALIZATION TESTS PASSED!")
        sys.exit(0)
    else:
        print("⚠️  SOME V2026 LOCALIZATION TESTS FAILED - Review results above")
        sys.exit(1)