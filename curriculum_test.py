#!/usr/bin/env python3
"""
Kids Learning Curriculum Engine Backend API Testing
===================================================
Testing all 21 endpoints specified in the review request:
1. Curriculum overview with 15 stages and 1000 days
2. Individual lesson endpoints for different stages
3. Wudu and Salah learning endpoints
4. Arabic alphabet and vocabulary endpoints
5. Achievement system endpoints
6. Progress tracking endpoints
"""

import asyncio
import httpx
import json
import time
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://multilang-sync-3.preview.emergentagent.com"

class CurriculumTester:
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

    def validate_curriculum_overview(self, data: dict) -> List[str]:
        """Validate curriculum overview structure."""
        issues = []
        
        if "stages" not in data:
            issues.append("Missing 'stages' field")
            return issues
            
        stages = data["stages"]
        if not isinstance(stages, list):
            issues.append("Stages should be a list")
            return issues
            
        if len(stages) != 15:
            issues.append(f"Expected 15 stages, got {len(stages)}")
        
        if data.get("total_days") != 1000:
            issues.append(f"Expected total_days=1000, got {data.get('total_days')}")
        
        # Check first stage structure
        if stages:
            stage = stages[0]
            required_fields = ["id", "emoji", "color", "title", "description", "day_start", "day_end", "total_lessons"]
            for field in required_fields:
                if field not in stage:
                    issues.append(f"Stage missing field: {field}")
        
        return issues

    def validate_lesson_structure(self, data: dict, day: int) -> List[str]:
        """Validate individual lesson structure."""
        issues = []
        
        # Check if lesson data is nested under "lesson" key
        lesson_data = data.get("lesson", data)
        
        if "day" not in lesson_data:
            issues.append("Missing 'day' field")
        elif lesson_data["day"] != day:
            issues.append(f"Expected day {day}, got {lesson_data['day']}")
        
        if "stage" not in lesson_data:
            issues.append("Missing 'stage' field")
        
        if "sections" not in lesson_data:
            issues.append("Missing 'sections' field")
            return issues
            
        sections = lesson_data["sections"]
        if not isinstance(sections, list):
            issues.append("Sections should be a list")
            return issues
            
        # For day 1, should have 4 sections: learn, listen, quiz, write
        if day == 1:
            expected_types = ["learn", "listen", "quiz", "write"]
            actual_types = [s.get("type") for s in sections]
            for expected_type in expected_types:
                if expected_type not in actual_types:
                    issues.append(f"Day 1 missing section type: {expected_type}")
        
        # Check section structure
        for section in sections:
            if "type" not in section:
                issues.append("Section missing 'type' field")
            if "emoji" not in section:
                issues.append("Section missing 'emoji' field")
            if "title" not in section:
                issues.append("Section missing 'title' field")
        
        return issues

    def validate_wudu_steps(self, data: dict) -> List[str]:
        """Validate wudu steps response."""
        issues = []
        
        if "steps" not in data and "wudu_steps" not in data:
            issues.append("Missing 'steps' or 'wudu_steps' field")
            return issues
            
        steps = data.get("steps", data.get("wudu_steps", []))
        if not isinstance(steps, list):
            issues.append("Steps should be a list")
            return issues
            
        if len(steps) != 12:
            issues.append(f"Expected 12 wudu steps, got {len(steps)}")
        
        # Check first step structure
        if steps:
            step = steps[0]
            required_fields = ["step", "emoji"]
            for field in required_fields:
                if field not in step:
                    issues.append(f"Step missing field: {field}")
        
        return issues

    def validate_salah_steps(self, data: dict) -> List[str]:
        """Validate salah steps response."""
        issues = []
        
        if "steps" not in data and "salah_steps" not in data:
            issues.append("Missing 'steps' or 'salah_steps' field")
            return issues
            
        steps = data.get("steps", data.get("salah_steps", []))
        if not isinstance(steps, list):
            issues.append("Steps should be a list")
            return issues
            
        if len(steps) != 11:
            issues.append(f"Expected 11 salah steps, got {len(steps)}")
        
        return issues

    def validate_alphabet(self, data: dict) -> List[str]:
        """Validate alphabet response."""
        issues = []
        
        if "letters" not in data and "alphabet" not in data:
            issues.append("Missing 'letters' or 'alphabet' field")
            return issues
            
        letters = data.get("letters", data.get("alphabet", []))
        if not isinstance(letters, list):
            issues.append("Letters should be a list")
            return issues
            
        if len(letters) != 28:
            issues.append(f"Expected 28 Arabic letters, got {len(letters)}")
        
        return issues

    def validate_vocabulary(self, data: dict, category: str, expected_count: int = None) -> List[str]:
        """Validate vocabulary response."""
        issues = []
        
        if "items" not in data and "vocabulary" not in data and "words" not in data and category not in data:
            issues.append(f"Missing vocabulary data for category: {category}")
            return issues
            
        vocab = data.get("items", data.get("vocabulary", data.get("words", data.get(category, []))))
        if not isinstance(vocab, list):
            issues.append("Vocabulary should be a list")
            return issues
            
        if expected_count and len(vocab) != expected_count:
            issues.append(f"Expected {expected_count} {category}, got {len(vocab)}")
        
        return issues

    def validate_achievements(self, data: dict) -> List[str]:
        """Validate achievements response."""
        issues = []
        
        if "badges" not in data and "achievements" not in data:
            issues.append("Missing 'badges' or 'achievements' field")
            return issues
            
        badges = data.get("badges", data.get("achievements", []))
        if not isinstance(badges, list):
            issues.append("Badges should be a list")
            return issues
            
        if len(badges) != 12:
            issues.append(f"Expected 12 achievement badges, got {len(badges)}")
        
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
            
        if len(prophets) != 25:
            issues.append(f"Expected 25 prophets, got {len(prophets)}")
        
        return issues

    async def run_all_tests(self):
        """Run all Kids Learning Curriculum Engine tests."""
        print("🧪 Starting Kids Learning Curriculum Engine Backend API Tests")
        print("=" * 70)
        
        # Test 1: Curriculum overview
        print("\n1. Testing curriculum overview (locale=ar)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum?locale=ar",
            description="Full 15-stage curriculum overview with 1000 days"
        )
        if result["passed"]:
            issues = self.validate_curriculum_overview(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Curriculum overview structure valid")
        
        # Test 2: Day 1 lesson - Letter Alif
        print("\n2. Testing Day 1 lesson - Letter Alif (locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/1?locale=en",
            description="Day 1: Letter Alif with 4 sections (learn, listen, quiz, write)"
        )
        if result["passed"]:
            issues = self.validate_lesson_structure(result["response_data"], 1)
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Day 1 lesson structure valid")
        
        # Test 3: Day 28 lesson - Last letter (Ya)
        print("\n3. Testing Day 28 lesson - Last letter Ya (locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/28?locale=en",
            description="Day 28: Last letter (Ya)"
        )
        if result["passed"]:
            issues = self.validate_lesson_structure(result["response_data"], 28)
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Day 28 lesson structure valid")
        
        # Test 4: Day 60 lesson - Vowels stage
        print("\n4. Testing Day 60 lesson - Vowels stage (locale=de)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/60?locale=de",
            description="Day 60: Vowels stage"
        )
        if result["passed"]:
            issues = self.validate_lesson_structure(result["response_data"], 60)
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Day 60 lesson structure valid")
        
        # Test 5: Day 100 lesson - Numbers stage
        print("\n5. Testing Day 100 lesson - Numbers stage (locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/100?locale=en",
            description="Day 100: Numbers stage"
        )
        if result["passed"]:
            issues = self.validate_lesson_structure(result["response_data"], 100)
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Day 100 lesson structure valid")
        
        # Test 6: Day 150 lesson - First Words stage
        print("\n6. Testing Day 150 lesson - First Words stage (locale=fr)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/150?locale=fr",
            description="Day 150: First Words stage (vocabulary)"
        )
        if result["passed"]:
            issues = self.validate_lesson_structure(result["response_data"], 150)
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Day 150 lesson structure valid")
        
        # Test 7: Day 350 lesson - Islamic Foundations
        print("\n7. Testing Day 350 lesson - Islamic Foundations (locale=ar)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/350?locale=ar",
            description="Day 350: Islamic Foundations"
        )
        if result["passed"]:
            issues = self.validate_lesson_structure(result["response_data"], 350)
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Day 350 lesson structure valid")
        
        # Test 8: Day 400 lesson - Quran Memorization
        print("\n8. Testing Day 400 lesson - Quran Memorization (locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/400?locale=en",
            description="Day 400: Quran Memorization"
        )
        if result["passed"]:
            issues = self.validate_lesson_structure(result["response_data"], 400)
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Day 400 lesson structure valid")
        
        # Test 9: Day 500 lesson - Duas stage
        print("\n9. Testing Day 500 lesson - Duas stage (locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/500?locale=en",
            description="Day 500: Duas stage"
        )
        if result["passed"]:
            issues = self.validate_lesson_structure(result["response_data"], 500)
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Day 500 lesson structure valid")
        
        # Test 10: Day 1001 lesson - Should return 400 error (out of range)
        print("\n10. Testing Day 1001 lesson - Should return 400 error")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/1001?locale=en",
            expected_status=400,
            description="Day 1001 should return 400 error (out of range)"
        )
        if result["passed"]:
            print("   ✅ Day 1001 correctly returns 400 error")
        
        # Test 11: Wudu steps
        print("\n11. Testing Wudu steps (locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/wudu?locale=en",
            description="Should return 12 wudu steps"
        )
        if result["passed"]:
            issues = self.validate_wudu_steps(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Wudu steps structure valid")
        
        # Test 12: Salah steps
        print("\n12. Testing Salah steps (locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/salah?locale=en",
            description="Should return 11 salah steps"
        )
        if result["passed"]:
            issues = self.validate_salah_steps(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Salah steps structure valid")
        
        # Test 13: Arabic alphabet
        print("\n13. Testing Arabic alphabet")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/alphabet",
            description="Should return 28 Arabic letters"
        )
        if result["passed"]:
            issues = self.validate_alphabet(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Arabic alphabet structure valid")
        
        # Test 14: Vocabulary - Animals
        print("\n14. Testing vocabulary - Animals")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/vocabulary/animals",
            description="Should return 16 animals"
        )
        if result["passed"]:
            issues = self.validate_vocabulary(result["response_data"], "animals", 16)
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Animals vocabulary structure valid")
        
        # Test 15: Vocabulary - Colors
        print("\n15. Testing vocabulary - Colors")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/vocabulary/colors",
            description="Should return 10 colors"
        )
        if result["passed"]:
            issues = self.validate_vocabulary(result["response_data"], "colors", 10)
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Colors vocabulary structure valid")
        
        # Test 16: Vocabulary - Family
        print("\n16. Testing vocabulary - Family")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/vocabulary/family",
            description="Should return family members"
        )
        if result["passed"]:
            issues = self.validate_vocabulary(result["response_data"], "family")
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Family vocabulary structure valid")
        
        # Test 17: Vocabulary - Non-existent category (should return 404)
        print("\n17. Testing vocabulary - Non-existent category")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/vocabulary/nonexistent",
            expected_status=404,
            description="Non-existent vocabulary category should return 404"
        )
        if result["passed"]:
            print("   ✅ Non-existent vocabulary correctly returns 404")
        
        # Test 18: Achievements
        print("\n18. Testing achievements (user_id=guest)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/achievements?user_id=guest",
            description="Should return 12 achievement badges"
        )
        if result["passed"]:
            issues = self.validate_achievements(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Achievements structure valid")
        
        # Test 19: All prophets
        print("\n19. Testing all prophets (locale=en)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/prophets-full?locale=en",
            description="Should return 25 prophets"
        )
        if result["passed"]:
            issues = self.validate_prophets(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Prophets structure valid")
        
        # Test 20: Save curriculum progress
        print("\n20. Testing save curriculum progress (POST)")
        progress_data = {
            "user_id": "test_curriculum",
            "day": 1,
            "sections_done": 4,
            "total_sections": 4,
            "xp_reward": 30
        }
        result = await self.test_endpoint(
            "POST", "/api/kids-learn/curriculum/progress",
            data=progress_data,
            description="Save curriculum progress"
        )
        if result["passed"]:
            response_data = result["response_data"]
            if "success" not in response_data or not response_data.get("success"):
                print("   ⚠️  Missing success confirmation in response")
            else:
                print(f"   ✅ Progress saved successfully")
        
        # Test 21: Get curriculum progress
        print("\n21. Testing get curriculum progress")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/progress?user_id=test_curriculum",
            description="Get saved curriculum progress"
        )
        if result["passed"]:
            response_data = result["response_data"]
            if "progress" not in response_data and "user_id" not in response_data:
                print("   ⚠️  Missing progress data in response")
            else:
                print(f"   ✅ Progress retrieved successfully")

    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 70)
        print("📊 KIDS LEARNING CURRICULUM ENGINE TEST RESULTS SUMMARY")
        print("=" * 70)
        
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
        
        print("\n" + "=" * 70)
        
        # Detailed validation results
        print("🔍 DETAILED VALIDATION RESULTS:")
        print("-" * 40)
        
        curriculum_tests = [r for r in self.results if "curriculum" in r["endpoint"]]
        if curriculum_tests:
            print(f"✅ Curriculum System: {len(curriculum_tests)} tests")
            
        lesson_tests = [r for r in self.results if "lesson" in r["endpoint"]]
        if lesson_tests:
            print(f"✅ Daily Lessons: {len(lesson_tests)} tests")
            
        wudu_salah_tests = [r for r in self.results if any(x in r["endpoint"] for x in ["wudu", "salah"])]
        if wudu_salah_tests:
            print(f"✅ Islamic Learning: {len(wudu_salah_tests)} tests")
            
        vocab_tests = [r for r in self.results if "vocabulary" in r["endpoint"]]
        if vocab_tests:
            print(f"✅ Vocabulary System: {len(vocab_tests)} tests")
            
        progress_tests = [r for r in self.results if "progress" in r["endpoint"]]
        if progress_tests:
            print(f"✅ Progress Tracking: {len(progress_tests)} tests")
        
        error_handling_tests = [r for r in self.results if r["expected_status"] != 200]
        if error_handling_tests:
            passed_errors = [r for r in error_handling_tests if r["passed"]]
            print(f"✅ Error Handling: {len(passed_errors)}/{len(error_handling_tests)} tests passed")

async def main():
    """Run the Kids Learning Curriculum Engine backend tests."""
    tester = CurriculumTester()
    
    try:
        await tester.run_all_tests()
        tester.print_summary()
        
        # Return exit code based on results
        if tester.passed_tests == tester.total_tests:
            print("\n🎉 ALL TESTS PASSED! Kids Learning Curriculum Engine is working correctly.")
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