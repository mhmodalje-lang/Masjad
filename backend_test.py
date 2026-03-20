#!/usr/bin/env python3
"""
Kids Zone Infinite Game Engine Backend Testing
Testing 8 specific endpoints for Islamic educational app
"""

import requests
import json
import time
from typing import Dict, Any, List

# Base URL from frontend .env file
BASE_URL = "https://structured-learning-3.preview.emergentagent.com"

def test_endpoint(method: str, endpoint: str, expected_status: int = 200, params: Dict = None, json_data: Dict = None) -> Dict[str, Any]:
    """Test a single endpoint and return results"""
    url = f"{BASE_URL}{endpoint}"
    start_time = time.time()
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data, timeout=10)
        else:
            response = requests.request(method, url, params=params, json=json_data, timeout=10)
            
        response_time = time.time() - start_time
        
        # Try to parse JSON
        try:
            json_response = response.json()
        except:
            json_response = None
            
        return {
            "endpoint": endpoint,
            "status_code": response.status_code,
            "expected_status": expected_status,
            "response_time": round(response_time, 3),
            "success": response.status_code == expected_status,
            "json_valid": json_response is not None,
            "json_data": json_response,
            "error": None
        }
        
    except Exception as e:
        return {
            "endpoint": endpoint,
            "status_code": None,
            "expected_status": expected_status,
            "response_time": None,
            "success": False,
            "json_valid": False,
            "json_data": None,
            "error": str(e)
        }

def validate_health_response(data: Dict) -> List[str]:
    """Validate health endpoint response"""
    issues = []
    if not data:
        issues.append("No JSON data returned")
        return issues
        
    if "status" not in data:
        issues.append("Missing 'status' field")
    elif data["status"] != "healthy":
        issues.append(f"Status is '{data['status']}', expected 'healthy'")
        
    if "timestamp" not in data:
        issues.append("Missing 'timestamp' field")
        
    if "app" not in data:
        issues.append("Missing 'app' field")
        
    return issues

def validate_generate_game_response(data: Dict, game_type: str) -> List[str]:
    """Validate generate-game endpoint response"""
    issues = []
    if not data:
        issues.append("No JSON data returned")
        return issues
        
    if "success" not in data:
        issues.append("Missing 'success' field")
        return issues
        
    if not data["success"]:
        issues.append("API returned success=false")
        return issues
        
    if "game" not in data:
        issues.append("Missing 'game' field")
        return issues
        
    game = data["game"]
    
    # Common fields for all games
    required_fields = ["game_id", "game_type", "difficulty", "time_limit", "brick_reward"]
    for field in required_fields:
        if field not in game:
            issues.append(f"Missing required field in game: '{field}'")
    
    # Check game_type matches request
    if game.get("game_type") != game_type:
        issues.append(f"Game type mismatch: expected '{game_type}', got '{game.get('game_type')}'")
    
    # Game-specific validations
    if game_type == "letter_maze":
        if "target_letter" not in game:
            issues.append("Missing 'target_letter' field for letter_maze game")
        if "grid" not in game:
            issues.append("Missing 'grid' field for letter_maze game")
    elif game_type == "word_match":
        if "words" not in game:
            issues.append("Missing 'words' field for word_match game")
        if "meanings" not in game:
            issues.append("Missing 'meanings' field for word_match game")
    elif game_type == "tajweed_puzzle":
        if "question_rule" not in game:
            issues.append("Missing 'question_rule' field for tajweed_puzzle game")
        if "choices" not in game:
            issues.append("Missing 'choices' field for tajweed_puzzle game")
        if "correct_answer" not in game:
            issues.append("Missing 'correct_answer' field for tajweed_puzzle game")
    elif game_type == "pronunciation":
        if "target_word" not in game:
            issues.append("Missing 'target_word' field for pronunciation game")
        if "transliteration" not in game:
            issues.append("Missing 'transliteration' field for pronunciation game")
        if "meaning" not in game:
            issues.append("Missing 'meaning' field for pronunciation game")
        if "accuracy_threshold" not in game:
            issues.append("Missing 'accuracy_threshold' field for pronunciation game")
            
    return issues

def validate_submit_result_response(data: Dict) -> List[str]:
    """Validate submit-result endpoint response"""
    issues = []
    if not data:
        issues.append("No JSON data returned")
        return issues
        
    if "success" not in data:
        issues.append("Missing 'success' field")
        return issues
        
    if not data["success"]:
        issues.append("API returned success=false")
        return issues
        
    required_fields = ["xp_earned", "bricks_earned", "total_xp", "mosque_progress"]
    for field in required_fields:
        if field not in data:
            issues.append(f"Missing required field: '{field}'")
            
    return issues

def validate_progress_response(data: Dict) -> List[str]:
    """Validate progress endpoint response"""
    issues = []
    if not data:
        issues.append("No JSON data returned")
        return issues
        
    if "success" not in data:
        issues.append("Missing 'success' field")
        return issues
        
    if not data["success"]:
        issues.append("API returned success=false")
        return issues
        
    if "profile" not in data:
        issues.append("Missing 'profile' field")
        return issues
        
    profile = data["profile"]
    required_profile_fields = ["total_xp", "golden_bricks", "difficulty"]
    for field in required_profile_fields:
        if field not in profile:
            issues.append(f"Missing required field in profile: '{field}'")
    
    if "letter_skills" not in data:
        issues.append("Missing 'letter_skills' field")
        return issues
        
    letter_skills = data["letter_skills"]
    if not isinstance(letter_skills, list):
        issues.append("letter_skills should be a list")
    elif len(letter_skills) != 28:
        issues.append(f"Expected 28 Arabic letters in letter_skills, got {len(letter_skills)}")
        
    if "mosque" not in data:
        issues.append("Missing 'mosque' field")
        
    return issues

def validate_mosque_response(data: Dict) -> List[str]:
    """Validate mosque endpoint response"""
    issues = []
    if not data:
        issues.append("No JSON data returned")
        return issues
        
    if "success" not in data:
        issues.append("Missing 'success' field")
        return issues
        
    if not data["success"]:
        issues.append("API returned success=false")
        return issues
        
    if "mosque" not in data:
        issues.append("Missing 'mosque' field")
        return issues
        
    mosque = data["mosque"]
    required_fields = ["current_stage", "next_stage", "stages"]
    for field in required_fields:
        if field not in mosque:
            issues.append(f"Missing required field in mosque: '{field}'")
            
    if "stages" in mosque and not isinstance(mosque["stages"], list):
        issues.append("mosque.stages should be a list")
        
    return issues

def main():
    """Run Kids Zone backend tests"""
    print("🎮 Kids Zone Infinite Game Engine Backend Testing")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print()
    
    # Define test cases for the 8 specific endpoints
    test_cases = [
        {
            "name": "Health Check",
            "method": "GET",
            "endpoint": "/api/health",
            "validator": validate_health_response
        },
        {
            "name": "Generate Letter Maze Game (Arabic)",
            "method": "GET",
            "endpoint": "/api/kids-zone/generate-game",
            "params": {"user_id": "test1", "game_type": "letter_maze", "locale": "ar"},
            "validator": lambda data: validate_generate_game_response(data, "letter_maze")
        },
        {
            "name": "Generate Word Match Game (German)",
            "method": "GET",
            "endpoint": "/api/kids-zone/generate-game",
            "params": {"user_id": "test1", "game_type": "word_match", "locale": "de"},
            "validator": lambda data: validate_generate_game_response(data, "word_match")
        },
        {
            "name": "Generate Tajweed Puzzle Game (French)",
            "method": "GET",
            "endpoint": "/api/kids-zone/generate-game",
            "params": {"user_id": "test1", "game_type": "tajweed_puzzle", "locale": "fr"},
            "validator": lambda data: validate_generate_game_response(data, "tajweed_puzzle")
        },
        {
            "name": "Generate Pronunciation Game (Turkish)",
            "method": "GET",
            "endpoint": "/api/kids-zone/generate-game",
            "params": {"user_id": "test1", "game_type": "pronunciation", "locale": "tr"},
            "validator": lambda data: validate_generate_game_response(data, "pronunciation")
        },
        {
            "name": "Submit Game Result",
            "method": "POST",
            "endpoint": "/api/kids-zone/submit-result",
            "json_data": {
                "user_id": "test1",
                "game_type": "letter_maze",
                "correct": True,
                "score": 15,
                "phonemes_tested": [6, 7],
                "pronunciation_accuracy": 0,
                "game_id": "test-game-1"
            },
            "validator": validate_submit_result_response
        },
        {
            "name": "Get User Progress",
            "method": "GET",
            "endpoint": "/api/kids-zone/progress",
            "params": {"user_id": "test1"},
            "validator": validate_progress_response
        },
        {
            "name": "Get Mosque Status",
            "method": "GET",
            "endpoint": "/api/kids-zone/mosque",
            "params": {"user_id": "test1"},
            "validator": validate_mosque_response
        }
    ]
    
    results = []
    total_tests = len(test_cases)
    passed_tests = 0
    
    # Run tests
    for i, test_case in enumerate(test_cases, 1):
        print(f"[{i}/{total_tests}] Testing {test_case['name']}...")
        
        result = test_endpoint(
            test_case["method"],
            test_case["endpoint"],
            params=test_case.get("params"),
            json_data=test_case.get("json_data")
        )
        
        # Validate response if validator provided
        validation_issues = []
        if result["success"] and result["json_valid"] and "validator" in test_case:
            validation_issues = test_case["validator"](result["json_data"])
            
        result["validation_issues"] = validation_issues
        result["name"] = test_case["name"]
        results.append(result)
        
        # Print immediate result
        if result["success"] and not validation_issues:
            print(f"   ✅ PASSED ({result['response_time']}s)")
            passed_tests += 1
        else:
            print(f"   ❌ FAILED")
            if result["error"]:
                print(f"      Error: {result['error']}")
            elif result["status_code"] != result["expected_status"]:
                print(f"      Status: {result['status_code']} (expected {result['expected_status']})")
            if validation_issues:
                for issue in validation_issues:
                    print(f"      Validation: {issue}")
        print()
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED - Kids Zone backend is working!")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed - Issues detected")
    
    # Detailed results
    print("\n" + "=" * 60)
    print("📋 DETAILED RESULTS")
    print("=" * 60)
    
    for result in results:
        status = "✅ PASSED" if result["success"] and not result["validation_issues"] else "❌ FAILED"
        print(f"\n{result['name']}: {status}")
        print(f"  Endpoint: {result['endpoint']}")
        print(f"  Status Code: {result['status_code']}")
        print(f"  Response Time: {result['response_time']}s")
        print(f"  JSON Valid: {result['json_valid']}")
        
        if result["validation_issues"]:
            print("  Validation Issues:")
            for issue in result["validation_issues"]:
                print(f"    - {issue}")
                
        if result["error"]:
            print(f"  Error: {result['error']}")
            
        # Show sample response data for successful tests
        if result["success"] and result["json_valid"] and not result["validation_issues"]:
            json_data = result["json_data"]
            if "game" in json_data:
                game = json_data["game"]
                print(f"  Game Type: {game.get('game_type', 'N/A')}")
                print(f"  Difficulty: {game.get('difficulty', 'N/A')}")
                print(f"  Brick Reward: {game.get('brick_reward', 'N/A')}")
            elif "profile" in json_data:
                profile = json_data["profile"]
                print(f"  Total XP: {profile.get('total_xp', 'N/A')}")
                print(f"  Golden Bricks: {profile.get('golden_bricks', 'N/A')}")
                print(f"  Difficulty: {profile.get('difficulty', 'N/A')}")
            elif "mosque" in json_data:
                mosque = json_data["mosque"]
                print(f"  Current Stage: {mosque.get('current_stage', {}).get('name', 'N/A')}")
                print(f"  Total Bricks: {mosque.get('total_bricks', 'N/A')}")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)