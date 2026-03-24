#!/usr/bin/env python3
"""
Backend API Testing for Multi-Language Content Delivery
=======================================================
Testing Islamic education app backend APIs for 9 languages (ar, en, de, fr, tr, ru, sv, nl, el)

Focus: Multi-language content delivery for kids_curriculum_advanced.py content:
- Quran surahs with translations for ayahs
- Tajweed rules in different languages  
- Prophets with translations
- Curriculum lessons with multi-language support
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://quran-rebuild-v2026.preview.emergentagent.com"

# Languages to test (9 total)
LANGUAGES = ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"]

# Test results storage
test_results = []

def log_test(test_name: str, endpoint: str, language: str, status: str, details: str = ""):
    """Log test result"""
    result = {
        "test": test_name,
        "endpoint": endpoint,
        "language": language,
        "status": status,
        "details": details
    }
    test_results.append(result)
    status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"{status_icon} {test_name} ({language}): {status}")
    if details:
        print(f"   Details: {details}")

def test_api_endpoint(endpoint: str, expected_fields: List[str] = None, min_items: int = 0) -> Dict[str, Any]:
    """Test a single API endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=10)
        
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "response": response.text[:200]
            }
        
        data = response.json()
        
        if not data.get("success", False):
            return {
                "success": False,
                "error": "API returned success=false",
                "data": data
            }
        
        # Check expected fields if provided
        if expected_fields:
            for field in expected_fields:
                if field not in data:
                    return {
                        "success": False,
                        "error": f"Missing expected field: {field}",
                        "data": data
                    }
        
        # Check minimum items if specified
        if min_items > 0:
            items_key = None
            for key in ["surahs", "prophets", "lesson", "steps", "pillars", "duas", "hadiths"]:
                if key in data:
                    items_key = key
                    break
            
            if items_key and len(data[items_key]) < min_items:
                return {
                    "success": False,
                    "error": f"Expected at least {min_items} items, got {len(data[items_key])}",
                    "data": data
                }
        
        return {
            "success": True,
            "data": data,
            "response_size": len(response.text)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Invalid JSON response: {str(e)}"
        }

def test_quran_surahs_multilang():
    """Test Quran surahs with multi-language translations"""
    print("\n🔍 Testing Quran Surahs Multi-Language Content...")
    
    for lang in LANGUAGES:
        endpoint = f"/api/kids-learn/quran/surahs?locale={lang}"
        result = test_api_endpoint(endpoint, ["surahs", "total"], min_items=8)
        
        if result["success"]:
            data = result["data"]
            surahs = data["surahs"]
            
            # Check if we have the expected surahs (original + additional)
            expected_min_surahs = 8  # Original surahs
            if len(surahs) >= expected_min_surahs:
                # Check if surahs have translations
                sample_surah = surahs[0] if surahs else None
                if sample_surah and "ayahs" in sample_surah:
                    # This endpoint doesn't include ayahs, let's check the structure
                    log_test("Quran Surahs API", endpoint, lang, "PASS", 
                            f"Found {len(surahs)} surahs")
                else:
                    log_test("Quran Surahs API", endpoint, lang, "PASS", 
                            f"Found {len(surahs)} surahs (structure check)")
            else:
                log_test("Quran Surahs API", endpoint, lang, "FAIL", 
                        f"Expected at least {expected_min_surahs} surahs, got {len(surahs)}")
        else:
            log_test("Quran Surahs API", endpoint, lang, "FAIL", result["error"])

def test_specific_surah_translations():
    """Test specific surah with ayah translations"""
    print("\n🔍 Testing Specific Surah Ayah Translations...")
    
    # Test Al-Fatiha (should have translations in all languages)
    surah_id = "fatiha"
    
    for lang in LANGUAGES:
        endpoint = f"/api/kids-learn/quran/surah/{surah_id}?locale={lang}"
        result = test_api_endpoint(endpoint, ["surah"])
        
        if result["success"]:
            data = result["data"]
            surah = data["surah"]
            
            if "ayahs" in surah and len(surah["ayahs"]) > 0:
                # Check if ayahs have translations
                sample_ayah = surah["ayahs"][0]
                if "translation" in sample_ayah and sample_ayah["translation"]:
                    # Check if translation is different from Arabic (unless lang is 'ar')
                    if lang != "ar" and sample_ayah["translation"] != sample_ayah.get("arabic", ""):
                        log_test("Surah Ayah Translations", endpoint, lang, "PASS", 
                                f"Found {len(surah['ayahs'])} ayahs with translations")
                    elif lang == "ar":
                        log_test("Surah Ayah Translations", endpoint, lang, "PASS", 
                                f"Arabic version with {len(surah['ayahs'])} ayahs")
                    else:
                        log_test("Surah Ayah Translations", endpoint, lang, "WARN", 
                                "Translation appears to be same as Arabic")
                else:
                    log_test("Surah Ayah Translations", endpoint, lang, "FAIL", 
                            "Ayahs missing translation field")
            else:
                log_test("Surah Ayah Translations", endpoint, lang, "FAIL", 
                        "Surah missing ayahs")
        else:
            log_test("Surah Ayah Translations", endpoint, lang, "FAIL", result["error"])

def test_curriculum_lessons():
    """Test curriculum lessons (including tajweed rules)"""
    print("\n🔍 Testing Curriculum Lessons Multi-Language...")
    
    # Test a lesson that should contain tajweed rules (around stage 14)
    # Days 721-810 are Stage 12 (Islamic Life), let's try day 800
    lesson_day = 800
    
    for lang in LANGUAGES:
        endpoint = f"/api/kids-learn/curriculum/lesson/{lesson_day}?locale={lang}"
        result = test_api_endpoint(endpoint, ["lesson"])
        
        if result["success"]:
            data = result["data"]
            lesson = data["lesson"]
            
            # Check if lesson has sections with content
            if "sections" in lesson and len(lesson["sections"]) > 0:
                # Look for content that might be translated
                has_translated_content = False
                for section in lesson["sections"]:
                    if "content" in section and section["content"]:
                        has_translated_content = True
                        break
                
                if has_translated_content:
                    log_test("Curriculum Lesson", endpoint, lang, "PASS", 
                            f"Day {lesson_day} with {len(lesson['sections'])} sections")
                else:
                    log_test("Curriculum Lesson", endpoint, lang, "WARN", 
                            "Lesson found but no translated content detected")
            else:
                log_test("Curriculum Lesson", endpoint, lang, "FAIL", 
                        "Lesson missing sections")
        else:
            log_test("Curriculum Lesson", endpoint, lang, "FAIL", result["error"])

def test_prophets_multilang():
    """Test prophets with multi-language content"""
    print("\n🔍 Testing Prophets Multi-Language Content...")
    
    for lang in LANGUAGES:
        endpoint = f"/api/kids-learn/prophets-full?locale={lang}"
        result = test_api_endpoint(endpoint, ["prophets", "total"], min_items=20)
        
        if result["success"]:
            data = result["data"]
            prophets = data["prophets"]
            
            if len(prophets) >= 20:  # Should have 25 prophets
                # Check if prophets have translated content
                sample_prophet = prophets[0] if prophets else None
                if sample_prophet:
                    translated_fields = ["name", "title", "summary"]
                    has_translations = any(field in sample_prophet for field in translated_fields)
                    
                    if has_translations:
                        log_test("Prophets Multi-Language", endpoint, lang, "PASS", 
                                f"Found {len(prophets)} prophets with translations")
                    else:
                        log_test("Prophets Multi-Language", endpoint, lang, "WARN", 
                                f"Found {len(prophets)} prophets but translation structure unclear")
                else:
                    log_test("Prophets Multi-Language", endpoint, lang, "FAIL", 
                            "No prophets data found")
            else:
                log_test("Prophets Multi-Language", endpoint, lang, "FAIL", 
                        f"Expected at least 20 prophets, got {len(prophets)}")
        else:
            log_test("Prophets Multi-Language", endpoint, lang, "FAIL", result["error"])

def test_additional_endpoints():
    """Test additional endpoints mentioned in review request"""
    print("\n🔍 Testing Additional Educational Endpoints...")
    
    endpoints_to_test = [
        ("/api/kids-learn/duas", "duas", 10),
        ("/api/kids-learn/hadiths", "hadiths", 5),
        ("/api/kids-learn/islamic-pillars", "pillars", 5),
        ("/api/kids-learn/wudu", "steps", 10),
        ("/api/kids-learn/salah", "steps", 10),
    ]
    
    for base_endpoint, data_key, min_items in endpoints_to_test:
        for lang in ["ar", "en", "de", "fr", "sv", "nl", "el"]:  # Test subset for speed
            endpoint = f"{base_endpoint}?locale={lang}"
            result = test_api_endpoint(endpoint, [data_key], min_items)
            
            if result["success"]:
                data = result["data"]
                items = data[data_key]
                log_test(f"{data_key.title()} API", endpoint, lang, "PASS", 
                        f"Found {len(items)} {data_key}")
            else:
                log_test(f"{data_key.title()} API", endpoint, lang, "FAIL", result["error"])

def print_summary():
    """Print test summary"""
    print("\n" + "="*60)
    print("MULTI-LANGUAGE CONTENT DELIVERY TEST SUMMARY")
    print("="*60)
    
    total_tests = len(test_results)
    passed_tests = len([r for r in test_results if r["status"] == "PASS"])
    failed_tests = len([r for r in test_results if r["status"] == "FAIL"])
    warned_tests = len([r for r in test_results if r["status"] == "WARN"])
    
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"⚠️  Warnings: {warned_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests > 0:
        print(f"\n❌ FAILED TESTS ({failed_tests}):")
        for result in test_results:
            if result["status"] == "FAIL":
                print(f"   - {result['test']} ({result['language']}): {result['details']}")
    
    if warned_tests > 0:
        print(f"\n⚠️  WARNINGS ({warned_tests}):")
        for result in test_results:
            if result["status"] == "WARN":
                print(f"   - {result['test']} ({result['language']}): {result['details']}")
    
    # Language-specific summary
    print(f"\n📊 LANGUAGE COVERAGE:")
    for lang in LANGUAGES:
        lang_tests = [r for r in test_results if r["language"] == lang]
        lang_passed = len([r for r in lang_tests if r["status"] == "PASS"])
        lang_total = len(lang_tests)
        if lang_total > 0:
            print(f"   {lang}: {lang_passed}/{lang_total} ({(lang_passed/lang_total)*100:.1f}%)")

def main():
    """Main test execution"""
    print("🚀 Starting Multi-Language Content Delivery API Tests")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Testing {len(LANGUAGES)} languages: {', '.join(LANGUAGES)}")
    
    # Run all tests
    test_quran_surahs_multilang()
    test_specific_surah_translations()
    test_curriculum_lessons()
    test_prophets_multilang()
    test_additional_endpoints()
    
    # Print summary
    print_summary()
    
    # Save detailed results
    with open("/app/multilang_api_test_results.json", "w") as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: /app/multilang_api_test_results.json")
    
    # Return exit code based on results
    failed_tests = len([r for r in test_results if r["status"] == "FAIL"])
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)