#!/usr/bin/env python3
"""
V2026 EMERGENCY FIX Testing Suite
Tests for concise explanations and Ibn Kathir blocking
"""

import requests
import json
import sys
from typing import Dict, Any

# Base URL from frontend/.env
BASE_URL = "https://quran-rebuild-v2026.preview.emergentagent.com"

class QuranAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.results = []
        self.failed_tests = []
        
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
                "status_code": response.status_code
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
    
    def test_health_check(self):
        """Test 1: Health check"""
        print("\n=== HEALTH CHECK ===")
        result = self.make_request("/api/health")
        
        if result["success"]:
            self.log_result("Health Check", "PASS", "API is healthy")
        else:
            self.log_result("Health Check", "FAIL", f"Health check failed: {result['error']}")
    
    def test_ibn_kathir_blocked(self):
        """Test 2: Ibn Kathir BLOCKED - English should use Abdel Haleem"""
        print("\n=== IBN KATHIR BLOCKING TEST ===")
        result = self.make_request("/api/quran/v4/global-verse/2/255?language=en")
        
        if not result["success"]:
            self.log_result("Ibn Kathir Blocked", "FAIL", f"API request failed: {result['error']}")
            return
        
        data = result["data"]
        explanation = data.get("explanation", "")
        source = data.get("explanation_source", "")
        
        # Check if Ibn Kathir is mentioned anywhere
        if "ibn kathir" in explanation.lower() or "ibn kathir" in source.lower():
            self.log_result("Ibn Kathir Blocked", "FAIL", f"Ibn Kathir found! Source: {source}, Explanation: {explanation[:100]}...")
            return
        
        # Check if source is Abdel Haleem
        if "abdel haleem" not in source.lower():
            self.log_result("Ibn Kathir Blocked", "FAIL", f"Expected Abdel Haleem, got: {source}")
            return
        
        # Check explanation length
        if len(explanation) > 300:
            self.log_result("Ibn Kathir Blocked", "FAIL", f"Explanation too long: {len(explanation)} chars")
            return
        
        self.log_result("Ibn Kathir Blocked", "PASS", f"Source: {source}, Length: {len(explanation)} chars")
    
    def test_language_concise_explanations(self):
        """Test 3: All languages have concise explanations"""
        print("\n=== CONCISE EXPLANATIONS TEST ===")
        
        test_cases = [
            {"lang": "fr", "expected_source": "Fondation Islamique Montada"},
            {"lang": "de", "expected_source": "Abu Reda Muhammad ibn Ahmad"},
            {"lang": "tr", "expected_source": None},  # No specific source requirement
            {"lang": "ru", "expected_source": "Эльмир Кулиев"},
            {"lang": "nl", "expected_source": None}   # No specific source requirement
        ]
        
        for case in test_cases:
            lang = case["lang"]
            expected_source = case["expected_source"]
            
            result = self.make_request(f"/api/quran/v4/global-verse/2/255?language={lang}")
            
            if not result["success"]:
                self.log_result(f"Concise {lang.upper()}", "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            explanation = data.get("explanation", "")
            source = data.get("explanation_source", "")
            
            # Check explanation length
            if len(explanation) > 300:
                self.log_result(f"Concise {lang.upper()}", "FAIL", f"Explanation too long: {len(explanation)} chars")
                continue
            
            # Check expected source if specified
            if expected_source and expected_source.lower() not in source.lower():
                self.log_result(f"Concise {lang.upper()}", "FAIL", f"Expected '{expected_source}', got: {source}")
                continue
            
            # Special check for Russian - should NOT be As-Sa'di
            if lang == "ru" and "as-sa'di" in source.lower():
                self.log_result(f"Concise {lang.upper()}", "FAIL", f"Found As-Sa'di instead of Kuliev: {source}")
                continue
            
            self.log_result(f"Concise {lang.upper()}", "PASS", f"Source: {source}, Length: {len(explanation)} chars")
    
    def test_no_explanation_languages(self):
        """Test 4: Arabic/Swedish/Greek should have NO explanation"""
        print("\n=== NO EXPLANATION LANGUAGES TEST ===")
        
        no_explanation_langs = ["ar", "sv", "el"]
        
        for lang in no_explanation_langs:
            result = self.make_request(f"/api/quran/v4/global-verse/1/1?language={lang}")
            
            if not result["success"]:
                self.log_result(f"No Explanation {lang.upper()}", "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            explanation = data.get("explanation", "")
            
            if explanation and explanation.strip():
                self.log_result(f"No Explanation {lang.upper()}", "FAIL", f"Expected empty explanation, got: {explanation[:50]}...")
                continue
            
            self.log_result(f"No Explanation {lang.upper()}", "PASS", "Explanation is empty as expected")
    
    def test_short_verse_explanation(self):
        """Test 5: Short verse (Bismillah) should have short explanation"""
        print("\n=== SHORT VERSE TEST ===")
        result = self.make_request("/api/quran/v4/global-verse/1/1?language=en")
        
        if not result["success"]:
            self.log_result("Short Verse", "FAIL", f"API request failed: {result['error']}")
            return
        
        data = result["data"]
        explanation = data.get("explanation", "")
        
        if len(explanation) > 100:
            self.log_result("Short Verse", "FAIL", f"Bismillah explanation too long: {len(explanation)} chars")
            return
        
        self.log_result("Short Verse", "PASS", f"Bismillah explanation length: {len(explanation)} chars")
    
    def test_comprehensive_character_limits(self):
        """Test 6: Comprehensive character limit verification"""
        print("\n=== COMPREHENSIVE CHARACTER LIMITS TEST ===")
        
        # Test multiple verses with different languages
        test_verses = [
            {"verse": "2/255", "lang": "en"},  # Ayat Al-Kursi
            {"verse": "2/255", "lang": "fr"},
            {"verse": "2/255", "lang": "de"},
            {"verse": "2/255", "lang": "tr"},
            {"verse": "2/255", "lang": "ru"},
            {"verse": "2/255", "lang": "nl"},
            {"verse": "18/1", "lang": "en"},   # Another potentially long verse
            {"verse": "36/1", "lang": "en"},   # Ya-Sin
        ]
        
        for test_case in test_verses:
            verse = test_case["verse"]
            lang = test_case["lang"]
            
            result = self.make_request(f"/api/quran/v4/global-verse/{verse}?language={lang}")
            
            if not result["success"]:
                self.log_result(f"Char Limit {verse} {lang.upper()}", "FAIL", f"API request failed: {result['error']}")
                continue
            
            data = result["data"]
            explanation = data.get("explanation", "")
            
            if len(explanation) > 300:
                self.log_result(f"Char Limit {verse} {lang.upper()}", "FAIL", f"Explanation exceeds 300 chars: {len(explanation)}")
                continue
            
            self.log_result(f"Char Limit {verse} {lang.upper()}", "PASS", f"Length: {len(explanation)} chars")
    
    def run_all_tests(self):
        """Run all tests"""
        print("Starting V2026 EMERGENCY FIX Testing Suite...")
        print(f"Base URL: {self.base_url}")
        
        # Run all tests
        self.test_health_check()
        self.test_ibn_kathir_blocked()
        self.test_language_concise_explanations()
        self.test_no_explanation_languages()
        self.test_short_verse_explanation()
        self.test_comprehensive_character_limits()
        
        # Summary
        print("\n" + "="*50)
        print("TEST SUMMARY")
        print("="*50)
        
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
        
        return failed_tests == 0

if __name__ == "__main__":
    tester = QuranAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)