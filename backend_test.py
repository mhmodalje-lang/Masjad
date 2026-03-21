#!/usr/bin/env python3
"""
Kids Learning System Backend API Testing
========================================
Testing all 16 endpoints specified in the review request:
1. Daily lessons with comprehensive content
2. Quran memorization system
3. Duas for kids
4. Hadiths for kids  
5. Prophet stories
6. Islamic pillars
7. Library system
8. Progress tracking
"""

import asyncio
import httpx
import json
import time
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://kids-learning-hub-25.preview.emergentagent.com"

class KidsLearningTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    async def test_endpoint(self, method: str, endpoint: str, expected_status: int = 200, 
                          data: dict = None, description: str = "") -> dict:
        """Test a single endpoint and return results."""
        self.total_tests += 1
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                url = f"{self.base_url}{endpoint}"
                
                if method.upper() == "GET":
                    response = await client.get(url)
                elif method.upper() == "POST":
                    response = await client.post(url, json=data)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                response_time = time.time() - start_time
                
                # Parse response
                try:
                    response_data = response.json()
                except:
                    response_data = {"raw_response": response.text}
                
                # Determine if test passed
                status_ok = response.status_code == expected_status
                has_success = response_data.get("success", True) if expected_status == 200 else True
                
                test_passed = status_ok and has_success
                if test_passed:
                    self.passed_tests += 1
                
                result = {
                    "endpoint": endpoint,
                    "method": method.upper(),
                    "description": description,
                    "status_code": response.status_code,
                    "expected_status": expected_status,
                    "response_time": round(response_time, 3),
                    "passed": test_passed,
                    "response_data": response_data,
                    "error": None
                }
                
                self.results.append(result)
                return result
                
        except Exception as e:
            response_time = time.time() - start_time
            result = {
                "endpoint": endpoint,
                "method": method.upper(), 
                "description": description,
                "status_code": 0,
                "expected_status": expected_status,
                "response_time": round(response_time, 3),
                "passed": False,
                "response_data": {},
                "error": str(e)
            }
            self.results.append(result)
            return result

    def validate_daily_lesson(self, data: dict) -> List[str]:
        """Validate daily lesson structure."""
        issues = []
        
        # Check required sections
        required_sections = ["quran", "dua", "hadith", "story", "islamic_knowledge", "library_pick", "activity"]
        for section in required_sections:
            if section not in data:
                issues.append(f"Missing required section: {section}")
        
        # Validate Quran section
        if "quran" in data:
            quran = data["quran"]
            if "ayah" not in quran:
                issues.append("Quran section missing ayah")
            elif "arabic" not in quran["ayah"] or "translation" not in quran["ayah"]:
                issues.append("Quran ayah missing arabic or translation")
        
        # Validate Dua section
        if "dua" in data:
            dua = data["dua"]
            if "arabic" not in dua or "transliteration" not in dua:
                issues.append("Dua section missing arabic or transliteration")
        
        return issues

    def validate_quran_surahs(self, data: dict) -> List[str]:
        """Validate Quran surahs response."""
        issues = []
        
        if "surahs" not in data:
            issues.append("Missing 'surahs' field")
            return issues
            
        surahs = data["surahs"]
        if not isinstance(surahs, list):
            issues.append("Surahs should be a list")
            return issues
            
        if len(surahs) != 8:
            issues.append(f"Expected 8 surahs, got {len(surahs)}")
        
        # Check first surah structure
        if surahs:
            surah = surahs[0]
            required_fields = ["id", "name_ar", "name_en", "total_ayahs"]
            for field in required_fields:
                if field not in surah:
                    issues.append(f"Surah missing field: {field}")
        
        return issues

    def validate_surah_detail(self, data: dict) -> List[str]:
        """Validate individual surah detail."""
        issues = []
        
        if "surah" not in data:
            issues.append("Missing 'surah' field")
            return issues
            
        surah = data["surah"]
        if "ayahs" not in surah:
            issues.append("Surah missing ayahs")
            return issues
            
        ayahs = surah["ayahs"]
        if not isinstance(ayahs, list) or len(ayahs) == 0:
            issues.append("Surah should have ayahs list")
            return issues
            
        # Check first ayah structure
        ayah = ayahs[0]
        if "ar" not in ayah:
            issues.append("Ayah missing Arabic text")
        
        return issues

    def validate_duas(self, data: dict) -> List[str]:
        """Validate duas response."""
        issues = []
        
        if "duas" not in data:
            issues.append("Missing 'duas' field")
            return issues
            
        duas = data["duas"]
        if not isinstance(duas, list):
            issues.append("Duas should be a list")
            return issues
            
        if len(duas) != 15:
            issues.append(f"Expected 15 duas, got {len(duas)}")
        
        # Check first dua structure
        if duas:
            dua = duas[0]
            required_fields = ["ar", "transliteration", "title"]
            for field in required_fields:
                if field not in dua:
                    issues.append(f"Dua missing field: {field}")
        
        return issues

    def validate_hadiths(self, data: dict) -> List[str]:
        """Validate hadiths response."""
        issues = []
        
        if "hadiths" not in data:
            issues.append("Missing 'hadiths' field")
            return issues
            
        hadiths = data["hadiths"]
        if not isinstance(hadiths, list):
            issues.append("Hadiths should be a list")
            return issues
            
        if len(hadiths) != 10:
            issues.append(f"Expected 10 hadiths, got {len(hadiths)}")
        
        return issues

    def validate_prophets(self, data: dict) -> List[str]:
        """Validate prophets response."""
        issues = []
        
        if "prophets" not in data:
            issues.append("Missing 'prophets' field")
            return issues
            
        prophets = data["prophets"]
        if not isinstance(prophets, list):
            issues.append("Prophets should be a list")
            return issues
            
        if len(prophets) != 6:
            issues.append(f"Expected 6 prophets, got {len(prophets)}")
        
        return issues

    def validate_progress(self, data: dict) -> List[str]:
        """Validate progress response."""
        issues = []
        
        required_fields = ["user_id", "completed_days", "total_xp", "current_level"]
        for field in required_fields:
            if field not in data:
                issues.append(f"Progress missing field: {field}")
        
        return issues

    async def run_all_tests(self):
        """Run all Kids Learning System tests."""
        print("🧪 Starting Kids Learning System Backend API Tests")
        print("=" * 60)
        
        # Test 1: Daily lesson in Arabic (day 1)
        print("\n1. Testing daily lesson (day=1, locale=ar)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/daily-lesson?day=1&locale=ar",
            description="Daily lesson day 1 in Arabic"
        )
        if result["passed"]:
            issues = self.validate_daily_lesson(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Daily lesson structure valid")
        
        # Test 2: Daily lesson in German (day 5)
        print("\n2. Testing daily lesson (day=5, locale=de)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/daily-lesson?day=5&locale=de",
            description="Daily lesson day 5 in German"
        )
        if result["passed"]:
            issues = self.validate_daily_lesson(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Daily lesson structure valid")
        
        # Test 3: Quran surahs list
        print("\n3. Testing Quran surahs list (locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/quran/surahs?locale=en",
            description="List of 8 surahs for kids memorization"
        )
        if result["passed"]:
            issues = self.validate_quran_surahs(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Quran surahs structure valid")
        
        # Test 4: Specific surah detail (Al-Fatiha in French)
        print("\n4. Testing surah detail (fatiha, locale=fr)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/quran/surah/fatiha?locale=fr",
            description="Al-Fatiha with 7 ayahs in French"
        )
        if result["passed"]:
            issues = self.validate_surah_detail(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Surah detail structure valid")
        
        # Test 5: Non-existent surah (should return 404)
        print("\n5. Testing non-existent surah (should return 404)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/quran/surah/nonexistent",
            expected_status=404,
            description="Non-existent surah should return 404"
        )
        
        # Test 6: All duas in Turkish
        print("\n6. Testing all duas (locale=tr)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/duas?locale=tr",
            description="15 duas with Turkish titles"
        )
        if result["passed"]:
            issues = self.validate_duas(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Duas structure valid")
        
        # Test 7: Filtered duas by category
        print("\n7. Testing duas by category (daily, locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/duas?category=daily&locale=en",
            description="Daily category duas only"
        )
        
        # Test 8: Hadiths in Russian
        print("\n8. Testing hadiths (locale=ru)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/hadiths?locale=ru",
            description="10 hadiths with Russian translations"
        )
        if result["passed"]:
            issues = self.validate_hadiths(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Hadiths structure valid")
        
        # Test 9: Prophet stories in Arabic
        print("\n9. Testing prophet stories (locale=ar)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/prophets?locale=ar",
            description="6 prophet stories"
        )
        if result["passed"]:
            issues = self.validate_prophets(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Prophets structure valid")
        
        # Test 10: Specific prophet story (Ibrahim in English)
        print("\n10. Testing specific prophet (ibrahim, locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/prophets/ibrahim?locale=en",
            description="Ibrahim's story detail"
        )
        
        # Test 11: Non-existent prophet (should return 404)
        print("\n11. Testing non-existent prophet (should return 404)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/prophets/nonexistent",
            expected_status=404,
            description="Non-existent prophet should return 404"
        )
        
        # Test 12: Islamic pillars in German
        print("\n12. Testing Islamic pillars (locale=de)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/islamic-pillars?locale=de",
            description="5 pillars of Islam"
        )
        
        # Test 13: Library categories in Arabic
        print("\n13. Testing library categories (locale=ar)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/library/categories?locale=ar",
            description="8 library categories"
        )
        
        # Test 14: Library items by category
        print("\n14. Testing library items (category=quran_stories, locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/library/items?category=quran_stories&locale=en",
            description="Library items filtered by category"
        )
        
        # Test 15: Get progress for new user
        print("\n15. Testing progress retrieval (user_id=test_kid)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/progress?user_id=test_kid",
            description="Progress for new user (should be empty)"
        )
        
        # Test 16: Save progress
        print("\n16. Testing progress saving (POST)")
        progress_data = {
            "user_id": "test_kid",
            "day": 1,
            "sections_completed": ["quran", "dua", "hadith"]
        }
        result = await self.test_endpoint(
            "POST", "/api/kids-learn/progress",
            data=progress_data,
            description="Save progress and return XP earned"
        )
        if result["passed"]:
            response_data = result["response_data"]
            if "xp_earned" not in response_data:
                print("   ⚠️  Missing xp_earned in response")
            else:
                print(f"   ✅ Progress saved, XP earned: {response_data.get('xp_earned', 0)}")

    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 60)
        print("📊 KIDS LEARNING SYSTEM TEST RESULTS SUMMARY")
        print("=" * 60)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        avg_response_time = sum(r["response_time"] for r in self.results) / len(self.results) if self.results else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.total_tests - self.passed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Average Response Time: {avg_response_time:.3f}s")
        
        # Show failed tests
        failed_tests = [r for r in self.results if not r["passed"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   • {test['method']} {test['endpoint']}")
                print(f"     Status: {test['status_code']} (expected {test['expected_status']})")
                if test['error']:
                    print(f"     Error: {test['error']}")
                print()
        
        # Show successful tests
        passed_tests = [r for r in self.results if r["passed"]]
        if passed_tests:
            print(f"✅ PASSED TESTS ({len(passed_tests)}):")
            for test in passed_tests:
                print(f"   • {test['method']} {test['endpoint']} ({test['response_time']}s)")
        
        print("\n" + "=" * 60)
        
        # Detailed validation results
        print("🔍 DETAILED VALIDATION RESULTS:")
        print("-" * 40)
        
        multilingual_tests = [r for r in self.results if "locale=" in r["endpoint"]]
        if multilingual_tests:
            print(f"✅ Multilingual Support: {len(multilingual_tests)} endpoints tested")
            locales_tested = set()
            for test in multilingual_tests:
                if "locale=" in test["endpoint"]:
                    locale = test["endpoint"].split("locale=")[1].split("&")[0]
                    locales_tested.add(locale)
            print(f"   Languages tested: {', '.join(sorted(locales_tested))}")
        
        daily_lesson_tests = [r for r in self.results if "daily-lesson" in r["endpoint"]]
        if daily_lesson_tests:
            print(f"✅ Daily Lessons: {len(daily_lesson_tests)} tests")
            
        quran_tests = [r for r in self.results if "/quran/" in r["endpoint"]]
        if quran_tests:
            print(f"✅ Quran System: {len(quran_tests)} tests")
            
        progress_tests = [r for r in self.results if "progress" in r["endpoint"]]
        if progress_tests:
            print(f"✅ Progress Tracking: {len(progress_tests)} tests")
        
        error_handling_tests = [r for r in self.results if r["expected_status"] == 404]
        if error_handling_tests:
            passed_404 = [r for r in error_handling_tests if r["passed"]]
            print(f"✅ Error Handling: {len(passed_404)}/{len(error_handling_tests)} 404 tests passed")

async def main():
    """Run the Kids Learning System backend tests."""
    tester = KidsLearningTester()
    
    try:
        await tester.run_all_tests()
        tester.print_summary()
        
        # Return exit code based on results
        if tester.passed_tests == tester.total_tests:
            print("\n🎉 ALL TESTS PASSED! Kids Learning System is working correctly.")
            return 0
        else:
            print(f"\n⚠️  {tester.total_tests - tester.passed_tests} tests failed. Please check the issues above.")
            return 1
            
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        return 1

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)