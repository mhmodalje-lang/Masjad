#!/usr/bin/env python3
"""
Debugging specific failed endpoints
"""

import requests
import json

BASE_URL = "https://app-ui-updates.preview.emergentagent.com/api"

def test_login_debug():
    """Debug login endpoint"""
    print("=== DEBUGGING LOGIN ENDPOINT ===")
    payload = {
        "email": "newuser@test.com",
        "password": "test123456"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_prayer_times_debug():
    """Debug prayer times endpoint"""
    print("\n=== DEBUGGING PRAYER TIMES ENDPOINT ===")
    params = {"lat": "21.4225", "lng": "39.8262"}
    response = requests.get(f"{BASE_URL}/prayer-times", params=params, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Try with different parameter names
    print("\n--- Trying with 'lon' instead of 'lng' ---")
    params2 = {"lat": "21.4225", "lon": "39.8262"}
    response2 = requests.get(f"{BASE_URL}/prayer-times", params=params2, timeout=10)
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.text}")

def test_ruqyah_debug():
    """Debug ruqyah endpoint"""
    print("\n=== DEBUGGING RUQYAH ENDPOINT ===")
    response = requests.get(f"{BASE_URL}/ruqyah", timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    test_login_debug()
    test_prayer_times_debug()
    test_ruqyah_debug()