#!/usr/bin/env python3
"""
Extended Kids Learn API Test - ALL 9 LANGUAGES
==============================================
Tests key Kids Learn API endpoints with ALL 9 languages as requested:
ar, en, de, fr, ru, tr, sv, nl, el

This test focuses on the core endpoints that should work with all languages.
"""

import requests
import json
import sys
from typing import Dict, List, Any
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://bug-fix-tools.preview.emergentagent.com"

# All 9 languages as requested
ALL_LANGUAGES = ["ar", "en", "de", "fr", "ru", "tr", "sv", "nl", "el"]

class ExtendedLanguageTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            print(f"✅ {test_name}: {details}")
        else:
            self.failed_tests += 1
            print(f"❌ {test_name}: {details}")
    
    def make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make HTTP request to API endpoint"""
        url = f"{BACKEND_URL}/api{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=30)
            return {
                "status_code": response.status_code,
                "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "headers": dict(response.headers)
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "data": {"error": str(e)},
                "headers": {}
            }
    
    def test_endpoint_all_languages(self, endpoint: str, endpoint_name: str, data_key: str):
        """Test an endpoint with all 9 languages"""
        print(f"\n🔍 Testing {endpoint_name} (All 9 Languages)...")
        
        for lang in ALL_LANGUAGES:
            response = self.make_request(endpoint, params={"locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"{endpoint_name} ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"{endpoint_name} ({lang})", "FAIL", 
                              f"success=false")
                continue
            
            items = data.get(data_key, [])
            
            if not items or len(items) == 0:
                self.log_result(f"{endpoint_name} ({lang})", "FAIL", 
                              f"Empty {data_key} array")
                continue
            
            self.log_result(f"{endpoint_name} ({lang})", "PASS", 
                          f"success=true, {len(items)} {data_key}")
    
    def run_extended_tests(self):
        """Run extended language tests"""
        print("🚀 Starting Extended Kids Learn API Test - ALL 9 LANGUAGES")
        print(f"🌐 Backend URL: {BACKEND_URL}")
        print(f"🗣️ Testing Languages: {', '.join(ALL_LANGUAGES)}")
        print("=" * 80)
        
        # Test key endpoints with all 9 languages
        self.test_endpoint_all_languages("/kids-learn/curriculum", "Curriculum", "stages")
        self.test_endpoint_all_languages("/kids-learn/duas", "Duas", "duas")
        self.test_endpoint_all_languages("/kids-learn/hadiths", "Hadiths", "hadiths")
        self.test_endpoint_all_languages("/kids-learn/prophets-full", "Prophets", "prophets")
        self.test_endpoint_all_languages("/kids-learn/islamic-pillars", "Islamic Pillars", "pillars")
        self.test_endpoint_all_languages("/kids-learn/wudu", "Wudu Steps", "steps")
        self.test_endpoint_all_languages("/kids-learn/salah", "Salah Steps", "steps")
        self.test_endpoint_all_languages("/kids-learn/library/categories", "Library Categories", "categories")
        self.test_endpoint_all_languages("/kids-learn/quran/surahs", "Quran Surahs", "surahs")
        
        # Test library items with all languages
        print(f"\n🔍 Testing Library Items (All 9 Languages)...")
        for lang in ALL_LANGUAGES:
            response = self.make_request("/kids-learn/library/items", params={"category": "all", "locale": lang})
            
            if response["status_code"] != 200:
                self.log_result(f"Library Items ({lang})", "FAIL", 
                              f"HTTP {response['status_code']}")
                continue
            
            data = response["data"]
            
            if not data.get("success"):
                self.log_result(f"Library Items ({lang})", "FAIL", 
                              f"success=false")
                continue
            
            items = data.get("items", [])
            
            if not items or len(items) == 0:
                self.log_result(f"Library Items ({lang})", "FAIL", 
                              f"Empty items array")
                continue
            
            self.log_result(f"Library Items ({lang})", "PASS", 
                          f"success=true, {len(items)} items")
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 EXTENDED LANGUAGE TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        # Show language breakdown
        print(f"\n🗣️ LANGUAGE BREAKDOWN:")
        for lang in ALL_LANGUAGES:
            lang_tests = [r for r in self.results if f"({lang})" in r["test"]]
            lang_passed = len([r for r in lang_tests if r["status"] == "PASS"])
            lang_total = len(lang_tests)
            if lang_total > 0:
                print(f"  {lang}: {lang_passed}/{lang_total} ({(lang_passed/lang_total*100):.1f}%)")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['details']}")
        
        # Save detailed results
        with open("/app/extended_language_test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_tests": self.total_tests,
                    "passed_tests": self.passed_tests,
                    "failed_tests": self.failed_tests,
                    "success_rate": round(self.passed_tests/self.total_tests*100, 1),
                    "test_date": datetime.now().isoformat(),
                    "backend_url": BACKEND_URL,
                    "languages_tested": ALL_LANGUAGES
                },
                "results": self.results
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: /app/extended_language_test_results.json")
        
        return self.failed_tests == 0

if __name__ == "__main__":
    tester = ExtendedLanguageTester()
    success = tester.run_extended_tests()
    sys.exit(0 if success else 1)