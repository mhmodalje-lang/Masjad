#!/usr/bin/env python3
"""
Noor Academy Game Engine Backend Testing Suite
Tests all game engine endpoints for the Islamic kids app
Base URL: https://hadith-cards.preview.emergentagent.com
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://hadith-cards.preview.emergentagent.com"
LANGUAGES = ["ar", "en", "fr", "de", "tr", "ru", "sv", "nl", "el"]
TEST_USER_ID = "test_backend_user"

class GameEngineTestSuite:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
        
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {status}: {message}")
        
    def test_endpoint(self, method, endpoint, expected_status=200, data=None, description=""):
        """Test a single endpoint"""
        url = f"{BASE_URL}{endpoint}"
        self.log(f"Testing {method} {endpoint} - {description}")
        
        try:
            if method == "GET":
                response = requests.get(url, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            if response.status_code == expected_status:
                self.passed += 1
                self.log(f"✅ PASS: {description}", "PASS")
                return response.json() if response.content else {}
            else:
                self.failed += 1
                self.log(f"❌ FAIL: {description} - Status {response.status_code}", "FAIL")
                self.log(f"Response: {response.text[:200]}", "ERROR")
                return None
                
        except Exception as e:
            self.failed += 1
            self.log(f"❌ ERROR: {description} - {str(e)}", "ERROR")
            return None
    
    def validate_daily_games_response(self, data, locale):
        """Validate daily games response structure"""
        if not data:
            return False
            
        # Check required fields
        required_fields = ["success", "games", "total_xp"]
        for field in required_fields:
            if field not in data:
                self.log(f"Missing required field: {field}", "ERROR")
                return False
                
        if not data.get("success"):
            self.log(f"Response success=false for locale {locale}", "ERROR")
            return False
            
        games = data.get("games", [])
        if len(games) != 4:
            self.log(f"Expected 4 games, got {len(games)} for locale {locale}", "ERROR")
            return False
            
        if data.get("total_xp") != 60:
            self.log(f"Expected total_xp=60, got {data.get('total_xp')} for locale {locale}", "ERROR")
            return False
            
        # Validate each game
        expected_types = ["quiz", "memory", "drag_drop", "scenario"]
        game_types = [game.get("type") for game in games]
        
        for expected_type in expected_types:
            if expected_type not in game_types:
                self.log(f"Missing game type {expected_type} for locale {locale}", "ERROR")
                return False
                
        # Check each game has required fields
        for i, game in enumerate(games):
            required_game_fields = ["type", "id", "title", "emoji", "xp"]
            for field in required_game_fields:
                if field not in game:
                    self.log(f"Game {i} missing field {field} for locale {locale}", "ERROR")
                    return False
                    
        # Check for Arabic text in non-Arabic locales
        if locale != "ar":
            for game in games:
                title = game.get("title", "")
                # Check for Arabic characters (Unicode range U+0600 to U+06FF)
                if any('\u0600' <= char <= '\u06FF' for char in title):
                    self.log(f"Found Arabic text in {locale} locale: {title}", "ERROR")
                    return False
                    
        return True
    
    def run_daily_games_tests(self):
        """Test daily games endpoint for all 9 languages"""
        self.log("=" * 60)
        self.log("TESTING DAILY GAMES ENDPOINT FOR ALL 9 LANGUAGES")
        self.log("=" * 60)
        
        for locale in LANGUAGES:
            endpoint = f"/api/kids-learn/daily-games?locale={locale}"
            description = f"Daily games for {locale}"
            
            data = self.test_endpoint("GET", endpoint, description=description)
            
            if data and self.validate_daily_games_response(data, locale):
                self.log(f"✅ Daily games validation passed for {locale}", "PASS")
            elif data:
                self.log(f"❌ Daily games validation failed for {locale}", "FAIL")
                self.failed += 1
    
    def run_game_by_day_tests(self):
        """Test game by day endpoint"""
        self.log("=" * 60)
        self.log("TESTING GAME BY DAY ENDPOINT")
        self.log("=" * 60)
        
        test_cases = [
            (1, "en", "Games for day 1 in English"),
            (100, "sv", "Games for day 100 in Swedish"),
            (365, "en", "Boundary test - day 365 in English"),
        ]
        
        for day, locale, description in test_cases:
            endpoint = f"/api/kids-learn/game/{day}?locale={locale}"
            data = self.test_endpoint("GET", endpoint, description=description)
            
            if data and self.validate_daily_games_response(data, locale):
                self.log(f"✅ Game by day validation passed for day {day}, locale {locale}", "PASS")
            elif data:
                self.log(f"❌ Game by day validation failed for day {day}, locale {locale}", "FAIL")
                self.failed += 1
    
    def run_save_game_result_test(self):
        """Test save game result endpoint"""
        self.log("=" * 60)
        self.log("TESTING SAVE GAME RESULT ENDPOINT")
        self.log("=" * 60)
        
        payload = {
            "user_id": TEST_USER_ID,
            "game_id": "quiz_1",
            "day": 1,
            "score": 1,
            "max_score": 1,
            "xp_earned": 10,
            "time_seconds": 15
        }
        
        endpoint = "/api/kids-learn/game-result"
        description = "Save game result"
        
        data = self.test_endpoint("POST", endpoint, data=payload, description=description)
        
        if data:
            required_fields = ["success", "xp_earned", "total_xp", "level", "streak_days"]
            valid = True
            for field in required_fields:
                if field not in data:
                    self.log(f"Missing field in game result response: {field}", "ERROR")
                    valid = False
                    
            if valid and data.get("success"):
                self.log("✅ Save game result validation passed", "PASS")
            else:
                self.log("❌ Save game result validation failed", "FAIL")
                self.failed += 1
    
    def run_profile_test(self):
        """Test profile endpoint"""
        self.log("=" * 60)
        self.log("TESTING PROFILE ENDPOINT")
        self.log("=" * 60)
        
        endpoint = f"/api/kids-learn/profile/{TEST_USER_ID}"
        description = "Get user profile"
        
        data = self.test_endpoint("GET", endpoint, description=description)
        
        if data:
            required_fields = ["success", "profile"]
            valid = True
            for field in required_fields:
                if field not in data:
                    self.log(f"Missing field in profile response: {field}", "ERROR")
                    valid = False
                    
            if valid and data.get("success"):
                profile = data.get("profile", {})
                profile_fields = ["user_id", "total_xp", "level", "streak_days", "games_completed", "coins"]
                for field in profile_fields:
                    if field not in profile:
                        self.log(f"Missing field in profile data: {field}", "ERROR")
                        valid = False
                        
            if valid:
                self.log("✅ Profile validation passed", "PASS")
            else:
                self.log("❌ Profile validation failed", "FAIL")
                self.failed += 1
    
    def run_reward_ad_test(self):
        """Test reward ad endpoint"""
        self.log("=" * 60)
        self.log("TESTING REWARD AD ENDPOINT")
        self.log("=" * 60)
        
        endpoint = f"/api/kids-learn/reward-ad?user_id={TEST_USER_ID}&coins=10"
        description = "Reward ad coins"
        
        data = self.test_endpoint("POST", endpoint, description=description)
        
        if data:
            required_fields = ["success", "coins", "earned"]
            valid = True
            for field in required_fields:
                if field not in data:
                    self.log(f"Missing field in reward ad response: {field}", "ERROR")
                    valid = False
                    
            if valid and data.get("success") and data.get("earned") == 10:
                self.log("✅ Reward ad validation passed", "PASS")
            else:
                self.log("❌ Reward ad validation failed", "FAIL")
                self.failed += 1
    
    def run_existing_endpoints_test(self):
        """Test that existing endpoints still work"""
        self.log("=" * 60)
        self.log("TESTING EXISTING ENDPOINTS")
        self.log("=" * 60)
        
        # Test Digital Shield endpoint
        endpoint = "/api/kids-learn/digital-shield?locale=en&theme=all"
        description = "Digital Shield - all lessons"
        
        data = self.test_endpoint("GET", endpoint, description=description)
        
        if data:
            if data.get("success") and len(data.get("lessons", [])) == 30:
                self.log("✅ Digital Shield endpoint working - 30 lessons found", "PASS")
            else:
                self.log(f"❌ Digital Shield endpoint failed - expected 30 lessons, got {len(data.get('lessons', []))}", "FAIL")
                self.failed += 1
        
        # Test Health endpoint
        endpoint = "/api/health"
        description = "Health check"
        
        data = self.test_endpoint("GET", endpoint, description=description)
        
        if data:
            if data.get("status") == "healthy":
                self.log("✅ Health endpoint working", "PASS")
            else:
                self.log("❌ Health endpoint failed", "FAIL")
                self.failed += 1
    
    def run_all_tests(self):
        """Run all test suites"""
        self.log("🚀 STARTING NOOR ACADEMY GAME ENGINE BACKEND TESTS")
        self.log(f"Base URL: {BASE_URL}")
        self.log(f"Test User ID: {TEST_USER_ID}")
        self.log(f"Languages to test: {', '.join(LANGUAGES)}")
        
        start_time = datetime.now()
        
        # Run all test suites
        self.run_daily_games_tests()
        self.run_game_by_day_tests()
        self.run_save_game_result_test()
        self.run_profile_test()
        self.run_reward_ad_test()
        self.run_existing_endpoints_test()
        
        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.log("=" * 60)
        self.log("TEST SUMMARY")
        self.log("=" * 60)
        self.log(f"Total Tests: {self.passed + self.failed}")
        self.log(f"Passed: {self.passed}")
        self.log(f"Failed: {self.failed}")
        self.log(f"Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        self.log(f"Duration: {duration:.2f} seconds")
        
        if self.failed == 0:
            self.log("🎉 ALL TESTS PASSED! Game Engine is working correctly.", "SUCCESS")
            return True
        else:
            self.log(f"⚠️  {self.failed} TESTS FAILED. See details above.", "WARNING")
            return False

if __name__ == "__main__":
    test_suite = GameEngineTestSuite()
    success = test_suite.run_all_tests()
    sys.exit(0 if success else 1)