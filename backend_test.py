#!/usr/bin/env python3
"""
Backend API Testing - Quran.com v4 and Hadith Integration
Tests all required endpoints according to the review request
"""

import asyncio
import httpx
import os
from datetime import datetime

# Get the backend URL from frontend environment
BACKEND_URL = "https://project-flow-73.preview.emergentagent.com/api"

async def test_endpoint(client, url, description):
    """Test a single endpoint and return results"""
    try:
        print(f"\n🔍 Testing: {description}")
        print(f"URL: {url}")
        
        response = await client.get(url)
        status_code = response.status_code
        
        if status_code == 200:
            data = response.json()
            print(f"✅ Status: {status_code}")
            
            # Basic data structure validation
            if isinstance(data, dict):
                if 'data' in data or 'chapters' in data or 'verses' in data or 'collections' in data or 'hadith' in data:
                    print(f"✅ Response structure: Valid")
                    print(f"📊 Response keys: {list(data.keys())[:10]}")  # Show first 10 keys
                    return True, f"✅ {description} - SUCCESS"
                elif 'error' in data:
                    print(f"❌ API Error: {data.get('error')}")
                    return False, f"❌ {description} - API Error: {data.get('error')}"
                else:
                    print(f"⚠️  Unknown structure: {list(data.keys())[:5]}")
                    return True, f"⚠️  {description} - Unknown structure but 200 OK"
            else:
                print(f"⚠️  Non-dict response: {type(data)}")
                return True, f"⚠️  {description} - Non-dict response but 200 OK"
        else:
            print(f"❌ Status: {status_code}")
            try:
                error_data = response.json()
                print(f"❌ Error: {error_data}")
            except:
                print(f"❌ Error text: {response.text[:200]}")
            return False, f"❌ {description} - Status {status_code}"
            
    except httpx.TimeoutException:
        print(f"❌ Timeout after 30 seconds")
        return False, f"❌ {description} - Timeout"
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False, f"❌ {description} - Exception: {str(e)}"

async def main():
    """Run all API tests according to review request"""
    
    print("=" * 80)
    print("🧪 BACKEND API TESTING - Quran.com v4 & Hadith Integration")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"🕒 Test Started: {datetime.now().isoformat()}")
    print("=" * 80)
    
    # Test cases from review request
    test_cases = [
        (f"{BACKEND_URL}/quran/v4/chapters", "GET /api/quran/v4/chapters - Should return all 114 surahs"),
        (f"{BACKEND_URL}/quran/v4/chapters?language=en", "GET /api/quran/v4/chapters?language=en - Should return surahs with English names"),
        (f"{BACKEND_URL}/quran/v4/chapters/1?language=en", "GET /api/quran/v4/chapters/1?language=en - Should return Al-Fatiha info"),
        (f"{BACKEND_URL}/quran/v4/verses/by_chapter/1?language=en", "GET /api/quran/v4/verses/by_chapter/1?language=en - Should return verses with English translation"),
        (f"{BACKEND_URL}/quran/v4/verses/by_chapter/1?language=de", "GET /api/quran/v4/verses/by_chapter/1?language=de - Should return verses with German translation"),
        (f"{BACKEND_URL}/quran/v4/search?q=mercy&language=en", "GET /api/quran/v4/search?q=mercy&language=en - Search Quran"),
        (f"{BACKEND_URL}/quran/v4/juzs", "GET /api/quran/v4/juzs - Fetch all Juz info"),
        (f"{BACKEND_URL}/hadith/collections", "GET /api/hadith/collections - Fetch Hadith collections"),
        (f"{BACKEND_URL}/daily-hadith", "GET /api/daily-hadith - Get daily hadith"),
        (f"{BACKEND_URL}/quran/surah/1", "GET /api/quran/surah/1 - Legacy endpoint still works"),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    # Set timeout and configure client
    timeout = httpx.Timeout(30.0)
    
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        for url, description in test_cases:
            success, message = await test_endpoint(client, url, description)
            results.append(message)
            if success:
                passed += 1
            else:
                failed += 1
            
            # Small delay between tests
            await asyncio.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 TEST SUMMARY")
    print("=" * 80)
    
    for result in results:
        print(result)
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed / (passed + failed) * 100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Backend API is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the issues above.")
    
    print(f"🕒 Test Completed: {datetime.now().isoformat()}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())