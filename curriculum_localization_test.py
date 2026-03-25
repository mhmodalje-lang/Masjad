#!/usr/bin/env python3
"""
Kids Curriculum Localization Fix Testing
========================================
Testing the curriculum API to ensure it returns TRANSLATED content (not English) 
when a non-English locale is requested.

Key validation: For EVERY non-English test, grep the full JSON response for the 
word "english" as a key - it should NOT exist.
"""

import asyncio
import httpx
import json
import time
import re
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://quran-engine-1.preview.emergentagent.com"

class CurriculumLocalizationTester:
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
        
        if locale != "en" and locale != "ar":  # Only check non-English, non-Arabic locales
            # Look for "english" as a JSON key
            if '"english"' in response_text.lower():
                issues.append(f"Found 'english' key in response for locale {locale} - should not exist")
                self.critical_issues.append(f"CRITICAL: 'english' key found in {locale} response")
        
        return issues

    def validate_curriculum_overview(self, data: dict, locale: str) -> List[str]:
        """Validate curriculum overview structure and translations."""
        issues = []
        
        if "stages" not in data:
            issues.append("Missing 'stages' field in curriculum overview")
            return issues
            
        stages = data["stages"]
        if not isinstance(stages, list):
            issues.append("Stages should be a list")
            return issues
        
        # Check that stages have titles and descriptions in the requested language
        for i, stage in enumerate(stages):
            if "title" not in stage:
                issues.append(f"Stage {i+1} missing title")
            elif locale != "en" and locale != "ar":
                # For non-English/Arabic locales, check if title is translated
                title = stage["title"]
                if isinstance(title, str) and self.is_english_text(title):
                    issues.append(f"Stage {i+1} title appears to be in English: '{title}'")
                    self.critical_issues.append(f"CRITICAL: Stage {i+1} title not translated for {locale}")
            
            if "description" not in stage:
                issues.append(f"Stage {i+1} missing description")
            elif locale != "en" and locale != "ar":
                # For non-English/Arabic locales, check if description is translated
                description = stage["description"]
                if isinstance(description, str) and self.is_english_text(description):
                    issues.append(f"Stage {i+1} description appears to be in English")
                    self.critical_issues.append(f"CRITICAL: Stage {i+1} description not translated for {locale}")
        
        return issues

    def validate_lesson_content(self, data: dict, locale: str, lesson_day: int) -> List[str]:
        """Validate lesson content structure and translations."""
        issues = []
        
        if "lesson" not in data:
            issues.append("Missing 'lesson' field")
            return issues
            
        lesson = data["lesson"]
        
        # Check lesson title
        if "title" in lesson:
            title = lesson["title"]
            if isinstance(title, dict):
                if locale not in title:
                    issues.append(f"Lesson title missing '{locale}' key")
                    self.critical_issues.append(f"CRITICAL: Lesson title missing {locale} translation")
            elif isinstance(title, str) and locale != "en" and locale != "ar":
                if self.is_english_text(title):
                    issues.append(f"Lesson title appears to be in English: '{title}'")
                    self.critical_issues.append(f"CRITICAL: Lesson title not translated for {locale}")
        
        # Check stage title
        if "stage" in lesson and "title" in lesson["stage"]:
            stage_title = lesson["stage"]["title"]
            if locale != "en" and locale != "ar" and self.is_english_text(stage_title):
                issues.append(f"Stage title appears to be in English: '{stage_title}'")
                self.critical_issues.append(f"CRITICAL: Stage title not translated for {locale}")
        
        # Check sections content
        if "sections" in lesson:
            sections = lesson["sections"]
            for i, section in enumerate(sections):
                if "content" in section:
                    content = section["content"]
                    
                    # Check for specific translation fields based on lesson type
                    if lesson_day == 1:  # Alphabet lesson
                        if "example_translated" in content:
                            example = content["example_translated"]
                            if locale == "de" and example != "Löwe":
                                issues.append(f"German example should be 'Löwe', got '{example}'")
                                self.critical_issues.append(f"CRITICAL: German example not translated correctly")
                            elif locale == "en" and example != "Lion":
                                issues.append(f"English example should be 'Lion', got '{example}'")
                    
                    elif lesson_day == 85:  # Numbers lesson
                        if "translated" in content:
                            translated = content["translated"]
                            if locale == "tr" and translated != "Sıfır":
                                issues.append(f"Turkish number should be 'Sıfır', got '{translated}'")
                                self.critical_issues.append(f"CRITICAL: Turkish number not translated correctly")
                    
                    elif lesson_day == 211:  # Sentences lesson
                        if "translated" in content:
                            translated = content["translated"]
                            if locale == "fr" and translated != "C'est un livre":
                                issues.append(f"French sentence should be 'C'est un livre', got '{translated}'")
                                self.critical_issues.append(f"CRITICAL: French sentence not translated correctly")
                    
                    # Check for any remaining "english" keys in content
                    if "english" in content:
                        issues.append(f"Found 'english' key in section {i+1} content")
                        self.critical_issues.append(f"CRITICAL: 'english' key found in lesson content for {locale}")
        
        return issues

    def is_english_text(self, text: str) -> bool:
        """Simple heuristic to detect if text is likely English."""
        if not text:
            return False
            
        # Common English words that shouldn't appear in other languages
        english_indicators = [
            "the", "and", "or", "of", "to", "in", "for", "with", "on", "at",
            "this", "that", "these", "those", "is", "are", "was", "were",
            "have", "has", "had", "will", "would", "could", "should",
            "alphabet", "letter", "word", "sentence", "reading", "writing"
        ]
        
        text_lower = text.lower()
        english_word_count = sum(1 for word in english_indicators if word in text_lower)
        
        # If more than 2 English indicators found, likely English text
        return english_word_count >= 2

    async def run_curriculum_tests(self):
        """Run all curriculum localization tests."""
        print("🧪 Starting Kids Curriculum Localization Fix Tests")
        print("=" * 60)
        
        # Test 1: Curriculum Overview - German
        print("\n1. Testing curriculum overview (locale=de)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum?locale=de",
            description="Curriculum overview in German - all stage titles/descriptions should be German"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "de")
            validation_issues = self.validate_curriculum_overview(result["response_data"], "de")
            all_issues = english_issues + validation_issues
            if all_issues:
                print(f"   ❌ Issues found: {'; '.join(all_issues)}")
            else:
                print("   ✅ German curriculum overview properly translated")
        
        # Test 2: Day 1 (Alphabet) - German
        print("\n2. Testing Day 1 Alphabet lesson (locale=de)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/1?locale=de",
            description="Day 1 lesson in German - example_translated should be 'Löwe', no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "de")
            validation_issues = self.validate_lesson_content(result["response_data"], "de", 1)
            all_issues = english_issues + validation_issues
            if all_issues:
                print(f"   ❌ Issues found: {'; '.join(all_issues)}")
            else:
                print("   ✅ German Day 1 lesson properly translated")
        
        # Test 3: Day 85 (Numbers) - Turkish
        print("\n3. Testing Day 85 Numbers lesson (locale=tr)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/85?locale=tr",
            description="Day 85 lesson in Turkish - translated should be 'Sıfır', no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "tr")
            validation_issues = self.validate_lesson_content(result["response_data"], "tr", 85)
            all_issues = english_issues + validation_issues
            if all_issues:
                print(f"   ❌ Issues found: {'; '.join(all_issues)}")
            else:
                print("   ✅ Turkish Day 85 lesson properly translated")
        
        # Test 4: Day 113 (Words) - Swedish
        print("\n4. Testing Day 113 Words lesson (locale=sv)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/113?locale=sv",
            description="Day 113 lesson in Swedish - content should be Swedish, no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "sv")
            validation_issues = self.validate_lesson_content(result["response_data"], "sv", 113)
            all_issues = english_issues + validation_issues
            if all_issues:
                print(f"   ❌ Issues found: {'; '.join(all_issues)}")
            else:
                print("   ✅ Swedish Day 113 lesson properly translated")
        
        # Test 5: Day 211 (Sentences) - French
        print("\n5. Testing Day 211 Sentences lesson (locale=fr)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/211?locale=fr",
            description="Day 211 lesson in French - translated should be 'C'est un livre', no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "fr")
            validation_issues = self.validate_lesson_content(result["response_data"], "fr", 211)
            all_issues = english_issues + validation_issues
            if all_issues:
                print(f"   ❌ Issues found: {'; '.join(all_issues)}")
            else:
                print("   ✅ French Day 211 lesson properly translated")
        
        # Test 6: Day 267 (Reading) - Dutch
        print("\n6. Testing Day 267 Reading lesson (locale=nl)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/267?locale=nl",
            description="Day 267 lesson in Dutch - content should be Dutch, no 'english' keys"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "nl")
            validation_issues = self.validate_lesson_content(result["response_data"], "nl", 267)
            all_issues = english_issues + validation_issues
            if all_issues:
                print(f"   ❌ Issues found: {'; '.join(all_issues)}")
            else:
                print("   ✅ Dutch Day 267 lesson properly translated")
        
        # Test 7: Day 57 (Vowels/Harakat) - Russian
        print("\n7. Testing Day 57 Vowels lesson (locale=ru)")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/57?locale=ru",
            description="Day 57 lesson in Russian - all content should be Russian, no English fallback"
        )
        if result["passed"]:
            english_issues = self.check_for_english_keys(result["response_text"], "ru")
            validation_issues = self.validate_lesson_content(result["response_data"], "ru", 57)
            all_issues = english_issues + validation_issues
            if all_issues:
                print(f"   ❌ Issues found: {'; '.join(all_issues)}")
            else:
                print("   ✅ Russian Day 57 lesson properly translated")
        
        # Test 8: Verify English still works
        print("\n8. Testing Day 1 lesson (locale=en) - English should still work")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/1?locale=en",
            description="Day 1 lesson in English - example_translated should be 'Lion'"
        )
        if result["passed"]:
            validation_issues = self.validate_lesson_content(result["response_data"], "en", 1)
            if validation_issues:
                print(f"   ❌ Issues found: {'; '.join(validation_issues)}")
            else:
                print("   ✅ English Day 1 lesson working correctly")
        
        # Test 9: Verify Arabic still works
        print("\n9. Testing Day 1 lesson (locale=ar) - Arabic should still work")
        result = await self.test_endpoint(
            "GET", "/api/kids-learn/curriculum/lesson/1?locale=ar",
            description="Day 1 lesson in Arabic - everything should be in Arabic"
        )
        if result["passed"]:
            validation_issues = self.validate_lesson_content(result["response_data"], "ar", 1)
            if validation_issues:
                print(f"   ❌ Issues found: {'; '.join(validation_issues)}")
            else:
                print("   ✅ Arabic Day 1 lesson working correctly")

    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 60)
        print("📊 CURRICULUM LOCALIZATION TEST RESULTS SUMMARY")
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
        
        # Localization validation summary
        print("🌍 LOCALIZATION VALIDATION SUMMARY:")
        print("-" * 40)
        
        locales_tested = set()
        for result in self.results:
            if "locale=" in result["endpoint"]:
                locale = result["endpoint"].split("locale=")[1].split("&")[0]
                locales_tested.add(locale)
        
        print(f"Languages tested: {', '.join(sorted(locales_tested))}")
        
        if not self.critical_issues:
            print("✅ No 'english' keys found in non-English responses")
            print("✅ All translations appear to be working correctly")
        else:
            print(f"❌ {len(self.critical_issues)} critical localization issues found")

async def main():
    """Run the curriculum localization tests."""
    tester = CurriculumLocalizationTester()
    
    try:
        await tester.run_curriculum_tests()
        tester.print_summary()
        
        # Return exit code based on results
        if tester.passed_tests == tester.total_tests and not tester.critical_issues:
            print("\n🎉 ALL TESTS PASSED! Curriculum localization is working correctly.")
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