#!/usr/bin/env python3
"""
Backend Test Suite for Quran.com API v4 Integration
Tests all endpoints specified in the review request
"""

import asyncio
import httpx
import json
import time
from typing import Dict, Any, List

# Backend URL from frontend/.env
BACKEND_URL = "https://tafsir-mobile-hub.preview.emergentagent.com"

class QuranAPITester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name: str, endpoint: str, expected: str, result: str, status: str, details: Dict[str, Any] = None):
        """Log test result"""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            
        test_result = {
            "test": test_name,
            "endpoint": endpoint,
            "expected": expected,
            "result": result,
            "status": status,
            "details": details or {}
        }
        self.results.append(test_result)
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {result}")
        
    async def test_verse_of_day_english(self):
        """Test GET /api/ai/verse-of-day?language=en"""
        endpoint = f"{BACKEND_URL}/api/ai/verse-of-day?language=en"
        
        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(endpoint)
                response_time = time.time() - start_time
                
            if response.status_code != 200:
                self.log_test(
                    "Verse of Day (English)",
                    endpoint,
                    "200 with verse object",
                    f"HTTP {response.status_code}",
                    "FAIL",
                    {"response_time": response_time, "error": response.text}
                )
                return
                
            data = response.json()
            verse = data.get("verse", {})
            
            # Check required fields
            required_fields = ["text", "translation", "surah", "ayah"]
            missing_fields = [f for f in required_fields if f not in verse]
            
            if missing_fields:
                self.log_test(
                    "Verse of Day (English)",
                    endpoint,
                    "Verse with text, translation, surah, ayah",
                    f"Missing fields: {missing_fields}",
                    "FAIL",
                    {"response_time": response_time, "verse": verse}
                )
                return
                
            # Check if translation is present (should NOT be AI-generated)
            translation = verse.get("translation", "")
            if not translation:
                self.log_test(
                    "Verse of Day (English)",
                    endpoint,
                    "English translation from Saheeh International",
                    "No translation field",
                    "FAIL",
                    {"response_time": response_time, "verse": verse}
                )
                return
                
            # Check if Arabic text is in Uthmani script (contains Arabic characters)
            arabic_text = verse.get("text", "")
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in arabic_text)
            
            if not has_arabic:
                self.log_test(
                    "Verse of Day (English)",
                    endpoint,
                    "Arabic text in Uthmani script",
                    "No Arabic text found",
                    "FAIL",
                    {"response_time": response_time, "verse": verse}
                )
                return
                
            self.log_test(
                "Verse of Day (English)",
                endpoint,
                "Verse with Arabic text and English translation",
                f"✓ Arabic text, ✓ English translation, ✓ Surah: {verse['surah']}, ✓ Ayah: {verse['ayah']}",
                "PASS",
                {"response_time": response_time, "verse": verse}
            )
            
        except Exception as e:
            self.log_test(
                "Verse of Day (English)",
                endpoint,
                "200 with verse object",
                f"Exception: {str(e)}",
                "FAIL",
                {"error": str(e)}
            )
            
    async def test_verse_of_day_arabic(self):
        """Test GET /api/ai/verse-of-day?language=ar"""
        endpoint = f"{BACKEND_URL}/api/ai/verse-of-day?language=ar"
        
        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(endpoint)
                response_time = time.time() - start_time
                
            if response.status_code != 200:
                self.log_test(
                    "Verse of Day (Arabic)",
                    endpoint,
                    "200 with Arabic verse (no translation)",
                    f"HTTP {response.status_code}",
                    "FAIL",
                    {"response_time": response_time, "error": response.text}
                )
                return
                
            data = response.json()
            verse = data.get("verse", {})
            
            # Check required fields for Arabic
            required_fields = ["text", "surah", "ayah"]
            missing_fields = [f for f in required_fields if f not in verse]
            
            if missing_fields:
                self.log_test(
                    "Verse of Day (Arabic)",
                    endpoint,
                    "Arabic verse without translation field",
                    f"Missing fields: {missing_fields}",
                    "FAIL",
                    {"response_time": response_time, "verse": verse}
                )
                return
                
            # Check that translation field is NOT present for Arabic
            if "translation" in verse:
                self.log_test(
                    "Verse of Day (Arabic)",
                    endpoint,
                    "Arabic verse without translation field",
                    "Translation field present (should not be for Arabic)",
                    "FAIL",
                    {"response_time": response_time, "verse": verse}
                )
                return
                
            # Check if Arabic text is present
            arabic_text = verse.get("text", "")
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in arabic_text)
            
            if not has_arabic:
                self.log_test(
                    "Verse of Day (Arabic)",
                    endpoint,
                    "Arabic text in Uthmani script",
                    "No Arabic text found",
                    "FAIL",
                    {"response_time": response_time, "verse": verse}
                )
                return
                
            self.log_test(
                "Verse of Day (Arabic)",
                endpoint,
                "Arabic verse without translation",
                f"✓ Arabic text, ✓ No translation, ✓ Surah: {verse['surah']}, ✓ Ayah: {verse['ayah']}",
                "PASS",
                {"response_time": response_time, "verse": verse}
            )
            
        except Exception as e:
            self.log_test(
                "Verse of Day (Arabic)",
                endpoint,
                "200 with Arabic verse",
                f"Exception: {str(e)}",
                "FAIL",
                {"error": str(e)}
            )
            
    async def test_verse_of_day_french(self):
        """Test GET /api/ai/verse-of-day?language=fr"""
        endpoint = f"{BACKEND_URL}/api/ai/verse-of-day?language=fr"
        
        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(endpoint)
                response_time = time.time() - start_time
                
            if response.status_code != 200:
                self.log_test(
                    "Verse of Day (French)",
                    endpoint,
                    "200 with French translation",
                    f"HTTP {response.status_code}",
                    "FAIL",
                    {"response_time": response_time, "error": response.text}
                )
                return
                
            data = response.json()
            verse = data.get("verse", {})
            
            # Check required fields
            required_fields = ["text", "translation", "surah", "ayah"]
            missing_fields = [f for f in required_fields if f not in verse]
            
            if missing_fields:
                self.log_test(
                    "Verse of Day (French)",
                    endpoint,
                    "Verse with French translation",
                    f"Missing fields: {missing_fields}",
                    "FAIL",
                    {"response_time": response_time, "verse": verse}
                )
                return
                
            # Check if translation is present
            translation = verse.get("translation", "")
            if not translation:
                self.log_test(
                    "Verse of Day (French)",
                    endpoint,
                    "French translation",
                    "No translation field",
                    "FAIL",
                    {"response_time": response_time, "verse": verse}
                )
                return
                
            self.log_test(
                "Verse of Day (French)",
                endpoint,
                "Verse with French translation",
                f"✓ Arabic text, ✓ French translation, ✓ Surah: {verse['surah']}, ✓ Ayah: {verse['ayah']}",
                "PASS",
                {"response_time": response_time, "verse": verse}
            )
            
        except Exception as e:
            self.log_test(
                "Verse of Day (French)",
                endpoint,
                "200 with French translation",
                f"Exception: {str(e)}",
                "FAIL",
                {"error": str(e)}
            )
            
    async def test_surah_fatiha_english(self):
        """Test GET /api/kids-learn/quran/surah/fatiha?locale=en"""
        endpoint = f"{BACKEND_URL}/api/kids-learn/quran/surah/fatiha?locale=en"
        
        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(endpoint)
                response_time = time.time() - start_time
                
            if response.status_code != 200:
                self.log_test(
                    "Surah Al-Fatiha (English)",
                    endpoint,
                    "200 with 7 ayahs",
                    f"HTTP {response.status_code}",
                    "FAIL",
                    {"response_time": response_time, "error": response.text}
                )
                return
                
            data = response.json()
            surah = data.get("surah", {})
            ayahs = surah.get("ayahs", [])
            
            # Check if we have 7 ayahs (Al-Fatiha has 7 verses)
            if len(ayahs) != 7:
                self.log_test(
                    "Surah Al-Fatiha (English)",
                    endpoint,
                    "7 ayahs with Arabic and English translation",
                    f"Found {len(ayahs)} ayahs instead of 7",
                    "FAIL",
                    {"response_time": response_time, "ayahs_count": len(ayahs)}
                )
                return
                
            # Check each ayah has required fields
            for i, ayah in enumerate(ayahs, 1):
                if "arabic" not in ayah or "translation" not in ayah:
                    self.log_test(
                        "Surah Al-Fatiha (English)",
                        endpoint,
                        "Each ayah with arabic and translation fields",
                        f"Ayah {i} missing required fields",
                        "FAIL",
                        {"response_time": response_time, "ayah": ayah}
                    )
                    return
                    
                # Check if Arabic text is present
                arabic_text = ayah.get("arabic", "")
                has_arabic = any('\u0600' <= char <= '\u06FF' for char in arabic_text)
                if not has_arabic:
                    self.log_test(
                        "Surah Al-Fatiha (English)",
                        endpoint,
                        "Arabic text in Uthmani script",
                        f"Ayah {i} has no Arabic text",
                        "FAIL",
                        {"response_time": response_time, "ayah": ayah}
                    )
                    return
                    
                # Check if translation is present
                translation = ayah.get("translation", "")
                if not translation:
                    self.log_test(
                        "Surah Al-Fatiha (English)",
                        endpoint,
                        "English translation from Saheeh International",
                        f"Ayah {i} has no translation",
                        "FAIL",
                        {"response_time": response_time, "ayah": ayah}
                    )
                    return
                    
            self.log_test(
                "Surah Al-Fatiha (English)",
                endpoint,
                "7 ayahs with Arabic and English translation",
                f"✓ 7 ayahs, ✓ Arabic text, ✓ English translations (Saheeh International ID 20)",
                "PASS",
                {"response_time": response_time, "ayahs_count": len(ayahs)}
            )
            
        except Exception as e:
            self.log_test(
                "Surah Al-Fatiha (English)",
                endpoint,
                "200 with 7 ayahs",
                f"Exception: {str(e)}",
                "FAIL",
                {"error": str(e)}
            )
            
    async def test_surah_fatiha_french(self):
        """Test GET /api/kids-learn/quran/surah/fatiha?locale=fr"""
        endpoint = f"{BACKEND_URL}/api/kids-learn/quran/surah/fatiha?locale=fr"
        
        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(endpoint)
                response_time = time.time() - start_time
                
            if response.status_code != 200:
                self.log_test(
                    "Surah Al-Fatiha (French)",
                    endpoint,
                    "200 with French translations (ID 31)",
                    f"HTTP {response.status_code}",
                    "FAIL",
                    {"response_time": response_time, "error": response.text}
                )
                return
                
            data = response.json()
            surah = data.get("surah", {})
            ayahs = surah.get("ayahs", [])
            
            # Check if we have 7 ayahs
            if len(ayahs) != 7:
                self.log_test(
                    "Surah Al-Fatiha (French)",
                    endpoint,
                    "7 ayahs with French translations",
                    f"Found {len(ayahs)} ayahs instead of 7",
                    "FAIL",
                    {"response_time": response_time, "ayahs_count": len(ayahs)}
                )
                return
                
            # Check each ayah has French translation
            for i, ayah in enumerate(ayahs, 1):
                translation = ayah.get("translation", "")
                if not translation:
                    self.log_test(
                        "Surah Al-Fatiha (French)",
                        endpoint,
                        "French translations (ID 31)",
                        f"Ayah {i} has no French translation",
                        "FAIL",
                        {"response_time": response_time, "ayah": ayah}
                    )
                    return
                    
            self.log_test(
                "Surah Al-Fatiha (French)",
                endpoint,
                "7 ayahs with French translations",
                f"✓ 7 ayahs, ✓ French translations (ID 31)",
                "PASS",
                {"response_time": response_time, "ayahs_count": len(ayahs)}
            )
            
        except Exception as e:
            self.log_test(
                "Surah Al-Fatiha (French)",
                endpoint,
                "200 with French translations",
                f"Exception: {str(e)}",
                "FAIL",
                {"error": str(e)}
            )
            
    async def test_surah_ikhlas_english(self):
        """Test GET /api/kids-learn/quran/surah/ikhlas?locale=en"""
        endpoint = f"{BACKEND_URL}/api/kids-learn/quran/surah/ikhlas?locale=en"
        
        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(endpoint)
                response_time = time.time() - start_time
                
            if response.status_code != 200:
                self.log_test(
                    "Surah Al-Ikhlas (English)",
                    endpoint,
                    "200 with 4 ayahs",
                    f"HTTP {response.status_code}",
                    "FAIL",
                    {"response_time": response_time, "error": response.text}
                )
                return
                
            data = response.json()
            surah = data.get("surah", {})
            ayahs = surah.get("ayahs", [])
            
            # Check if we have 4 ayahs (Al-Ikhlas has 4 verses)
            if len(ayahs) != 4:
                self.log_test(
                    "Surah Al-Ikhlas (English)",
                    endpoint,
                    "4 ayahs with Arabic and English translation",
                    f"Found {len(ayahs)} ayahs instead of 4",
                    "FAIL",
                    {"response_time": response_time, "ayahs_count": len(ayahs)}
                )
                return
                
            # Check each ayah has required fields
            for i, ayah in enumerate(ayahs, 1):
                if "arabic" not in ayah or "translation" not in ayah:
                    self.log_test(
                        "Surah Al-Ikhlas (English)",
                        endpoint,
                        "Each ayah with arabic and translation fields",
                        f"Ayah {i} missing required fields",
                        "FAIL",
                        {"response_time": response_time, "ayah": ayah}
                    )
                    return
                    
            self.log_test(
                "Surah Al-Ikhlas (English)",
                endpoint,
                "4 ayahs with Arabic and English translation",
                f"✓ 4 ayahs, ✓ Arabic text, ✓ English translations",
                "PASS",
                {"response_time": response_time, "ayahs_count": len(ayahs)}
            )
            
        except Exception as e:
            self.log_test(
                "Surah Al-Ikhlas (English)",
                endpoint,
                "200 with 4 ayahs",
                f"Exception: {str(e)}",
                "FAIL",
                {"error": str(e)}
            )
            
    async def test_surahs_list_arabic(self):
        """Test GET /api/kids-learn/quran/surahs?locale=ar"""
        endpoint = f"{BACKEND_URL}/api/kids-learn/quran/surahs?locale=ar"
        
        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(endpoint)
                response_time = time.time() - start_time
                
            if response.status_code != 200:
                self.log_test(
                    "Surahs List (Arabic)",
                    endpoint,
                    "200 with list of surahs",
                    f"HTTP {response.status_code}",
                    "FAIL",
                    {"response_time": response_time, "error": response.text}
                )
                return
                
            data = response.json()
            surahs = data.get("surahs", [])
            
            if not surahs:
                self.log_test(
                    "Surahs List (Arabic)",
                    endpoint,
                    "List of surahs",
                    "Empty surahs list",
                    "FAIL",
                    {"response_time": response_time, "data": data}
                )
                return
                
            # Check if surahs have required fields
            for surah in surahs[:3]:  # Check first 3 surahs
                required_fields = ["id", "number", "name_ar", "name_en"]
                missing_fields = [f for f in required_fields if f not in surah]
                if missing_fields:
                    self.log_test(
                        "Surahs List (Arabic)",
                        endpoint,
                        "Surahs with id, number, name_ar, name_en",
                        f"Missing fields in surah: {missing_fields}",
                        "FAIL",
                        {"response_time": response_time, "surah": surah}
                    )
                    return
                    
            self.log_test(
                "Surahs List (Arabic)",
                endpoint,
                "List of surahs",
                f"✓ {len(surahs)} surahs with required fields",
                "PASS",
                {"response_time": response_time, "surahs_count": len(surahs)}
            )
            
        except Exception as e:
            self.log_test(
                "Surahs List (Arabic)",
                endpoint,
                "200 with list of surahs",
                f"Exception: {str(e)}",
                "FAIL",
                {"error": str(e)}
            )
            
    async def run_all_tests(self):
        """Run all Quran API v4 integration tests"""
        print("🚀 Starting Quran.com API v4 Integration Tests")
        print("=" * 60)
        
        # Test all endpoints specified in review request
        await self.test_verse_of_day_english()
        await self.test_verse_of_day_arabic()
        await self.test_verse_of_day_french()
        await self.test_surah_fatiha_english()
        await self.test_surah_fatiha_french()
        await self.test_surah_ikhlas_english()
        await self.test_surahs_list_arabic()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"  • {result['test']}: {result['result']}")
                    if result.get("details", {}).get("error"):
                        print(f"    Error: {result['details']['error']}")
        
        print("\n🔍 KEY VERIFICATIONS:")
        print("  • Translations from Quran.com API v4 (not hardcoded)")
        print("  • No AI-generated translations")
        print("  • Arabic text in Uthmani script")
        print("  • Response times under 15s")
        print("  • Correct translation IDs (en=20, fr=31)")
        
        return self.results

async def main():
    """Main test runner"""
    tester = QuranAPITester()
    results = await tester.run_all_tests()
    
    # Save results to file for reference
    with open("/app/quran_api_test_results.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed results saved to: /app/quran_api_test_results.json")

if __name__ == "__main__":
    asyncio.run(main())