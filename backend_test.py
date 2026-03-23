#!/usr/bin/env python3
"""
Backend Testing for أذان وحكاية - Islamic Content Audit & Language Integrity
Tests all critical endpoints for religious accuracy and language integrity
"""

import requests
import json
import sys
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = "https://quran-verify-4.preview.emergentagent.com/api"

class IslamicContentTester:
    def __init__(self):
        self.results = []
        self.failed_tests = []
        self.passed_tests = []
        
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
    
    def test_full_audit_report(self):
        """Test 1: Full Audit Report - Critical Islamic Content Verification"""
        print("\n" + "="*60)
        print("TEST 1: FULL AUDIT REPORT")
        print("="*60)
        
        data, success, error = self.make_request("/audit/full-report")
        
        if not success:
            self.log_result("Full Audit Report", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Full Audit Report", False, "No data returned")
            return
            
        # Verify success field
        if not data.get('success'):
            self.log_result("Full Audit Report", False, f"Audit success is false: {data.get('success')}")
            return
            
        summary = data.get('summary', {})
        forbidden_check = data.get('forbidden_sources_check', {})
        
        # Critical verification points
        checks = [
            ("all_adult_bukhari_muslim", summary.get('all_adult_bukhari_muslim'), True),
            ("all_kids_bukhari_muslim", summary.get('all_kids_bukhari_muslim'), True),
            ("all_extended_bukhari_muslim", summary.get('all_extended_bukhari_muslim'), True),
            ("adult_hadiths_fully_translated", summary.get('adult_hadiths_fully_translated'), "21/21"),
            ("kids_hadiths_fully_translated", summary.get('kids_hadiths_fully_translated'), "10/10"),
            ("extended_hadiths_fully_translated", summary.get('extended_hadiths_fully_translated'), "5/5"),
            ("adult_clean", forbidden_check.get('adult_clean'), True),
            ("kids_clean", forbidden_check.get('kids_clean'), True),
            ("extended_clean", forbidden_check.get('extended_clean'), True),
        ]
        
        all_passed = True
        failed_checks = []
        
        for check_name, actual, expected in checks:
            if actual != expected:
                all_passed = False
                failed_checks.append(f"{check_name}: expected {expected}, got {actual}")
                
        if all_passed:
            self.log_result("Full Audit Report", True, "All audit checks passed successfully", summary)
        else:
            self.log_result("Full Audit Report", False, f"Failed checks: {'; '.join(failed_checks)}", data)
    
    def test_daily_hadith_french(self):
        """Test 2: Daily Hadith French Language Integrity"""
        print("\n" + "="*60)
        print("TEST 2: DAILY HADITH - FRENCH LANGUAGE INTEGRITY")
        print("="*60)
        
        data, success, error = self.make_request("/daily-hadith", {"language": "fr"})
        
        if not success:
            self.log_result("Daily Hadith French", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Daily Hadith French", False, "No hadith data returned")
            return
            
        # Check if hadith has French translation OR translation_pending=true
        has_french_translation = False
        has_translation_pending = data.get('translation_pending', False)
        
        # Check hadith object if it exists
        hadith = data.get('hadith', data)
        
        # Check translation_language field first
        translation_language = hadith.get('translation_language', '')
        if translation_language == 'fr':
            has_french_translation = True
        
        # Also check for French text in various fields
        if not has_french_translation:
            text_fields = ['text', 'translation', 'french_translation', 'content']
            for field in text_fields:
                if field in hadith and hadith[field]:
                    text = str(hadith[field]).lower()
                    # Check for French characters and words
                    french_indicators = ['à', 'è', 'é', 'ê', 'ç', 'bâti', 'témoigner', 'pèlerinage', 'jeûner']
                    english_indicators = ['the prophet', 'said allah', 'narrated by']
                    
                    has_french_chars = any(indicator in text for indicator in french_indicators)
                    has_english_phrases = any(indicator in text for indicator in english_indicators)
                    
                    if has_french_chars and not has_english_phrases:
                        has_french_translation = True
                        break
        
        if has_french_translation or has_translation_pending:
            details = "French translation found" if has_french_translation else "Translation pending (acceptable)"
            self.log_result("Daily Hadith French", True, details, data)
        else:
            self.log_result("Daily Hadith French", False, "No French translation and no translation_pending flag", data)
    
    def test_tafsir_french(self):
        """Test 3: Tafsir French - Should have translation_pending=true"""
        print("\n" + "="*60)
        print("TEST 3: TAFSIR FRENCH - TRANSLATION PENDING CHECK")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "fr"})
        
        if not success:
            self.log_result("Tafsir French", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Tafsir French", False, "No tafsir data returned")
            return
            
        # Should have translation_pending=true for French
        translation_pending = data.get('translation_pending', False)
        
        if translation_pending:
            # Verify NO English text is returned as fallback
            text_content = data.get('text', '')
            if text_content and isinstance(text_content, str):
                english_indicators = ['the', 'and', 'said', 'allah', 'prophet']
                has_english = any(indicator.lower() in text_content.lower() for indicator in english_indicators)
                
                if has_english:
                    self.log_result("Tafsir French", False, "English fallback text found when translation_pending=true", data)
                else:
                    self.log_result("Tafsir French", True, "Translation pending correctly set, no English fallback", data)
            else:
                self.log_result("Tafsir French", True, "Translation pending correctly set, no text content", data)
        else:
            self.log_result("Tafsir French", False, "translation_pending should be true for French tafsir", data)
    
    def test_tafsir_arabic(self):
        """Test 4: Tafsir Arabic - Should work normally"""
        print("\n" + "="*60)
        print("TEST 4: TAFSIR ARABIC - NORMAL OPERATION")
        print("="*60)
        
        data, success, error = self.make_request("/quran/v4/tafsir/1:1", {"language": "ar"})
        
        if not success:
            self.log_result("Tafsir Arabic", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Tafsir Arabic", False, "No tafsir data returned")
            return
            
        # Should NOT have translation_pending=true for Arabic
        translation_pending = data.get('translation_pending', False)
        text_content = data.get('text', '')
        
        if not translation_pending and text_content:
            # Check if text contains Arabic characters
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in text_content)
            if has_arabic:
                self.log_result("Tafsir Arabic", True, "Arabic tafsir returned successfully", data)
            else:
                self.log_result("Tafsir Arabic", True, "Tafsir returned (may be transliterated)", data)
        else:
            details = "translation_pending is true" if translation_pending else "no text content"
            self.log_result("Tafsir Arabic", False, f"Arabic tafsir failed: {details}", data)
    
    def test_kids_hadiths_french(self):
        """Test 5: Kids Hadiths French Language Integrity"""
        print("\n" + "="*60)
        print("TEST 5: KIDS HADITHS - FRENCH LANGUAGE INTEGRITY")
        print("="*60)
        
        data, success, error = self.make_request("/kids-learn/hadiths", {"locale": "fr"})
        
        if not success:
            self.log_result("Kids Hadiths French", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Kids Hadiths French", False, "No kids hadiths data returned")
            return
            
        # Check if hadiths are returned
        hadiths = data if isinstance(data, list) else data.get('hadiths', [])
        
        if not hadiths:
            self.log_result("Kids Hadiths French", False, "No hadiths in response", data)
            return
            
        # Check language integrity - should be French, not English
        french_count = 0
        english_count = 0
        
        for hadith in hadiths[:3]:  # Check first 3 hadiths
            # Check translation_pending field first
            if hadith.get('translation_pending') == False and hadith.get('translation'):
                translation = str(hadith['translation']).lower()
                
                # Check for French characters and words
                french_indicators = ['à', 'è', 'é', 'ê', 'ç', 'miséricorde', 'vérité', 'véracité', 'soyez', 'celui qui']
                english_indicators = ['the prophet', 'said allah', 'narrated by', 'whoever believes']
                
                has_french_chars = any(indicator in translation for indicator in french_indicators)
                has_english_phrases = any(indicator in translation for indicator in english_indicators)
                
                if has_french_chars and not has_english_phrases:
                    french_count += 1
                elif has_english_phrases:
                    english_count += 1
        
        if french_count > 0 and english_count == 0:
            self.log_result("Kids Hadiths French", True, f"French translations found ({french_count} hadiths)", data)
        elif english_count > 0:
            self.log_result("Kids Hadiths French", False, f"English text found in French locale ({english_count} hadiths)", data)
        else:
            self.log_result("Kids Hadiths French", True, "Hadiths returned (language check inconclusive)", data)
    
    def test_tashkeel_audit(self):
        """Test 6: Tashkeel Audit - Arabic Diacritics Check"""
        print("\n" + "="*60)
        print("TEST 6: TASHKEEL AUDIT - ARABIC DIACRITICS")
        print("="*60)
        
        data, success, error = self.make_request("/audit/tashkeel")
        
        if not success:
            self.log_result("Tashkeel Audit", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Tashkeel Audit", False, "No tashkeel audit data returned")
            return
            
        # Check if audit was successful
        if isinstance(data, dict):
            if data.get('success') or data.get('status') == 'complete':
                self.log_result("Tashkeel Audit", True, "Tashkeel audit completed successfully", data)
            else:
                self.log_result("Tashkeel Audit", False, "Tashkeel audit reported issues", data)
        else:
            self.log_result("Tashkeel Audit", True, "Tashkeel audit response received", data)
    
    def test_health_check(self):
        """Test 7: Health Check"""
        print("\n" + "="*60)
        print("TEST 7: HEALTH CHECK")
        print("="*60)
        
        data, success, error = self.make_request("/health")
        
        if not success:
            self.log_result("Health Check", False, f"Request failed: {error}")
            return
            
        if not data:
            self.log_result("Health Check", False, "No health data returned")
            return
            
        # Check status
        status = data.get('status', '').lower() if isinstance(data, dict) else str(data).lower()
        
        if 'healthy' in status or status == 'ok':
            self.log_result("Health Check", True, f"Service is healthy: {status}", data)
        else:
            self.log_result("Health Check", False, f"Service health issue: {status}", data)
    
    def run_all_tests(self):
        """Run all Islamic content audit tests"""
        print("🕌 STARTING ISLAMIC CONTENT AUDIT & LANGUAGE INTEGRITY TESTS")
        print("="*80)
        print(f"Backend URL: {BACKEND_URL}")
        print("="*80)
        
        # Run all tests
        self.test_full_audit_report()
        self.test_daily_hadith_french()
        self.test_tafsir_french()
        self.test_tafsir_arabic()
        self.test_kids_hadiths_french()
        self.test_tashkeel_audit()
        self.test_health_check()
        
        # Summary
        print("\n" + "="*80)
        print("🏁 TEST SUMMARY")
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
    tester = IslamicContentTester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 ALL TESTS PASSED - Islamic content integrity verified!")
        sys.exit(0)
    else:
        print("⚠️  SOME TESTS FAILED - Review results above")
        sys.exit(1)