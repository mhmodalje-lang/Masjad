#!/usr/bin/env python3
"""
Islamic App (أذان وحكاية) Backend API Testing
Test Date: 2026-01-27
Focus: Comprehensive testing of all 15 critical endpoints as specified in review request
"""

import requests
import json
import re
from typing import Dict, List, Any

# Configuration
BASE_URL = "https://code-cleanup-deploy.preview.emergentagent.com"
TIMEOUT = 30

class IslamicAppTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        self.results.append({
            'test': test_name,
            'status': status,
            'details': details
        })
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            
    def make_request(self, endpoint: str) -> tuple:
        """Make HTTP request and return (success, data, status_code)"""
        try:
            url = f"{BASE_URL}{endpoint}"
            print(f"Testing: {url}")
            response = requests.get(url, timeout=TIMEOUT)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return True, data, 200
                except json.JSONDecodeError:
                    return False, f"Invalid JSON response", response.status_code
            else:
                return False, f"HTTP {response.status_code}: {response.text[:200]}", response.status_code
                
        except requests.exceptions.Timeout:
            return False, "Request timeout", 0
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {str(e)}", 0
            
    def test_health_endpoint(self):
        """Test 1: Health endpoint"""
        print("\n🔸 TEST 1: HEALTH ENDPOINT")
        
        endpoint = "/api/health"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/health"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        # Check for status healthy
        if data.get('status') != 'healthy':
            self.log_result(test_name, "FAIL", f"Expected status 'healthy', got '{data.get('status')}'")
            return
            
        self.log_result(test_name, "PASS", f"Status: {data.get('status')}, App: {data.get('app', 'N/A')}")
        
    def test_live_streams(self):
        """Test 2: Live streams endpoint"""
        print("\n🔸 TEST 2: LIVE STREAMS")
        
        endpoint = "/api/live-streams"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/live-streams"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        # Check for success:true and streams array
        if not data.get('success', False):
            self.log_result(test_name, "FAIL", f"Expected success:true, got success:{data.get('success')}")
            return
            
        streams = data.get('streams', [])
        if not isinstance(streams, list):
            self.log_result(test_name, "FAIL", f"Expected streams array, got {type(streams)}")
            return
            
        self.log_result(test_name, "PASS", f"Success: {data.get('success')}, Streams count: {len(streams)}")
        
    def test_kids_zone_game(self):
        """Test 3: Kids zone generate game"""
        print("\n🔸 TEST 3: KIDS ZONE GENERATE GAME")
        
        endpoint = "/api/kids-zone/generate-game"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/kids-zone/generate-game"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        # Check for success:true and game data
        if not data.get('success', False):
            self.log_result(test_name, "FAIL", f"Expected success:true, got success:{data.get('success')}")
            return
            
        game_data = data.get('game', {})
        if not game_data:
            self.log_result(test_name, "FAIL", f"Expected game data, got empty")
            return
            
        self.log_result(test_name, "PASS", f"Success: {data.get('success')}, Game type: {game_data.get('type', 'N/A')}")
        
    def test_arabic_academy_letters(self):
        """Test 4: Arabic academy letters"""
        print("\n🔸 TEST 4: ARABIC ACADEMY LETTERS")
        
        endpoint = "/api/arabic-academy/letters"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/arabic-academy/letters"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        # Check for 28 Arabic letters
        letters = data.get('letters', [])
        if not isinstance(letters, list):
            self.log_result(test_name, "FAIL", f"Expected letters array, got {type(letters)}")
            return
            
        if len(letters) != 28:
            self.log_result(test_name, "FAIL", f"Expected 28 Arabic letters, got {len(letters)}")
            return
            
        self.log_result(test_name, "PASS", f"Found {len(letters)} Arabic letters")
        
    def test_ad_config(self):
        """Test 5: Ad configuration"""
        print("\n🔸 TEST 5: AD CONFIGURATION")
        
        endpoint = "/api/ad-config"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/ad-config"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        self.log_result(test_name, "PASS", f"Ad config returned successfully")
        
    def test_quran_chapters(self):
        """Test 6: Quran chapters"""
        print("\n🔸 TEST 6: QURAN CHAPTERS")
        
        endpoint = "/api/quran/v4/chapters?language=ar"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/quran/v4/chapters?language=ar"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        # Check for 114 chapters
        chapters = data.get('chapters', [])
        if not isinstance(chapters, list):
            self.log_result(test_name, "FAIL", f"Expected chapters array, got {type(chapters)}")
            return
            
        if len(chapters) != 114:
            self.log_result(test_name, "FAIL", f"Expected 114 chapters, got {len(chapters)}")
            return
            
        self.log_result(test_name, "PASS", f"Found {len(chapters)} Quran chapters")
        
    def test_sohba_explore(self):
        """Test 7: Sohba explore"""
        print("\n🔸 TEST 7: SOHBA EXPLORE")
        
        endpoint = "/api/sohba/explore"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/sohba/explore"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        # Check for posts array
        posts = data.get('posts', [])
        if not isinstance(posts, list):
            self.log_result(test_name, "FAIL", f"Expected posts array, got {type(posts)}")
            return
            
        self.log_result(test_name, "PASS", f"Found {len(posts)} posts")
        
    def test_stories_list(self):
        """Test 8: Stories list"""
        print("\n🔸 TEST 8: STORIES LIST")
        
        endpoint = "/api/stories/list"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/stories/list"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        self.log_result(test_name, "PASS", f"Stories list returned successfully")
        
    def test_prayer_times(self):
        """Test 9: Prayer times"""
        print("\n🔸 TEST 9: PRAYER TIMES")
        
        endpoint = "/api/prayer-times?lat=48.2&lon=16.3"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/prayer-times?lat=48.2&lon=16.3"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        self.log_result(test_name, "PASS", f"Prayer times returned successfully")
        
    def test_hadith_collections(self):
        """Test 10: Hadith collections"""
        print("\n🔸 TEST 10: HADITH COLLECTIONS")
        
        endpoint = "/api/hadith/collections?language=en"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/hadith/collections?language=en"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        self.log_result(test_name, "PASS", f"Hadith collections returned successfully")
        
    def test_kids_learn_academy_overview(self):
        """Test 11: Kids learn academy overview"""
        print("\n🔸 TEST 11: KIDS LEARN ACADEMY OVERVIEW")
        
        endpoint = "/api/kids-learn/academy/overview?locale=en"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/kids-learn/academy/overview?locale=en"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        # Check for 5 tracks
        tracks = data.get('tracks', [])
        if not isinstance(tracks, list):
            self.log_result(test_name, "FAIL", f"Expected tracks array, got {type(tracks)}")
            return
            
        if len(tracks) != 5:
            self.log_result(test_name, "FAIL", f"Expected 5 tracks, got {len(tracks)}")
            return
            
        self.log_result(test_name, "PASS", f"Found {len(tracks)} tracks")
        
    def test_rewards_leaderboard(self):
        """Test 12: Rewards leaderboard"""
        print("\n🔸 TEST 12: REWARDS LEADERBOARD")
        
        endpoint = "/api/rewards/leaderboard"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/rewards/leaderboard"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        self.log_result(test_name, "PASS", f"Leaderboard returned successfully")
        
    def test_marketplace_products(self):
        """Test 13: Marketplace products"""
        print("\n🔸 TEST 13: MARKETPLACE PRODUCTS")
        
        endpoint = "/api/marketplace/products"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/marketplace/products"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        self.log_result(test_name, "PASS", f"Marketplace products returned successfully")
        
    def test_ai_daily_dua(self):
        """Test 14: AI daily dua"""
        print("\n🔸 TEST 14: AI DAILY DUA")
        
        endpoint = "/api/ai/daily-dua"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/ai/daily-dua"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        self.log_result(test_name, "PASS", f"Daily dua returned successfully")
        
    def test_store_items(self):
        """Test 15: Store items"""
        print("\n🔸 TEST 15: STORE ITEMS")
        
        endpoint = "/api/store/items"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "GET /api/store/items"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check if response has expected structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", f"Invalid response structure")
            return
            
        self.log_result(test_name, "PASS", f"Store items returned successfully")
        
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 STARTING ISLAMIC APP (أذان وحكاية) BACKEND API TESTING")
        print(f"📍 Base URL: {BASE_URL}")
        print("🎯 Focus: Testing all 15 critical endpoints as per review request")
        
        # Run all test suites
        self.test_health_endpoint()
        self.test_live_streams()
        self.test_kids_zone_game()
        self.test_arabic_academy_letters()
        self.test_ad_config()
        self.test_quran_chapters()
        self.test_sohba_explore()
        self.test_stories_list()
        self.test_prayer_times()
        self.test_hadith_collections()
        self.test_kids_learn_academy_overview()
        self.test_rewards_leaderboard()
        self.test_marketplace_products()
        self.test_ai_daily_dua()
        self.test_store_items()
        
        # Generate summary report
        self.generate_report()
        
    def generate_report(self):
        """Generate final test report"""
        print("\n" + "="*80)
        print("📊 ISLAMIC APP (أذان وحكاية) API TESTING RESULTS")
        print("="*80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"📈 SUMMARY: {success_rate:.1f}% SUCCESS ({self.passed_tests}/{self.total_tests} tests passed)")
        print(f"✅ PASSED: {self.passed_tests}")
        print(f"❌ FAILED: {self.failed_tests}")
        
        # Group results by status
        passed_tests = [r for r in self.results if r['status'] == 'PASS']
        failed_tests = [r for r in self.results if r['status'] == 'FAIL']
        
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for result in failed_tests:
                print(f"   • {result['test']}: {result['details']}")
                
        if passed_tests:
            print(f"\n✅ PASSED TESTS ({len(passed_tests)}):")
            for result in passed_tests:
                print(f"   • {result['test']}: {result['details']}")
                
        # Critical findings
        critical_failures = [r for r in failed_tests if any(word in r['details'].lower() for word in ['timeout', 'connection', 'invalid json', 'http 5'])]
        if critical_failures:
            print(f"\n🚨 CRITICAL ISSUES FOUND ({len(critical_failures)}):")
            for result in critical_failures:
                print(f"   • {result['test']}: {result['details']}")
        else:
            print(f"\n🎉 ALL ENDPOINTS RESPONDING: No critical connection or server issues found")
            
        print("\n" + "="*80)

if __name__ == "__main__":
    tester = IslamicAppTester()
    tester.run_all_tests()