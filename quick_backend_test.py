#!/usr/bin/env python3
"""
Backend API Testing for Islamic Prayer App (أذان وحكاية)
Testing specific endpoints after frontend-only changes (sound mode feature)
Review Request: Test 3 specific endpoints to ensure backend still works after frontend changes
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend/.env
BACKEND_URL = "https://mobile-deploy-23.preview.emergentagent.com"

def test_endpoint(endpoint, description, expected_checks=None):
    """Test a single API endpoint"""
    url = f"{BACKEND_URL}{endpoint}"
    print(f"\n🔍 Testing: {description}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ SUCCESS: {description}")
                
                # Run specific checks if provided
                if expected_checks:
                    for check_name, check_func in expected_checks.items():
                        try:
                            result = check_func(data)
                            if result:
                                print(f"  ✅ {check_name}: {result}")
                            else:
                                print(f"  ❌ {check_name}: Failed")
                        except Exception as e:
                            print(f"  ❌ {check_name}: Error - {str(e)}")
                
                # Show sample of response data
                if isinstance(data, dict):
                    if len(str(data)) > 500:
                        print(f"Response sample: {str(data)[:500]}...")
                    else:
                        print(f"Response: {data}")
                elif isinstance(data, list):
                    print(f"Response: List with {len(data)} items")
                    if data and len(str(data[0])) < 200:
                        print(f"First item: {data[0]}")
                
                return True, data
                
            except json.JSONDecodeError:
                print(f"❌ FAILED: {description} - Invalid JSON response")
                print(f"Response text: {response.text[:200]}...")
                return False, None
        else:
            print(f"❌ FAILED: {description} - Status {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False, None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED: {description} - Request error: {str(e)}")
        return False, None

def main():
    """Run all backend API tests"""
    print("=" * 60)
    print("🕌 Islamic Prayer App Backend API Testing")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Purpose: Verify backend still works after frontend sound mode changes")
    
    # Test results tracking
    tests = []
    
    # Test 1: Health Check
    success, data = test_endpoint(
        "/api/health",
        "Health Check",
        {
            "Has status": lambda d: d.get("status") == "healthy",
            "Has app name": lambda d: "أذان وحكاية" in str(d.get("app", ""))
        }
    )
    tests.append(("Health Check", success))
    
    # Test 2: Prayer Times
    success, data = test_endpoint(
        "/api/prayer-times?lat=48.2&lon=16.3",
        "Prayer Times (Vienna coordinates)",
        {
            "Has prayer times": lambda d: "fajr" in str(d).lower() or "maghrib" in str(d).lower(),
            "Has location data": lambda d: "lat" in str(d) or "location" in str(d),
            "Valid response structure": lambda d: isinstance(d, dict) and len(d) > 0
        }
    )
    tests.append(("Prayer Times", success))
    
    # Test 3: Arabic Academy Letters
    success, data = test_endpoint(
        "/api/arabic-academy/letters",
        "Arabic Academy Letters",
        {
            "Has 28 letters": lambda d: len(d) == 28 if isinstance(d, list) else False,
            "Letters have Arabic content": lambda d: any("ا" in str(item) or "ب" in str(item) for item in d) if isinstance(d, list) else False,
            "Letters have meaning": lambda d: any("meaning" in str(item).lower() for item in d) if isinstance(d, list) else False
        }
    )
    tests.append(("Arabic Academy Letters", success))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Backend is working correctly!")
        print("✅ Frontend sound mode changes did not break backend functionality")
        return 0
    else:
        print("⚠️  Some tests failed - Backend may have issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())