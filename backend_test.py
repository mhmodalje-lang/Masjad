#!/usr/bin/env python3
"""
V2026 Global Islamic Localization Backend Test
Tests the specific requirements for Quran/Hadith backend APIs
Focus: Each language gets DIFFERENT text from its verse translation
"""

import requests
import json
import sys
from typing import Dict, Any, List

# Backend URL from frontend environment
BACKEND_URL = "https://quran-verify-4.preview.emergentagent.com/api"

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

    def test_tafsir_french_1_2(self):
        """Test 1a: Tafsir API - French 1:2 (should contain Hamidullah, DIFFERENT from Montada translation)"""
        print("\n" + "="*60)
        print("TEST 1a: TAFSIR FRENCH 1:2 - Should contain Hamidullah, DIFFERENT from Montada")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:2", {"language": "fr"})
        
        if not success:
            self.log_result("Tafsir French 1:2", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir French 1:2", False, "No data returned", critical=True)
            return
            
        # Check required fields
        success_field = data.get('success', False)
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if not success_field:
            issues.append(f"success should be true, got {success_field}")
            
        if 'Hamidullah' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Hamidullah', got '{tafsir_name}'")
            
        # Check that text is NOT the Montada translation
        montada_text = "Louange à Allah, Seigneur des mondes"
        if montada_text in text:
            issues.append(f"text should be DIFFERENT from Montada translation, got Montada text: '{text[:100]}...'")
            
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir French 1:2", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir French 1:2", True, f"French tafsir correct: {tafsir_name}, text is different from Montada", data)

    def test_tafsir_german_1_2(self):
        """Test 1b: Tafsir API - German 1:2 (should contain Abu Reda)"""
        print("\n" + "="*60)
        print("TEST 1b: TAFSIR GERMAN 1:2 - Should contain Abu Reda")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:2", {"language": "de"})
        
        if not success:
            self.log_result("Tafsir German 1:2", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir German 1:2", False, "No data returned", critical=True)
            return
            
        # Check required fields
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if 'Abu Reda' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Abu Reda', got '{tafsir_name}'")
            
        # Check that text is in German
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir German 1:2", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir German 1:2", True, f"German tafsir correct: {tafsir_name}", data)

    def test_tafsir_turkish_1_2(self):
        """Test 1c: Tafsir API - Turkish 1:2 (should contain Elmalılı)"""
        print("\n" + "="*60)
        print("TEST 1c: TAFSIR TURKISH 1:2 - Should contain Elmalılı")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:2", {"language": "tr"})
        
        if not success:
            self.log_result("Tafsir Turkish 1:2", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Turkish 1:2", False, "No data returned", critical=True)
            return
            
        # Check required fields
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if 'Elmalılı' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Elmalılı', got '{tafsir_name}'")
            
        # Check that text is in Turkish
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Turkish 1:2", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Turkish 1:2", True, f"Turkish tafsir correct: {tafsir_name}", data)

    def test_tafsir_swedish_1_2(self):
        """Test 1d: Tafsir API - Swedish 1:2 (should be Arabic Al-Muyassar)"""
        print("\n" + "="*60)
        print("TEST 1d: TAFSIR SWEDISH 1:2 - Should be Arabic Al-Muyassar")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:2", {"language": "sv"})
        
        if not success:
            self.log_result("Tafsir Swedish 1:2", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Swedish 1:2", False, "No data returned", critical=True)
            return
            
        # Check required fields
        is_arabic_tafsir = data.get('is_arabic_tafsir', False)
        text = data.get('text', '')
        
        issues = []
        
        if not is_arabic_tafsir:
            issues.append(f"is_arabic_tafsir should be true, got {is_arabic_tafsir}")
            
        # Check that text is in Arabic (Al-Muyassar)
        has_arabic = any('\u0600' <= char <= '\u06FF' for char in text) if text else False
        if not has_arabic:
            issues.append(f"text should be in Arabic (Al-Muyassar), got '{text[:50]}...'")
            
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Swedish 1:2", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Swedish 1:2", True, f"Swedish tafsir correct: Arabic Al-Muyassar text", data)

    def test_tafsir_dutch_1_2(self):
        """Test 1e: Tafsir API - Dutch 1:2 (should contain Abdalsalaam)"""
        print("\n" + "="*60)
        print("TEST 1e: TAFSIR DUTCH 1:2 - Should contain Abdalsalaam")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:2", {"language": "nl"})
        
        if not success:
            self.log_result("Tafsir Dutch 1:2", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Dutch 1:2", False, "No data returned", critical=True)
            return
            
        # Check required fields
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if 'Abdalsalaam' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Abdalsalaam', got '{tafsir_name}'")
            
        # Check that text is in Dutch
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Dutch 1:2", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Dutch 1:2", True, f"Dutch tafsir correct: {tafsir_name}", data)

    def test_tafsir_greek_1_2(self):
        """Test 1f: Tafsir API - Greek 1:2 (should have translation_pending=true, empty text)"""
        print("\n" + "="*60)
        print("TEST 1f: TAFSIR GREEK 1:2 - Should have translation_pending=true, empty text")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:2", {"language": "el"})
        
        if not success:
            self.log_result("Tafsir Greek 1:2", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Greek 1:2", False, "No data returned", critical=True)
            return
            
        # Check required fields
        translation_pending = data.get('translation_pending', False)
        text = data.get('text', '')
        
        issues = []
        
        if not translation_pending:
            issues.append(f"translation_pending should be true, got {translation_pending}")
            
        if text and len(text) > 0:
            issues.append(f"text should be empty when translation_pending=true, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Greek 1:2", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Greek 1:2", True, f"Greek tafsir correct: translation_pending=true, empty text", data)

    def test_tafsir_arabic_1_2(self):
        """Test 1g: Tafsir API - Arabic 1:2 (should contain الميسر)"""
        print("\n" + "="*60)
        print("TEST 1g: TAFSIR ARABIC 1:2 - Should contain الميسر")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:2", {"language": "ar"})
        
        if not success:
            self.log_result("Tafsir Arabic 1:2", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Arabic 1:2", False, "No data returned", critical=True)
            return
            
        # Check required fields
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if 'الميسر' not in tafsir_name and 'المیسر' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'الميسر' or 'المیسر', got '{tafsir_name}'")
            
        # Check that text is in Arabic
        has_arabic = any('\u0600' <= char <= '\u06FF' for char in text) if text else False
        if not has_arabic:
            issues.append(f"text should be in Arabic, got '{text[:50]}...'")
            
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Arabic 1:2", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Arabic 1:2", True, f"Arabic tafsir correct: {tafsir_name}", data)

    def test_tafsir_english_1_2(self):
        """Test 1h: Tafsir API - English 1:2 (should contain Ibn Kathir)"""
        print("\n" + "="*60)
        print("TEST 1h: TAFSIR ENGLISH 1:2 - Should contain Ibn Kathir")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:2", {"language": "en"})
        
        if not success:
            self.log_result("Tafsir English 1:2", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir English 1:2", False, "No data returned", critical=True)
            return
            
        # Check required fields
        tafsir_name = data.get('tafsir_name', '')
        text = data.get('text', '')
        
        issues = []
        
        if 'Ibn Kathir' not in tafsir_name:
            issues.append(f"tafsir_name should contain 'Ibn Kathir', got '{tafsir_name}'")
            
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir English 1:2", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir English 1:2", True, f"English tafsir correct: {tafsir_name}", data)

    def test_tafsir_russian_1_2(self):
        """Test 1i: Tafsir API - Russian 1:2 (should be in Cyrillic)"""
        print("\n" + "="*60)
        print("TEST 1i: TAFSIR RUSSIAN 1:2 - Should be in Cyrillic")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:2", {"language": "ru"})
        
        if not success:
            self.log_result("Tafsir Russian 1:2", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Tafsir Russian 1:2", False, "No data returned", critical=True)
            return
            
        # Check required fields
        text = data.get('text', '')
        
        issues = []
        
        # Check for Cyrillic characters
        has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in text) if text else False
        if not has_cyrillic:
            issues.append(f"text should contain Cyrillic characters, got '{text[:50]}...'")
            
        if not text or len(text) < 10:
            issues.append(f"text should not be empty, got '{text[:50]}...'")
            
        if issues:
            self.log_result("Tafsir Russian 1:2", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Tafsir Russian 1:2", True, f"Russian tafsir correct with Cyrillic text", data)

    def test_kids_quran_fatiha_french(self):
        """Test 2a: Kids Quran Tafsir - Fatiha in French (should have tafsir_kids field)"""
        print("\n" + "="*60)
        print("TEST 2a: KIDS QURAN FATIHA FRENCH - Should have tafsir_kids field")
        print("="*60)
        
        data, success, error = self.make_request("/kids-learn/quran/surah/fatiha", {"locale": "fr"})
        
        if not success:
            self.log_result("Kids Quran Fatiha French", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Kids Quran Fatiha French", False, "No data returned", critical=True)
            return
            
        # Check that each ayah has tafsir_kids field
        surah = data.get('surah', {})
        ayahs = surah.get('ayahs', [])
        issues = []
        
        if not ayahs:
            issues.append("No ayahs found in response")
        else:
            for i, ayah in enumerate(ayahs):
                tafsir_kids = ayah.get('tafsir_kids', '')
                if not tafsir_kids:
                    issues.append(f"Ayah {i+1} missing tafsir_kids field")
                elif len(tafsir_kids) < 10:
                    issues.append(f"Ayah {i+1} tafsir_kids too short: '{tafsir_kids[:30]}...'")
                    
        if issues:
            self.log_result("Kids Quran Fatiha French", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Kids Quran Fatiha French", True, f"French kids tafsir correct for {len(ayahs)} ayahs", data)

    def test_kids_quran_ikhlas_turkish(self):
        """Test 2b: Kids Quran Tafsir - Ikhlas in Turkish (should have tafsir_kids field)"""
        print("\n" + "="*60)
        print("TEST 2b: KIDS QURAN IKHLAS TURKISH - Should have tafsir_kids field")
        print("="*60)
        
        data, success, error = self.make_request("/kids-learn/quran/surah/ikhlas", {"locale": "tr"})
        
        if not success:
            self.log_result("Kids Quran Ikhlas Turkish", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Kids Quran Ikhlas Turkish", False, "No data returned", critical=True)
            return
            
        # Check that each ayah has tafsir_kids field
        surah = data.get('surah', {})
        ayahs = surah.get('ayahs', [])
        issues = []
        
        if not ayahs:
            issues.append("No ayahs found in response")
        else:
            for i, ayah in enumerate(ayahs):
                tafsir_kids = ayah.get('tafsir_kids', '')
                if not tafsir_kids:
                    issues.append(f"Ayah {i+1} missing tafsir_kids field")
                elif len(tafsir_kids) < 10:
                    issues.append(f"Ayah {i+1} tafsir_kids too short: '{tafsir_kids[:30]}...'")
                    
        if issues:
            self.log_result("Kids Quran Ikhlas Turkish", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Kids Quran Ikhlas Turkish", True, f"Turkish kids tafsir correct for {len(ayahs)} ayahs", data)

    def test_kids_quran_fatiha_arabic(self):
        """Test 2c: Kids Quran Tafsir - Fatiha in Arabic (should have tafsir_kids field)"""
        print("\n" + "="*60)
        print("TEST 2c: KIDS QURAN FATIHA ARABIC - Should have tafsir_kids field")
        print("="*60)
        
        data, success, error = self.make_request("/kids-learn/quran/surah/fatiha", {"locale": "ar"})
        
        if not success:
            self.log_result("Kids Quran Fatiha Arabic", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Kids Quran Fatiha Arabic", False, "No data returned", critical=True)
            return
            
        # Check that each ayah has tafsir_kids field
        surah = data.get('surah', {})
        ayahs = surah.get('ayahs', [])
        issues = []
        
        if not ayahs:
            issues.append("No ayahs found in response")
        else:
            for i, ayah in enumerate(ayahs):
                tafsir_kids = ayah.get('tafsir_kids', '')
                if not tafsir_kids:
                    issues.append(f"Ayah {i+1} missing tafsir_kids field")
                elif len(tafsir_kids) < 10:
                    issues.append(f"Ayah {i+1} tafsir_kids too short: '{tafsir_kids[:30]}...'")
                    
        if issues:
            self.log_result("Kids Quran Fatiha Arabic", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Kids Quran Fatiha Arabic", True, f"Arabic kids tafsir correct for {len(ayahs)} ayahs", data)

    def test_kids_quran_nas_english(self):
        """Test 2d: Kids Quran Tafsir - Nas in English (should have tafsir_kids field)"""
        print("\n" + "="*60)
        print("TEST 2d: KIDS QURAN NAS ENGLISH - Should have tafsir_kids field")
        print("="*60)
        
        data, success, error = self.make_request("/kids-learn/quran/surah/nas", {"locale": "en"})
        
        if not success:
            self.log_result("Kids Quran Nas English", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Kids Quran Nas English", False, "No data returned", critical=True)
            return
            
        # Check that each ayah has tafsir_kids field
        surah = data.get('surah', {})
        ayahs = surah.get('ayahs', [])
        issues = []
        
        if not ayahs:
            issues.append("No ayahs found in response")
        else:
            for i, ayah in enumerate(ayahs):
                tafsir_kids = ayah.get('tafsir_kids', '')
                if not tafsir_kids:
                    issues.append(f"Ayah {i+1} missing tafsir_kids field")
                elif len(tafsir_kids) < 10:
                    issues.append(f"Ayah {i+1} tafsir_kids too short: '{tafsir_kids[:30]}...'")
                    
        if issues:
            self.log_result("Kids Quran Nas English", False, "; ".join(issues), data, critical=True)
        else:
            self.log_result("Kids Quran Nas English", True, f"English kids tafsir correct for {len(ayahs)} ayahs", data)

    def test_daily_hadith_german(self):
        """Test 3a: Daily Hadith - German (should have German narrator/source names)"""
        print("\n" + "="*60)
        print("TEST 3a: DAILY HADITH GERMAN - Should have German narrator/source names")
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
        """Test 3b: Daily Hadith - Turkish (should have Turkish narrator/source names)"""
        print("\n" + "="*60)
        print("TEST 3b: DAILY HADITH TURKISH - Should have Turkish narrator/source names")
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

    def test_cache_clear(self):
        """Test 4a: Cache Management - Clear cache (should return success=true)"""
        print("\n" + "="*60)
        print("TEST 4a: CACHE CLEAR - Should return success=true")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/cache/clear", method="POST")
        
        if not success:
            self.log_result("Cache Clear", False, f"Request failed: {error}", critical=True)
            return
            
        if not data:
            self.log_result("Cache Clear", False, "No data returned", critical=True)
            return
            
        # Check success field
        cache_success = data.get('success', False)
        
        if cache_success:
            self.log_result("Cache Clear", True, f"Cache cleared successfully", data)
        else:
            self.log_result("Cache Clear", False, f"Cache clear failed: success={cache_success}", data, critical=True)

    def run_all_tests(self):
        """Run all V2026 Global Islamic Localization tests"""
        print("🕌 STARTING V2026 GLOBAL ISLAMIC LOCALIZATION TESTS")
        print("="*80)
        print(f"Backend URL: {BACKEND_URL}")
        print("Focus: Each language gets DIFFERENT text from its verse translation")
        print("="*80)
        
        # Run all tests in order
        self.test_tafsir_french_1_2()
        self.test_tafsir_german_1_2()
        self.test_tafsir_turkish_1_2()
        self.test_tafsir_swedish_1_2()
        self.test_tafsir_dutch_1_2()
        self.test_tafsir_greek_1_2()
        self.test_tafsir_arabic_1_2()
        self.test_tafsir_english_1_2()
        self.test_tafsir_russian_1_2()
        self.test_kids_quran_fatiha_french()
        self.test_kids_quran_ikhlas_turkish()
        self.test_kids_quran_fatiha_arabic()
        self.test_kids_quran_nas_english()
        self.test_daily_hadith_german()
        self.test_daily_hadith_turkish()
        self.test_cache_clear()
        
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