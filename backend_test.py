#!/usr/bin/env python3
"""
Arabic Academy & Live Streams Backend API Testing
Tests the 10 specific endpoints mentioned in the review request
"""
import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, List

# Base URL from frontend environment
BASE_URL = "https://athan-tales.preview.emergentagent.com/api"

class ArabicAcademyAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_endpoint(self, method: str, endpoint: str, body: dict = None, expected_keys: List[str] = None, description: str = "") -> Dict[str, Any]:
        """Test a single endpoint and return results"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            kwargs = {
                'headers': {'Content-Type': 'application/json'} if body else {}
            }
            if body:
                kwargs['json'] = body
            
            async with self.session.request(method, url, **kwargs) as response:
                duration = time.time() - start_time
                
                # Get response data
                if response.content_type == 'application/json':
                    data = await response.json()
                else:
                    text_data = await response.text()
                    try:
                        data = json.loads(text_data)
                    except:
                        data = {"response_text": text_data}
                
                result = {
                    "endpoint": endpoint,
                    "method": method,
                    "url": url,
                    "status_code": response.status,
                    "success": response.status == 200,
                    "duration": round(duration, 3),
                    "description": description,
                    "content_type": response.content_type,
                    "response_size": len(str(data)),
                    "has_data": bool(data),
                    "issues": [],
                    "validation_notes": [],
                    "data_sample": None
                }
                
                # Status code validation
                if response.status != 200:
                    result["issues"].append(f"Non-200 status code: {response.status}")
                
                # Empty response check
                if not data:
                    result["issues"].append("Empty response body")
                else:
                    result["validation_notes"].append("✓ Non-empty response received")
                
                # Expected keys check
                if expected_keys and isinstance(data, dict):
                    missing_keys = [key for key in expected_keys if key not in data]
                    if missing_keys:
                        result["issues"].append(f"Missing expected keys: {missing_keys}")
                    else:
                        result["validation_notes"].append(f"✓ Contains expected keys: {expected_keys}")
                
                # Special validation based on endpoint
                if "/health" in endpoint:
                    self._validate_health_response(data, result)
                elif "/arabic-academy/letters" in endpoint:
                    self._validate_letters_response(data, result)
                elif "/arabic-academy/vocab" in endpoint:
                    self._validate_vocab_response(data, result)
                elif "/arabic-academy/quiz/" in endpoint:
                    self._validate_quiz_response(data, result)
                elif "/arabic-academy/daily-word" in endpoint:
                    self._validate_daily_word_response(data, result)
                elif "/arabic-academy/progress" in endpoint:
                    if method == "GET":
                        self._validate_progress_get_response(data, result)
                    else:
                        self._validate_progress_post_response(data, result)
                elif "/live-streams" in endpoint:
                    self._validate_streams_response(endpoint, data, result)
                
                # Store sample data for verification
                if isinstance(data, dict) and data:
                    result["sample_keys"] = list(data.keys())[:5]  # First 5 keys
                    # Sample a few fields for verification
                    sample = {}
                    for key in list(data.keys())[:3]:
                        value = data[key]
                        if isinstance(value, (str, int, bool)):
                            sample[key] = value
                        elif isinstance(value, list) and len(value) > 0:
                            sample[key] = f"[{len(value)} items]"
                        elif isinstance(value, dict):
                            sample[key] = f"{{dict with {len(value)} keys}}"
                    result["data_sample"] = sample
                
                return result
                
        except asyncio.TimeoutError:
            return {
                "endpoint": endpoint,
                "method": method,
                "url": url,
                "status_code": "TIMEOUT",
                "success": False,
                "duration": time.time() - start_time,
                "description": description,
                "issues": ["Request timeout (30s)"]
            }
        except Exception as e:
            return {
                "endpoint": endpoint,
                "method": method,
                "url": url,
                "status_code": "ERROR",
                "success": False,
                "duration": time.time() - start_time,
                "description": description,
                "issues": [f"Request error: {str(e)}"]
            }
    
    def _validate_health_response(self, data: dict, result: dict):
        """Validate health check response"""
        if not isinstance(data, dict):
            result["issues"].append("Health response is not a dictionary")
            return
        
        if "status" not in data:
            result["issues"].append("Missing 'status' field in health response")
        elif data["status"] == "healthy":
            result["validation_notes"].append("✓ Health status is 'healthy'")
        else:
            result["issues"].append(f"Health status is not 'healthy': {data['status']}")
        
        if "timestamp" in data:
            result["validation_notes"].append("✓ Contains timestamp")
        
        if "app" in data:
            result["validation_notes"].append(f"✓ App name: {data['app']}")
    
    def _validate_letters_response(self, data: dict, result: dict):
        """Validate Arabic letters response"""
        if not isinstance(data, dict):
            result["issues"].append("Letters response is not a dictionary")
            return
        
        if "letters" not in data:
            result["issues"].append("Missing 'letters' field")
            return
            
        letters = data["letters"]
        if not isinstance(letters, list):
            result["issues"].append("Letters field is not a list")
            return
            
        if len(letters) != 28:
            result["issues"].append(f"Expected 28 Arabic letters, got {len(letters)}")
        else:
            result["validation_notes"].append("✓ Contains all 28 Arabic letters")
        
        # Validate letter structure
        if letters:
            sample_letter = letters[0]
            required_fields = ["id", "letter", "name_ar", "name_en", "transliteration", "example_word", "example_meaning"]
            missing_fields = [field for field in required_fields if field not in sample_letter]
            if missing_fields:
                result["issues"].append(f"Letter missing fields: {missing_fields}")
            else:
                result["validation_notes"].append("✓ Letters contain required fields")
                
            # Check for forms
            form_fields = ["form_isolated", "form_initial", "form_medial", "form_final"]
            if any(field in sample_letter for field in form_fields):
                result["validation_notes"].append("✓ Letters contain form variations")
    
    def _validate_vocab_response(self, data: dict, result: dict):
        """Validate vocabulary response"""
        if not isinstance(data, dict):
            result["issues"].append("Vocab response is not a dictionary")
            return
        
        if "words" not in data:
            result["issues"].append("Missing 'words' field")
            return
            
        words = data["words"]
        if not isinstance(words, list):
            result["issues"].append("Words field is not a list")
            return
            
        if len(words) < 20:
            result["issues"].append(f"Expected at least 20 vocabulary words, got {len(words)}")
        else:
            result["validation_notes"].append(f"✓ Contains {len(words)} vocabulary words")
        
        # Validate word structure
        if words:
            sample_word = words[0]
            required_fields = ["word", "transliteration", "meaning", "surah", "ayah"]
            missing_fields = [field for field in required_fields if field not in sample_word]
            if missing_fields:
                result["issues"].append(f"Word missing fields: {missing_fields}")
            else:
                result["validation_notes"].append("✓ Words contain required fields (word, transliteration, meaning, surah, ayah)")
    
    def _validate_quiz_response(self, data: dict, result: dict):
        """Validate quiz response"""
        if not isinstance(data, dict):
            result["issues"].append("Quiz response is not a dictionary")
            return
        
        if "quiz" not in data:
            result["issues"].append("Missing 'quiz' field")
            return
            
        quiz = data["quiz"]
        if not isinstance(quiz, dict):
            result["issues"].append("Quiz field is not a dictionary")
            return
        
        if "options" not in quiz:
            result["issues"].append("Quiz missing 'options' field")
            return
            
        options = quiz["options"]
        if not isinstance(options, list):
            result["issues"].append("Quiz options is not a list")
            return
            
        if len(options) != 4:
            result["issues"].append(f"Expected 4 quiz options, got {len(options)}")
        else:
            result["validation_notes"].append("✓ Contains 4 quiz options")
            
        # Check for correct answer
        correct_options = [opt for opt in options if opt.get("correct", False)]
        if len(correct_options) != 1:
            result["issues"].append(f"Expected 1 correct option, found {len(correct_options)}")
        else:
            result["validation_notes"].append("✓ Contains exactly 1 correct answer")
            
        # Check wrong answers
        wrong_options = [opt for opt in options if not opt.get("correct", False)]
        if len(wrong_options) != 3:
            result["issues"].append(f"Expected 3 wrong options, found {len(wrong_options)}")
        else:
            result["validation_notes"].append("✓ Contains exactly 3 wrong answers")
    
    def _validate_daily_word_response(self, data: dict, result: dict):
        """Validate daily word response"""
        if not isinstance(data, dict):
            result["issues"].append("Daily word response is not a dictionary")
            return
        
        if "word" not in data:
            result["issues"].append("Missing 'word' field")
            return
            
        word = data["word"]
        if not isinstance(word, dict):
            result["issues"].append("Word field is not a dictionary")
            return
        
        required_fields = ["word", "transliteration", "meaning"]
        missing_fields = [field for field in required_fields if field not in word]
        if missing_fields:
            result["issues"].append(f"Daily word missing fields: {missing_fields}")
        else:
            result["validation_notes"].append("✓ Daily word contains required fields")
    
    def _validate_progress_get_response(self, data: dict, result: dict):
        """Validate progress GET response"""
        if not isinstance(data, dict):
            result["issues"].append("Progress response is not a dictionary")
            return
        
        if "progress" not in data:
            result["issues"].append("Missing 'progress' field")
            return
            
        progress = data["progress"]
        if not isinstance(progress, dict):
            result["issues"].append("Progress field is not a dictionary")
            return
        
        expected_fields = ["completed_letters", "stars", "total_xp", "level", "golden_bricks"]
        missing_fields = [field for field in expected_fields if field not in progress]
        if missing_fields:
            result["issues"].append(f"Progress missing fields: {missing_fields}")
        else:
            result["validation_notes"].append("✓ Progress contains expected tracking fields")
    
    def _validate_progress_post_response(self, data: dict, result: dict):
        """Validate progress POST response"""
        if not isinstance(data, dict):
            result["issues"].append("Progress save response is not a dictionary")
            return
        
        if not data.get("success"):
            result["issues"].append("Progress save did not return success=true")
        else:
            result["validation_notes"].append("✓ Progress saved successfully")
        
        if "message" in data:
            result["validation_notes"].append(f"✓ Response message: {data['message']}")
    
    def _validate_streams_response(self, endpoint: str, data: dict, result: dict):
        """Validate live streams response"""
        if not isinstance(data, dict):
            result["issues"].append("Streams response is not a dictionary")
            return
        
        if "streams" not in data:
            result["issues"].append("Missing 'streams' field")
            return
            
        streams = data["streams"]
        if not isinstance(streams, list):
            result["issues"].append("Streams field is not a list")
            return
        
        # Check stream count based on endpoint
        if "?category=haramain" in endpoint:
            if len(streams) != 2:
                result["issues"].append(f"Expected 2 Haramain streams (Makkah, Madinah), got {len(streams)}")
            else:
                result["validation_notes"].append("✓ Contains 2 Haramain streams (Makkah, Madinah)")
        elif endpoint == "/live-streams":
            if len(streams) != 5:
                result["issues"].append(f"Expected 5 total streams, got {len(streams)}")
            else:
                result["validation_notes"].append("✓ Contains all 5 live streams")
        elif "/live-streams/" in endpoint:
            # Single stream response - streams should contain 1 item or be a single stream object
            if "stream" in data:
                stream = data["stream"]
                if isinstance(stream, dict):
                    result["validation_notes"].append("✓ Single stream response format")
                    if "embed_id" in stream:
                        result["validation_notes"].append("✓ Stream contains embed_id")
            else:
                result["issues"].append("Single stream endpoint missing 'stream' field")
        
        # Validate stream structure for list responses
        if streams and isinstance(streams, list):
            sample_stream = streams[0]
            required_fields = ["id", "embed_id"]
            missing_fields = [field for field in required_fields if field not in sample_stream]
            if missing_fields:
                result["issues"].append(f"Stream missing fields: {missing_fields}")
            else:
                result["validation_notes"].append("✓ Streams contain required fields (id, embed_id)")
    
    async def run_tests(self):
        """Run all the requested Arabic Academy API tests"""
        print("🏛️ Starting Arabic Academy & Live Streams Backend API Tests...")
        print(f"Testing the 10 specific endpoints from review request")
        print(f"Base URL: {self.base_url}")
        print("-" * 70)
        
        # The exact 10 test cases from review request
        test_cases = [
            {
                "method": "GET",
                "endpoint": "/health",
                "expected_keys": ["status"],
                "description": "Health check - Should return healthy status"
            },
            {
                "method": "GET",
                "endpoint": "/arabic-academy/letters",
                "expected_keys": ["letters"],
                "description": "Arabic letters - Should return 28 Arabic letters with forms and examples"
            },
            {
                "method": "GET",
                "endpoint": "/arabic-academy/vocab",
                "expected_keys": ["words"],
                "description": "Quranic vocabulary - Should return 20 vocabulary words"
            },
            {
                "method": "GET",
                "endpoint": "/arabic-academy/quiz/1",
                "expected_keys": ["quiz"],
                "description": "Letter quiz - Should return quiz for letter id=1 (Alif) with 4 options"
            },
            {
                "method": "GET",
                "endpoint": "/arabic-academy/daily-word",
                "expected_keys": ["word"],
                "description": "Daily word - Should return a single daily Quranic word"
            },
            {
                "method": "GET",
                "endpoint": "/arabic-academy/progress/guest",
                "expected_keys": ["progress"],
                "description": "Progress GET - Should return progress object (empty for new users)"
            },
            {
                "method": "POST",
                "endpoint": "/arabic-academy/progress",
                "body": {
                    "user_id": "test-user-123",
                    "completed_letters": [1, 2],
                    "stars": 2,
                    "total_xp": 20,
                    "level": 1,
                    "golden_bricks": 2
                },
                "expected_keys": ["success"],
                "description": "Progress POST - Should save and return success"
            },
            {
                "method": "GET",
                "endpoint": "/live-streams",
                "expected_keys": ["streams"],
                "description": "Live streams - Should return 5 live streams (Makkah, Madinah, Al-Aqsa, Umayyad, Cologne)"
            },
            {
                "method": "GET",
                "endpoint": "/live-streams/makkah",
                "expected_keys": ["stream"],
                "description": "Makkah stream - Should return Makkah stream details with embed_id"
            },
            {
                "method": "GET",
                "endpoint": "/live-streams?category=haramain",
                "expected_keys": ["streams"],
                "description": "Haramain streams - Should return only 2 streams (Makkah and Madinah)"
            }
        ]
        
        # Run tests
        for i, test_case in enumerate(test_cases, 1):
            print(f"Test {i:2d}/{len(test_cases)}: {test_case['description']}")
            result = await self.test_endpoint(**test_case)
            self.results.append(result)
            
            # Print immediate result
            status_icon = "✅" if result["success"] else "❌"
            print(f"  {status_icon} {result['method']} {result['endpoint']}")
            print(f"      Status: {result['status_code']} | Duration: {result['duration']}s")
            
            if result["issues"]:
                for issue in result["issues"]:
                    print(f"      ❌ {issue}")
            
            if result.get("validation_notes"):
                for note in result["validation_notes"]:
                    print(f"      {note}")
            
            if result.get("data_sample"):
                print(f"      Sample: {result['data_sample']}")
            
            print()
        
        return self.results
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate test summary"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        
        summary = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": round((passed_tests / total_tests) * 100, 1) if total_tests > 0 else 0,
            "total_duration": round(sum(r["duration"] for r in self.results), 3),
            "avg_response_time": round(sum(r["duration"] for r in self.results) / total_tests, 3) if total_tests > 0 else 0,
            "critical_issues": [],
            "working_endpoints": [],
            "failed_endpoints": []
        }
        
        # Categorize results
        for result in self.results:
            if result["success"]:
                summary["working_endpoints"].append(result["endpoint"])
            else:
                summary["failed_endpoints"].append(result["endpoint"])
                summary["critical_issues"].append({
                    "endpoint": result["endpoint"],
                    "issues": result["issues"]
                })
        
        return summary
    
    def print_detailed_report(self):
        """Print detailed test report"""
        summary = self.generate_summary()
        
        print("=" * 70)
        print("🎯 ARABIC ACADEMY & LIVE STREAMS API TEST RESULTS")
        print("=" * 70)
        print(f"Total Endpoints Tested: {summary['total_tests']}")
        print(f"✅ Working: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"Success Rate: {summary['success_rate']}%")
        print(f"Total Test Duration: {summary['total_duration']}s")
        print(f"Average Response Time: {summary['avg_response_time']}s")
        print()
        
        if summary["working_endpoints"]:
            print("✅ WORKING ENDPOINTS:")
            for endpoint in summary["working_endpoints"]:
                print(f"   ✓ {endpoint}")
            print()
        
        if summary["critical_issues"]:
            print("🚨 FAILED ENDPOINTS:")
            for issue in summary["critical_issues"]:
                print(f"   ❌ {issue['endpoint']}")
                for detail in issue["issues"]:
                    print(f"      - {detail}")
            print()
        
        # Detailed breakdown
        print("📋 DETAILED ENDPOINT ANALYSIS:")
        print("-" * 70)
        for result in self.results:
            status_icon = "✅" if result["success"] else "❌"
            print(f"{status_icon} {result['method']} {result['endpoint']}")
            print(f"    Description: {result['description']}")
            print(f"    Status Code: {result['status_code']}")
            print(f"    Response Time: {result['duration']}s")
            
            if result.get("sample_keys"):
                print(f"    Response Structure: {result['sample_keys']}")
            
            if result.get("data_sample"):
                print(f"    Sample Data: {result['data_sample']}")
            
            if result.get("validation_notes"):
                print(f"    Validation: {', '.join(result['validation_notes'])}")
            
            if result["issues"]:
                print(f"    Issues: {', '.join(result['issues'])}")
            
            print()

async def main():
    """Main test runner"""
    try:
        async with ArabicAcademyAPITester(BASE_URL) as tester:
            results = await tester.run_tests()
            tester.print_detailed_report()
            
            # Return summary for potential use by other tools
            summary = tester.generate_summary()
            return {
                "summary": summary,
                "results": results
            }
    
    except Exception as e:
        print(f"❌ Testing failed with error: {e}")
        return {
            "summary": {"total_tests": 0, "passed": 0, "failed": 0, "success_rate": 0},
            "results": [],
            "error": str(e)
        }

if __name__ == "__main__":
    asyncio.run(main())