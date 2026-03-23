#!/usr/bin/env python3
"""
Islamic App Backend API Testing Script
Tests the specific multilingual endpoints requested in the review request
"""

import asyncio
import httpx
import json
from typing import Dict, Any, List

# Backend URL from frontend .env
BACKEND_URL = "https://quran-integrity-1.preview.emergentagent.com"

class IslamicAppAPITester:
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
    
    async def test_health_endpoint(self):
        """Test Health Check - GET /api/health"""
        test_name = "Health Check API"
        endpoint = "/api/health"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "status" in data and data["status"] == "healthy":
                        self.log_result(test_name, endpoint, "PASS", 
                                      f"Health check successful: {data}")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"Invalid health response: {data}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_quran_surahs_russian(self):
        """Test Quran Surahs Russian - GET /api/kids-learn/quran/surahs?locale=ru"""
        test_name = "Quran Surahs Russian Locale"
        endpoint = "/api/kids-learn/quran/surahs?locale=ru"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "success" in data and data["success"] and "surahs" in data:
                        surahs = data["surahs"]
                        
                        if len(surahs) > 0:
                            # Check first surah structure
                            surah = surahs[0]
                            required_fields = ["id", "number", "name_ar", "name_en"]
                            missing_fields = [field for field in required_fields if field not in surah]
                            
                            if not missing_fields:
                                self.log_result(test_name, endpoint, "PASS", 
                                              f"Returned {len(surahs)} surahs with Russian locale support")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"Missing fields in surah: {missing_fields}")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          "No surahs returned")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      "Response missing 'success' or 'surahs' fields")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_surah_fatiha_russian(self):
        """Test Surah Fatiha Russian - GET /api/kids-learn/quran/surah/fatiha?locale=ru"""
        test_name = "Surah Fatiha Russian Translations"
        endpoint = "/api/kids-learn/quran/surah/fatiha?locale=ru"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "success" in data and data["success"] and "surah" in data:
                        surah = data["surah"]
                        
                        if "ayahs" in surah and len(surah["ayahs"]) > 0:
                            # Check first ayah structure
                            ayah = surah["ayahs"][0]
                            required_fields = ["number", "arabic", "translation"]
                            missing_fields = [field for field in required_fields if field not in ayah]
                            
                            if not missing_fields:
                                self.log_result(test_name, endpoint, "PASS", 
                                              f"Returned Fatiha with {len(surah['ayahs'])} ayahs and Russian translations")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"Missing fields in ayah: {missing_fields}")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          "No ayahs returned for Fatiha")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      "Response missing 'success' or 'surah' fields")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_daily_lesson_arabic(self):
        """Test Daily Lesson Arabic - GET /api/kids-learn/daily-lesson?locale=ar"""
        test_name = "Daily Lesson Arabic Locale"
        endpoint = "/api/kids-learn/daily-lesson?locale=ar"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "success" in data and data["success"] and "lesson" in data:
                        lesson = data["lesson"]
                        
                        # Check lesson structure
                        if isinstance(lesson, dict) and len(lesson) > 0:
                            self.log_result(test_name, endpoint, "PASS", 
                                          f"Returned Arabic daily lesson with {len(lesson)} sections")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          "Empty or invalid lesson structure")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      "Response missing 'success' or 'lesson' fields")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_daily_lesson_russian(self):
        """Test Daily Lesson Russian - GET /api/kids-learn/daily-lesson?locale=ru"""
        test_name = "Daily Lesson Russian Locale"
        endpoint = "/api/kids-learn/daily-lesson?locale=ru"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "success" in data and data["success"] and "lesson" in data:
                        lesson = data["lesson"]
                        
                        # Check lesson structure
                        if isinstance(lesson, dict) and len(lesson) > 0:
                            self.log_result(test_name, endpoint, "PASS", 
                                          f"Returned Russian daily lesson with {len(lesson)} sections")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          "Empty or invalid lesson structure")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      "Response missing 'success' or 'lesson' fields")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_duas_german(self):
        """Test Duas German - GET /api/kids-learn/duas?locale=de"""
        test_name = "Duas German Locale"
        endpoint = "/api/kids-learn/duas?locale=de"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "success" in data and data["success"] and "duas" in data:
                        duas = data["duas"]
                        
                        if len(duas) > 0:
                            # Check first dua structure
                            dua = duas[0]
                            required_fields = ["id", "category", "arabic", "title"]
                            missing_fields = [field for field in required_fields if field not in dua]
                            
                            if not missing_fields:
                                self.log_result(test_name, endpoint, "PASS", 
                                              f"Returned {len(duas)} duas with German locale support")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"Missing fields in dua: {missing_fields}")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          "No duas returned")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      "Response missing 'success' or 'duas' fields")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_hadiths_french(self):
        """Test Hadiths French - GET /api/kids-learn/hadiths?locale=fr"""
        test_name = "Hadiths French Locale"
        endpoint = "/api/kids-learn/hadiths?locale=fr"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "success" in data and data["success"] and "hadiths" in data:
                        hadiths = data["hadiths"]
                        
                        if len(hadiths) > 0:
                            # Check first hadith structure
                            hadith = hadiths[0]
                            required_fields = ["id", "category", "arabic", "lesson"]
                            missing_fields = [field for field in required_fields if field not in hadith]
                            
                            if not missing_fields:
                                self.log_result(test_name, endpoint, "PASS", 
                                              f"Returned {len(hadiths)} hadiths with French locale support")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"Missing fields in hadith: {missing_fields}")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          "No hadiths returned")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      "Response missing 'success' or 'hadiths' fields")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_prophets_turkish(self):
        """Test Prophets Turkish - GET /api/kids-learn/prophets?locale=tr"""
        test_name = "Prophets Turkish Locale"
        endpoint = "/api/kids-learn/prophets?locale=tr"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "success" in data and data["success"] and "prophets" in data:
                        prophets = data["prophets"]
                        
                        if len(prophets) > 0:
                            # Check first prophet structure
                            prophet = prophets[0]
                            required_fields = ["id", "number", "name", "title"]
                            missing_fields = [field for field in required_fields if field not in prophet]
                            
                            if not missing_fields:
                                self.log_result(test_name, endpoint, "PASS", 
                                              f"Returned {len(prophets)} prophets with Turkish locale support")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"Missing fields in prophet: {missing_fields}")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          "No prophets returned")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      "Response missing 'success' or 'prophets' fields")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_data_deletion_request(self):
        """Test Data Deletion Request - POST /api/data-deletion-request"""
        test_name = "Data Deletion Request API"
        endpoint = "/api/data-deletion-request"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                payload = {
                    "email": "test@test.com",
                    "reason": "test"
                }
                response = await client.post(f"{self.base_url}{endpoint}", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "success" in data and data["success"]:
                        self.log_result(test_name, endpoint, "PASS", 
                                      f"Data deletion request submitted successfully: {data.get('message', '')}")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"Invalid response structure: {data}")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_app_ads_txt(self):
        """Test App Ads Txt - GET /api/app-ads-txt"""
        test_name = "App Ads Txt API"
        endpoint = "/api/app-ads-txt"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    content = response.text
                    content_type = response.headers.get("content-type", "")
                    
                    # Check content type
                    if "text/plain" in content_type:
                        self.log_result(test_name, endpoint, "PASS", 
                                      f"Returned text/plain content: {content[:100]}...")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      f"Wrong content type: {content_type}, expected text/plain")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def run_all_tests(self):
        """Run all Islamic App API tests"""
        print(f"🚀 Starting Islamic App Backend API Tests for: {self.base_url}")
        print("=" * 80)
        
        # Run all tests
        await self.test_health_endpoint()
        await self.test_quran_surahs_russian()
        await self.test_surah_fatiha_russian()
        await self.test_daily_lesson_arabic()
        await self.test_daily_lesson_russian()
        await self.test_duas_german()
        await self.test_hadiths_french()
        await self.test_prophets_turkish()
        await self.test_data_deletion_request()
        await self.test_app_ads_txt()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 ISLAMIC APP API TEST SUMMARY")
        print("=" * 80)
        
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
        
        # Multilingual verification summary
        print("\n🌍 MULTILINGUAL ENDPOINT VERIFICATION:")
        multilingual_tests = [
            ("Russian", "Quran Surahs Russian Locale"),
            ("Russian", "Surah Fatiha Russian Translations"),
            ("Arabic", "Daily Lesson Arabic Locale"),
            ("Russian", "Daily Lesson Russian Locale"),
            ("German", "Duas German Locale"),
            ("French", "Hadiths French Locale"),
            ("Turkish", "Prophets Turkish Locale")
        ]
        
        for lang, test_name in multilingual_tests:
            result = next((r for r in self.results if r["test"] == test_name), None)
            if result:
                status_icon = "✅" if result["status"] == "PASS" else "❌"
                print(f"{status_icon} {lang}: {result['status']}")
        
        return self.results

async def main():
    """Main test runner"""
    tester = IslamicAppAPITester()
    results = await tester.run_all_tests()
    
    # Save results to JSON file for future reference
    with open("/app/islamic_app_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return results

if __name__ == "__main__":
    asyncio.run(main())