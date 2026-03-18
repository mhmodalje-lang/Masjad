#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Islamic App
Tests all critical endpoints as specified in the review request.
"""

import asyncio
import httpx
import json
import sys
import os
from datetime import datetime

# Load frontend .env to get the backend URL
BACKEND_URL = None
try:
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                BACKEND_URL = line.split('=', 1)[1].strip().rstrip('/') + '/api'
                break
except FileNotFoundError:
    BACKEND_URL = "http://localhost:8001/api"

if not BACKEND_URL:
    BACKEND_URL = "http://localhost:8001/api"

print(f"Using backend URL: {BACKEND_URL}")

class TestResults:
    def __init__(self):
        self.passed = []
        self.failed = []
    
    def add_pass(self, endpoint, details=""):
        self.passed.append(f"✅ {endpoint}: {details}")
    
    def add_fail(self, endpoint, error):
        self.failed.append(f"❌ {endpoint}: {error}")
    
    def print_summary(self):
        print("\n" + "="*80)
        print("🔍 BACKEND API TEST RESULTS SUMMARY")
        print("="*80)
        
        if self.passed:
            print(f"\n✅ PASSED ({len(self.passed)}/13 endpoints):")
            for result in self.passed:
                print(f"   {result}")
        
        if self.failed:
            print(f"\n❌ FAILED ({len(self.failed)}/13 endpoints):")
            for result in self.failed:
                print(f"   {result}")
        
        print(f"\n📊 OVERALL RESULT: {len(self.passed)}/13 endpoints working ({len(self.passed)/13*100:.1f}% success rate)")
        
        if len(self.failed) == 0:
            print("🎉 ALL ENDPOINTS PASSING! Islamic app backend is fully functional.")
        else:
            print(f"⚠️  {len(self.failed)} endpoints need attention.")
        
        print("="*80)

async def test_endpoint(client, endpoint, method="GET", data=None, headers=None, expected_status=200, validation_func=None):
    """Generic endpoint testing function"""
    url = f"{BACKEND_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = await client.get(url, headers=headers or {})
        elif method == "POST":
            response = await client.post(url, json=data, headers=headers or {})
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        # Check status code
        if response.status_code != expected_status:
            return False, f"Expected status {expected_status}, got {response.status_code}"
        
        # Parse JSON response
        try:
            json_data = response.json()
        except Exception as e:
            return False, f"Invalid JSON response: {str(e)}"
        
        # Custom validation
        if validation_func:
            is_valid, error = validation_func(json_data)
            if not is_valid:
                return False, error
        
        return True, json_data
    
    except Exception as e:
        return False, f"Request failed: {str(e)}"

async def main():
    results = TestResults()
    
    print("🚀 Starting comprehensive Islamic app backend testing...")
    print(f"📡 Testing against: {BACKEND_URL}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # 1. Health Check
        print("\n1. Testing health endpoint...")
        success, data = await test_endpoint(
            client, "/health",
            validation_func=lambda d: (
                ("status" in d and d["status"] == "healthy" and "app" in d, "")
                if "status" in d else (False, "Missing status field")
            )
        )
        if success:
            results.add_pass("GET /api/health", f"Status: {data.get('status')}, App: {data.get('app')}")
        else:
            results.add_fail("GET /api/health", data)
        
        # 2. User Registration
        print("\n2. Testing user registration...")
        import time
        unique_email = f"finaltest{int(time.time())}@test.com"
        register_data = {
            "email": unique_email,
            "password": "test123456", 
            "name": "Final Test"
        }
        success, data = await test_endpoint(
            client, "/auth/register", method="POST", data=register_data,
            validation_func=lambda d: (
                (True, "") if "access_token" in d and "user" in d
                else (False, "Missing access_token or user in response")
            )
        )
        if success:
            results.add_pass("POST /api/auth/register", "User registered successfully, OAuth2 token returned")
        else:
            results.add_fail("POST /api/auth/register", data)
        
        # Store token for subsequent requests
        auth_token = None
        if success and isinstance(data, dict):
            auth_token = data.get("access_token")
        
        # 3. User Login
        print("\n3. Testing user login...")
        login_data = {
            "email": unique_email,
            "password": "test123456"
        }
        success, data = await test_endpoint(
            client, "/auth/login", method="POST", data=login_data,
            validation_func=lambda d: (
                (True, "") if "access_token" in d and "user" in d
                else (False, "Missing access_token or user in response")
            )
        )
        if success:
            results.add_pass("POST /api/auth/login", "Login successful, OAuth2 access_token returned")
            if isinstance(data, dict):
                auth_token = data.get("access_token")  # Update token
        else:
            results.add_fail("POST /api/auth/login", data)
        
        auth_headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
        
        # 4. Stories List
        print("\n4. Testing stories list...")
        success, data = await test_endpoint(
            client, "/stories/list?limit=5",
            validation_func=lambda d: (
                (True, f"Found {len(d.get('stories', []))} stories, total: {d.get('total', 0)}") 
                if "stories" in d and d.get("total", 0) > 100
                else (False, f"Expected total >100 stories, found total: {d.get('total', 0)}, returned: {len(d.get('stories', []))}")
            )
        )
        if success:
            story_count = len(data.get("stories", []))
            total_count = data.get("total", 0)
            results.add_pass("GET /api/stories/list", f"Returns {story_count} stories (total: {total_count} > 100 ✓)")
        else:
            results.add_fail("GET /api/stories/list", data)
        
        # 5. Story Categories
        print("\n5. Testing story categories...")
        success, data = await test_endpoint(
            client, "/stories/categories",
            validation_func=lambda d: (
                (True, f"Found {len(d.get('categories', []))} categories")
                if "categories" in d and len(d["categories"]) >= 10
                else (False, f"Expected >=10 categories, found {len(d.get('categories', []))}")
            )
        )
        if success:
            categories_count = len(data.get("categories", []))
            results.add_pass("GET /api/stories/categories", f"Returns {categories_count} Islamic story categories")
        else:
            results.add_fail("GET /api/stories/categories", data)
        
        # 6. Ruqyah Content
        print("\n6. Testing ruqyah content...")
        success, data = await test_endpoint(
            client, "/ruqyah",
            validation_func=lambda d: (
                (True, f"Found {len(d.get('items', []))} ruqyah items")
                if "items" in d and len(d["items"]) > 0
                else (False, f"Expected >0 ruqyah items, found {len(d.get('items', []))}")
            )
        )
        if success:
            ruqyah_count = len(data.get("items", []))
            results.add_pass("GET /api/ruqyah", f"Returns {ruqyah_count} ruqyah items (> 0 ✓)")
        else:
            results.add_fail("GET /api/ruqyah", data)
        
        # 7. Asma Al-Husna (99 Names of Allah)
        print("\n7. Testing Asma Al-Husna...")
        success, data = await test_endpoint(
            client, "/asma-al-husna",
            validation_func=lambda d: (
                (True, "Exactly 99 names returned")
                if "names" in d and len(d["names"]) == 99 and d.get("total") == 99
                else (False, f"Expected exactly 99 names, found {len(d.get('names', []))}")
            )
        )
        if success:
            results.add_pass("GET /api/asma-al-husna", "Returns exactly 99 Names of Allah ✓")
        else:
            results.add_fail("GET /api/asma-al-husna", data)
        
        # 8. Rewards Leaderboard
        print("\n8. Testing rewards leaderboard...")
        success, data = await test_endpoint(
            client, "/rewards/leaderboard",
            validation_func=lambda d: (
                (True, "Leaderboard structure valid")
                if "leaderboard" in d and isinstance(d["leaderboard"], list)
                else (False, "Missing leaderboard field")
            )
        )
        if success:
            leaderboard_count = len(data.get("leaderboard", []))
            results.add_pass("GET /api/rewards/leaderboard", f"Returns user ranking system ({leaderboard_count} users)")
        else:
            results.add_fail("GET /api/rewards/leaderboard", data)
        
        # 9. Prayer Times (Mecca coordinates)
        print("\n9. Testing prayer times...")
        success, data = await test_endpoint(
            client, "/prayer-times?lat=21.4225&lon=39.8262",
            validation_func=lambda d: (
                (True, "Prayer times structure valid")
                if "times" in d and "fajr" in d["times"] and "dhuhr" in d["times"]
                else (False, "Invalid prayer times structure")
            )
        )
        if success:
            times = data.get("times", {})
            source = data.get("source", "unknown")
            results.add_pass("GET /api/prayer-times", f"Returns Mecca prayer times via {source} (uses 'lon' parameter ✓)")
        else:
            results.add_fail("GET /api/prayer-times", data)
        
        # 10. Quran Surah 1 (Al-Fatiha)
        print("\n10. Testing Quran Surah 1...")
        success, data = await test_endpoint(
            client, "/quran/surah/1",
            validation_func=lambda d: (
                (True, f"Surah has {len(data.get('data', {}).get('ayahs', []))} verses")
                if "data" in d and "ayahs" in d["data"] and len(d["data"]["ayahs"]) == 7
                else (False, f"Expected 7 verses in Al-Fatiha, found {len(d.get('data', {}).get('ayahs', []))}")
            )
        )
        if success:
            ayahs = len(data.get("data", {}).get("ayahs", []))
            surah_name = data.get("data", {}).get("englishName", "Al-Fatiha")
            results.add_pass("GET /api/quran/surah/1", f"Returns {surah_name} with {ayahs} verses from Quran API")
        else:
            results.add_fail("GET /api/quran/surah/1", data)
        
        # 11. Hijri Date
        print("\n11. Testing Hijri date...")
        success, data = await test_endpoint(
            client, "/hijri-date",
            validation_func=lambda d: (
                (True, "Hijri date structure valid")
                if "hijriDate" in d and "day" in d and "year" in d
                else (False, "Invalid hijri date structure")
            )
        )
        if success:
            hijri_date = data.get("hijriDate", "")
            results.add_pass("GET /api/hijri-date", f"Returns current Islamic date: {hijri_date}")
        else:
            results.add_fail("GET /api/hijri-date", data)
        
        # 12. Announcements
        print("\n12. Testing announcements...")
        success, data = await test_endpoint(
            client, "/announcements",
            validation_func=lambda d: (
                (True, f"Announcements structure valid ({len(d.get('announcements', []))} active)")
                if "announcements" in d and isinstance(d["announcements"], list)
                else (False, "Invalid announcements structure")
            )
        )
        if success:
            announcements_count = len(data.get("announcements", []))
            results.add_pass("GET /api/announcements", f"Returns {announcements_count} active announcements (0 = normal)")
        else:
            results.add_fail("GET /api/announcements", data)
        
        # 13. Daily Hadith
        print("\n13. Testing daily hadith...")
        success, data = await test_endpoint(
            client, "/daily-hadith",
            validation_func=lambda d: (
                (True, "Daily hadith structure valid")
                if "hadith" in d and "text" in d["hadith"] and "narrator" in d["hadith"]
                else (False, "Invalid daily hadith structure")
            )
        )
        if success:
            hadith_text = data.get("hadith", {}).get("text", "")[:50]
            narrator = data.get("hadith", {}).get("narrator", "")
            results.add_pass("GET /api/daily-hadith", f"Returns daily hadith from {narrator}: '{hadith_text}...'")
        else:
            results.add_fail("GET /api/daily-hadith", data)
        
        # 14. Embed Content (public endpoint for videos)
        print("\n14. Testing embed content...")
        success, data = await test_endpoint(
            client, "/embed-content",
            validation_func=lambda d: (
                (True, f"Embed content structure valid ({len(d.get('content', []))} items)")
                if "content" in d and isinstance(d["content"], list)
                else (False, "Invalid embed content structure")
            )
        )
        if success:
            content_count = len(data.get("content", []))
            results.add_pass("GET /api/embed-content", f"Returns {content_count} embedded videos/content items")
        else:
            results.add_fail("GET /api/embed-content", data)
    
    # Print comprehensive results
    results.print_summary()
    
    # Return exit code
    return 0 if len(results.failed) == 0 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)