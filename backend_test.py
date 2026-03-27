#!/usr/bin/env python3
"""
Backend API Testing for Islamic App
===================================
Testing the following endpoints:
1. GET /api/stories/moderation-status (Public)
2. GET /api/ads/active?placement=prayer/quran/duas/ruqyah/tasbeeh (Public)  
3. POST /api/stories/request-publish (Requires auth - should return 401)
4. GET /api/stories/my-publish-status (Requires auth - should return 401)
5. GET /api/admin/publish-requests (Requires admin auth - should return 401)
6. POST /api/admin/generate-stories (Requires admin auth - should return 401)
7. GET /api/admin/generate-stories/progress (Requires admin auth - should return 401)
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend/.env
BACKEND_URL = "https://content-moderation-266.preview.emergentagent.com/api"

def log_test(test_name, status, details=""):
    """Log test results"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"[{timestamp}] {status_emoji} {test_name}: {status}")
    if details:
        print(f"    Details: {details}")
    print()

def test_moderation_status():
    """Test GET /api/stories/moderation-status"""
    try:
        url = f"{BACKEND_URL}/stories/moderation-status"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "moderation_enabled" in data and isinstance(data["moderation_enabled"], bool):
                log_test("Moderation Status API", "PASS", f"Response: {data}")
                return True
            else:
                log_test("Moderation Status API", "FAIL", f"Invalid response format: {data}")
                return False
        else:
            log_test("Moderation Status API", "FAIL", f"HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        log_test("Moderation Status API", "FAIL", f"Exception: {str(e)}")
        return False

def test_active_ads():
    """Test GET /api/ads/active with different placements"""
    placements = ["prayer", "quran", "duas", "ruqyah", "tasbeeh"]
    all_passed = True
    
    for placement in placements:
        try:
            url = f"{BACKEND_URL}/ads/active?placement={placement}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "ads" in data and isinstance(data["ads"], list):
                    log_test(f"Active Ads API (placement={placement})", "PASS", 
                           f"Found {len(data['ads'])} ads")
                else:
                    log_test(f"Active Ads API (placement={placement})", "FAIL", 
                           f"Invalid response format: {data}")
                    all_passed = False
            else:
                log_test(f"Active Ads API (placement={placement})", "FAIL", 
                       f"HTTP {response.status_code}: {response.text}")
                all_passed = False
                
        except Exception as e:
            log_test(f"Active Ads API (placement={placement})", "FAIL", f"Exception: {str(e)}")
            all_passed = False
    
    return all_passed

def test_auth_protected_endpoints():
    """Test auth-protected endpoints (without auth - expect 401)"""
    auth_endpoints = [
        "/stories/request-publish",  # POST
        "/stories/my-publish-status",  # GET
    ]
    
    results = {}
    
    # Test GET endpoints
    for endpoint in ["/stories/my-publish-status"]:
        try:
            url = f"{BACKEND_URL}{endpoint}"
            response = requests.get(url, timeout=10)
            
            # We expect 401 for auth endpoints without auth
            if response.status_code == 401:
                log_test(f"Auth Endpoint {endpoint}", "PASS", 
                       f"Correctly requires auth (HTTP {response.status_code})")
                results[endpoint] = True
            else:
                log_test(f"Auth Endpoint {endpoint}", "FAIL", 
                       f"Expected 401, got HTTP {response.status_code}: {response.text}")
                results[endpoint] = False
                
        except Exception as e:
            log_test(f"Auth Endpoint {endpoint}", "FAIL", f"Exception: {str(e)}")
            results[endpoint] = False
    
    # Test POST endpoint
    try:
        url = f"{BACKEND_URL}/stories/request-publish"
        response = requests.post(url, json={}, timeout=10)
        
        if response.status_code == 401:
            log_test("Auth Endpoint /stories/request-publish", "PASS", 
                   f"Correctly requires auth (HTTP {response.status_code})")
            results["/stories/request-publish"] = True
        else:
            log_test("Auth Endpoint /stories/request-publish", "FAIL", 
                   f"Expected 401, got HTTP {response.status_code}: {response.text}")
            results["/stories/request-publish"] = False
            
    except Exception as e:
        log_test("Auth Endpoint /stories/request-publish", "FAIL", f"Exception: {str(e)}")
        results["/stories/request-publish"] = False
    
    return all(results.values())

def test_admin_endpoints():
    """Test admin endpoints (without auth - expect 401/403)"""
    admin_endpoints = [
        "/admin/publish-requests",  # GET
        "/admin/generate-stories",  # POST
        "/admin/generate-stories/progress",  # GET
    ]
    
    results = {}
    
    # Test GET endpoints
    for endpoint in ["/admin/publish-requests", "/admin/generate-stories/progress"]:
        try:
            url = f"{BACKEND_URL}{endpoint}"
            response = requests.get(url, timeout=10)
            
            # We expect 401 or 403 for admin endpoints without auth
            if response.status_code in [401, 403]:
                log_test(f"Admin Endpoint {endpoint}", "PASS", 
                       f"Correctly requires auth (HTTP {response.status_code})")
                results[endpoint] = True
            else:
                log_test(f"Admin Endpoint {endpoint}", "FAIL", 
                       f"Expected 401/403, got HTTP {response.status_code}: {response.text}")
                results[endpoint] = False
                
        except Exception as e:
            log_test(f"Admin Endpoint {endpoint}", "FAIL", f"Exception: {str(e)}")
            results[endpoint] = False
    
    # Test POST endpoint
    try:
        url = f"{BACKEND_URL}/admin/generate-stories"
        response = requests.post(url, json={}, timeout=10)
        
        if response.status_code in [401, 403]:
            log_test("Admin Endpoint /admin/generate-stories", "PASS", 
                   f"Correctly requires auth (HTTP {response.status_code})")
            results["/admin/generate-stories"] = True
        else:
            log_test("Admin Endpoint /admin/generate-stories", "FAIL", 
                   f"Expected 401/403, got HTTP {response.status_code}: {response.text}")
            results["/admin/generate-stories"] = False
            
    except Exception as e:
        log_test("Admin Endpoint /admin/generate-stories", "FAIL", f"Exception: {str(e)}")
        results["/admin/generate-stories"] = False
    
    return all(results.values())

def main():
    """Run all backend API tests"""
    print("=" * 60)
    print("🕌 ISLAMIC APP - BACKEND API TESTING")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test results
    results = {}
    
    # Test public endpoints first (as requested)
    print("📋 TESTING PUBLIC ENDPOINTS")
    print("-" * 30)
    results["moderation_status"] = test_moderation_status()
    results["active_ads"] = test_active_ads()
    
    print("🔐 TESTING AUTH-PROTECTED ENDPOINTS (Should return 401)")
    print("-" * 50)
    results["auth_endpoints"] = test_auth_protected_endpoints()
    
    print("👑 TESTING ADMIN ENDPOINTS (Should return 401/403)")
    print("-" * 45)
    results["admin_endpoints"] = test_admin_endpoints()
    
    # Summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print()
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All backend API tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed - check details above")
        return 1

if __name__ == "__main__":
    sys.exit(main())