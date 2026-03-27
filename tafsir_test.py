#!/usr/bin/env python3
"""
Tafsir (Exegesis) API Testing Script
Tests the Tafsir API endpoints as specified in the review request
"""

import asyncio
import httpx
import json
from typing import Dict, Any, List

# Backend URL from frontend .env
BACKEND_URL = "https://content-moderation-266.preview.emergentagent.com"

class TafsirAPITester:
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
    
    async def test_arabic_tafsir_al_muyassar(self):
        """Test Arabic Tafsir Al-Muyassar: GET /api/quran/v4/tafsir/1:1?language=ar"""
        test_name = "Arabic Tafsir Al-Muyassar"
        endpoint = "/api/quran/v4/tafsir/1:1?language=ar"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check required fields
                    if data.get("success") == True:
                        tafsir_id = data.get("tafsir_id")
                        text = data.get("text", "")
                        tafsir_name = data.get("tafsir_name", "")
                        
                        # Validate tafsir_id should be 16 for Arabic Al-Muyassar
                        if tafsir_id == 16:
                            # Check if text is non-empty Arabic text
                            if text and len(text.strip()) > 0:
                                # Check if tafsir_name contains "الم" (part of Al-Muyassar)
                                if "الم" in tafsir_name or "ميسر" in tafsir_name:
                                    self.log_result(test_name, endpoint, "PASS", 
                                                  f"tafsir_id={tafsir_id}, text_length={len(text)}, name contains Arabic")
                                else:
                                    self.log_result(test_name, endpoint, "PASS", 
                                                  f"tafsir_id={tafsir_id}, text_length={len(text)}, name='{tafsir_name}' (may not contain expected Arabic)")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"tafsir_id={tafsir_id} but text is empty")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          f"Expected tafsir_id=16, got {tafsir_id}")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"success={data.get('success')}, response: {data}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_english_ibn_kathir(self):
        """Test English Ibn Kathir: GET /api/quran/v4/tafsir/2:255?language=en"""
        test_name = "English Ibn Kathir"
        endpoint = "/api/quran/v4/tafsir/2:255?language=en"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check required fields
                    if data.get("success") == True:
                        tafsir_id = data.get("tafsir_id")
                        text = data.get("text", "")
                        
                        # Validate tafsir_id should be 169 for English Ibn Kathir
                        if tafsir_id == 169:
                            # Check if text is non-empty English text
                            if text and len(text.strip()) > 0:
                                self.log_result(test_name, endpoint, "PASS", 
                                              f"tafsir_id={tafsir_id}, text_length={len(text)}")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"tafsir_id={tafsir_id} but text is empty")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          f"Expected tafsir_id=169, got {tafsir_id}")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"success={data.get('success')}, response: {data}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_russian_al_sadi(self):
        """Test Russian Al-Sa'di: GET /api/quran/v4/tafsir/1:1?language=ru"""
        test_name = "Russian Al-Sa'di"
        endpoint = "/api/quran/v4/tafsir/1:1?language=ru"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check required fields
                    if data.get("success") == True:
                        tafsir_id = data.get("tafsir_id")
                        text = data.get("text", "")
                        
                        # Validate tafsir_id should be 170 for Russian Al-Sa'di
                        if tafsir_id == 170:
                            # Check if text is non-empty
                            if text and len(text.strip()) > 0:
                                self.log_result(test_name, endpoint, "PASS", 
                                              f"tafsir_id={tafsir_id}, text_length={len(text)}")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"tafsir_id={tafsir_id} but text is empty")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          f"Expected tafsir_id=170, got {tafsir_id}")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"success={data.get('success')}, response: {data}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_german_fallback_to_english(self):
        """Test German fallback to English: GET /api/quran/v4/tafsir/1:1?language=de"""
        test_name = "German fallback to English"
        endpoint = "/api/quran/v4/tafsir/1:1?language=de"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check required fields
                    if data.get("success") == True:
                        tafsir_id = data.get("tafsir_id")
                        text = data.get("text", "")
                        is_fallback = data.get("is_fallback_language")
                        
                        # Validate tafsir_id should be 169 (English Ibn Kathir fallback)
                        if tafsir_id == 169:
                            # Check if is_fallback_language is true
                            if is_fallback == True:
                                # Check if text is non-empty
                                if text and len(text.strip()) > 0:
                                    self.log_result(test_name, endpoint, "PASS", 
                                                  f"tafsir_id={tafsir_id}, is_fallback={is_fallback}, text_length={len(text)}")
                                else:
                                    self.log_result(test_name, endpoint, "FAIL", 
                                                  f"tafsir_id={tafsir_id}, is_fallback={is_fallback} but text is empty")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"Expected is_fallback_language=true, got {is_fallback}")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          f"Expected tafsir_id=169, got {tafsir_id}")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"success={data.get('success')}, response: {data}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_invalid_verse_key(self):
        """Test Invalid verse key: GET /api/quran/v4/tafsir/invalid"""
        test_name = "Invalid verse key"
        endpoint = "/api/quran/v4/tafsir/invalid"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                # Should return 400 error
                if response.status_code == 400:
                    self.log_result(test_name, endpoint, "PASS", 
                                  f"Correctly returns 400 for invalid verse key")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"Expected HTTP 400, got {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_caching_functionality(self):
        """Test Caching: Call GET /api/quran/v4/tafsir/1:2?language=ar twice"""
        test_name = "Caching functionality"
        endpoint = "/api/quran/v4/tafsir/1:2?language=ar"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # First call - should be cached=false
                response1 = await client.get(f"{self.base_url}{endpoint}")
                
                if response1.status_code == 200:
                    data1 = response1.json()
                    
                    if data1.get("success") == True:
                        cached1 = data1.get("cached")
                        
                        # First call should be cached=false
                        if cached1 == False:
                            # Second call - should be cached=true
                            response2 = await client.get(f"{self.base_url}{endpoint}")
                            
                            if response2.status_code == 200:
                                data2 = response2.json()
                                
                                if data2.get("success") == True:
                                    cached2 = data2.get("cached")
                                    
                                    # Second call should be cached=true
                                    if cached2 == True:
                                        self.log_result(test_name, endpoint, "PASS", 
                                                      f"First call: cached={cached1}, Second call: cached={cached2}")
                                    else:
                                        self.log_result(test_name, endpoint, "FAIL", 
                                                      f"Second call should be cached=true, got {cached2}")
                                else:
                                    self.log_result(test_name, endpoint, "FAIL", 
                                                  f"Second call failed: success={data2.get('success')}")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"Second call HTTP {response2.status_code}: {response2.text[:200]}")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          f"First call should be cached=false, got {cached1}")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"First call failed: success={data1.get('success')}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"First call HTTP {response1.status_code}: {response1.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_multiple_verses_al_asr(self):
        """Test Multiple verses in Al-Asr (Chapter 103)"""
        test_name = "Multiple verses in Al-Asr"
        verses = ["103:1", "103:2", "103:3"]
        
        all_passed = True
        details = []
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                for verse in verses:
                    endpoint = f"/api/quran/v4/tafsir/{verse}?language=en"
                    response = await client.get(f"{self.base_url}{endpoint}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if data.get("success") == True:
                            text = data.get("text", "")
                            if text and len(text.strip()) > 0:
                                details.append(f"{verse}: ✅ (text_length={len(text)})")
                            else:
                                details.append(f"{verse}: ❌ (empty text)")
                                all_passed = False
                        else:
                            details.append(f"{verse}: ❌ (success={data.get('success')})")
                            all_passed = False
                    else:
                        details.append(f"{verse}: ❌ (HTTP {response.status_code})")
                        all_passed = False
                
                if all_passed:
                    self.log_result(test_name, "103:1-3", "PASS", 
                                  f"All verses successful: {', '.join(details)}")
                else:
                    self.log_result(test_name, "103:1-3", "FAIL", 
                                  f"Some verses failed: {', '.join(details)}")
                    
        except Exception as e:
            self.log_result(test_name, "103:1-3", "FAIL", f"Exception: {str(e)}")
    
    async def run_all_tests(self):
        """Run all Tafsir API tests"""
        print(f"🚀 Starting Tafsir API Tests for: {self.base_url}")
        print("=" * 60)
        
        # Run all tests
        await self.test_arabic_tafsir_al_muyassar()
        await self.test_english_ibn_kathir()
        await self.test_russian_al_sadi()
        await self.test_german_fallback_to_english()
        await self.test_invalid_verse_key()
        await self.test_caching_functionality()
        await self.test_multiple_verses_al_asr()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TAFSIR API TEST SUMMARY")
        print("=" * 60)
        
        passed = len([r for r in self.results if r["status"] == "PASS"])
        failed = len([r for r in self.results if r["status"] == "FAIL"])
        skipped = len([r for r in self.results if r["status"] == "SKIP"])
        
        print(f"✅ PASSED: {passed}")
        print(f"❌ FAILED: {failed}")
        print(f"⏭️  SKIPPED: {skipped}")
        print(f"📈 SUCCESS RATE: {passed}/{passed+failed} ({(passed/(passed+failed)*100) if (passed+failed) > 0 else 0:.1f}%)")
        
        # Detailed results
        if failed > 0:
            print("\n🔍 FAILED TESTS DETAILS:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"❌ {result['test']}: {result['details']}")
        
        return self.results

async def main():
    """Main test runner"""
    tester = TafsirAPITester()
    results = await tester.run_all_tests()
    
    # Return results for potential use by other scripts
    return results

if __name__ == "__main__":
    asyncio.run(main())