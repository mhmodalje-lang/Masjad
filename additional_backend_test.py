#!/usr/bin/env python3
"""
Additional Backend Verification Test
Testing additional endpoints to ensure comprehensive backend functionality
"""

import requests
import json
import sys

BASE_URL = "https://code-cleanup-deploy.preview.emergentagent.com"

def test_additional_endpoints():
    """Test additional endpoints for comprehensive verification"""
    print("🔍 Testing Additional Backend Endpoints...")
    
    endpoints_to_test = [
        ("/api/kids-learn/course/overview", {"locale": "en"}),
        ("/api/kids-learn/course/alphabet", {"locale": "en"}),
        ("/api/quran/v4/chapters", {"language": "en"}),
    ]
    
    results = []
    
    for endpoint, params in endpoints_to_test:
        try:
            url = f"{BASE_URL}{endpoint}"
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ {endpoint} - Status 200")
                results.append(True)
            else:
                print(f"❌ {endpoint} - Status {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")
            results.append(False)
    
    return all(results)

if __name__ == "__main__":
    success = test_additional_endpoints()
    if success:
        print("\n🎉 Additional endpoints verification PASSED!")
    else:
        print("\n💥 Some additional endpoints failed!")