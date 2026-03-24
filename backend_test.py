#!/usr/bin/env python3
"""
V2026 Global Rebuild Backend Testing Suite
Tests critical scenarios for the Islamic app backend.
"""

import asyncio
import httpx
import json
import sys
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://quran-rebuild-v2026.preview.emergentagent.com"

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def add_result(self, test_name, passed, details="", expected="", actual=""):
        self.results.append({
            "test": test_name,
            "passed": passed,
            "details": details,
            "expected": expected,
            "actual": actual,
            "timestamp": datetime.now().isoformat()
        })
        if passed:
            self.passed += 1
            print(f"✅ {test_name}")
        else:
            self.failed += 1
            print(f"❌ {test_name}")
            if details:
                print(f"   Details: {details}")
            if expected and actual:
                print(f"   Expected: {expected}")
                print(f"   Actual: {actual}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY: {self.passed}/{total} passed")
        print(f"{'='*60}")
        return self.passed == total

async def test_quran_translation_ids():
    """Test CRITICAL Quran Translation IDs - French should be Hamidullah, Russian should be Abu Adel"""
    print("\n🔍 Testing Quran Translation IDs...")
    results = TestResults()
    
    async with httpx.AsyncClient(timeout=30) as client:
        # Test French translation (should be Hamidullah, NOT Montada)
        try:
            response = await client.get(f"{BACKEND_URL}/api/quran/v4/verses/by_chapter/1?language=fr&per_page=7")
            if response.status_code == 200:
                data = response.json()
                verses = data.get("verses", [])
                if verses and verses[0].get("translations"):
                    resource_id = verses[0]["translations"][0].get("resource_id", 0)
                    # Check if resource_id is 31 (Hamidullah) and NOT 136 (Montada)
                    is_hamidullah = resource_id == 31
                    is_montada = resource_id == 136
                    
                    if is_hamidullah and not is_montada:
                        results.add_result("French Translation ID (Hamidullah)", True, 
                                         f"Found resource_id: {resource_id} (Hamidullah)")
                    else:
                        results.add_result("French Translation ID (Hamidullah)", False,
                                         f"Expected resource_id 31 (Hamidullah), got: {resource_id}",
                                         "31 (Hamidullah)", str(resource_id))
                else:
                    results.add_result("French Translation ID (Hamidullah)", False,
                                     "No translations found in response")
            else:
                results.add_result("French Translation ID (Hamidullah)", False,
                                 f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            results.add_result("French Translation ID (Hamidullah)", False, f"Exception: {str(e)}")
        
        # Test Russian translation (should be Abu Adel, NOT Kuliev)
        try:
            response = await client.get(f"{BACKEND_URL}/api/quran/v4/verses/by_chapter/1?language=ru&per_page=7")
            if response.status_code == 200:
                data = response.json()
                verses = data.get("verses", [])
                if verses and verses[0].get("translations"):
                    resource_id = verses[0]["translations"][0].get("resource_id", 0)
                    # Check if resource_id is 79 (Abu Adel) and NOT 45 (Kuliev)
                    is_abu_adel = resource_id == 79
                    is_kuliev = resource_id == 45
                    
                    if is_abu_adel and not is_kuliev:
                        results.add_result("Russian Translation ID (Abu Adel)", True,
                                         f"Found resource_id: {resource_id} (Abu Adel)")
                    else:
                        results.add_result("Russian Translation ID (Abu Adel)", False,
                                         f"Expected resource_id 79 (Abu Adel), got: {resource_id}",
                                         "79 (Abu Adel)", str(resource_id))
                else:
                    results.add_result("Russian Translation ID (Abu Adel)", False,
                                     "No translations found in response")
            else:
                results.add_result("Russian Translation ID (Abu Adel)", False,
                                 f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            results.add_result("Russian Translation ID (Abu Adel)", False, f"Exception: {str(e)}")
    
    return results

async def test_tafsir_no_translation_pending():
    """Test Tafsir endpoints - All languages should return pending=false with actual text"""
    print("\n🔍 Testing Tafsir - No Translation Pending...")
    results = TestResults()
    
    languages = ["fr", "de", "tr", "ru", "el", "nl", "sv"]
    
    async with httpx.AsyncClient(timeout=30) as client:
        for lang in languages:
            try:
                response = await client.get(f"{BACKEND_URL}/api/quran/v4/tafsir/1:1?language={lang}")
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check translation_pending is false
                    translation_pending = data.get("translation_pending", True)
                    has_text = bool(data.get("text", "").strip())
                    tafsir_name = data.get("tafsir_name", "")
                    
                    if not translation_pending and has_text:
                        # Additional check: tafsir_name should be localized (not just "Ibn Kathir" for non-English)
                        if lang != "en" and tafsir_name == "Ibn Kathir":
                            results.add_result(f"Tafsir {lang.upper()} - Localized Name", False,
                                             f"Tafsir name not localized: {tafsir_name}",
                                             "Localized tafsir name", "Ibn Kathir")
                        else:
                            results.add_result(f"Tafsir {lang.upper()} - No Pending", True,
                                             f"Text length: {len(data.get('text', ''))}, Name: {tafsir_name}")
                    else:
                        results.add_result(f"Tafsir {lang.upper()} - No Pending", False,
                                         f"pending={translation_pending}, has_text={has_text}",
                                         "pending=false, has_text=true", 
                                         f"pending={translation_pending}, has_text={has_text}")
                else:
                    results.add_result(f"Tafsir {lang.upper()} - No Pending", False,
                                     f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                results.add_result(f"Tafsir {lang.upper()} - No Pending", False, f"Exception: {str(e)}")
    
    return results

async def test_daily_hadith_no_translation_pending():
    """Test Daily Hadith endpoints - All languages should return translation_pending=false"""
    print("\n🔍 Testing Daily Hadith - No Translation Pending...")
    results = TestResults()
    
    languages = ["fr", "de", "el"]  # Test subset of languages
    
    async with httpx.AsyncClient(timeout=30) as client:
        for lang in languages:
            try:
                response = await client.get(f"{BACKEND_URL}/api/daily-hadith?language={lang}")
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        hadith = data.get("hadith", {})
                        translation_pending = hadith.get("translation_pending", True)
                        has_text = bool(hadith.get("text", "").strip())
                        
                        if not translation_pending and has_text:
                            results.add_result(f"Daily Hadith {lang.upper()} - No Pending", True,
                                             f"Text length: {len(hadith.get('text', ''))}")
                        else:
                            results.add_result(f"Daily Hadith {lang.upper()} - No Pending", False,
                                             f"pending={translation_pending}, has_text={has_text}",
                                             "pending=false, has_text=true",
                                             f"pending={translation_pending}, has_text={has_text}")
                    else:
                        results.add_result(f"Daily Hadith {lang.upper()} - No Pending", False,
                                         "API returned success=false")
                else:
                    results.add_result(f"Daily Hadith {lang.upper()} - No Pending", False,
                                     f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                results.add_result(f"Daily Hadith {lang.upper()} - No Pending", False, f"Exception: {str(e)}")
    
    return results

async def test_system_info():
    """Test System Info endpoint - Should show v2026 info with no pending languages"""
    print("\n🔍 Testing System Info...")
    results = TestResults()
    
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.get(f"{BACKEND_URL}/api/")
            if response.status_code == 200:
                data = response.json()
                
                # Check if it mentions v2026 or similar version info
                data_str = json.dumps(data).lower()
                has_version_info = "v2026" in data_str or "2026" in data_str or "rebuild" in data_str or "3.0" in data_str
                
                results.add_result("System Info - V2026", has_version_info,
                                 f"Response contains version info: {has_version_info}, Version: {data.get('version', 'N/A')}")
                
                # Check for no pending languages mentioned
                has_pending = "pending" in data_str or "traduction en cours" in data_str
                results.add_result("System Info - No Pending Languages", not has_pending,
                                 f"No pending language mentions: {not has_pending}")
            else:
                results.add_result("System Info - V2026", False,
                                 f"HTTP {response.status_code}: {response.text}")
                results.add_result("System Info - No Pending Languages", False,
                                 f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            results.add_result("System Info - V2026", False, f"Exception: {str(e)}")
            results.add_result("System Info - No Pending Languages", False, f"Exception: {str(e)}")
    
    return results

async def test_comprehensive_language_coverage():
    """Test comprehensive language coverage across all endpoints"""
    print("\n🔍 Testing Comprehensive Language Coverage...")
    results = TestResults()
    
    languages = ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"]
    
    async with httpx.AsyncClient(timeout=30) as client:
        # Test basic API health
        try:
            response = await client.get(f"{BACKEND_URL}/api/health")
            if response.status_code == 200:
                results.add_result("API Health Check", True, "Backend is responding")
            else:
                results.add_result("API Health Check", False, f"HTTP {response.status_code}")
        except Exception as e:
            results.add_result("API Health Check", False, f"Exception: {str(e)}")
        
        # Test chapters endpoint for different languages
        for lang in ["ar", "en", "fr", "de"]:  # Test subset
            try:
                response = await client.get(f"{BACKEND_URL}/api/quran/v4/chapters?language={lang}")
                if response.status_code == 200:
                    data = response.json()
                    chapters = data.get("chapters", [])
                    if chapters:
                        results.add_result(f"Chapters API - {lang.upper()}", True,
                                         f"Found {len(chapters)} chapters")
                    else:
                        results.add_result(f"Chapters API - {lang.upper()}", False,
                                         "No chapters found")
                else:
                    results.add_result(f"Chapters API - {lang.upper()}", False,
                                     f"HTTP {response.status_code}")
            except Exception as e:
                results.add_result(f"Chapters API - {lang.upper()}", False, f"Exception: {str(e)}")
    
    return results

async def main():
    """Run all tests"""
    print("🚀 Starting V2026 Global Rebuild Backend Tests")
    print(f"Backend URL: {BACKEND_URL}")
    print("="*60)
    
    all_results = []
    
    # Run all test suites
    test_suites = [
        test_quran_translation_ids,
        test_tafsir_no_translation_pending,
        test_daily_hadith_no_translation_pending,
        test_system_info,
        test_comprehensive_language_coverage
    ]
    
    for test_suite in test_suites:
        try:
            result = await test_suite()
            all_results.append(result)
        except Exception as e:
            print(f"❌ Test suite {test_suite.__name__} failed with exception: {str(e)}")
    
    # Aggregate results
    total_passed = sum(r.passed for r in all_results)
    total_failed = sum(r.failed for r in all_results)
    total_tests = total_passed + total_failed
    
    print(f"\n{'='*60}")
    print(f"FINAL RESULTS: {total_passed}/{total_tests} tests passed")
    print(f"{'='*60}")
    
    # Print failed tests summary
    if total_failed > 0:
        print("\n❌ FAILED TESTS:")
        for result_set in all_results:
            for result in result_set.results:
                if not result["passed"]:
                    print(f"  - {result['test']}: {result['details']}")
    
    # Print critical issues
    critical_issues = []
    for result_set in all_results:
        for result in result_set.results:
            if not result["passed"] and any(keyword in result["test"].lower() 
                                          for keyword in ["translation id", "pending", "hamidullah", "abu adel"]):
                critical_issues.append(result["test"])
    
    if critical_issues:
        print(f"\n🚨 CRITICAL ISSUES FOUND:")
        for issue in critical_issues:
            print(f"  - {issue}")
    
    return total_failed == 0

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)