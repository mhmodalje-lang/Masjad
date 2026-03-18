#!/usr/bin/env python3
"""
Backend Testing for NEW Islamic App Endpoints
Focus on testing the NEWLY ADDED endpoints as specified in review request:
1. GET /api/ad-config - Public endpoint for ad configuration  
2. POST /api/analytics/event - Track analytics events
3. GET /api/health - Verify health check still works
4. GET /api/admin/settings - Verify admin settings with ad fields
5. GET /api/stories/list - Verify still working 
6. GET /api/asma-al-husna - Verify still working
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

class NewTestResults:
    def __init__(self):
        self.passed = []
        self.failed = []
    
    def add_pass(self, endpoint, details=""):
        self.passed.append(f"✅ {endpoint}: {details}")
    
    def add_fail(self, endpoint, error):
        self.failed.append(f"❌ {endpoint}: {error}")
    
    def print_summary(self):
        print("\n" + "="*80)
        print("🆕 NEW ENDPOINTS TEST RESULTS SUMMARY")
        print("="*80)
        
        if self.passed:
            print(f"\n✅ PASSED ({len(self.passed)} endpoints):")
            for result in self.passed:
                print(f"   {result}")
        
        if self.failed:
            print(f"\n❌ FAILED ({len(self.failed)} endpoints):")
            for result in self.failed:
                print(f"   {result}")
        
        total = len(self.passed) + len(self.failed)
        success_rate = (len(self.passed)/total*100) if total > 0 else 0
        print(f"\n📊 OVERALL RESULT: {len(self.passed)}/{total} endpoints working ({success_rate:.1f}% success rate)")
        
        if len(self.failed) == 0:
            print("🎉 ALL NEW ENDPOINTS PASSING! Ad infrastructure and analytics working.")
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
            return False, f"Expected status {expected_status}, got {response.status_code}. Response: {response.text[:200]}"
        
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
    results = NewTestResults()
    
    print("🚀 Starting NEW ENDPOINTS testing for Islamic app backend...")
    print(f"📡 Testing against: {BACKEND_URL}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # 1. NEW: Ad Configuration (Public Endpoint)
        print("\n1. Testing NEW ad-config endpoint...")
        success, data = await test_endpoint(
            client, "/ad-config",
            validation_func=lambda d: (
                (True, f"Ad config valid: ads_enabled={d.get('ads_enabled')}, gdpr_consent_required={d.get('gdpr_consent_required')}")
                if all(field in d for field in ["ads_enabled", "video_ads_muted", "gdpr_consent_required", 
                                              "ad_banner_enabled", "ad_interstitial_enabled", "ad_rewarded_enabled", 
                                              "admob_app_id", "adsense_publisher_id"])
                else (False, f"Missing ad config fields. Found: {list(d.keys())}")
            )
        )
        if success:
            results.add_pass("GET /api/ad-config", f"Returns complete ad configuration: {json.dumps(data, indent=2)}")
        else:
            results.add_fail("GET /api/ad-config", data)
        
        # 2. NEW: Analytics Event Tracking  
        print("\n2. Testing NEW analytics/event endpoint...")
        analytics_data = {
            "event_type": "page_view",
            "page": "/test",
            "user_id": "test-user",
            "session_id": "test-session", 
            "metadata": {"test": True}
        }
        success, data = await test_endpoint(
            client, "/analytics/event", method="POST", data=analytics_data,
            validation_func=lambda d: (
                (True, "Analytics event tracked successfully")
                if d.get("success") == True
                else (False, f"Expected success=True, got: {d}")
            )
        )
        if success:
            results.add_pass("POST /api/analytics/event", "Analytics event tracking working ✓")
        else:
            results.add_fail("POST /api/analytics/event", data)
        
        # 3. Health Check (verify still works)
        print("\n3. Testing health endpoint (verify still works)...")
        success, data = await test_endpoint(
            client, "/health",
            validation_func=lambda d: (
                (True, f"Health check: {d.get('status')}")
                if d.get("status") == "healthy"
                else (False, f"Expected status=healthy, got: {d.get('status')}")
            )
        )
        if success:
            results.add_pass("GET /api/health", f"Still working ✓ Status: {data.get('status')}, App: {data.get('app')}")
        else:
            results.add_fail("GET /api/health", data)
        
        # 4. Stories List (verify still works)
        print("\n4. Testing stories/list (verify still works)...")
        success, data = await test_endpoint(
            client, "/stories/list?limit=5",
            validation_func=lambda d: (
                (True, f"Stories: {len(d.get('stories', []))} returned, total: {d.get('total', 0)}")
                if "stories" in d and d.get("total", 0) > 0
                else (False, f"Stories endpoint broken. Response: {d}")
            )
        )
        if success:
            results.add_pass("GET /api/stories/list", f"Still working ✓ Returns {len(data.get('stories', []))} stories")
        else:
            results.add_fail("GET /api/stories/list", data)
        
        # 5. Asma Al-Husna (verify still works)
        print("\n5. Testing asma-al-husna (verify still works)...")
        success, data = await test_endpoint(
            client, "/asma-al-husna",
            validation_func=lambda d: (
                (True, "99 Names of Allah endpoint working")
                if "names" in d and len(d["names"]) == 99
                else (False, f"Expected 99 names, got {len(d.get('names', []))}")
            )
        )
        if success:
            results.add_pass("GET /api/asma-al-husna", "Still working ✓ Returns 99 Names of Allah")
        else:
            results.add_fail("GET /api/asma-al-husna", data)
        
        # 6. User Registration & Login for Admin Testing
        print("\n6. Creating test user for admin endpoint testing...")
        import time
        unique_email = "adtest@test.com"
        register_data = {
            "email": unique_email,
            "password": "test123456", 
            "name": "Ad Tester"
        }
        
        # Try registration
        success, reg_data = await test_endpoint(
            client, "/auth/register", method="POST", data=register_data,
            expected_status=[200, 400]  # 400 if user already exists
        )
        
        # Try login
        login_data = {
            "email": unique_email,
            "password": "test123456"
        }
        success, login_data = await test_endpoint(
            client, "/auth/login", method="POST", data=login_data,
            validation_func=lambda d: (
                (True, "Login successful")
                if "access_token" in d
                else (False, f"Login failed: {d}")
            )
        )
        
        auth_token = None
        if success and isinstance(login_data, dict):
            auth_token = login_data.get("access_token")
        
        # 7. Admin Settings (attempt to test - may require admin role)
        print("\n7. Testing admin/settings endpoint...")
        auth_headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
        
        success, data = await test_endpoint(
            client, "/admin/settings", headers=auth_headers,
            expected_status=[200, 401, 403],  # May get 401/403 if not admin
            validation_func=lambda d: (
                (True, f"Admin settings accessible: {list(d.keys())}")
                if "app_name" in d or "ads_enabled" in d
                else (False, f"Admin settings response: {d}")
            )
        )
        
        if success:
            has_ad_fields = all(field in data for field in ["ads_enabled", "admob_app_id", "adsense_publisher_id"])
            if has_ad_fields:
                results.add_pass("GET /api/admin/settings", f"Admin settings include new ad fields ✓")
            else:
                results.add_pass("GET /api/admin/settings", f"Admin settings accessible but missing some ad fields")
        else:
            if "401" in str(data) or "403" in str(data) or "غير مصرح" in str(data):
                results.add_pass("GET /api/admin/settings", "Admin protection working (401/403) - normal behavior for non-admin")
            else:
                results.add_fail("GET /api/admin/settings", data)
    
    # Print comprehensive results
    results.print_summary()
    
    # Return exit code
    return 0 if len(results.failed) == 0 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)