#!/usr/bin/env python3
"""
Review Request Specific Backend API Testing
==========================================
Testing the exact 7 endpoints mentioned in the review request:

1. GET /api/health - Should return 200
2. GET /api/quran/v4/chapters?language=ar - Should return 200 with Arabic chapters
3. GET /api/quran/v4/chapters?language=en - Should return 200 with English chapters
4. GET /api/kids-learn/daily-games?locale=en - Should return 200
5. GET /api/kids-learn/daily-games?locale=ar - Should return 200
6. GET /api/sohba/posts - Should return 200
7. GET /api/sohba/categories - Should return 200

Focus: Verify no backend regressions from translation file updates.
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend/.env
BACKEND_URL = "https://multilang-sync-3.preview.emergentagent.com"

# Review request specific endpoints
REVIEW_ENDPOINTS = [
    {
        "endpoint": "/api/health",
        "name": "Health Check",
        "description": "Backend health status"
    },
    {
        "endpoint": "/api/quran/v4/chapters?language=ar",
        "name": "Quran Chapters (Arabic)",
        "description": "Arabic chapters list"
    },
    {
        "endpoint": "/api/quran/v4/chapters?language=en",
        "name": "Quran Chapters (English)",
        "description": "English chapters list"
    },
    {
        "endpoint": "/api/kids-learn/daily-games?locale=en",
        "name": "Kids Daily Games (English)",
        "description": "English daily games"
    },
    {
        "endpoint": "/api/kids-learn/daily-games?locale=ar",
        "name": "Kids Daily Games (Arabic)",
        "description": "Arabic daily games"
    },
    {
        "endpoint": "/api/sohba/posts",
        "name": "Sohba Posts",
        "description": "Social posts"
    },
    {
        "endpoint": "/api/sohba/categories",
        "name": "Sohba Categories",
        "description": "Social categories"
    }
]

def test_endpoint(endpoint_info):
    """Test a single endpoint"""
    endpoint = endpoint_info["endpoint"]
    name = endpoint_info["name"]
    description = endpoint_info["description"]
    
    full_url = f"{BACKEND_URL}{endpoint}"
    
    print(f"🔍 Testing: {name}")
    print(f"   URL: {full_url}")
    print(f"   Expected: {description}")
    
    try:
        response = requests.get(full_url, timeout=15)
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ PASS - Status 200, Valid JSON response")
                
                # Show data summary
                if isinstance(data, dict):
                    if "chapters" in data:
                        print(f"      📊 Found {len(data['chapters'])} chapters")
                    elif "games" in data:
                        print(f"      📊 Found {len(data['games'])} games")
                    elif "posts" in data:
                        print(f"      📊 Found {len(data['posts'])} posts")
                    elif "categories" in data:
                        print(f"      📊 Found {len(data['categories'])} categories")
                    elif "status" in data:
                        print(f"      📊 Health status: {data['status']}")
                elif isinstance(data, list):
                    print(f"      📊 Found {len(data)} items")
                
                return True
                
            except json.JSONDecodeError:
                print(f"   ❌ FAIL - Status 200 but invalid JSON")
                return False
        else:
            print(f"   ❌ FAIL - Status {response.status_code}")
            print(f"      Error: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"   ❌ FAIL - Request timeout (15s)")
        return False
    except requests.exceptions.ConnectionError:
        print(f"   ❌ FAIL - Connection error")
        return False
    except Exception as e:
        print(f"   ❌ FAIL - Unexpected error: {str(e)}")
        return False

def main():
    """Main test execution"""
    print("🚀 REVIEW REQUEST BACKEND API TESTING")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Focus: Translation file regression testing")
    print("="*80)
    
    results = []
    
    # Test all review request endpoints
    for i, endpoint_info in enumerate(REVIEW_ENDPOINTS, 1):
        print(f"\n{i}. {endpoint_info['name'].upper()}")
        print("-" * 60)
        
        success = test_endpoint(endpoint_info)
        results.append({
            "endpoint": endpoint_info["endpoint"],
            "name": endpoint_info["name"],
            "success": success
        })
    
    # Summary
    print("\n" + "="*80)
    print("REVIEW REQUEST TESTING SUMMARY")
    print("="*80)
    
    total_tests = len(results)
    passed_tests = len([r for r in results if r["success"]])
    failed_tests = total_tests - passed_tests
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"📊 OVERALL RESULTS:")
    print(f"   Total Endpoints: {total_tests}")
    print(f"   ✅ Passed: {passed_tests}")
    print(f"   ❌ Failed: {failed_tests}")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    print(f"\n📋 DETAILED RESULTS:")
    for result in results:
        status_icon = "✅" if result["success"] else "❌"
        status_text = "PASS" if result["success"] else "FAIL"
        print(f"   {status_icon} {result['name']}: {status_text}")
    
    if failed_tests > 0:
        print(f"\n❌ FAILED ENDPOINTS:")
        for result in results:
            if not result["success"]:
                print(f"   - {result['name']}: {result['endpoint']}")
    
    print(f"\n🎯 REVIEW REQUEST COMPLIANCE:")
    if passed_tests == total_tests:
        print("   ✅ ALL 7 ENDPOINTS RETURNING 200 STATUS CODES")
        print("   ✅ NO BACKEND REGRESSIONS FROM TRANSLATION FILE UPDATES")
        print("   ✅ BACKEND API FULLY FUNCTIONAL")
    else:
        print(f"   ❌ {failed_tests} ENDPOINT(S) FAILING")
        print("   ⚠️  POTENTIAL BACKEND REGRESSION DETECTED")
    
    # Save results
    results_file = "/app/review_request_results.json"
    with open(results_file, "w") as f:
        json.dump({
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": success_rate,
                "all_endpoints_working": failed_tests == 0
            },
            "detailed_results": results,
            "test_date": datetime.now().isoformat(),
            "backend_url": BACKEND_URL
        }, f, indent=2)
    
    print(f"\n📄 Results saved to: {results_file}")
    
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)