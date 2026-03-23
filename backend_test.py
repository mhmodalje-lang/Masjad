#!/usr/bin/env python3
"""
Backend API Testing Script for Islamic Data Accuracy Overhaul
Tests the specific APIs requested in the review request for Phase 1+2+3 completion
"""

import asyncio
import httpx
import json
from typing import Dict, Any, List
import re

# Backend URL from frontend .env
BACKEND_URL = "https://quran-authentic-1.preview.emergentagent.com"

class IslamicDataTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.results = []
        
    def log_result(self, test_name: str, endpoint: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "endpoint": endpoint,
            "status": status,
            "details": details
        }
        self.results.append(result)
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
    
    async def test_hadith_authenticity(self):
        """Test Hadith Authenticity - Call daily-hadith 5 times and verify only Bukhari/Muslim sources"""
        test_name = "Hadith Authenticity Test"
        endpoint = "/api/daily-hadith"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                all_sources = []
                invalid_sources = []
                
                # Call the API 5 times to get different hadiths
                for i in range(5):
                    response = await client.get(f"{self.base_url}{endpoint}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Check if response has success: true
                        if not data.get("success", False):
                            self.log_result(test_name, endpoint, "FAIL", 
                                          f"Response missing 'success: true' on call {i+1}")
                            return
                        
                        # Check hadith structure
                        hadith = data.get("hadith", {})
                        source = hadith.get("source", "")
                        
                        if not source:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          f"Missing 'source' field on call {i+1}")
                            return
                        
                        all_sources.append(source)
                        
                        # Check if source contains only allowed sources
                        allowed_sources = ["صحيح البخاري", "صحيح مسلم", "صحيح البخاري ومسلم"]
                        forbidden_sources = ["الترمذي", "النسائي", "ابن ماجه"]
                        
                        # Check if source is exactly one of the allowed sources
                        if source not in allowed_sources:
                            invalid_sources.append(f"Call {i+1}: '{source}'")
                        
                        # Check if source contains any forbidden sources
                        for forbidden in forbidden_sources:
                            if forbidden in source:
                                invalid_sources.append(f"Call {i+1}: Contains forbidden '{forbidden}' in '{source}'")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"HTTP {response.status_code} on call {i+1}: {response.text[:200]}")
                        return
                
                # Final validation
                if invalid_sources:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"Invalid sources found: {'; '.join(invalid_sources)}")
                else:
                    unique_sources = list(set(all_sources))
                    self.log_result(test_name, endpoint, "PASS", 
                                  f"All 5 calls returned valid Bukhari/Muslim sources: {unique_sources}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_tafsir_arabic_muyassar(self):
        """Test Tafsir API - Arabic (Muyassar) for verse 1:1"""
        test_name = "Tafsir Arabic (Al-Muyassar)"
        endpoint = "/api/quran/v4/tafsir/1:1?language=ar"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check success field
                    if not data.get("success", False):
                        self.log_result(test_name, endpoint, "FAIL", "Response missing 'success: true'")
                        return
                    
                    # Check tafsir_id should be 16 (Al-Muyassar)
                    tafsir_id = data.get("tafsir_id")
                    if tafsir_id != 16:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"Expected tafsir_id=16, got {tafsir_id}")
                        return
                    
                    # Check text is non-empty Arabic
                    text = data.get("text", "")
                    if not text or len(text.strip()) == 0:
                        self.log_result(test_name, endpoint, "FAIL", "Empty tafsir text")
                        return
                    
                    # Basic check for Arabic characters
                    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
                    if not arabic_pattern.search(text):
                        self.log_result(test_name, endpoint, "FAIL", "Text doesn't contain Arabic characters")
                        return
                    
                    self.log_result(test_name, endpoint, "PASS", 
                                  f"tafsir_id={tafsir_id}, text length={len(text)} chars, contains Arabic")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_tafsir_english_ibn_kathir(self):
        """Test Tafsir API - English (Ibn Kathir) for verse 2:255 (Ayat al-Kursi)"""
        test_name = "Tafsir English (Ibn Kathir)"
        endpoint = "/api/quran/v4/tafsir/2:255?language=en"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check success field
                    if not data.get("success", False):
                        self.log_result(test_name, endpoint, "FAIL", "Response missing 'success: true'")
                        return
                    
                    # Check tafsir_id should be 169 (Ibn Kathir)
                    tafsir_id = data.get("tafsir_id")
                    if tafsir_id != 169:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"Expected tafsir_id=169, got {tafsir_id}")
                        return
                    
                    # Check text is non-empty English
                    text = data.get("text", "")
                    if not text or len(text.strip()) == 0:
                        self.log_result(test_name, endpoint, "FAIL", "Empty tafsir text")
                        return
                    
                    self.log_result(test_name, endpoint, "PASS", 
                                  f"tafsir_id={tafsir_id}, text length={len(text)} chars")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_tafsir_dutch_fallback(self):
        """Test Tafsir API - Dutch fallback to English"""
        test_name = "Tafsir Dutch Fallback"
        endpoint = "/api/quran/v4/tafsir/1:5?language=nl"  # Using verse 1:5 to avoid cache
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check success field
                    if not data.get("success", False):
                        self.log_result(test_name, endpoint, "FAIL", "Response missing 'success: true'")
                        return
                    
                    # Check is_fallback_language should be true
                    is_fallback = data.get("is_fallback_language", False)
                    if not is_fallback:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"Expected is_fallback_language=true, got {is_fallback}")
                        return
                    
                    # Check tafsir_id should be 169 (fallback to English Ibn Kathir)
                    tafsir_id = data.get("tafsir_id")
                    if tafsir_id != 169:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"Expected tafsir_id=169 (fallback), got {tafsir_id}")
                        return
                    
                    # Check text is non-empty
                    text = data.get("text", "")
                    if not text or len(text.strip()) == 0:
                        self.log_result(test_name, endpoint, "FAIL", "Empty tafsir text")
                        return
                    
                    self.log_result(test_name, endpoint, "PASS", 
                                  f"Correctly falls back: tafsir_id={tafsir_id}, is_fallback={is_fallback}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_tafsir_russian_alsadi(self):
        """Test Tafsir API - Russian (Al-Sa'di)"""
        test_name = "Tafsir Russian (Al-Sa'di)"
        endpoint = "/api/quran/v4/tafsir/1:1?language=ru"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check success field
                    if not data.get("success", False):
                        self.log_result(test_name, endpoint, "FAIL", "Response missing 'success: true'")
                        return
                    
                    # Check tafsir_id should be 170 (Al-Sa'di Russian)
                    tafsir_id = data.get("tafsir_id")
                    if tafsir_id != 170:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"Expected tafsir_id=170, got {tafsir_id}")
                        return
                    
                    # Check text is non-empty
                    text = data.get("text", "")
                    if not text or len(text.strip()) == 0:
                        self.log_result(test_name, endpoint, "FAIL", "Empty tafsir text")
                        return
                    
                    self.log_result(test_name, endpoint, "PASS", 
                                  f"tafsir_id={tafsir_id}, text length={len(text)} chars")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_invalid_verse(self):
        """Test Tafsir API with invalid verse - should return 400"""
        test_name = "Invalid Verse Test"
        endpoint = "/api/quran/v4/tafsir/invalid"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 400:
                    self.log_result(test_name, endpoint, "PASS", 
                                  "Correctly returns 400 for invalid verse format")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"Expected HTTP 400, got {response.status_code}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_caching_functionality(self):
        """Test Tafsir caching - first call should be cached=false, second cached=true"""
        test_name = "Caching Test"
        endpoint = "/api/quran/v4/tafsir/1:6?language=ar"  # Using verse 1:6 to avoid cache
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # First call - should be cached=false
                response1 = await client.get(f"{self.base_url}{endpoint}")
                
                if response1.status_code == 200:
                    data1 = response1.json()
                    cached1 = data1.get("cached", None)
                    
                    if cached1 is not False:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"First call: expected cached=false, got {cached1}")
                        return
                    
                    # Second call - should be cached=true
                    response2 = await client.get(f"{self.base_url}{endpoint}")
                    
                    if response2.status_code == 200:
                        data2 = response2.json()
                        cached2 = data2.get("cached", None)
                        
                        if cached2 is not True:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          f"Second call: expected cached=true, got {cached2}")
                            return
                        
                        self.log_result(test_name, endpoint, "PASS", 
                                      f"Caching works: first call cached={cached1}, second call cached={cached2}")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"Second call HTTP {response2.status_code}: {response2.text[:200]}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"First call HTTP {response1.status_code}: {response1.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def run_all_tests(self):
        """Run all Islamic data accuracy tests"""
        print(f"🚀 Starting Islamic Data Accuracy Tests for: {self.base_url}")
        print("=" * 80)
        
        # Run all tests in sequence
        await self.test_hadith_authenticity()
        await self.test_tafsir_arabic_muyassar()
        await self.test_tafsir_english_ibn_kathir()
        await self.test_tafsir_dutch_fallback()
        await self.test_tafsir_russian_alsadi()
        await self.test_invalid_verse()
        await self.test_caching_functionality()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 ISLAMIC DATA ACCURACY TEST SUMMARY")
        print("=" * 80)
        
        passed = len([r for r in self.results if r["status"] == "PASS"])
        failed = len([r for r in self.results if r["status"] == "FAIL"])
        
        print(f"✅ PASSED: {passed}")
        print(f"❌ FAILED: {failed}")
        print(f"📈 SUCCESS RATE: {passed}/{passed+failed} ({(passed/(passed+failed)*100) if (passed+failed) > 0 else 0:.1f}%)")
        
        # Detailed results for failed tests
        if failed > 0:
            print("\n🔍 FAILED TESTS DETAILS:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"❌ {result['test']}: {result['details']}")
        
        # Success details
        if passed > 0:
            print(f"\n✅ SUCCESSFUL TESTS:")
            for result in self.results:
                if result["status"] == "PASS":
                    print(f"✅ {result['test']}")
        
        return self.results

async def main():
    """Main test runner"""
    tester = IslamicDataTester()
    results = await tester.run_all_tests()
    
    # Return results for potential use by other scripts
    return results

if __name__ == "__main__":
    asyncio.run(main())