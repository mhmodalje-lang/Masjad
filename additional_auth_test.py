#!/usr/bin/env python3
"""
Additional testing for report and block-user endpoints with proper request bodies
"""

import requests
import json

BACKEND_URL = "https://quran-114-surahs.preview.emergentagent.com"

def test_with_body():
    print("🔍 TESTING REPORT AND BLOCK-USER WITH PROPER REQUEST BODIES")
    print("=" * 60)
    
    # Test report endpoint with proper body
    print("Test 1: Report Content (With Body, No Auth)")
    report_data = {
        "content_id": "test123",
        "content_type": "story",
        "reported_user_id": "user123",
        "reason": "inappropriate",
        "reason_category": "spam",
        "details": "test report"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/report", json=report_data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 401:
            print("✅ PASS - Returns 401 for authentication as expected")
        else:
            print(f"⚠️  Returns {response.status_code} instead of 401")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test block-user endpoint with proper body
    print("Test 2: Block User (With Body, No Auth)")
    block_data = {
        "user_id": "user123"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/block-user", json=block_data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 401:
            print("✅ PASS - Returns 401 for authentication as expected")
        else:
            print(f"⚠️  Returns {response.status_code} instead of 401")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_with_body()