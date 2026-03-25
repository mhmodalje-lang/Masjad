#!/usr/bin/env python3
"""
Critical Endpoints Test Suite
Testing specific endpoints after frontend native app changes
Base URL: https://quran-engine-1.preview.emergentagent.com
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Base URL from frontend/.env
BASE_URL = "https://quran-engine-1.preview.emergentagent.com"

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.failures = []
    
    def add_pass(self, test_name: str):
        self.passed += 1
        print(f"✅ PASS: {test_name}")
    
    def add_fail(self, test_name: str, error: str):
        self.failed += 1
        self.failures.append(f"{test_name}: {error}")
        print(f"❌ FAIL: {test_name} - {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY: {self.passed}/{total} PASSED")
        print(f"{'='*60}")
        if self.failures:
            print("FAILURES:")
            for failure in self.failures:
                print(f"  - {failure}")
        return self.failed == 0

def make_request(endpoint: str, params: Dict = None) -> tuple:
    """Make HTTP request with error handling. Returns (status_code, data)."""
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, params=params, timeout=30)
        
        # Return status code and data
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = {"text": response.text}
        
        return response.status_code, data
    except requests.exceptions.RequestException as e:
        return 0, {"error": str(e)}

def test_health_check(results: TestResults):
    """Test 1: Health Check - GET /api/health"""
    print("\n🔍 Testing Health Check...")
    status_code, data = make_request("/api/health")
    
    if status_code == 200:
        if data.get("status") == "healthy":
            results.add_pass("Health Check")
        else:
            results.add_fail("Health Check", f"Status not healthy: {data}")
    else:
        results.add_fail("Health Check", f"Status code {status_code}: {data}")

def test_quran_chapters(results: TestResults):
    """Test 2: Quran Chapters - GET /api/quran/v4/chapters?language=ar"""
    print("\n🔍 Testing Quran Chapters...")
    status_code, data = make_request("/api/quran/v4/chapters", {"language": "ar"})
    
    if status_code == 200:
        if isinstance(data, dict) and "chapters" in data:
            chapters = data.get("chapters", [])
            if len(chapters) > 0:
                results.add_pass("Quran Chapters")
            else:
                results.add_fail("Quran Chapters", "No chapters returned")
        elif isinstance(data, list) and len(data) > 0:
            results.add_pass("Quran Chapters")
        else:
            results.add_fail("Quran Chapters", f"Unexpected response format: {data}")
    else:
        results.add_fail("Quran Chapters", f"Status code {status_code}: {data}")

def test_global_verse(results: TestResults):
    """Test 3: Global Verse - GET /api/quran/v4/global-verse/2/255?language=en"""
    print("\n🔍 Testing Global Verse (Ayat al-Kursi)...")
    status_code, data = make_request("/api/quran/v4/global-verse/2/255", {"language": "en"})
    
    if status_code == 200:
        if isinstance(data, dict) and ("verse" in data or "text" in data or "translation" in data):
            results.add_pass("Global Verse")
        elif isinstance(data, dict) and data.get("success"):
            results.add_pass("Global Verse")
        else:
            results.add_fail("Global Verse", f"Unexpected response format: {data}")
    else:
        results.add_fail("Global Verse", f"Status code {status_code}: {data}")

def test_kids_learn_daily_games(results: TestResults):
    """Test 4: Kids Learn Daily Games - GET /api/kids-learn/daily-games?locale=en"""
    print("\n🔍 Testing Kids Learn Daily Games...")
    status_code, data = make_request("/api/kids-learn/daily-games", {"locale": "en"})
    
    if status_code == 200:
        if isinstance(data, dict) and data.get("success"):
            games = data.get("games", [])
            if len(games) > 0:
                results.add_pass("Kids Learn Daily Games")
            else:
                results.add_fail("Kids Learn Daily Games", "No games returned")
        else:
            results.add_fail("Kids Learn Daily Games", f"API returned success=false: {data}")
    else:
        results.add_fail("Kids Learn Daily Games", f"Status code {status_code}: {data}")

def test_privacy_pages(results: TestResults):
    """Test 5: Privacy/Terms Pages - GET /privacy, GET /terms, GET /delete-data"""
    print("\n🔍 Testing Privacy/Terms Pages...")
    
    # Test Privacy Page
    status_code, data = make_request("/privacy")
    if status_code == 200:
        results.add_pass("Privacy Page")
    else:
        results.add_fail("Privacy Page", f"Status code {status_code}: {data}")
    
    # Test Terms Page
    status_code, data = make_request("/terms")
    if status_code == 200:
        results.add_pass("Terms Page")
    else:
        results.add_fail("Terms Page", f"Status code {status_code}: {data}")
    
    # Test Delete Data Page
    status_code, data = make_request("/delete-data")
    if status_code == 200:
        results.add_pass("Delete Data Page")
    else:
        results.add_fail("Delete Data Page", f"Status code {status_code}: {data}")

def main():
    """Run all critical endpoint tests."""
    print("🚀 Starting Critical Endpoints Test Suite")
    print(f"Base URL: {BASE_URL}")
    print("Testing backend functionality after frontend native app changes...")
    
    results = TestResults()
    
    # Run all test suites
    test_health_check(results)
    test_quran_chapters(results)
    test_global_verse(results)
    test_kids_learn_daily_games(results)
    test_privacy_pages(results)
    
    # Print final summary
    success = results.summary()
    
    if success:
        print("\n🎉 ALL CRITICAL ENDPOINTS PASSED! Backend is fully functional after frontend changes.")
        sys.exit(0)
    else:
        print(f"\n💥 {results.failed} CRITICAL ENDPOINTS FAILED! Backend issues detected.")
        sys.exit(1)

if __name__ == "__main__":
    main()