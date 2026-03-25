#!/usr/bin/env python3
"""
Digital Shield + Quran Tafsir Fallback Backend Testing
======================================================
Testing specific endpoints as requested in the review:

1. Digital Shield API Tests (NEW FEATURE)
   - Test 1.1: Digital Shield Overview for all 9 languages
   - Test 1.2: Digital Shield Individual Lessons
   - Test 1.3: Digital Shield Module Listing

2. Quran Tafsir Fallback Test — Top 10 Surahs
   - Test specific verse keys across all 9 languages
   - CRITICAL: Verify NO Arabic text for non-Arabic locales

Backend URL: https://code-cleanup-deploy.preview.emergentagent.com
All API routes have /api prefix
"""

import asyncio
import aiohttp
import json
import sys
import re
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://code-cleanup-deploy.preview.emergentagent.com"

# Test languages as specified in review request
ALL_LANGUAGES = ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"]

class DigitalShieldTester:
    def __init__(self):
        self.session = None
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def log_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            print(f"✅ {test_name}: {status}")
        else:
            self.failed_tests += 1
            print(f"❌ {test_name}: {status}")
            if details:
                print(f"   Details: {details}")
        
        self.results.append({
            "test": test_name,
            "status": status,
            "details": details
        })

    def has_arabic_text(self, text: str) -> bool:
        """Check if text contains Arabic characters (Unicode range 0x0600-0x06FF)"""
        if not text:
            return False
        return any('\u0600' <= char <= '\u06FF' for char in text)

    async def test_endpoint(self, endpoint: str, test_name: str = "") -> Dict[str, Any]:
        """Test a single endpoint"""
        try:
            url = f"{BACKEND_URL}/api{endpoint}"
            async with self.session.get(url) as response:
                if response.status != 200:
                    self.log_result(test_name, f"FAIL - HTTP {response.status}")
                    return {"status": "fail", "error": f"HTTP {response.status}"}
                
                try:
                    data = await response.json()
                except json.JSONDecodeError as e:
                    self.log_result(test_name, f"FAIL - Invalid JSON: {str(e)}")
                    return {"status": "fail", "error": f"Invalid JSON: {str(e)}"}
                
                self.log_result(test_name, "PASS")
                return {"status": "pass", "data": data}
                
        except Exception as e:
            self.log_result(test_name, f"FAIL - Exception: {str(e)}")
            return {"status": "fail", "error": str(e)}

    async def test_digital_shield_overview(self):
        """Test 1.1: Digital Shield Overview — All 9 Languages"""
        print("\n🔸 Test 1.1: Digital Shield Overview — All 9 Languages")
        print("=" * 80)
        
        for locale in ALL_LANGUAGES:
            endpoint = f"/digital-shield/overview?locale={locale}"
            test_name = f"Digital Shield Overview ({locale})"
            
            result = await self.test_endpoint(endpoint, test_name)
            
            if result["status"] == "pass":
                data = result["data"]
                
                # Verify success=true
                if not data.get("success", False):
                    self.log_result(f"{test_name} - Success Check", f"FAIL - success={data.get('success')}")
                    continue
                else:
                    self.log_result(f"{test_name} - Success Check", "PASS")
                
                # Verify 3 modules returned
                modules = data.get("modules", [])
                if len(modules) != 3:
                    self.log_result(f"{test_name} - Module Count", f"FAIL - Expected 3 modules, got {len(modules)}")
                    continue
                else:
                    self.log_result(f"{test_name} - Module Count", "PASS")
                
                # Verify total_lessons=30
                total_lessons = data.get("total_lessons", 0)
                if total_lessons != 30:
                    self.log_result(f"{test_name} - Total Lessons", f"FAIL - Expected 30 lessons, got {total_lessons}")
                    continue
                else:
                    self.log_result(f"{test_name} - Total Lessons", "PASS")
                
                # CRITICAL: For non-Arabic locales, verify NO Arabic text
                if locale != "ar":
                    arabic_found = False
                    arabic_locations = []
                    
                    # Check title and subtitle
                    if self.has_arabic_text(data.get("title", "")):
                        arabic_found = True
                        arabic_locations.append("title")
                    if self.has_arabic_text(data.get("subtitle", "")):
                        arabic_found = True
                        arabic_locations.append("subtitle")
                    
                    # Check module titles
                    for i, module in enumerate(modules):
                        if self.has_arabic_text(module.get("title", "")):
                            arabic_found = True
                            arabic_locations.append(f"module_{i+1}_title")
                        if self.has_arabic_text(module.get("description", "")):
                            arabic_found = True
                            arabic_locations.append(f"module_{i+1}_description")
                    
                    if arabic_found:
                        self.log_result(f"{test_name} - Arabic Text Check", f"FAIL - Arabic text found in: {', '.join(arabic_locations)}")
                    else:
                        self.log_result(f"{test_name} - Arabic Text Check", "PASS")
                
                # For Arabic locale, verify Arabic text IS present
                elif locale == "ar":
                    arabic_found = False
                    if self.has_arabic_text(data.get("title", "")) or any(self.has_arabic_text(m.get("title", "")) for m in modules):
                        arabic_found = True
                    
                    if arabic_found:
                        self.log_result(f"{test_name} - Arabic Text Present", "PASS")
                    else:
                        self.log_result(f"{test_name} - Arabic Text Present", "FAIL - No Arabic text found in Arabic locale")

    async def test_digital_shield_lessons(self):
        """Test 1.2: Digital Shield Individual Lessons"""
        print("\n🔸 Test 1.2: Digital Shield Individual Lessons")
        print("=" * 80)
        
        # Test cases as specified in review request
        test_cases = [
            (1, "en", "English lesson 1"),
            (15, "tr", "Turkish lesson 15"),
            (30, "ar", "Arabic lesson 30"),
            (99, "en", "Invalid lesson 99"),
            (1, "sv", "Swedish lesson 1"),
            (1, "el", "Greek lesson 1"),
        ]
        
        for lesson_id, locale, description in test_cases:
            endpoint = f"/digital-shield/lesson/{lesson_id}?locale={locale}"
            test_name = f"Digital Shield Lesson ({description})"
            
            result = await self.test_endpoint(endpoint, test_name)
            
            if result["status"] == "pass":
                data = result["data"]
                
                if lesson_id == 99:
                    # Invalid lesson should return success=false
                    if data.get("success", True):
                        self.log_result(f"{test_name} - Invalid Lesson Check", "FAIL - Expected success=false for invalid lesson")
                    else:
                        self.log_result(f"{test_name} - Invalid Lesson Check", "PASS")
                else:
                    # Valid lessons should return success=true
                    if not data.get("success", False):
                        self.log_result(f"{test_name} - Success Check", f"FAIL - success={data.get('success')}")
                        continue
                    else:
                        self.log_result(f"{test_name} - Success Check", "PASS")
                    
                    lesson = data.get("lesson", {})
                    
                    # Verify required fields
                    required_fields = ["title", "content", "islamic_reference", "moral"]
                    missing_fields = [field for field in required_fields if not lesson.get(field)]
                    
                    if missing_fields:
                        self.log_result(f"{test_name} - Required Fields", f"FAIL - Missing: {missing_fields}")
                        continue
                    else:
                        self.log_result(f"{test_name} - Required Fields", "PASS")
                    
                    # CRITICAL: For non-Arabic locales, verify NO Arabic text
                    if locale != "ar":
                        arabic_found = False
                        arabic_locations = []
                        
                        for field in required_fields:
                            if self.has_arabic_text(lesson.get(field, "")):
                                arabic_found = True
                                arabic_locations.append(field)
                        
                        if arabic_found:
                            self.log_result(f"{test_name} - Arabic Text Check", f"FAIL - Arabic text found in: {', '.join(arabic_locations)}")
                        else:
                            self.log_result(f"{test_name} - Arabic Text Check", "PASS")
                    
                    # For Arabic locale, verify Arabic text IS present
                    elif locale == "ar":
                        arabic_found = any(self.has_arabic_text(lesson.get(field, "")) for field in required_fields)
                        
                        if arabic_found:
                            self.log_result(f"{test_name} - Arabic Text Present", "PASS")
                        else:
                            self.log_result(f"{test_name} - Arabic Text Present", "FAIL - No Arabic text found in Arabic locale")

    async def test_digital_shield_modules(self):
        """Test 1.3: Digital Shield Module Listing"""
        print("\n🔸 Test 1.3: Digital Shield Module Listing")
        print("=" * 80)
        
        # Test cases as specified in review request
        test_cases = [
            (1, "en", "AI Safety module in English"),
            (2, "fr", "Digital Privacy module in French"),
            (3, "de", "Cyber-Ethics module in German"),
            (4, "en", "Invalid module 4"),
        ]
        
        for module_id, locale, description in test_cases:
            endpoint = f"/digital-shield/module/{module_id}?locale={locale}"
            test_name = f"Digital Shield Module ({description})"
            
            result = await self.test_endpoint(endpoint, test_name)
            
            if result["status"] == "pass":
                data = result["data"]
                
                if module_id == 4:
                    # Invalid module should return success=false
                    if data.get("success", True):
                        self.log_result(f"{test_name} - Invalid Module Check", "FAIL - Expected success=false for invalid module")
                    else:
                        self.log_result(f"{test_name} - Invalid Module Check", "PASS")
                else:
                    # Valid modules should return success=true
                    if not data.get("success", False):
                        self.log_result(f"{test_name} - Success Check", f"FAIL - success={data.get('success')}")
                        continue
                    else:
                        self.log_result(f"{test_name} - Success Check", "PASS")
                    
                    # Verify 10 lessons per module
                    lessons = data.get("lessons", [])
                    if len(lessons) != 10:
                        self.log_result(f"{test_name} - Lesson Count", f"FAIL - Expected 10 lessons, got {len(lessons)}")
                        continue
                    else:
                        self.log_result(f"{test_name} - Lesson Count", "PASS")
                    
                    # Verify module titles are properly localized
                    module_title = data.get("module", {}).get("title", "")
                    if not module_title:
                        self.log_result(f"{test_name} - Module Title", "FAIL - Module title is empty")
                        continue
                    
                    # CRITICAL: For non-Arabic locales, verify NO Arabic text in module title
                    if locale != "ar":
                        if self.has_arabic_text(module_title):
                            self.log_result(f"{test_name} - Arabic Text Check", f"FAIL - Arabic text found in module title: {module_title}")
                        else:
                            self.log_result(f"{test_name} - Arabic Text Check", "PASS")
                    
                    # Verify lesson titles are localized
                    arabic_found_in_lessons = False
                    for i, lesson in enumerate(lessons):
                        lesson_title = lesson.get("title", "")
                        if locale != "ar" and self.has_arabic_text(lesson_title):
                            arabic_found_in_lessons = True
                            break
                    
                    if locale != "ar" and arabic_found_in_lessons:
                        self.log_result(f"{test_name} - Lesson Titles Arabic Check", "FAIL - Arabic text found in lesson titles")
                    else:
                        self.log_result(f"{test_name} - Lesson Titles Arabic Check", "PASS")

    async def test_quran_tafsir_fallback(self):
        """Test 2: Quran Tafsir Fallback Test — Top 10 Surahs"""
        print("\n🔸 Test 2: Quran Tafsir Fallback Test — Top 10 Surahs")
        print("=" * 80)
        
        # Test verse keys as specified in review request
        verse_keys = [
            ("1:1", "Al-Fatiha first verse"),
            ("2:255", "Ayat Al-Kursi"),
            ("36:1", "Yasin first verse"),
        ]
        
        for verse_key, description in verse_keys:
            for locale in ALL_LANGUAGES:
                # Convert verse_key format from "1:1" to "/1/1"
                surah_id, ayah_id = verse_key.split(":")
                endpoint = f"/quran/v4/global-verse/{surah_id}/{ayah_id}?language={locale}"
                test_name = f"Quran Verse {verse_key} ({locale}) - {description}"
                
                result = await self.test_endpoint(endpoint, test_name)
                
                if result["status"] == "pass":
                    data = result["data"]
                    
                    # Verify translation text exists and is NOT empty
                    translation = data.get("text", "") or data.get("translation", "")
                    if not translation:
                        self.log_result(f"{test_name} - Translation Check", "FAIL - Translation text is empty")
                        continue
                    else:
                        self.log_result(f"{test_name} - Translation Check", "PASS")
                    
                    # CRITICAL: For non-Arabic locales, verify NO Arabic characters in translation and tafsir
                    if locale != "ar":
                        arabic_found = False
                        arabic_locations = []
                        
                        # Check translation text
                        if self.has_arabic_text(translation):
                            arabic_found = True
                            arabic_locations.append("translation")
                        
                        # Check tafsir text
                        tafsir = data.get("tafsir", "")
                        if tafsir and self.has_arabic_text(tafsir):
                            arabic_found = True
                            arabic_locations.append("tafsir")
                        
                        if arabic_found:
                            self.log_result(f"{test_name} - Arabic Text Check", f"FAIL - Arabic text found in: {', '.join(arabic_locations)}")
                        else:
                            self.log_result(f"{test_name} - Arabic Text Check", "PASS")
                    
                    # For Arabic locale, verify Arabic text IS present
                    elif locale == "ar":
                        if self.has_arabic_text(translation):
                            self.log_result(f"{test_name} - Arabic Text Present", "PASS")
                        else:
                            self.log_result(f"{test_name} - Arabic Text Present", "FAIL - No Arabic text found in Arabic locale")
                    
                    # Verify tafsir field exists (can be null, that's OK)
                    if "tafsir" not in data:
                        self.log_result(f"{test_name} - Tafsir Field", "FAIL - Tafsir field missing")
                    else:
                        self.log_result(f"{test_name} - Tafsir Field", "PASS")

    async def run_all_tests(self):
        """Run all Digital Shield and Quran Tafsir tests"""
        print("🚀 Starting Digital Shield + Quran Tafsir Backend Testing")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print("Testing Digital Shield API endpoints and Quran Tafsir fallback as per review request")
        print("=" * 80)
        
        # Run all test suites
        await self.test_digital_shield_overview()
        await self.test_digital_shield_lessons()
        await self.test_digital_shield_modules()
        await self.test_quran_tafsir_fallback()
        
        # Print summary
        print("\n" + "=" * 80)
        print("🏁 DIGITAL SHIELD + QURAN TAFSIR TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%" if self.total_tests > 0 else "0%")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if result["status"] != "PASS":
                    print(f"  - {result['test']}: {result['status']}")
                    if result["details"]:
                        print(f"    {result['details']}")
        
        print("\n" + "=" * 80)
        return self.failed_tests == 0

async def main():
    """Main test runner"""
    async with DigitalShieldTester() as tester:
        success = await tester.run_all_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())