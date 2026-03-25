#!/usr/bin/env python3
"""
Quran API Backend Testing for Review Request
============================================
Testing specific Quran API endpoints as requested:

1. Surah List (chapters) in Arabic, Turkish, English
2. Bulk Verses with Turkish, French, German, English, Russian translations
3. Single Verse with Tafsir in Turkish, French, English, Arabic

Backend URL: https://quran-engine-1.preview.emergentagent.com
All API routes have /api prefix
"""

import asyncio
import aiohttp
import json
import sys
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://quran-engine-1.preview.emergentagent.com"

class QuranAPITester:
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

    async def test_surah_chapters(self):
        """Test Surah List (chapters) endpoints"""
        print("\n🔸 Testing Surah List (Chapters)")
        print("=" * 60)
        
        languages = ["ar", "tr", "en"]
        
        for lang in languages:
            endpoint = f"/quran/v4/chapters?language={lang}"
            test_name = f"Chapters List ({lang})"
            
            result = await self.test_endpoint(endpoint, test_name)
            
            if result["status"] == "pass":
                data = result["data"]
                chapters = data.get("chapters", [])
                
                # Verify we have 114 chapters
                if len(chapters) != 114:
                    self.log_result(f"{test_name} - Count Check", f"FAIL - Expected 114 chapters, got {len(chapters)}")
                else:
                    self.log_result(f"{test_name} - Count Check", "PASS")
                
                # Verify chapter structure
                if chapters:
                    sample_chapter = chapters[0]
                    required_fields = ["id", "name_arabic", "name_simple", "revelation_place", "verses_count"]
                    missing_fields = [field for field in required_fields if field not in sample_chapter]
                    
                    if missing_fields:
                        self.log_result(f"{test_name} - Structure Check", f"FAIL - Missing fields: {missing_fields}")
                    else:
                        self.log_result(f"{test_name} - Structure Check", "PASS")

    async def test_bulk_verses(self):
        """Test Bulk Verses with different language translations"""
        print("\n🔸 Testing Bulk Verses with Translations")
        print("=" * 60)
        
        # Test languages as specified in review request
        test_cases = [
            ("tr", "Turkish"),
            ("fr", "French"), 
            ("de", "German"),
            ("en", "English"),
            ("ru", "Russian")
        ]
        
        for lang_code, lang_name in test_cases:
            endpoint = f"/quran/v4/global-verse/bulk/1?language={lang_code}&from_ayah=1&to_ayah=7"
            test_name = f"Bulk Verses - Surah 1:1-7 ({lang_name})"
            
            result = await self.test_endpoint(endpoint, test_name)
            
            if result["status"] == "pass":
                data = result["data"]
                verses = data.get("verses", [])
                
                # Verify we have 7 verses
                if len(verses) != 7:
                    self.log_result(f"{test_name} - Count Check", f"FAIL - Expected 7 verses, got {len(verses)}")
                else:
                    self.log_result(f"{test_name} - Count Check", "PASS")
                
                # Verify verse structure
                if verses:
                    sample_verse = verses[0]
                    required_fields = ["arabic_text", "translation"]
                    missing_fields = [field for field in required_fields if field not in sample_verse]
                    
                    if missing_fields:
                        self.log_result(f"{test_name} - Structure Check", f"FAIL - Missing fields: {missing_fields}")
                    else:
                        self.log_result(f"{test_name} - Structure Check", "PASS")
                    
                    # Verify translation is not empty and not Arabic for non-Arabic languages
                    translation = sample_verse.get("translation", "")
                    if not translation:
                        self.log_result(f"{test_name} - Translation Check", "FAIL - Translation is empty")
                    elif lang_code != "ar":
                        # Check if translation contains Arabic characters (should not for non-Arabic languages)
                        has_arabic = any('\u0600' <= char <= '\u06FF' for char in translation)
                        if has_arabic and lang_code in ["tr", "fr", "de", "en", "ru"]:
                            self.log_result(f"{test_name} - Translation Language Check", f"WARN - Translation may contain Arabic text: {translation[:50]}...")
                        else:
                            self.log_result(f"{test_name} - Translation Check", "PASS")
                    else:
                        self.log_result(f"{test_name} - Translation Check", "PASS")

    async def test_single_verse_with_tafsir(self):
        """Test Single Verse with Tafsir in different languages"""
        print("\n🔸 Testing Single Verse with Tafsir")
        print("=" * 60)
        
        # Test cases as specified in review request
        test_cases = [
            ("tr", "1/1", "Turkish - Surah 1:1"),
            ("fr", "1/2", "French - Surah 1:2"),
            ("en", "2/255", "English - Ayat al-Kursi"),
            ("ar", "2/255", "Arabic - Ayat al-Kursi")
        ]
        
        for lang_code, verse_ref, description in test_cases:
            endpoint = f"/quran/v4/global-verse/{verse_ref}?language={lang_code}"
            test_name = f"Single Verse with Tafsir ({description})"
            
            result = await self.test_endpoint(endpoint, test_name)
            
            if result["status"] == "pass":
                data = result["data"]
                
                # Verify required fields
                required_fields = ["arabic_text", "translation", "tafsir", "tafsir_source", "tafsir_is_arabic", "surah_name", "audio_url"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_result(f"{test_name} - Structure Check", f"FAIL - Missing fields: {missing_fields}")
                else:
                    self.log_result(f"{test_name} - Structure Check", "PASS")
                
                # Verify tafsir content
                tafsir = data.get("tafsir", "")
                tafsir_source = data.get("tafsir_source", "")
                tafsir_is_arabic = data.get("tafsir_is_arabic", False)
                
                if not tafsir:
                    self.log_result(f"{test_name} - Tafsir Content Check", "FAIL - Tafsir is empty")
                else:
                    self.log_result(f"{test_name} - Tafsir Content Check", "PASS")
                
                if not tafsir_source:
                    self.log_result(f"{test_name} - Tafsir Source Check", "FAIL - Tafsir source is empty")
                else:
                    self.log_result(f"{test_name} - Tafsir Source Check", "PASS")
                
                # Specific checks based on language
                if lang_code == "fr" and tafsir:
                    # French should have native footnotes (tafsir_is_arabic should be False)
                    if tafsir_is_arabic:
                        self.log_result(f"{test_name} - French Native Footnotes Check", "FAIL - Expected French footnotes, got Arabic tafsir")
                    else:
                        self.log_result(f"{test_name} - French Native Footnotes Check", "PASS")
                
                elif lang_code == "en" and tafsir_source:
                    # English should have Ibn Kathir
                    if "Ibn Kathir" in tafsir_source:
                        self.log_result(f"{test_name} - Ibn Kathir Source Check", "PASS")
                    else:
                        self.log_result(f"{test_name} - Ibn Kathir Source Check", f"FAIL - Expected Ibn Kathir, got: {tafsir_source}")
                
                elif lang_code == "ar" and tafsir_source:
                    # Arabic should have التفسير الميسر
                    if "التفسير الميسر" in tafsir_source:
                        self.log_result(f"{test_name} - Arabic Tafsir Source Check", "PASS")
                    else:
                        self.log_result(f"{test_name} - Arabic Tafsir Source Check", f"FAIL - Expected التفسير الميسر, got: {tafsir_source}")
                
                # Verify translation language authenticity
                translation = data.get("translation", "")
                if translation and lang_code != "ar":
                    # For Turkish and French, verify it's not English
                    if lang_code == "tr":
                        # Special case: Bismillah is often transliterated, not translated
                        if "bismillâh" in translation.lower() or "bismillah" in translation.lower():
                            self.log_result(f"{test_name} - Turkish Translation Authenticity", "PASS")
                        else:
                            # Basic check - Turkish should not look like English
                            english_words = ["the", "and", "of", "to", "in", "is", "that", "for", "with", "as"]
                            has_english_words = any(word.lower() in translation.lower() for word in english_words)
                            if has_english_words:
                                self.log_result(f"{test_name} - Turkish Translation Authenticity", f"WARN - Translation may be English: {translation[:50]}...")
                            else:
                                self.log_result(f"{test_name} - Turkish Translation Authenticity", "PASS")
                    
                    elif lang_code == "fr":
                        # Basic check - French should not look like English
                        french_indicators = ["le", "la", "les", "de", "du", "des", "et", "à", "dans", "pour", "louange", "allah", "seigneur"]
                        has_french_indicators = any(word.lower() in translation.lower() for word in french_indicators)
                        if not has_french_indicators:
                            self.log_result(f"{test_name} - French Translation Authenticity", f"WARN - Translation may not be French: {translation[:50]}...")
                        else:
                            self.log_result(f"{test_name} - French Translation Authenticity", "PASS")

    async def run_all_tests(self):
        """Run all Quran API tests"""
        print("🚀 Starting Quran API Backend Testing")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print("Testing Quran API endpoints as per review request")
        print("=" * 80)
        
        # Run all test suites
        await self.test_surah_chapters()
        await self.test_bulk_verses()
        await self.test_single_verse_with_tafsir()
        
        # Print summary
        print("\n" + "=" * 80)
        print("🏁 QURAN API TEST SUMMARY")
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
    async with QuranAPITester() as tester:
        success = await tester.run_all_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())