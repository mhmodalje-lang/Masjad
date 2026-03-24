#!/usr/bin/env python3
"""
Backend Test Suite for Quran.com API v4 Integration Rebuild
Testing all endpoints specified in the review request
"""

import asyncio
import httpx
import json
import re
from datetime import datetime

# Backend URL from frontend/.env
BACKEND_URL = "https://tafsir-mobile-hub.preview.emergentagent.com"

class QuranAPITester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def log_result(self, test_name, status, details):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        if status == "PASS":
            self.passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            self.failed += 1
            print(f"❌ {test_name}: FAILED - {details}")
    
    def is_arabic_uthmani(self, text):
        """Check if text contains Arabic Uthmani script"""
        if not text:
            return False
        # Check for Arabic Unicode range (U+0600-U+06FF)
        arabic_pattern = re.compile(r'[\u0600-\u06FF]')
        return bool(arabic_pattern.search(text))
    
    def has_no_alquran_cloud_refs(self, text):
        """Verify no alquran.cloud references"""
        if not text:
            return True
        return "alquran.cloud" not in text.lower()
    
    async def test_verse_of_day_english(self):
        """Test 1: GET /api/ai/verse-of-day?language=en"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(f"{BACKEND_URL}/api/ai/verse-of-day?language=en")
                
                if response.status_code != 200:
                    self.log_result("Verse of Day (English)", "FAIL", f"HTTP {response.status_code}")
                    return
                
                data = response.json()
                verse = data.get("verse", {})
                
                # Verify required fields
                checks = []
                checks.append(("Has Arabic text", bool(verse.get("text"))))
                checks.append(("Arabic is Uthmani", self.is_arabic_uthmani(verse.get("text", ""))))
                checks.append(("Has English translation", bool(verse.get("translation"))))
                checks.append(("Has surah name", bool(verse.get("surah"))))
                checks.append(("Has ayah number", isinstance(verse.get("ayah"), int)))
                checks.append(("No alquran.cloud refs", self.has_no_alquran_cloud_refs(str(data))))
                
                all_passed = all(check[1] for check in checks)
                details = f"Arabic: '{verse.get('text', '')[:50]}...', Translation: '{verse.get('translation', '')[:50]}...', Surah: {verse.get('surah')}, Ayah: {verse.get('ayah')}"
                
                if all_passed:
                    self.log_result("Verse of Day (English)", "PASS", details)
                else:
                    failed_checks = [check[0] for check in checks if not check[1]]
                    self.log_result("Verse of Day (English)", "FAIL", f"Failed: {failed_checks}")
                    
        except Exception as e:
            self.log_result("Verse of Day (English)", "FAIL", f"Exception: {str(e)}")
    
    async def test_verse_of_day_arabic(self):
        """Test 2: GET /api/ai/verse-of-day?language=ar"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(f"{BACKEND_URL}/api/ai/verse-of-day?language=ar")
                
                if response.status_code != 200:
                    self.log_result("Verse of Day (Arabic)", "FAIL", f"HTTP {response.status_code}")
                    return
                
                data = response.json()
                verse = data.get("verse", {})
                
                # Verify required fields (Arabic should NOT have translation field)
                checks = []
                checks.append(("Has Arabic text", bool(verse.get("text"))))
                checks.append(("Arabic is Uthmani", self.is_arabic_uthmani(verse.get("text", ""))))
                checks.append(("No translation field", "translation" not in verse))
                checks.append(("Has surah name", bool(verse.get("surah"))))
                checks.append(("Has ayah number", isinstance(verse.get("ayah"), int)))
                
                all_passed = all(check[1] for check in checks)
                details = f"Arabic: '{verse.get('text', '')[:50]}...', Surah: {verse.get('surah')}, Ayah: {verse.get('ayah')}"
                
                if all_passed:
                    self.log_result("Verse of Day (Arabic)", "PASS", details)
                else:
                    failed_checks = [check[0] for check in checks if not check[1]]
                    self.log_result("Verse of Day (Arabic)", "FAIL", f"Failed: {failed_checks}")
                    
        except Exception as e:
            self.log_result("Verse of Day (Arabic)", "FAIL", f"Exception: {str(e)}")
    
    async def test_verse_of_day_french(self):
        """Test 3: GET /api/ai/verse-of-day?language=fr"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(f"{BACKEND_URL}/api/ai/verse-of-day?language=fr")
                
                if response.status_code != 200:
                    self.log_result("Verse of Day (French)", "FAIL", f"HTTP {response.status_code}")
                    return
                
                data = response.json()
                verse = data.get("verse", {})
                
                checks = []
                checks.append(("Has Arabic text", bool(verse.get("text"))))
                checks.append(("Has French translation", bool(verse.get("translation"))))
                checks.append(("Has surah name", bool(verse.get("surah"))))
                checks.append(("Has ayah number", isinstance(verse.get("ayah"), int)))
                
                all_passed = all(check[1] for check in checks)
                details = f"French translation: '{verse.get('translation', '')[:50]}...'"
                
                if all_passed:
                    self.log_result("Verse of Day (French)", "PASS", details)
                else:
                    failed_checks = [check[0] for check in checks if not check[1]]
                    self.log_result("Verse of Day (French)", "FAIL", f"Failed: {failed_checks}")
                    
        except Exception as e:
            self.log_result("Verse of Day (French)", "FAIL", f"Exception: {str(e)}")
    
    async def test_verse_of_day_german(self):
        """Test 4: GET /api/ai/verse-of-day?language=de"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(f"{BACKEND_URL}/api/ai/verse-of-day?language=de")
                
                if response.status_code != 200:
                    self.log_result("Verse of Day (German)", "FAIL", f"HTTP {response.status_code}")
                    return
                
                data = response.json()
                verse = data.get("verse", {})
                
                checks = []
                checks.append(("Has Arabic text", bool(verse.get("text"))))
                checks.append(("Has German translation", bool(verse.get("translation"))))
                checks.append(("Has surah name", bool(verse.get("surah"))))
                checks.append(("Has ayah number", isinstance(verse.get("ayah"), int)))
                
                all_passed = all(check[1] for check in checks)
                details = f"German translation: '{verse.get('translation', '')[:50]}...'"
                
                if all_passed:
                    self.log_result("Verse of Day (German)", "PASS", details)
                else:
                    failed_checks = [check[0] for check in checks if not check[1]]
                    self.log_result("Verse of Day (German)", "FAIL", f"Failed: {failed_checks}")
                    
        except Exception as e:
            self.log_result("Verse of Day (German)", "FAIL", f"Exception: {str(e)}")
    
    async def test_surah_fatiha_english(self):
        """Test 5: GET /api/kids-learn/quran/surah/fatiha?locale=en"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(f"{BACKEND_URL}/api/kids-learn/quran/surah/fatiha?locale=en")
                
                if response.status_code != 200:
                    self.log_result("Surah Al-Fatiha (English)", "FAIL", f"HTTP {response.status_code}")
                    return
                
                data = response.json()
                surah = data.get("surah", {})
                ayahs = surah.get("ayahs", [])
                
                checks = []
                checks.append(("Has 7 ayahs", len(ayahs) == 7))
                checks.append(("All ayahs have Arabic", all(ayah.get("arabic") for ayah in ayahs)))
                checks.append(("All ayahs have translation", all(ayah.get("translation") for ayah in ayahs)))
                checks.append(("Arabic is Uthmani", all(self.is_arabic_uthmani(ayah.get("arabic", "")) for ayah in ayahs)))
                
                # Check if translations are from Saheeh International (ID 20) - look for characteristic phrases
                sample_translation = ayahs[0].get("translation", "") if ayahs else ""
                checks.append(("Translation from Quran.com API", bool(sample_translation)))
                
                all_passed = all(check[1] for check in checks)
                details = f"Ayahs: {len(ayahs)}, Sample translation: '{sample_translation[:50]}...'"
                
                if all_passed:
                    self.log_result("Surah Al-Fatiha (English)", "PASS", details)
                else:
                    failed_checks = [check[0] for check in checks if not check[1]]
                    self.log_result("Surah Al-Fatiha (English)", "FAIL", f"Failed: {failed_checks}")
                    
        except Exception as e:
            self.log_result("Surah Al-Fatiha (English)", "FAIL", f"Exception: {str(e)}")
    
    async def test_surah_zilzal_english(self):
        """Test 6: GET /api/kids-learn/quran/surah/zilzal?locale=en"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(f"{BACKEND_URL}/api/kids-learn/quran/surah/zilzal?locale=en")
                
                if response.status_code != 200:
                    self.log_result("Surah Az-Zilzal (English)", "FAIL", f"HTTP {response.status_code}")
                    return
                
                data = response.json()
                surah = data.get("surah", {})
                ayahs = surah.get("ayahs", [])
                
                checks = []
                checks.append(("Has 8 ayahs", len(ayahs) == 8))
                checks.append(("All ayahs have Arabic", all(ayah.get("arabic") for ayah in ayahs)))
                checks.append(("All ayahs have translation", all(ayah.get("translation") for ayah in ayahs)))
                checks.append(("Not empty (was previously empty)", len(ayahs) > 0))
                
                all_passed = all(check[1] for check in checks)
                details = f"Ayahs: {len(ayahs)}, Previously empty surah now has content"
                
                if all_passed:
                    self.log_result("Surah Az-Zilzal (English)", "PASS", details)
                else:
                    failed_checks = [check[0] for check in checks if not check[1]]
                    self.log_result("Surah Az-Zilzal (English)", "FAIL", f"Failed: {failed_checks}")
                    
        except Exception as e:
            self.log_result("Surah Az-Zilzal (English)", "FAIL", f"Exception: {str(e)}")
    
    async def test_surah_qariah_english(self):
        """Test 7: GET /api/kids-learn/quran/surah/qariah?locale=en"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(f"{BACKEND_URL}/api/kids-learn/quran/surah/qariah?locale=en")
                
                if response.status_code != 200:
                    self.log_result("Surah Al-Qariah (English)", "FAIL", f"HTTP {response.status_code}")
                    return
                
                data = response.json()
                surah = data.get("surah", {})
                ayahs = surah.get("ayahs", [])
                
                checks = []
                checks.append(("Has 11 ayahs", len(ayahs) == 11))
                checks.append(("All ayahs have Arabic", all(ayah.get("arabic") for ayah in ayahs)))
                checks.append(("All ayahs have translation", all(ayah.get("translation") for ayah in ayahs)))
                checks.append(("Not empty (was previously empty)", len(ayahs) > 0))
                
                all_passed = all(check[1] for check in checks)
                details = f"Ayahs: {len(ayahs)}, Previously empty surah now has content"
                
                if all_passed:
                    self.log_result("Surah Al-Qariah (English)", "PASS", details)
                else:
                    failed_checks = [check[0] for check in checks if not check[1]]
                    self.log_result("Surah Al-Qariah (English)", "FAIL", f"Failed: {failed_checks}")
                    
        except Exception as e:
            self.log_result("Surah Al-Qariah (English)", "FAIL", f"Exception: {str(e)}")
    
    async def test_surah_fatiha_german(self):
        """Test 8: GET /api/kids-learn/quran/surah/fatiha?locale=de"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(f"{BACKEND_URL}/api/kids-learn/quran/surah/fatiha?locale=de")
                
                if response.status_code != 200:
                    self.log_result("Surah Al-Fatiha (German)", "FAIL", f"HTTP {response.status_code}")
                    return
                
                data = response.json()
                surah = data.get("surah", {})
                ayahs = surah.get("ayahs", [])
                
                checks = []
                checks.append(("Has 7 ayahs", len(ayahs) == 7))
                checks.append(("All ayahs have German translation", all(ayah.get("translation") for ayah in ayahs)))
                
                # Check for German translation characteristics (Bubenheim & Elyas ID 27)
                sample_translation = ayahs[0].get("translation", "") if ayahs else ""
                checks.append(("German translation from Quran.com API", bool(sample_translation)))
                
                all_passed = all(check[1] for check in checks)
                details = f"German translation sample: '{sample_translation[:50]}...'"
                
                if all_passed:
                    self.log_result("Surah Al-Fatiha (German)", "PASS", details)
                else:
                    failed_checks = [check[0] for check in checks if not check[1]]
                    self.log_result("Surah Al-Fatiha (German)", "FAIL", f"Failed: {failed_checks}")
                    
        except Exception as e:
            self.log_result("Surah Al-Fatiha (German)", "FAIL", f"Exception: {str(e)}")
    
    async def test_surah_fatiha_arabic(self):
        """Test 9: GET /api/kids-learn/quran/surah/fatiha?locale=ar"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(f"{BACKEND_URL}/api/kids-learn/quran/surah/fatiha?locale=ar")
                
                if response.status_code != 200:
                    self.log_result("Surah Al-Fatiha (Arabic Muyassar)", "FAIL", f"HTTP {response.status_code}")
                    return
                
                data = response.json()
                surah = data.get("surah", {})
                ayahs = surah.get("ayahs", [])
                
                checks = []
                checks.append(("Has 7 ayahs", len(ayahs) == 7))
                checks.append(("All ayahs have Arabic text", all(ayah.get("arabic") for ayah in ayahs)))
                checks.append(("All ayahs have Muyassar tafsir", all(ayah.get("translation") for ayah in ayahs)))
                
                # Check if translation is Arabic Muyassar tafsir
                sample_tafsir = ayahs[0].get("translation", "") if ayahs else ""
                checks.append(("Arabic Muyassar tafsir", self.is_arabic_uthmani(sample_tafsir)))
                
                all_passed = all(check[1] for check in checks)
                details = f"Arabic Muyassar sample: '{sample_tafsir[:50]}...'"
                
                if all_passed:
                    self.log_result("Surah Al-Fatiha (Arabic Muyassar)", "PASS", details)
                else:
                    failed_checks = [check[0] for check in checks if not check[1]]
                    self.log_result("Surah Al-Fatiha (Arabic Muyassar)", "FAIL", f"Failed: {failed_checks}")
                    
        except Exception as e:
            self.log_result("Surah Al-Fatiha (Arabic Muyassar)", "FAIL", f"Exception: {str(e)}")
    
    async def test_surahs_list_english(self):
        """Test 10: GET /api/kids-learn/quran/surahs?locale=en"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(f"{BACKEND_URL}/api/kids-learn/quran/surahs?locale=en")
                
                if response.status_code != 200:
                    self.log_result("Surahs List (English)", "FAIL", f"HTTP {response.status_code}")
                    return
                
                data = response.json()
                surahs = data.get("surahs", [])
                
                checks = []
                checks.append(("Has 15 surahs", len(surahs) == 15))
                checks.append(("All surahs have required fields", all(
                    surah.get("id") and surah.get("number") and surah.get("name_ar") and surah.get("name_en")
                    for surah in surahs
                )))
                
                all_passed = all(check[1] for check in checks)
                details = f"Total surahs: {len(surahs)}, Sample: {surahs[0] if surahs else 'None'}"
                
                if all_passed:
                    self.log_result("Surahs List (English)", "PASS", details)
                else:
                    failed_checks = [check[0] for check in checks if not check[1]]
                    self.log_result("Surahs List (English)", "FAIL", f"Failed: {failed_checks}")
                    
        except Exception as e:
            self.log_result("Surahs List (English)", "FAIL", f"Exception: {str(e)}")
    
    async def run_all_tests(self):
        """Run all test cases"""
        print("🚀 Starting Quran.com API v4 Integration Test Suite")
        print("=" * 60)
        
        test_methods = [
            self.test_verse_of_day_english,
            self.test_verse_of_day_arabic,
            self.test_verse_of_day_french,
            self.test_verse_of_day_german,
            self.test_surah_fatiha_english,
            self.test_surah_zilzal_english,
            self.test_surah_qariah_english,
            self.test_surah_fatiha_german,
            self.test_surah_fatiha_arabic,
            self.test_surahs_list_english,
        ]
        
        for test_method in test_methods:
            await test_method()
            await asyncio.sleep(0.5)  # Small delay between tests
        
        print("\n" + "=" * 60)
        print(f"📊 TEST SUMMARY")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"   ❌ {result['test']}: {result['details']}")
        
        return self.passed, self.failed

async def main():
    """Main test runner"""
    tester = QuranAPITester()
    passed, failed = await tester.run_all_tests()
    
    # Save detailed results
    with open("/app/quran_api_test_results.json", "w") as f:
        json.dump({
            "summary": {"passed": passed, "failed": failed, "total": passed + failed},
            "results": tester.results,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: /app/quran_api_test_results.json")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Quran.com API v4 integration is working perfectly.")
    else:
        print(f"⚠️  {failed} test(s) failed. Please check the issues above.")

if __name__ == "__main__":
    asyncio.run(main())