#!/usr/bin/env python3
"""
Arabic Academy Backend API Testing Suite - Updated for actual response structure
Testing all requested endpoints for the Arabic Academy system
"""

import httpx
import asyncio
import json
import os
from typing import Dict, Any
from datetime import datetime

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except:
        pass
    return "http://localhost:8001"

BACKEND_URL = get_backend_url()

class ArabicAcademyTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.results = []
        self.failed_tests = []
        self.passed_tests = 0
        self.total_tests = 0

    async def test_endpoint(self, method: str, endpoint: str, expected_status: int = 200, 
                          data: Dict[Any, Any] = None, validator_func=None, 
                          description: str = "") -> Dict[str, Any]:
        """Test a single endpoint with custom validation"""
        self.total_tests += 1
        url = f"{self.backend_url}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method.upper() == "GET":
                    response = await client.get(url)
                elif method.upper() == "POST":
                    response = await client.post(url, json=data)
                else:
                    response = await client.request(method, url, json=data)
                
                result = {
                    "endpoint": endpoint,
                    "method": method,
                    "description": description,
                    "status_code": response.status_code,
                    "expected_status": expected_status,
                    "success": response.status_code == expected_status,
                    "response_time": f"{response.elapsed.total_seconds():.3f}s",
                    "response_size": len(response.content),
                }
                
                # Parse JSON response
                try:
                    json_data = response.json()
                    result["has_json"] = True
                    result["json_valid"] = True
                    
                    # Custom validation
                    if validator_func and result["success"]:
                        validation_result = validator_func(json_data)
                        result.update(validation_result)
                    
                    # Store sample for debugging
                    if isinstance(json_data, dict) and len(str(json_data)) < 500:
                        result["sample_response"] = json_data
                    
                except json.JSONDecodeError:
                    result["has_json"] = False
                    result["json_valid"] = False
                    result["raw_response"] = response.text[:200] + "..." if len(response.text) > 200 else response.text
                
                # Overall success
                overall_success = result["success"] and result.get("validation_success", True)
                result["overall_success"] = overall_success
                
                if overall_success:
                    self.passed_tests += 1
                    print(f"✅ PASSED: {method} {endpoint} ({result['response_time']})")
                else:
                    self.failed_tests.append(result)
                    print(f"❌ FAILED: {method} {endpoint} - Status: {response.status_code}")
                    if "validation_errors" in result:
                        for error in result["validation_errors"]:
                            print(f"   ❌ {error}")
                
                self.results.append(result)
                return result
                
        except Exception as e:
            result = {
                "endpoint": endpoint,
                "method": method,
                "description": description,
                "success": False,
                "overall_success": False,
                "error": str(e),
                "error_type": type(e).__name__,
            }
            self.failed_tests.append(result)
            self.results.append(result)
            print(f"❌ ERROR: {method} {endpoint} - {str(e)}")
            return result

    def validate_health(self, data):
        """Validate health endpoint response"""
        errors = []
        if "status" not in data:
            errors.append("Missing 'status' field")
        elif data["status"] != "healthy":
            errors.append(f"Expected status 'healthy', got '{data['status']}'")
        
        return {
            "validation_success": len(errors) == 0,
            "validation_errors": errors,
            "validation_details": f"Health status: {data.get('status', 'missing')}"
        }

    def validate_letters(self, data):
        """Validate letters endpoint (28 letters)"""
        errors = []
        if "letters" not in data:
            errors.append("Missing 'letters' field")
            return {"validation_success": False, "validation_errors": errors}
        
        letters = data["letters"]
        if not isinstance(letters, list):
            errors.append("'letters' should be a list")
        elif len(letters) != 28:
            errors.append(f"Expected 28 letters, got {len(letters)}")
        else:
            # Check first letter has required fields
            if len(letters) > 0:
                first_letter = letters[0]
                required_fields = ["id", "letter", "name_ar", "name_en"]
                for field in required_fields:
                    if field not in first_letter:
                        errors.append(f"Letter missing field: {field}")
        
        return {
            "validation_success": len(errors) == 0,
            "validation_errors": errors,
            "validation_details": f"Found {len(letters) if isinstance(letters, list) else 0} letters"
        }

    def validate_curriculum(self, data):
        """Validate curriculum endpoint (90 days)"""
        errors = []
        if "curriculum" not in data:
            errors.append("Missing 'curriculum' field")
            return {"validation_success": False, "validation_errors": errors}
        
        curriculum = data["curriculum"]
        if not isinstance(curriculum, list):
            errors.append("'curriculum' should be a list")
        elif len(curriculum) != 90:
            errors.append(f"Expected 90 days, got {len(curriculum)}")
        
        return {
            "validation_success": len(errors) == 0,
            "validation_errors": errors,
            "validation_details": f"Found {len(curriculum) if isinstance(curriculum, list) else 0} days"
        }

    def validate_day_lesson(self, data, expected_day=None, expected_type=None):
        """Validate individual day lesson"""
        errors = []
        
        if "lesson" not in data:
            errors.append("Missing 'lesson' field")
        else:
            lesson = data["lesson"]
            if "day" not in lesson:
                errors.append("Missing 'day' field in lesson")
            elif expected_day and lesson["day"] != expected_day:
                errors.append(f"Expected day {expected_day}, got {lesson['day']}")
            
            if "type" not in lesson:
                errors.append("Missing 'type' field in lesson")
            elif expected_type and lesson["type"] != expected_type:
                errors.append(f"Expected type '{expected_type}', got '{lesson['type']}'")
        
        if "content" not in data:
            errors.append("Missing 'content' field")
        
        return {
            "validation_success": len(errors) == 0,
            "validation_errors": errors,
            "validation_details": f"Day {data.get('lesson', {}).get('day', '?')} - Type: {data.get('lesson', {}).get('type', '?')}"
        }

    def validate_numbers(self, data):
        """Validate numbers endpoint (17 numbers)"""
        errors = []
        if "numbers" not in data:
            errors.append("Missing 'numbers' field")
            return {"validation_success": False, "validation_errors": errors}
        
        numbers = data["numbers"]
        if not isinstance(numbers, list):
            errors.append("'numbers' should be a list")
        elif len(numbers) != 17:
            errors.append(f"Expected 17 numbers, got {len(numbers)}")
        else:
            # Check first number has required fields
            if len(numbers) > 0:
                first_number = numbers[0]
                required_fields = ["arabic", "word_ar", "word_en", "transliteration"]
                for field in required_fields:
                    if field not in first_number:
                        errors.append(f"Number missing field: {field}")
        
        return {
            "validation_success": len(errors) == 0,
            "validation_errors": errors,
            "validation_details": f"Found {len(numbers) if isinstance(numbers, list) else 0} numbers"
        }

    def validate_vocabulary(self, data, expected_count=None):
        """Validate vocabulary endpoint"""
        errors = []
        if "words" not in data:
            errors.append("Missing 'words' field (should contain vocabulary)")
            return {"validation_success": False, "validation_errors": errors}
        
        words = data["words"]
        if not isinstance(words, list):
            errors.append("'words' should be a list")
        elif expected_count and len(words) != expected_count:
            errors.append(f"Expected {expected_count} words, got {len(words)}")
        elif expected_count is None and len(words) < 76:
            errors.append(f"Expected at least 76 words, got {len(words)}")
        
        # Check categories exist
        if "categories" not in data:
            errors.append("Missing 'categories' field")
        elif len(data["categories"]) < 9:
            errors.append(f"Expected at least 9 categories, got {len(data['categories'])}")
        
        return {
            "validation_success": len(errors) == 0,
            "validation_errors": errors,
            "validation_details": f"Found {len(words) if isinstance(words, list) else 0} words, {len(data.get('categories', [])) if 'categories' in data else 0} categories"
        }

    def validate_sentences(self, data):
        """Validate sentences endpoint (10 sentences)"""
        errors = []
        if "sentences" not in data:
            errors.append("Missing 'sentences' field")
            return {"validation_success": False, "validation_errors": errors}
        
        sentences = data["sentences"]
        if not isinstance(sentences, list):
            errors.append("'sentences' should be a list")
        elif len(sentences) != 10:
            errors.append(f"Expected 10 sentences, got {len(sentences)}")
        
        return {
            "validation_success": len(errors) == 0,
            "validation_errors": errors,
            "validation_details": f"Found {len(sentences) if isinstance(sentences, list) else 0} sentences"
        }

    def validate_quiz(self, data, expected_letter_id=5):
        """Validate quiz endpoint"""
        errors = []
        if "quiz" not in data:
            errors.append("Missing 'quiz' field")
            return {"validation_success": False, "validation_errors": errors}
        
        quiz = data["quiz"]
        
        # Check for question_letter (contains the letter info)
        if "question_letter" not in quiz:
            errors.append("Quiz missing 'question_letter' field")
        else:
            question_letter = quiz["question_letter"]
            if "id" not in question_letter:
                errors.append("Question letter missing 'id' field")
            elif question_letter["id"] != expected_letter_id:
                errors.append(f"Expected letter ID {expected_letter_id}, got {question_letter['id']}")
        
        # Check for options (should have 4 options)
        if "options" not in quiz:
            errors.append("Quiz missing 'options' field")
        elif len(quiz["options"]) != 4:
            errors.append(f"Expected 4 options, got {len(quiz['options'])}")
        else:
            # Check that one option is correct
            correct_count = sum(1 for option in quiz["options"] if option.get("correct", False))
            if correct_count != 1:
                errors.append(f"Expected exactly 1 correct answer, got {correct_count}")
        
        # Check quiz type
        if "type" not in quiz:
            errors.append("Quiz missing 'type' field")
        
        return {
            "validation_success": len(errors) == 0,
            "validation_errors": errors,
            "validation_details": f"Letter ID: {quiz.get('question_letter', {}).get('id', '?')}, Options: {len(quiz.get('options', []))}, Type: {quiz.get('type', '?')}"
        }

    def validate_streams(self, data):
        """Validate live streams endpoint"""
        errors = []
        if "streams" not in data:
            errors.append("Missing 'streams' field")
            return {"validation_success": False, "validation_errors": errors}
        
        streams = data["streams"]
        if not isinstance(streams, list):
            errors.append("'streams' should be a list")
        elif len(streams) == 0:
            errors.append("No streams found")
        else:
            # Check first stream has embed_url
            first_stream = streams[0]
            if "embed_url" not in first_stream and "embed_id" not in first_stream:
                errors.append("Stream missing 'embed_url' or 'embed_id' field")
        
        return {
            "validation_success": len(errors) == 0,
            "validation_errors": errors,
            "validation_details": f"Found {len(streams) if isinstance(streams, list) else 0} streams"
        }

    def validate_progress(self, data):
        """Validate progress POST response"""
        errors = []
        if "success" not in data:
            errors.append("Missing 'success' field")
        elif not data["success"]:
            errors.append("Progress save was not successful")
        
        return {
            "validation_success": len(errors) == 0,
            "validation_errors": errors,
            "validation_details": f"Success: {data.get('success', False)}"
        }

    async def run_all_tests(self):
        """Run all Arabic Academy API tests from the review request"""
        print(f"🚀 Starting Arabic Academy Backend Testing - Updated")
        print(f"Backend URL: {self.backend_url}")
        print("=" * 80)
        
        # Test 1: Health check
        await self.test_endpoint(
            "GET", "/api/health", 
            validator_func=self.validate_health,
            description="Health check endpoint"
        )
        
        # Test 2: Get Arabic letters (should return 28 letters)
        await self.test_endpoint(
            "GET", "/api/arabic-academy/letters",
            validator_func=self.validate_letters,
            description="Get all 28 Arabic letters with metadata"
        )
        
        # Test 3: Get curriculum (should return 90 days)
        await self.test_endpoint(
            "GET", "/api/arabic-academy/curriculum",
            validator_func=self.validate_curriculum,
            description="Get full 90-day curriculum"
        )
        
        # Test 4: Get Day 1 lesson (should return Alif letter lesson)
        await self.test_endpoint(
            "GET", "/api/arabic-academy/curriculum/day/1",
            validator_func=lambda data: self.validate_day_lesson(data, expected_day=1, expected_type="letter"),
            description="Get Day 1 letter lesson with Alif content"
        )
        
        # Test 5: Get Day 35 lesson (should return number lesson)
        await self.test_endpoint(
            "GET", "/api/arabic-academy/curriculum/day/35",
            validator_func=lambda data: self.validate_day_lesson(data, expected_day=35, expected_type="number"),
            description="Get Day 35 number lesson"
        )
        
        # Test 6: Get Day 45 lesson (should return vocab lesson)
        await self.test_endpoint(
            "GET", "/api/arabic-academy/curriculum/day/45",
            validator_func=lambda data: self.validate_day_lesson(data, expected_day=45, expected_type="vocab"),
            description="Get Day 45 vocabulary lesson with emoji, word, meaning"
        )
        
        # Test 7: Get Day 80 lesson (should return sentence lesson)
        await self.test_endpoint(
            "GET", "/api/arabic-academy/curriculum/day/80",
            validator_func=lambda data: self.validate_day_lesson(data, expected_day=80, expected_type="sentence"),
            description="Get Day 80 sentence lesson with words_ar and sentence_ar"
        )
        
        # Test 8: Get Arabic numbers (should return 17 numbers)
        await self.test_endpoint(
            "GET", "/api/arabic-academy/numbers",
            validator_func=self.validate_numbers,
            description="Get 17 Arabic numbers with transliteration"
        )
        
        # Test 9: Get vocabulary (should return 76+ words with categories)
        await self.test_endpoint(
            "GET", "/api/arabic-academy/vocabulary",
            validator_func=lambda data: self.validate_vocabulary(data),
            description="Get vocabulary with 9 categories (76+ words)"
        )
        
        # Test 10: Get vocabulary filtered by animals category
        await self.test_endpoint(
            "GET", "/api/arabic-academy/vocabulary?category=animals",
            validator_func=lambda data: self.validate_vocabulary(data, expected_count=10),
            description="Get animals vocabulary (should return 10 words)"
        )
        
        # Test 11: Get sentence templates
        await self.test_endpoint(
            "GET", "/api/arabic-academy/sentences",
            validator_func=self.validate_sentences,
            description="Get 10 sentence templates"
        )
        
        # Test 12: Get quiz for letter 5 (Jim)
        await self.test_endpoint(
            "GET", "/api/arabic-academy/quiz/5",
            validator_func=lambda data: self.validate_quiz(data, expected_letter_id=5),
            description="Get quiz for letter 5 (Jim) with 4 options"
        )
        
        # Test 13: Get live streams (should have embed_url field)
        await self.test_endpoint(
            "GET", "/api/live-streams",
            validator_func=self.validate_streams,
            description="Get live streams with embed_url field"
        )
        
        # Test 14: POST progress tracking
        progress_data = {
            "user_id": "test_user_2024",
            "completed_days": [1, 2],
            "total_xp": 20,
            "stars": 2
        }
        await self.test_endpoint(
            "POST", "/api/arabic-academy/progress-v2",
            data=progress_data,
            validator_func=self.validate_progress,
            description="POST progress tracking with user data"
        )
        
        # Print final results
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("🎯 ARABIC ACADEMY BACKEND TEST SUMMARY - FINAL RESULTS")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {len(self.failed_tests)} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.failed_tests:
            print(f"\n🔴 FAILED TESTS ({len(self.failed_tests)}):")
            print("-" * 40)
            for i, failure in enumerate(self.failed_tests, 1):
                print(f"{i}. {failure['method']} {failure['endpoint']}")
                print(f"   Description: {failure.get('description', 'N/A')}")
                if 'error' in failure:
                    print(f"   Error: {failure['error']}")
                elif 'status_code' in failure:
                    print(f"   Status: {failure['status_code']}, Expected: {failure.get('expected_status', 200)}")
                if failure.get('validation_errors'):
                    for error in failure['validation_errors']:
                        print(f"   ❌ {error}")
                print()
        else:
            print("\n🎉 ALL TESTS PASSED!")
        
        # Performance summary
        if self.results:
            times = [float(r['response_time'].replace('s', '')) for r in self.results if 'response_time' in r]
            if times:
                avg_time = sum(times) / len(times)
                print(f"📊 PERFORMANCE:")
                print(f"   Average Response Time: {avg_time:.3f}s")
                print(f"   Fastest: {min(times):.3f}s")
                print(f"   Slowest: {max(times):.3f}s")
        
        print("\n" + "=" * 80)
        
        return {
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": len(self.failed_tests),
            "success_rate": success_rate,
            "backend_url": self.backend_url,
            "avg_response_time": sum([float(r['response_time'].replace('s', '')) for r in self.results if 'response_time' in r]) / len(self.results) if self.results else 0,
            "failed_details": self.failed_tests
        }

async def main():
    """Main test runner"""
    print("🔍 Arabic Academy Backend API Testing Suite - Updated")
    print(f"Testing against: {BACKEND_URL}")
    
    tester = ArabicAcademyTester()
    summary = await tester.run_all_tests()
    
    # Save detailed results to JSON for debugging
    with open('/app/backend_test_results_final.json', 'w') as f:
        json.dump({
            "summary": summary,
            "detailed_results": tester.results,
            "timestamp": datetime.utcnow().isoformat(),
            "backend_url": BACKEND_URL
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Detailed results saved to: /app/backend_test_results_final.json")
    return summary

if __name__ == "__main__":
    asyncio.run(main())