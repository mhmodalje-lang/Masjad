#!/usr/bin/env python3
"""
App Store Compliance Backend API Testing
Tests the specific endpoints required for App Store & Play Store compliance
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend/.env
BACKEND_URL = "https://multilang-app-fix.preview.emergentagent.com"

def test_delete_account_endpoint():
    """Test DELETE /api/auth/delete-account - Account deletion endpoint"""
    print("🧪 Testing DELETE /api/auth/delete-account...")
    
    url = f"{BACKEND_URL}/api/auth/delete-account"
    
    # Test 1: No authentication token
    print("   Test 1: No authentication token")
    try:
        response = requests.delete(url, timeout=10)
        print(f"     Status Code: {response.status_code}")
        print(f"     Response: {response.text[:100]}...")
        
        if response.status_code == 401:
            print("     ✅ PASS: Correctly returns 401 without auth token")
        else:
            print(f"     ❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"     ❌ ERROR: {e}")
        return False
    
    # Test 2: Invalid authentication token
    print("   Test 2: Invalid authentication token")
    try:
        headers = {"Authorization": "Bearer invalid_token_12345"}
        response = requests.delete(url, headers=headers, timeout=10)
        print(f"     Status Code: {response.status_code}")
        print(f"     Response: {response.text[:100]}...")
        
        if response.status_code == 401:
            print("     ✅ PASS: Correctly returns 401 with invalid token")
        else:
            print(f"     ❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"     ❌ ERROR: {e}")
        return False
    
    # Test 3: Malformed authentication header
    print("   Test 3: Malformed authentication header")
    try:
        headers = {"Authorization": "InvalidFormat token123"}
        response = requests.delete(url, headers=headers, timeout=10)
        print(f"     Status Code: {response.status_code}")
        print(f"     Response: {response.text[:100]}...")
        
        if response.status_code == 401:
            print("     ✅ PASS: Correctly returns 401 with malformed auth")
        else:
            print(f"     ❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"     ❌ ERROR: {e}")
        return False
    
    print("   ✅ OVERALL PASS: Account deletion endpoint exists and handles auth properly")
    return True

def test_report_content_endpoint():
    """Test POST /api/report - Content reporting endpoint"""
    print("🧪 Testing POST /api/report...")
    
    url = f"{BACKEND_URL}/api/report"
    
    # Test 1: No authentication token
    print("   Test 1: No authentication token")
    try:
        payload = {
            "content_id": "test_post_123",
            "content_type": "post",
            "reported_user_id": "user_456",
            "reason": "Inappropriate content",
            "reason_category": "inappropriate",
            "details": "This content violates community guidelines"
        }
        response = requests.post(url, json=payload, timeout=10)
        print(f"     Status Code: {response.status_code}")
        print(f"     Response: {response.text[:100]}...")
        
        if response.status_code == 401:
            print("     ✅ PASS: Correctly returns 401 without auth token")
        else:
            print(f"     ❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"     ❌ ERROR: {e}")
        return False
    
    # Test 2: Invalid authentication token
    print("   Test 2: Invalid authentication token")
    try:
        headers = {"Authorization": "Bearer invalid_token_12345"}
        payload = {
            "content_id": "test_comment_789",
            "content_type": "comment",
            "reported_user_id": "user_101",
            "reason": "Spam content",
            "reason_category": "spam",
            "details": "User is posting spam repeatedly"
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"     Status Code: {response.status_code}")
        print(f"     Response: {response.text[:100]}...")
        
        if response.status_code == 401:
            print("     ✅ PASS: Correctly returns 401 with invalid token")
        else:
            print(f"     ❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"     ❌ ERROR: {e}")
        return False
    
    print("   ✅ OVERALL PASS: Report content endpoint exists and handles auth properly")
    return True

def test_block_user_endpoint():
    """Test POST /api/block-user - User blocking endpoint"""
    print("🧪 Testing POST /api/block-user...")
    
    url = f"{BACKEND_URL}/api/block-user"
    
    # Test 1: No authentication token
    print("   Test 1: No authentication token")
    try:
        payload = {"user_id": "user_to_block_123"}
        response = requests.post(url, json=payload, timeout=10)
        print(f"     Status Code: {response.status_code}")
        print(f"     Response: {response.text[:100]}...")
        
        if response.status_code == 401:
            print("     ✅ PASS: Correctly returns 401 without auth token")
        else:
            print(f"     ❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"     ❌ ERROR: {e}")
        return False
    
    # Test 2: Invalid authentication token
    print("   Test 2: Invalid authentication token")
    try:
        headers = {"Authorization": "Bearer invalid_token_12345"}
        payload = {"user_id": "user_to_block_456"}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"     Status Code: {response.status_code}")
        print(f"     Response: {response.text[:100]}...")
        
        if response.status_code == 401:
            print("     ✅ PASS: Correctly returns 401 with invalid token")
        else:
            print(f"     ❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"     ❌ ERROR: {e}")
        return False
    
    print("   ✅ OVERALL PASS: Block user endpoint exists and handles auth properly")
    return True

def test_blocked_users_endpoint():
    """Test GET /api/blocked-users - Get blocked users list"""
    print("🧪 Testing GET /api/blocked-users...")
    
    url = f"{BACKEND_URL}/api/blocked-users"
    
    # Test 1: No authentication token
    print("   Test 1: No authentication token")
    try:
        response = requests.get(url, timeout=10)
        print(f"     Status Code: {response.status_code}")
        print(f"     Response: {response.text[:100]}...")
        
        if response.status_code == 401:
            print("     ✅ PASS: Correctly returns 401 without auth token")
        else:
            print(f"     ❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"     ❌ ERROR: {e}")
        return False
    
    # Test 2: Invalid authentication token
    print("   Test 2: Invalid authentication token")
    try:
        headers = {"Authorization": "Bearer invalid_token_12345"}
        response = requests.get(url, headers=headers, timeout=10)
        print(f"     Status Code: {response.status_code}")
        print(f"     Response: {response.text[:100]}...")
        
        if response.status_code == 401:
            print("     ✅ PASS: Correctly returns 401 with invalid token")
        else:
            print(f"     ❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"     ❌ ERROR: {e}")
        return False
    
    print("   ✅ OVERALL PASS: Blocked users endpoint exists and handles auth properly")
    return True

def test_health_endpoint():
    """Test GET /api/health - Health check endpoint"""
    print("🧪 Testing GET /api/health...")
    
    url = f"{BACKEND_URL}/api/health"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    print("   ✅ PASS: Health endpoint returns healthy status")
                    return True
                else:
                    print(f"   ❌ FAIL: Health endpoint doesn't return healthy status: {data}")
                    return False
            except json.JSONDecodeError:
                print("   ❌ FAIL: Health endpoint doesn't return valid JSON")
                return False
        else:
            print(f"   ❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_pages_endpoint():
    """Test GET /api/pages - Privacy/Terms pages endpoint"""
    print("🧪 Testing GET /api/pages...")
    
    url = f"{BACKEND_URL}/api/pages"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if "pages" in data and isinstance(data["pages"], list):
                    print(f"   ✅ PASS: Pages endpoint returns pages list (count: {len(data['pages'])})")
                    return True
                else:
                    print(f"   ❌ FAIL: Pages endpoint doesn't return pages array: {data}")
                    return False
            except json.JSONDecodeError:
                print("   ❌ FAIL: Pages endpoint doesn't return valid JSON")
                return False
        else:
            print(f"   ❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_frontend_privacy_terms_routes():
    """Test frontend routes /privacy and /terms return 200"""
    print("🧪 Testing frontend privacy/terms routes...")
    
    base_url = BACKEND_URL.replace("/api", "")  # Remove /api for frontend routes
    
    routes = ["/privacy", "/terms"]
    all_passed = True
    
    for route in routes:
        print(f"   Testing {route}...")
        try:
            url = f"{base_url}{route}"
            response = requests.get(url, timeout=10)
            print(f"     Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"     ✅ PASS: {route} returns 200")
            else:
                print(f"     ❌ FAIL: {route} returns {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"     ❌ ERROR testing {route}: {e}")
            all_passed = False
    
    if all_passed:
        print("   ✅ OVERALL PASS: Privacy/Terms routes accessible")
        return True
    else:
        print("   ❌ OVERALL FAIL: Some privacy/terms routes not accessible")
        return False

def main():
    """Run all App Store compliance tests"""
    print("🚀 Starting App Store Compliance Backend API Tests")
    print(f"📍 Backend URL: {BACKEND_URL}")
    print("=" * 70)
    
    tests = [
        ("Account Deletion Endpoint", test_delete_account_endpoint),
        ("Report Content Endpoint", test_report_content_endpoint),
        ("Block User Endpoint", test_block_user_endpoint),
        ("Get Blocked Users", test_blocked_users_endpoint),
        ("Health Check", test_health_endpoint),
        ("Pages Endpoint", test_pages_endpoint),
        ("Privacy & Terms Routes", test_frontend_privacy_terms_routes),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 50)
        success = test_func()
        results.append((test_name, success))
        print()
    
    # Summary
    print("=" * 70)
    print("📊 APP STORE COMPLIANCE TEST SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All App Store compliance tests passed!")
        print("✅ App is ready for App Store submission regarding these endpoints")
        return 0
    else:
        print("⚠️  Some compliance tests failed - check details above")
        print("❌ App Store submission may be rejected due to missing compliance features")
        return 1

if __name__ == "__main__":
    sys.exit(main())