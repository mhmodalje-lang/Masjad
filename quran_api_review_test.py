#!/usr/bin/env python3
"""
Quran API Review Request Testing
===============================
CRITICAL: Each language must show ONLY its own language. NO Arabic text should appear for non-Arabic users.

Testing 12 specific scenarios:
1. ARABIC bulk - GET /api/quran/v4/global-verse/bulk/1?language=ar&from_ayah=1&to_ayah=7
2. TURKISH bulk - GET /api/quran/v4/global-verse/bulk/1?language=tr&from_ayah=1&to_ayah=7
3. RUSSIAN bulk - GET /api/quran/v4/global-verse/bulk/1?language=ru&from_ayah=1&to_ayah=7
4. ENGLISH bulk - GET /api/quran/v4/global-verse/bulk/1?language=en&from_ayah=1&to_ayah=7
5. FRENCH bulk - GET /api/quran/v4/global-verse/bulk/1?language=fr&from_ayah=1&to_ayah=7
6. GERMAN bulk - GET /api/quran/v4/global-verse/bulk/1?language=de&from_ayah=1&to_ayah=7
7. Single verse + tafsir ENGLISH - GET /api/quran/v4/global-verse/2/255?language=en
8. Single verse + tafsir RUSSIAN - GET /api/quran/v4/global-verse/2/255?language=ru
9. Single verse + tafsir FRENCH - GET /api/quran/v4/global-verse/1/2?language=fr
10. Single verse TURKISH - GET /api/quran/v4/global-verse/2/255?language=tr
11. Single verse SWEDISH - GET /api/quran/v4/global-verse/1/1?language=sv
12. Single verse DUTCH - GET /api/quran/v4/global-verse/1/1?language=nl

Backend URL: https://maintain-momentum.preview.emergentagent.com
"""

import asyncio
import aiohttp
import json
import sys
import re
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://maintain-momentum.preview.emergentagent.com"

class QuranAPIReviewTester:
    def __init__(self):
        self.session = None
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.critical_failures = []

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def has_arabic_text(self, text: str) -> bool:
        """Check if text contains Arabic characters (Unicode range 0600-06FF)"""
        if not text:
            return False
        return bool(re.search(r'[\u0600-\u06FF]', text))

    def log_result(self, test_name: str, status: str, details: str = "", is_critical: bool = False):
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
            if is_critical:
                self.critical_failures.append(f"{test_name}: {status} - {details}")
        
        self.results.append({
            "test": test_name,
            "status": status,
            "details": details,
            "critical": is_critical
        })

    async def test_endpoint(self, endpoint: str, test_name: str = "") -> Dict[str, Any]:
        """Test a single endpoint"""
        try:
            url = f"{BACKEND_URL}/api{endpoint}"
            print(f"🔍 Testing: {url}")
            
            async with self.session.get(url) as response:
                if response.status != 200:
                    self.log_result(test_name, f"FAIL - HTTP {response.status}", is_critical=True)
                    return {"status": "fail", "error": f"HTTP {response.status}"}
                
                try:
                    data = await response.json()
                except json.JSONDecodeError as e:
                    self.log_result(test_name, f"FAIL - Invalid JSON: {str(e)}", is_critical=True)
                    return {"status": "fail", "error": f"Invalid JSON: {str(e)}"}
                
                return {"status": "pass", "data": data}
                
        except Exception as e:
            self.log_result(test_name, f"FAIL - Exception: {str(e)}", is_critical=True)
            return {"status": "fail", "error": str(e)}

    async def test_bulk_verses_scenario(self, language: str, language_name: str, scenario_num: int):
        """Test bulk verses for a specific language"""
        print(f"\n🔸 Scenario {scenario_num}: {language_name.upper()} bulk verses")
        print("=" * 60)
        
        endpoint = f"/quran/v4/global-verse/bulk/1?language={language}&from_ayah=1&to_ayah=7"
        test_name = f"Scenario {scenario_num} - {language_name} bulk (1:1-7)"
        
        result = await self.test_endpoint(endpoint, test_name)
        
        if result["status"] == "pass":
            data = result["data"]
            verses = data.get("verses", [])
            
            # Check verse count
            if len(verses) != 7:
                self.log_result(f"{test_name} - Verse Count", f"FAIL - Expected 7 verses, got {len(verses)}", is_critical=True)
                return
            else:
                self.log_result(f"{test_name} - Verse Count", "PASS")
            
            # Check each verse
            for i, verse in enumerate(verses, 1):
                verse_text = verse.get("text", "")
                
                # Critical check: Verify text is not empty
                if not verse_text:
                    self.log_result(f"{test_name} - Verse {i} Text", "FAIL - Text is empty", is_critical=True)
                    continue
                
                # Critical check: For non-Arabic languages, verify NO Arabic text
                if language != "ar":
                    if self.has_arabic_text(verse_text):
                        self.log_result(f"{test_name} - Verse {i} Language Purity", 
                                      f"CRITICAL FAIL - Arabic text found in {language_name}: {verse_text[:50]}...", 
                                      is_critical=True)
                    else:
                        self.log_result(f"{test_name} - Verse {i} Language Purity", "PASS")
                else:
                    # For Arabic, verify it DOES contain Arabic text
                    if self.has_arabic_text(verse_text):
                        self.log_result(f"{test_name} - Verse {i} Arabic Text", "PASS")
                    else:
                        self.log_result(f"{test_name} - Verse {i} Arabic Text", 
                                      f"FAIL - Expected Arabic text, got: {verse_text[:50]}...", 
                                      is_critical=True)
            
            # Language-specific content verification
            if verses:
                first_verse_text = verses[0].get("text", "")
                self.verify_language_specific_content(first_verse_text, language, language_name, f"{test_name} - Content Verification")

    async def test_single_verse_scenario(self, language: str, language_name: str, surah: int, ayah: int, scenario_num: int, expect_tafsir: bool = False):
        """Test single verse for a specific language"""
        print(f"\n🔸 Scenario {scenario_num}: {language_name.upper()} single verse ({surah}:{ayah})")
        print("=" * 60)
        
        endpoint = f"/quran/v4/global-verse/{surah}/{ayah}?language={language}"
        test_name = f"Scenario {scenario_num} - {language_name} single verse ({surah}:{ayah})"
        
        result = await self.test_endpoint(endpoint, test_name)
        
        if result["status"] == "pass":
            data = result["data"]
            
            # Check required fields
            text = data.get("text", "")
            if not text:
                self.log_result(f"{test_name} - Text Field", "FAIL - Text is empty", is_critical=True)
                return
            else:
                self.log_result(f"{test_name} - Text Field", "PASS")
            
            # Critical check: For non-Arabic languages, verify NO Arabic text
            if language != "ar":
                if self.has_arabic_text(text):
                    self.log_result(f"{test_name} - Language Purity", 
                                  f"CRITICAL FAIL - Arabic text found in {language_name}: {text[:50]}...", 
                                  is_critical=True)
                else:
                    self.log_result(f"{test_name} - Language Purity", "PASS")
            else:
                # For Arabic, verify it DOES contain Arabic text
                if self.has_arabic_text(text):
                    self.log_result(f"{test_name} - Arabic Text", "PASS")
                else:
                    self.log_result(f"{test_name} - Arabic Text", 
                                  f"FAIL - Expected Arabic text, got: {text[:50]}...", 
                                  is_critical=True)
            
            # Check tafsir if expected
            if expect_tafsir:
                tafsir = data.get("tafsir", "")
                tafsir_source = data.get("tafsir_source", "")
                
                if not tafsir:
                    self.log_result(f"{test_name} - Tafsir Content", "FAIL - Tafsir is empty")
                else:
                    self.log_result(f"{test_name} - Tafsir Content", "PASS")
                
                if not tafsir_source:
                    self.log_result(f"{test_name} - Tafsir Source", "FAIL - Tafsir source is empty")
                else:
                    self.log_result(f"{test_name} - Tafsir Source", "PASS")
                    
                    # Specific tafsir source checks
                    if language == "en" and "Ibn Kathir" in tafsir_source:
                        self.log_result(f"{test_name} - Ibn Kathir Source", "PASS")
                    elif language == "ru" and "As-Sa'di" in tafsir_source:
                        self.log_result(f"{test_name} - As-Sa'di Source", "PASS")
                    elif language == "fr" and "QuranEnc" in tafsir_source:
                        self.log_result(f"{test_name} - QuranEnc Source", "PASS")
            
            # Language-specific content verification
            self.verify_language_specific_content(text, language, language_name, f"{test_name} - Content Verification")

    def verify_language_specific_content(self, text: str, language: str, language_name: str, test_name: str):
        """Verify language-specific content characteristics"""
        if not text:
            return
        
        text_lower = text.lower()
        
        # Language-specific indicators
        language_indicators = {
            "ar": ["بسم", "الله", "الرحمن", "الرحيم"],
            "tr": ["bismillâh", "rahman", "rahim", "allah", "hamd"],
            "en": ["in the name", "allah", "most gracious", "most merciful", "praise"],
            "fr": ["au nom", "allah", "louange", "seigneur", "miséricordieux"],
            "de": ["im namen", "allah", "barmherzige", "gnädige", "lob"],
            "ru": ["именем", "аллаха", "милостивого", "милосердного", "хвала"],
            "sv": ["i guds namn", "allah", "nådig", "barmhärtig"],
            "nl": ["in de naam", "allah", "genadige", "barmhartige", "lof"]
        }
        
        if language in language_indicators:
            indicators = language_indicators[language]
            has_indicators = any(indicator in text_lower for indicator in indicators)
            
            if has_indicators:
                self.log_result(f"{test_name}", "PASS")
            else:
                # For some languages, transliteration is acceptable
                if language in ["tr", "sv", "nl"] and ("bismillah" in text_lower or "allah" in text_lower):
                    self.log_result(f"{test_name}", "PASS")
                else:
                    self.log_result(f"{test_name}", f"WARN - May not be authentic {language_name}: {text[:50]}...")

    async def run_all_review_scenarios(self):
        """Run all 12 scenarios from the review request"""
        print("🚀 Starting Quran API Review Request Testing")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print("CRITICAL: Testing that each language shows ONLY its own language")
        print("NO Arabic text should appear for non-Arabic users")
        print("=" * 80)
        
        # Scenarios 1-6: Bulk verses
        await self.test_bulk_verses_scenario("ar", "Arabic", 1)
        await self.test_bulk_verses_scenario("tr", "Turkish", 2)
        await self.test_bulk_verses_scenario("ru", "Russian", 3)
        await self.test_bulk_verses_scenario("en", "English", 4)
        await self.test_bulk_verses_scenario("fr", "French", 5)
        await self.test_bulk_verses_scenario("de", "German", 6)
        
        # Scenarios 7-12: Single verses
        await self.test_single_verse_scenario("en", "English", 2, 255, 7, expect_tafsir=True)
        await self.test_single_verse_scenario("ru", "Russian", 2, 255, 8, expect_tafsir=True)
        await self.test_single_verse_scenario("fr", "French", 1, 2, 9, expect_tafsir=True)
        await self.test_single_verse_scenario("tr", "Turkish", 2, 255, 10)
        await self.test_single_verse_scenario("sv", "Swedish", 1, 1, 11)
        await self.test_single_verse_scenario("nl", "Dutch", 1, 1, 12)
        
        # Print summary
        print("\n" + "=" * 80)
        print("🏁 QURAN API REVIEW TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%" if self.total_tests > 0 else "0%")
        
        # Critical failures
        if self.critical_failures:
            print(f"\n🚨 CRITICAL FAILURES ({len(self.critical_failures)}):")
            for failure in self.critical_failures:
                print(f"  - {failure}")
        
        # All failures
        if self.failed_tests > 0:
            print(f"\n❌ ALL FAILED TESTS ({self.failed_tests}):")
            for result in self.results:
                if result["status"] != "PASS":
                    print(f"  - {result['test']}: {result['status']}")
                    if result["details"]:
                        print(f"    {result['details']}")
        
        print("\n" + "=" * 80)
        
        # Return success status
        return len(self.critical_failures) == 0

async def main():
    """Main test runner"""
    async with QuranAPIReviewTester() as tester:
        success = await tester.run_all_review_scenarios()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())