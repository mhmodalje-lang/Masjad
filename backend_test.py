#!/usr/bin/env python3
"""
Islamic App Backend API Testing - Review Request Specific
=========================================================
Testing the exact endpoints mentioned in the review request.

Review Request Endpoints:
1. Health: GET /api/health
2. Quran chapters: GET /api/quran/v4/chapters?language=ar
3. Quran chapters English: GET /api/quran/v4/chapters?language=en
4. Global verse: GET /api/quran/v4/global-verse/2/255?language=ar
5. Global verse English: GET /api/quran/v4/global-verse/1/1?language=en
6. Kids learn daily games: GET /api/kids-learn/daily-games?locale=en
7. Kids learn daily games Arabic: GET /api/kids-learn/daily-games?locale=ar
8. Sohba sessions: GET /api/sohba/sessions
9. Tafsir: GET /api/quran/v4/global-verse/2/1?language=ar

All endpoints should return 200 status codes.
"""

import requests
import json
import sys
from typing import Dict, List, Any
from datetime import datetime

# Backend URL from frontend/.env
BACKEND_URL = "https://multilang-sync-3.preview.emergentagent.com"

# Test results storage
test_results = []

def log_test(test_name: str, endpoint: str, status: str, status_code: int = None, details: str = "", response_data: Any = None):
    """Log test result with comprehensive details"""
    result = {
        "test": test_name,
        "endpoint": endpoint,
        "status": status,
        "status_code": status_code,
        "details": details,
        "timestamp": datetime.now().isoformat(),
        "response_preview": str(response_data)[:200] + "..." if response_data and len(str(response_data)) > 200 else str(response_data)
    }
    test_results.append(result)
    
    status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"{status_icon} {test_name}: {status} (Status: {status_code})")
    if details:
        print(f"   Details: {details}")

def test_endpoint(endpoint: str, test_name: str) -> Dict[str, Any]:
    """Test a single endpoint with comprehensive error handling"""
    full_url = f"{BACKEND_URL}{endpoint}"
    print(f"\n🔍 Testing: {test_name}")
    print(f"   URL: {full_url}")
    
    try:
        response = requests.get(full_url, timeout=15)
        
        # Log the response
        if response.status_code == 200:
            try:
                data = response.json()
                log_test(test_name, endpoint, "PASS", response.status_code, 
                        f"Successfully returned data", data)
                return {"success": True, "data": data, "status_code": response.status_code}
            except json.JSONDecodeError:
                log_test(test_name, endpoint, "FAIL", response.status_code, 
                        "Response is not valid JSON", response.text[:200])
                return {"success": False, "error": "Invalid JSON response", "status_code": response.status_code}
        else:
            log_test(test_name, endpoint, "FAIL", response.status_code, 
                    f"HTTP {response.status_code}: {response.text[:200]}")
            return {"success": False, "error": response.text, "status_code": response.status_code}
            
    except requests.exceptions.Timeout:
        log_test(test_name, endpoint, "FAIL", None, "Request timeout (15s)")
        return {"success": False, "error": "Timeout"}
    except requests.exceptions.ConnectionError:
        log_test(test_name, endpoint, "FAIL", None, "Connection error")
        return {"success": False, "error": "Connection error"}
    except Exception as e:
        log_test(test_name, endpoint, "FAIL", None, f"Unexpected error: {str(e)}")
        return {"success": False, "error": str(e)}

def test_health_endpoint():
    """Test the health endpoint"""
    print("\n" + "="*60)
    print("1. TESTING HEALTH ENDPOINT")
    print("="*60)
    
    result = test_endpoint("/api/health", "Health Check")
    
    if result["success"]:
        data = result["data"]
        print(f"   ✅ Health Status: {data}")
    
    return result["success"]

def test_quran_chapters():
    """Test Quran chapters endpoints"""
    print("\n" + "="*60)
    print("2. TESTING QURAN CHAPTERS ENDPOINTS")
    print("="*60)
    
    results = []
    
    # Test Arabic chapters
    result_ar = test_endpoint("/api/quran/v4/chapters?language=ar", "Quran Chapters (Arabic)")
    results.append(result_ar["success"])
    
    if result_ar["success"]:
        chapters = result_ar["data"]
        if isinstance(chapters, dict) and "chapters" in chapters:
            chapter_count = len(chapters["chapters"])
            print(f"   ✅ Found {chapter_count} Arabic chapters")
        elif isinstance(chapters, list):
            chapter_count = len(chapters)
            print(f"   ✅ Found {chapter_count} Arabic chapters")
    
    # Test English chapters
    result_en = test_endpoint("/api/quran/v4/chapters?language=en", "Quran Chapters (English)")
    results.append(result_en["success"])
    
    if result_en["success"]:
        chapters = result_en["data"]
        if isinstance(chapters, dict) and "chapters" in chapters:
            chapter_count = len(chapters["chapters"])
            print(f"   ✅ Found {chapter_count} English chapters")
        elif isinstance(chapters, list):
            chapter_count = len(chapters)
            print(f"   ✅ Found {chapter_count} English chapters")
    
    return all(results)

def test_global_verses():
    """Test global verse endpoints"""
    print("\n" + "="*60)
    print("3. TESTING GLOBAL VERSE ENDPOINTS")
    print("="*60)
    
    results = []
    
    # Test Ayat al-Kursi (2:255) in Arabic
    result_kursi = test_endpoint("/api/quran/v4/global-verse/2/255?language=ar", "Ayat al-Kursi (Arabic)")
    results.append(result_kursi["success"])
    
    if result_kursi["success"]:
        verse_data = result_kursi["data"]
        print(f"   ✅ Ayat al-Kursi data: {str(verse_data)[:100]}...")
    
    # Test first verse (1:1) in English
    result_first = test_endpoint("/api/quran/v4/global-verse/1/1?language=en", "First Verse (English)")
    results.append(result_first["success"])
    
    if result_first["success"]:
        verse_data = result_first["data"]
        print(f"   ✅ First verse data: {str(verse_data)[:100]}...")
    
    # Test Tafsir endpoint (2:1) in Arabic
    result_tafsir = test_endpoint("/api/quran/v4/global-verse/2/1?language=ar", "Tafsir Verse (Arabic)")
    results.append(result_tafsir["success"])
    
    if result_tafsir["success"]:
        verse_data = result_tafsir["data"]
        print(f"   ✅ Tafsir verse data: {str(verse_data)[:100]}...")
    
    return all(results)

def test_kids_learn_daily_games():
    """Test kids learn daily games endpoints"""
    print("\n" + "="*60)
    print("4. TESTING KIDS LEARN DAILY GAMES ENDPOINTS")
    print("="*60)
    
    results = []
    
    # Test English daily games
    result_en = test_endpoint("/api/kids-learn/daily-games?locale=en", "Kids Daily Games (English)")
    results.append(result_en["success"])
    
    if result_en["success"]:
        games_data = result_en["data"]
        if isinstance(games_data, dict) and "games" in games_data:
            game_count = len(games_data["games"])
            print(f"   ✅ Found {game_count} English daily games")
        elif isinstance(games_data, list):
            game_count = len(games_data)
            print(f"   ✅ Found {game_count} English daily games")
    
    # Test Arabic daily games
    result_ar = test_endpoint("/api/kids-learn/daily-games?locale=ar", "Kids Daily Games (Arabic)")
    results.append(result_ar["success"])
    
    if result_ar["success"]:
        games_data = result_ar["data"]
        if isinstance(games_data, dict) and "games" in games_data:
            game_count = len(games_data["games"])
            print(f"   ✅ Found {game_count} Arabic daily games")
        elif isinstance(games_data, list):
            game_count = len(games_data)
            print(f"   ✅ Found {game_count} Arabic daily games")
    
    return all(results)

def test_sohba_endpoints():
    """Test Sohba endpoints (corrected from review request)"""
    print("\n" + "="*60)
    print("5. TESTING SOHBA ENDPOINTS")
    print("="*60)
    
    # Test the requested endpoint (which doesn't exist)
    result_sessions = test_endpoint("/api/sohba/sessions", "Sohba Sessions (Requested)")
    
    # Test the actual working sohba endpoints
    result_posts = test_endpoint("/api/sohba/posts", "Sohba Posts (Actual)")
    result_categories = test_endpoint("/api/sohba/categories", "Sohba Categories (Actual)")
    
    if result_posts["success"]:
        posts_data = result_posts["data"]
        if isinstance(posts_data, dict) and "posts" in posts_data:
            post_count = len(posts_data["posts"])
            total_count = posts_data.get("total", post_count)
            print(f"   ✅ Found {post_count} Sohba posts (total: {total_count})")
        elif isinstance(posts_data, list):
            post_count = len(posts_data)
            print(f"   ✅ Found {post_count} Sohba posts")
    
    if result_categories["success"]:
        categories_data = result_categories["data"]
        if isinstance(categories_data, dict) and "categories" in categories_data:
            category_count = len(categories_data["categories"])
            print(f"   ✅ Found {category_count} Sohba categories")
        elif isinstance(categories_data, list):
            category_count = len(categories_data)
            print(f"   ✅ Found {category_count} Sohba categories")
    
    # Return true if at least one sohba endpoint works
    return result_posts["success"] or result_categories["success"]

def print_comprehensive_summary():
    """Print comprehensive test summary"""
    print("\n" + "="*80)
    print("ISLAMIC APP BACKEND API TESTING SUMMARY")
    print("="*80)
    
    total_tests = len(test_results)
    passed_tests = len([r for r in test_results if r["status"] == "PASS"])
    failed_tests = len([r for r in test_results if r["status"] == "FAIL"])
    
    print(f"📊 OVERALL RESULTS:")
    print(f"   Total Tests: {total_tests}")
    print(f"   ✅ Passed: {passed_tests}")
    print(f"   ❌ Failed: {failed_tests}")
    print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print(f"\n📋 ENDPOINT RESULTS:")
    for result in test_results:
        status_icon = "✅" if result["status"] == "PASS" else "❌"
        print(f"   {status_icon} {result['test']}: {result['status']} ({result['status_code']})")
    
    if failed_tests > 0:
        print(f"\n❌ FAILED TESTS DETAILS:")
        for result in test_results:
            if result["status"] == "FAIL":
                print(f"   - {result['test']}")
                print(f"     Endpoint: {result['endpoint']}")
                print(f"     Status Code: {result['status_code']}")
                print(f"     Details: {result['details']}")
                print()
    
    print(f"\n🎯 REVIEW REQUEST COMPLIANCE:")
    if passed_tests == total_tests:
        print("   ✅ ALL ENDPOINTS RETURNING 200 STATUS CODES")
        print("   ✅ Health endpoint working")
        print("   ✅ Quran chapters (Arabic & English) working")
        print("   ✅ Global verses (Arabic & English) working")
        print("   ✅ Kids learn daily games (English & Arabic) working")
        print("   ✅ Sohba sessions working")
        print("   ✅ Tafsir endpoint working")
    else:
        print(f"   ❌ {failed_tests} ENDPOINTS FAILING")
        print("   ⚠️  Review request requirements not fully met")
    
    return failed_tests == 0

def main():
    """Main test execution"""
    print("🚀 ISLAMIC APP BACKEND API TESTING")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Focus: Review Request Specific Endpoints")
    
    # Run all tests
    health_success = test_health_endpoint()
    chapters_success = test_quran_chapters()
    verses_success = test_global_verses()
    games_success = test_kids_learn_daily_games()
    sohba_success = test_sohba_endpoints()
    
    # Print comprehensive summary
    all_success = print_comprehensive_summary()
    
    # Save detailed results
    results_file = "/app/backend_test_results.json"
    with open(results_file, "w") as f:
        json.dump({
            "test_summary": {
                "total_tests": len(test_results),
                "passed_tests": len([r for r in test_results if r["status"] == "PASS"]),
                "failed_tests": len([r for r in test_results if r["status"] == "FAIL"]),
                "success_rate": (len([r for r in test_results if r["status"] == "PASS"])/len(test_results))*100,
                "all_endpoints_working": all_success
            },
            "detailed_results": test_results
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {results_file}")
    
    # Return appropriate exit code
    return 0 if all_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)