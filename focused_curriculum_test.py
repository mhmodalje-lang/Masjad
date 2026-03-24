#!/usr/bin/env python3
"""
Kids Curriculum Localization Fix Testing - Focused Validation
============================================================
Testing the specific requirements from the review request:
1. No "english" keys in non-English responses
2. Specific translation validations for key lessons
3. Verify English and Arabic still work
"""

import asyncio
import httpx
import json
import time
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://kidszone-learn.preview.emergentagent.com"

class FocusedCurriculumTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.critical_issues = []
        
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
                    response_text = response.text
                except:
                    response_data = {"raw_response": response.text}
                    response_text = response.text
                
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
                    "response_text": response_text,
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
                "response_text": "",
                "error": str(e)
            }
            self.results.append(result)
            return result

    def check_for_english_keys(self, response_text: str, locale: str) -> List[str]:
        """Check if response contains 'english' as a key (should not exist for non-English locales)."""
        issues = []
        
        if locale not in ["en", "ar"]:  # Only check non-English, non-Arabic locales
            # Look for "english" as a JSON key (case insensitive)
            if '"english"' in response_text.lower():
                issues.append(f"Found 'english' key in response for locale {locale}")
                self.critical_issues.append(f"CRITICAL: 'english' key found in {locale} response")
        
        return issues

    def validate_specific_translations(self, data: dict, locale: str, lesson_day: int) -> List[str]:
        """Validate specific translations as required in the review request."""
        issues = []
        
        if "lesson" not in data:
            issues.append("Missing 'lesson' field")
            return issues
            
        lesson = data["lesson"]
        
        # Check lesson title has locale key
        if "title" in lesson and isinstance(lesson["title"], dict):
            if locale not in lesson["title"]:
                issues.append(f"Lesson title missing '{locale}' key")
                self.critical_issues.append(f"CRITICAL: Lesson title missing {locale} translation")
        
        # Check sections content for specific validations
        if "sections" in lesson and lesson["sections"]:
            section = lesson["sections"][0]  # Check first section
            if "content" in section:
                content = section["content"]
                
                # Specific validations based on lesson and locale
                if lesson_day == 1 and locale == "de":
                    # Day 1 German: example_translated should be "Löwe"
                    if "example_translated" in content:
                        if content["example_translated"] != "Löwe":
                            issues.append(f"German example should be 'Löwe', got '{content['example_translated']}'")
                            self.critical_issues.append("CRITICAL: German example not 'Löwe'")
                    else:
                        issues.append("Missing example_translated field")
                        self.critical_issues.append("CRITICAL: Missing example_translated field")
                
                elif lesson_day == 85 and locale == "tr":
                    # Day 85 Turkish: translated should be "Sıfır"
                    if "translated" in content:
                        if content["translated"] != "Sıfır":
                            issues.append(f"Turkish number should be 'Sıfır', got '{content['translated']}'")
                            self.critical_issues.append("CRITICAL: Turkish number not 'Sıfır'")
                    else:
                        issues.append("Missing translated field")
                        self.critical_issues.append("CRITICAL: Missing translated field")
                
                elif lesson_day == 211 and locale == "fr":
                    # Day 211 French: translated should be "C'est un livre"
                    if "translated" in content:
                        if content["translated"] != "C'est un livre":
                            issues.append(f"French sentence should be 'C'est un livre', got '{content['translated']}'")
                            self.critical_issues.append("CRITICAL: French sentence not 'C'est un livre'")
                    else:
                        issues.append("Missing translated field")
                        self.critical_issues.append("CRITICAL: Missing translated field")
                
                elif lesson_day == 1 and locale == "en":
                    # Day 1 English: example_translated should be "Lion"
                    if "example_translated" in content:
                        if content["example_translated"] != "Lion":
                            issues.append(f"English example should be 'Lion', got '{content['example_translated']}'")
                            self.critical_issues.append("CRITICAL: English example not 'Lion'")
                    else:
                        issues.append("Missing example_translated field")
                        self.critical_issues.append("CRITICAL: Missing example_translated field")
                
                # Check for any "english" keys in content
                if "english" in content:
                    issues.append("Found 'english' key in section content")
                    self.critical_issues.append(f"CRITICAL: 'english' key found in lesson content for {locale}")
        
        return issues

    async def run_focused_tests(self):
        """Run focused curriculum localization tests based on review request."""
        print("🧪 Starting Focused Kids Curriculum Localization Tests")
        print("=" * 60)
        
        # Test 1: Curriculum Overview - German
        print("\n1. Testing curriculum overview (locale=de)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum?locale=de",
            description="German curriculum overview - verify no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "de")
            if english_issues:
                print(f"   ❌ Issues: {'; '.join(english_issues)}")
            else:
                print("   ✅ German curriculum overview - no 'english' keys found")
        
        # Test 2: Day 1 (Alphabet) - German
        print("\n2. Testing Day 1 Alphabet lesson (locale=de)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/1?locale=de",
            description="Day 1 German - example_translated='Löwe', no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "de")
            validation_issues = self.validate_specific_translations(result["response_data"], "de", 1)
            all_issues = english_issues + validation_issues
            if all_issues:
                print(f"   ❌ Issues: {'; '.join(all_issues)}")
            else:
                print("   ✅ Day 1 German lesson - example_translated='Löwe', no 'english' keys")
        
        # Test 3: Day 85 (Numbers) - Turkish
        print("\n3. Testing Day 85 Numbers lesson (locale=tr)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/85?locale=tr",
            description="Day 85 Turkish - translated='Sıfır', no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "tr")
            validation_issues = self.validate_specific_translations(result["response_data"], "tr", 85)
            all_issues = english_issues + validation_issues
            if all_issues:
                print(f"   ❌ Issues: {'; '.join(all_issues)}")
            else:
                print("   ✅ Day 85 Turkish lesson - translated='Sıfır', no 'english' keys")
        
        # Test 4: Day 113 (Words) - Swedish
        print("\n4. Testing Day 113 Words lesson (locale=sv)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/113?locale=sv",
            description="Day 113 Swedish - verify no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "sv")
            if english_issues:
                print(f"   ❌ Issues: {'; '.join(english_issues)}")
            else:
                print("   ✅ Day 113 Swedish lesson - no 'english' keys found")
        
        # Test 5: Day 211 (Sentences) - French
        print("\n5. Testing Day 211 Sentences lesson (locale=fr)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/211?locale=fr",
            description="Day 211 French - translated='C'est un livre', no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "fr")
            validation_issues = self.validate_specific_translations(result["response_data"], "fr", 211)
            all_issues = english_issues + validation_issues
            if all_issues:
                print(f"   ❌ Issues: {'; '.join(all_issues)}")
            else:
                print("   ✅ Day 211 French lesson - translated='C'est un livre', no 'english' keys")
        
        # Test 6: Day 267 (Reading) - Dutch
        print("\n6. Testing Day 267 Reading lesson (locale=nl)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/267?locale=nl",
            description="Day 267 Dutch - verify no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "nl")
            if english_issues:
                print(f"   ❌ Issues: {'; '.join(english_issues)}")
            else:
                print("   ✅ Day 267 Dutch lesson - no 'english' keys found")
        
        # Test 7: Day 57 (Vowels/Harakat) - Russian
        print("\n7. Testing Day 57 Vowels lesson (locale=ru)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/57?locale=ru",
            description="Day 57 Russian - verify no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "ru")
            if english_issues:
                print(f"   ❌ Issues: {'; '.join(english_issues)}")
            else:
                print("   ✅ Day 57 Russian lesson - no 'english' keys found")
        
        # Test 8: Verify English still works
        print("\n8. Testing Day 1 lesson (locale=en) - English should still work")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/1?locale=en",
            description="Day 1 English - example_translated='Lion'"
        )
        if result["passed"]:
            validation_issues = self.validate_specific_translations(result["response_data"], "en", 1)
            if validation_issues:
                print(f"   ❌ Issues: {'; '.join(validation_issues)}")
            else:
                print("   ✅ Day 1 English lesson - example_translated='Lion'")
        
        # Test 9: Verify Arabic still works
        print("\n9. Testing Day 1 lesson (locale=ar) - Arabic should still work")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/1?locale=ar",
            description="Day 1 Arabic - verify working"
        )
        if result["passed"]:
            print("   ✅ Day 1 Arabic lesson working correctly")
        else:
            print("   ❌ Day 1 Arabic lesson failed")

    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 60)
        print("📊 FOCUSED CURRICULUM LOCALIZATION TEST SUMMARY")
        print("=" * 60)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        avg_response_time = sum(r["response_time"] for r in self.results) / len(self.results) if self.results else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.total_tests - self.passed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Average Response Time: {avg_response_time:.3f}s")
        
        # Show critical issues first
        if self.critical_issues:
            print(f"\n🚨 CRITICAL LOCALIZATION ISSUES ({len(self.critical_issues)}):")
            for issue in self.critical_issues:
                print(f"   • {issue}")
        else:
            print("\n✅ NO CRITICAL LOCALIZATION ISSUES FOUND")
        
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
            print(f"\n✅ PASSED TESTS ({len(passed_tests)}):")
            for test in passed_tests:
                print(f"   • {test['method']} {test['endpoint']} ({test['response_time']}s)")
        
        print("\n" + "=" * 60)
        
        # Key validation summary
        print("🔍 KEY VALIDATION RESULTS:")
        print("-" * 40)
        
        locales_tested = set()
        for result in self.results:
            if "locale=" in result["endpoint"]:
                locale = result["endpoint"].split("locale=")[1].split("&")[0]
                locales_tested.add(locale)
        
        print(f"Languages tested: {', '.join(sorted(locales_tested))}")
        
        if not self.critical_issues:
            print("✅ No 'english' keys found in non-English responses")
            print("✅ All specific translation validations passed")
            print("✅ German example_translated = 'Löwe' ✓")
            print("✅ Turkish translated = 'Sıfır' ✓") 
            print("✅ French translated = 'C'est un livre' ✓")
            print("✅ English example_translated = 'Lion' ✓")
        else:
            print(f"❌ {len(self.critical_issues)} critical localization issues found")

async def main():
    """Run the focused curriculum localization tests."""
    tester = FocusedCurriculumTester()
    
    try:
        await tester.run_focused_tests()
        tester.print_summary()
        
        # Return exit code based on results
        if tester.passed_tests == tester.total_tests and not tester.critical_issues:
            print("\n🎉 ALL TESTS PASSED! Curriculum localization fix is working correctly.")
            return 0
        else:
            issues = tester.total_tests - tester.passed_tests + len(tester.critical_issues)
            print(f"\n⚠️  {issues} issues found. Please check the problems above.")
            return 1
            
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        return 1

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)