#!/usr/bin/env python3
"""
Global Application Audit - Backend Testing
Tests for Religious Accuracy & Language Integrity (V2026)
"""

import requests
import json
from typing import Dict, Any
import sys

# Backend URL from environment
BACKEND_URL = "https://quran-integrity-1.preview.emergentagent.com/api"

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def assert_test(self, condition: bool, test_name: str, details: str = ""):
        if condition:
            self.passed += 1
            print(f"✅ PASS: {test_name}")
            if details:
                print(f"   {details}")
        else:
            self.failed += 1
            error_msg = f"❌ FAIL: {test_name}"
            if details:
                error_msg += f" - {details}"
            print(error_msg)
            self.errors.append(error_msg)
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY: {self.passed}/{total} PASSED")
        if self.failed > 0:
            print(f"FAILED TESTS:")
            for error in self.errors:
                print(f"  {error}")
        print(f"{'='*60}")
        return self.failed == 0

def make_request(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make HTTP request to backend API"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 404:
            return {"status_code": 404, "error": "Not Found"}
        elif response.status_code != 200:
            return {"status_code": response.status_code, "error": f"HTTP {response.status_code}"}
            
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode failed: {str(e)}", "raw_response": response.text[:200]}

def test_language_integrity_tafsir_no_fallback(results: TestResults):
    """Test 1: LANGUAGE INTEGRITY - No English Fallback for Tafsir"""
    print("\n🔍 Testing Language Integrity - No English Fallback for Tafsir")
    
    test_cases = [
        ("fr", "French"),
        ("de", "German"), 
        ("nl", "Dutch")
    ]
    
    for lang_code, lang_name in test_cases:
        response = make_request("/quran/v4/tafsir/1:1", {"language": lang_code})
        
        if "error" in response:
            results.assert_test(False, f"{lang_name} tafsir language integrity", f"API Error: {response['error']}")
            continue
            
        # Must have translation_pending: true
        has_translation_pending = response.get("translation_pending") == True
        results.assert_test(has_translation_pending, 
                          f"{lang_name} tafsir has translation_pending=true",
                          f"Got translation_pending: {response.get('translation_pending')}")
        
        # Must have empty text
        text_empty = not response.get("text", "").strip()
        results.assert_test(text_empty,
                          f"{lang_name} tafsir has empty text",
                          f"Text length: {len(response.get('text', ''))}")

def test_native_tafsir_languages_work(results: TestResults):
    """Test 2: Native Tafsir Languages Still Work"""
    print("\n🔍 Testing Native Tafsir Languages Still Work")
    
    test_cases = [
        ("ar", "1:1", 16, "Arabic"),
        ("en", "2:255", 169, "English"),
        ("ru", "1:1", 170, "Russian")
    ]
    
    for lang_code, verse, expected_tafsir_id, lang_name in test_cases:
        response = make_request(f"/quran/v4/tafsir/{verse}", {"language": lang_code})
        
        if "error" in response:
            results.assert_test(False, f"{lang_name} native tafsir", f"API Error: {response['error']}")
            continue
            
        # Must have translation_pending: false
        translation_pending_false = response.get("translation_pending") == False
        results.assert_test(translation_pending_false,
                          f"{lang_name} tafsir translation_pending=false",
                          f"Got translation_pending: {response.get('translation_pending')}")
        
        # Must have non-empty text
        has_text = bool(response.get("text", "").strip())
        results.assert_test(has_text,
                          f"{lang_name} tafsir has non-empty text",
                          f"Text length: {len(response.get('text', ''))}")
        
        # Must have correct tafsir_id
        correct_tafsir_id = response.get("tafsir_id") == expected_tafsir_id
        results.assert_test(correct_tafsir_id,
                          f"{lang_name} tafsir has correct tafsir_id",
                          f"Expected: {expected_tafsir_id}, Got: {response.get('tafsir_id')}")

def test_language_integrity_hadith(results: TestResults):
    """Test 3: LANGUAGE INTEGRITY - Hadith"""
    print("\n🔍 Testing Language Integrity - Hadith")
    
    test_cases = [
        ("ar", "Arabic"),
        ("en", "English"),
        ("de", "German")
    ]
    
    for lang_code, lang_name in test_cases:
        response = make_request("/daily-hadith", {"language": lang_code})
        
        if "error" in response:
            results.assert_test(False, f"{lang_name} daily hadith", f"API Error: {response['error']}")
            continue
            
        # Check if response is successful
        is_successful = response.get("success") == True
        results.assert_test(is_successful,
                          f"{lang_name} daily hadith successful response",
                          f"Success: {response.get('success')}")
        
        # For Arabic, translation_pending should be false or not present
        if lang_code == "ar":
            hadith_data = response.get("hadith", {})
            translation_pending = hadith_data.get("translation_pending", False)
            results.assert_test(translation_pending == False,
                              f"{lang_name} hadith translation_pending=false",
                              f"Got translation_pending: {translation_pending}")
        
        # For other languages, check if translation_pending field exists and log its value
        else:
            hadith_data = response.get("hadith", {})
            translation_pending = hadith_data.get("translation_pending")
            print(f"   {lang_name} hadith translation_pending: {translation_pending}")

def test_dorar_hadith_verification(results: TestResults):
    """Test 4: Dorar.net Hadith Verification"""
    print("\n🔍 Testing Dorar.net Hadith Verification")
    
    # Test valid hadith numbers
    valid_test_cases = [
        ("1", "Hadith #1"),
        ("15", "Hadith #15")
    ]
    
    for hadith_num, test_name in valid_test_cases:
        response = make_request(f"/hadith-verify/{hadith_num}")
        
        if "error" in response:
            results.assert_test(False, f"{test_name} verification", f"API Error: {response['error']}")
            continue
            
        # Must be verified: true
        is_verified = response.get("verified") == True
        results.assert_test(is_verified,
                          f"{test_name} verified=true",
                          f"Got verified: {response.get('verified')}")
        
        # For hadith #1, must have dorar_ruling: "صحيح"
        if hadith_num == "1":
            dorar_ruling = response.get("dorar_ruling")
            is_sahih = dorar_ruling == "صحيح"
            results.assert_test(is_sahih,
                              f"{test_name} dorar_ruling='صحيح'",
                              f"Got dorar_ruling: {dorar_ruling}")
    
    # Test invalid hadith number - should return 404
    response = make_request("/hadith-verify/999999")
    is_404 = response.get("status_code") == 404
    results.assert_test(is_404,
                      "Invalid hadith #999999 returns 404",
                      f"Got status_code: {response.get('status_code')}")

def test_automated_tashkeel_audit(results: TestResults):
    """Test 5: Automated Tashkeel Audit"""
    print("\n🔍 Testing Automated Tashkeel Audit")
    
    response = make_request("/audit/tashkeel")
    
    if "error" in response:
        results.assert_test(False, "Tashkeel audit", f"API Error: {response['error']}")
        return
        
    # Must be successful
    is_successful = response.get("success") == True
    results.assert_test(is_successful,
                      "Tashkeel audit successful",
                      f"Success: {response.get('success')}")
    
    # overall_status should contain "All texts properly diacritized"
    overall_status = response.get("overall_status", "")
    has_all_diacritized = "All texts properly diacritized" in overall_status
    results.assert_test(has_all_diacritized,
                      "Overall status shows all texts properly diacritized",
                      f"Status: {overall_status}")
    
    # needs_review should be 0
    needs_review = response.get("needs_review", -1)
    no_review_needed = needs_review == 0
    results.assert_test(no_review_needed,
                      "No texts need review (needs_review=0)",
                      f"needs_review: {needs_review}")

def test_full_audit_report(results: TestResults):
    """Test 6: Full Audit Report"""
    print("\n🔍 Testing Full Audit Report")
    
    response = make_request("/audit/full-report")
    
    if "error" in response:
        results.assert_test(False, "Full audit report", f"API Error: {response['error']}")
        return
        
    # Must be successful
    is_successful = response.get("success") == True
    results.assert_test(is_successful,
                      "Full audit report successful",
                      f"Success: {response.get('success')}")
    
    summary = response.get("summary", {})
    
    # summary.all_bukhari_muslim should be true
    all_bukhari_muslim = summary.get("all_bukhari_muslim") == True
    results.assert_test(all_bukhari_muslim,
                      "All hadiths from Bukhari/Muslim (all_bukhari_muslim=true)",
                      f"all_bukhari_muslim: {summary.get('all_bukhari_muslim')}")
    
    # summary.hadith_count should be 21
    hadith_count = summary.get("hadith_count")
    correct_count = hadith_count == 21
    results.assert_test(correct_count,
                      "Hadith count is 21",
                      f"hadith_count: {hadith_count}")

def test_source_verification(results: TestResults):
    """Test 7: Source Verification"""
    print("\n🔍 Testing Source Verification")
    
    response = make_request("/audit/full-report")
    
    if "error" in response:
        results.assert_test(False, "Source verification", f"API Error: {response['error']}")
        return
        
    summary = response.get("summary", {})
    hadith_sources = summary.get("hadith_sources", {})
    
    # Check that all sources are only from Bukhari or Muslim
    allowed_sources = ["صحيح البخاري", "صحيح مسلم", "صحيح البخاري ومسلم"]
    forbidden_sources = ["الترمذي", "النسائي"]
    
    all_sources_valid = True
    invalid_sources = []
    
    for source, count in hadith_sources.items():
        is_valid_source = any(allowed in source for allowed in allowed_sources)
        has_forbidden = any(forbidden in source for forbidden in forbidden_sources)
        
        if not is_valid_source or has_forbidden:
            all_sources_valid = False
            invalid_sources.append(f"{source} ({count} hadiths)")
    
    results.assert_test(all_sources_valid,
                      "All hadith sources are from Bukhari/Muslim only",
                      f"Invalid sources found: {invalid_sources}" if invalid_sources else "All sources valid")
    
    # Check forbidden sources check
    forbidden_check = response.get("forbidden_sources_check", {})
    is_clean = forbidden_check.get("clean") == True
    results.assert_test(is_clean,
                      "Forbidden sources check is clean",
                      f"Clean: {forbidden_check.get('clean')}")

def main():
    """Run all backend tests for Global Application Audit"""
    print("🚀 Starting Global Application Audit - Backend Testing")
    print(f"Backend URL: {BACKEND_URL}")
    
    results = TestResults()
    
    # Run all test suites
    test_language_integrity_tafsir_no_fallback(results)
    test_native_tafsir_languages_work(results)
    test_language_integrity_hadith(results)
    test_dorar_hadith_verification(results)
    test_automated_tashkeel_audit(results)
    test_full_audit_report(results)
    test_source_verification(results)
    
    # Print final summary
    success = results.summary()
    
    if success:
        print("\n🎉 ALL TESTS PASSED - Global Application Audit Complete!")
        sys.exit(0)
    else:
        print(f"\n💥 {results.failed} TESTS FAILED - Issues found in Global Application Audit")
        sys.exit(1)

if __name__ == "__main__":
    main()