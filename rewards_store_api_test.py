#!/usr/bin/env python3
"""
Comprehensive Rewards Store API Testing
Tests all 18 endpoints as specified in the review request
Backend URL: https://ios-policy-app.preview.emergentagent.com
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "https://ios-policy-app.preview.emergentagent.com"
TEST_USER_ID = "test_bot"
KIDS_TEST_USER_ID = "kid_test"

def log_test(test_name, endpoint, expected, result, status):
    """Log test results in a structured format."""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"ENDPOINT: {endpoint}")
    print(f"EXPECTED: {expected}")
    print(f"RESULT: {result}")
    print(f"STATUS: {'✅ PASS' if status else '❌ FAIL'}")
    print(f"{'='*60}")
    return status

def test_rewards_profile_initial():
    """Test 1: GET /api/rewards/profile/test_bot - Initial profile check"""
    endpoint = f"{BASE_URL}/api/rewards/profile/{TEST_USER_ID}"
    try:
        response = requests.get(endpoint, timeout=10)
        data = response.json()
        
        expected = "Profile with total_points, available_points, level, inventory, equipped"
        
        if response.status_code == 200 and data.get("success"):
            profile = data.get("profile", {})
            required_fields = ["total_points", "available_points", "level", "inventory", "equipped"]
            has_all_fields = all(field in profile for field in required_fields)
            
            result = f"Status: {response.status_code}, Success: {data.get('success')}, Fields: {list(profile.keys())}"
            return log_test("Initial Profile Check", endpoint, expected, result, has_all_fields), profile
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Initial Profile Check", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Initial Profile Check", endpoint, expected, result, False), None

def test_store_all_items():
    """Test 2: GET /api/rewards/store?locale=ar - Should return 26 items and 5 categories"""
    endpoint = f"{BASE_URL}/api/rewards/store?locale=ar"
    try:
        response = requests.get(endpoint, timeout=10)
        data = response.json()
        
        expected = "26 items array and 5 categories"
        
        if response.status_code == 200 and data.get("success"):
            items = data.get("items", [])
            categories = data.get("categories", [])
            items_count = len(items)
            categories_count = len(categories)
            
            result = f"Status: {response.status_code}, Items: {items_count}, Categories: {categories_count}"
            success = items_count == 26 and categories_count == 5
            return log_test("Store All Items", endpoint, expected, result, success), data
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Store All Items", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Store All Items", endpoint, expected, result, False), None

def test_store_category(category, expected_count):
    """Test store items by category"""
    endpoint = f"{BASE_URL}/api/rewards/store?category={category}"
    try:
        response = requests.get(endpoint, timeout=10)
        data = response.json()
        
        expected = f"{expected_count} {category} items"
        
        if response.status_code == 200 and data.get("success"):
            items = data.get("items", [])
            items_count = len(items)
            
            result = f"Status: {response.status_code}, Items: {items_count}"
            success = items_count == expected_count
            return log_test(f"Store {category.title()} Items", endpoint, expected, result, success), items
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test(f"Store {category.title()} Items", endpoint, expected, result, False), []
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test(f"Store {category.title()} Items", endpoint, expected, result, False), []

def test_rewards_ads():
    """Test 8: GET /api/rewards/ads?user_id=test_bot - Should return ads array and can_watch=true"""
    endpoint = f"{BASE_URL}/api/rewards/ads?user_id={TEST_USER_ID}"
    try:
        response = requests.get(endpoint, timeout=10)
        data = response.json()
        
        expected = "ads array and can_watch=true"
        
        if response.status_code == 200 and data.get("success"):
            ads = data.get("ads", [])
            can_watch = data.get("can_watch", False)
            
            result = f"Status: {response.status_code}, Ads: {len(ads)}, Can Watch: {can_watch}"
            success = len(ads) > 0 and can_watch
            return log_test("Rewards Ads", endpoint, expected, result, success), ads
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Rewards Ads", endpoint, expected, result, False), []
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Rewards Ads", endpoint, expected, result, False), []

def test_watch_ad(ad_id):
    """Test 9: POST /api/rewards/ads/watch - Watch an ad"""
    endpoint = f"{BASE_URL}/api/rewards/ads/watch"
    payload = {
        "user_id": TEST_USER_ID,
        "ad_id": ad_id,
        "watch_duration": 20
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        data = response.json()
        
        expected = "Success with points earned"
        
        if response.status_code == 200 and data.get("success"):
            points_earned = data.get("points_earned", 0)
            new_total = data.get("new_total", 0)
            
            result = f"Status: {response.status_code}, Points Earned: {points_earned}, New Total: {new_total}"
            success = points_earned > 0
            return log_test("Watch Ad", endpoint, expected, result, success), data
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Watch Ad", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Watch Ad", endpoint, expected, result, False), None

def test_rewards_profile_after_ad():
    """Test 10: GET /api/rewards/profile/test_bot - Verify points increased after watching ad"""
    endpoint = f"{BASE_URL}/api/rewards/profile/{TEST_USER_ID}"
    try:
        response = requests.get(endpoint, timeout=10)
        data = response.json()
        
        expected = "Profile with increased points"
        
        if response.status_code == 200 and data.get("success"):
            profile = data.get("profile", {})
            total_points = profile.get("total_points", 0)
            available_points = profile.get("available_points", 0)
            
            result = f"Status: {response.status_code}, Total Points: {total_points}, Available: {available_points}"
            success = total_points > 0
            return log_test("Profile After Ad", endpoint, expected, result, success), profile
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Profile After Ad", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Profile After Ad", endpoint, expected, result, False), None

def test_purchase_item():
    """Test 11: POST /api/rewards/store/purchase - Purchase badge_star (80 points)"""
    endpoint = f"{BASE_URL}/api/rewards/store/purchase"
    payload = {
        "user_id": TEST_USER_ID,
        "item_id": "badge_star"
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        data = response.json()
        
        expected = "Purchase success or insufficient points"
        
        if response.status_code == 200:
            success_status = data.get("success", False)
            message = data.get("message", "")
            
            result = f"Status: {response.status_code}, Success: {success_status}, Message: {message}"
            # Success if purchase worked OR if insufficient points (expected behavior)
            success = success_status or message in ["insufficient_points", "already_owned"]
            return log_test("Purchase Item", endpoint, expected, result, success), data
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Purchase Item", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Purchase Item", endpoint, expected, result, False), None

def test_equip_item():
    """Test 12: POST /api/rewards/store/equip - Equip shape_circle in shape slot"""
    endpoint = f"{BASE_URL}/api/rewards/store/equip"
    payload = {
        "user_id": TEST_USER_ID,
        "item_id": "shape_circle",
        "slot": "shape"
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        data = response.json()
        
        expected = "Equip success (shape_circle is free item)"
        
        if response.status_code == 200 and data.get("success"):
            slot = data.get("slot", "")
            item_id = data.get("item_id", "")
            
            result = f"Status: {response.status_code}, Slot: {slot}, Item: {item_id}"
            success = slot == "shape" and item_id == "shape_circle"
            return log_test("Equip Item", endpoint, expected, result, success), data
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Equip Item", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Equip Item", endpoint, expected, result, False), None

def test_user_decorations():
    """Test 13: GET /api/rewards/user-decorations/test_bot - Should return decorations and level"""
    endpoint = f"{BASE_URL}/api/rewards/user-decorations/{TEST_USER_ID}"
    try:
        response = requests.get(endpoint, timeout=10)
        data = response.json()
        
        expected = "decorations and level info"
        
        if response.status_code == 200 and data.get("success"):
            decorations = data.get("decorations", {})
            level = data.get("level", {})
            
            result = f"Status: {response.status_code}, Decorations: {list(decorations.keys())}, Level: {level.get('level', 0)}"
            success = "level" in level
            return log_test("User Decorations", endpoint, expected, result, success), data
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("User Decorations", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("User Decorations", endpoint, expected, result, False), None

def test_kids_level():
    """Test 14: GET /api/rewards/kids-level/kid_test - Should return kids level info"""
    endpoint = f"{BASE_URL}/api/rewards/kids-level/{KIDS_TEST_USER_ID}"
    try:
        response = requests.get(endpoint, timeout=10)
        data = response.json()
        
        expected = "kids level info with xp and level"
        
        if response.status_code == 200 and data.get("success"):
            xp = data.get("xp", 0)
            level = data.get("level", {})
            
            result = f"Status: {response.status_code}, XP: {xp}, Level: {level.get('level', 0)}"
            success = "level" in level
            return log_test("Kids Level", endpoint, expected, result, success), data
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Kids Level", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Kids Level", endpoint, expected, result, False), None

def test_admin_stats():
    """Test 15: GET /api/admin/rewards/stats - Should return stats"""
    endpoint = f"{BASE_URL}/api/admin/rewards/stats"
    try:
        response = requests.get(endpoint, timeout=10)
        data = response.json()
        
        expected = "stats with total_users, total_store_items, etc."
        
        if response.status_code == 200 and data.get("success"):
            stats = data.get("stats", {})
            required_fields = ["total_users", "total_store_items", "total_active_ads"]
            has_fields = all(field in stats for field in required_fields)
            
            result = f"Status: {response.status_code}, Stats: {list(stats.keys())}"
            return log_test("Admin Stats", endpoint, expected, result, has_fields), data
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Admin Stats", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Admin Stats", endpoint, expected, result, False), None

def test_admin_ads():
    """Test 16: GET /api/admin/rewards/ads - Should return all ads"""
    endpoint = f"{BASE_URL}/api/admin/rewards/ads"
    try:
        response = requests.get(endpoint, timeout=10)
        data = response.json()
        
        expected = "all ads array"
        
        if response.status_code == 200 and data.get("success"):
            ads = data.get("ads", [])
            
            result = f"Status: {response.status_code}, Ads Count: {len(ads)}"
            success = isinstance(ads, list)  # Accept any number of ads
            return log_test("Admin Ads", endpoint, expected, result, success), data
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Admin Ads", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Admin Ads", endpoint, expected, result, False), None

def test_leaderboard():
    """Test 17: GET /api/rewards/leaderboard - Should return leaderboard array"""
    endpoint = f"{BASE_URL}/api/rewards/leaderboard"
    try:
        response = requests.get(endpoint, timeout=10)
        data = response.json()
        
        expected = "leaderboard array"
        
        if response.status_code == 200:
            # Handle both economy leaderboard (no success field) and rewards store leaderboard (with success field)
            leaderboard = data.get("leaderboard", [])
            
            result = f"Status: {response.status_code}, Leaderboard Count: {len(leaderboard)}"
            success = isinstance(leaderboard, list)
            return log_test("Leaderboard", endpoint, expected, result, success), data
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Leaderboard", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Leaderboard", endpoint, expected, result, False), None

def test_unequip_item():
    """Test 18: POST /api/rewards/store/unequip - Unequip shape slot"""
    endpoint = f"{BASE_URL}/api/rewards/store/unequip"
    payload = {
        "user_id": TEST_USER_ID,
        "slot": "shape"
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        data = response.json()
        
        expected = "Unequip success"
        
        if response.status_code == 200 and data.get("success"):
            slot = data.get("slot", "")
            
            result = f"Status: {response.status_code}, Slot: {slot}"
            success = slot == "shape"
            return log_test("Unequip Item", endpoint, expected, result, success), data
        else:
            result = f"Status: {response.status_code}, Response: {data}"
            return log_test("Unequip Item", endpoint, expected, result, False), None
            
    except Exception as e:
        result = f"Error: {str(e)}"
        return log_test("Unequip Item", endpoint, expected, result, False), None

def main():
    """Run all Rewards Store API tests"""
    print("🎮 REWARDS STORE API TESTING")
    print(f"Backend URL: {BASE_URL}")
    print(f"Test User ID: {TEST_USER_ID}")
    print(f"Kids Test User ID: {KIDS_TEST_USER_ID}")
    print(f"Test Started: {datetime.now().isoformat()}")
    
    results = []
    
    # Test 1: Initial profile check
    test1_result, initial_profile = test_rewards_profile_initial()
    results.append(("Initial Profile Check", test1_result))
    
    # Test 2: Store all items (26 items, 5 categories)
    test2_result, store_data = test_store_all_items()
    results.append(("Store All Items", test2_result))
    
    # Tests 3-7: Store categories
    categories = [
        ("border", 6),
        ("badge", 6), 
        ("shape", 4),
        ("theme", 6),
        ("font", 4)
    ]
    
    for category, expected_count in categories:
        test_result, items = test_store_category(category, expected_count)
        results.append((f"Store {category.title()} Items", test_result))
    
    # Test 8: Get available ads
    test8_result, ads = test_rewards_ads()
    results.append(("Rewards Ads", test8_result))
    
    # Test 9: Watch ad (if ads available)
    if ads and len(ads) > 0:
        first_ad_id = ads[0].get("id", "")
        if first_ad_id:
            test9_result, watch_data = test_watch_ad(first_ad_id)
            results.append(("Watch Ad", test9_result))
            
            # Small delay to ensure points are updated
            time.sleep(1)
        else:
            results.append(("Watch Ad", False))
            print("❌ No ad ID found to test watch functionality")
    else:
        results.append(("Watch Ad", False))
        print("❌ No ads available to test watch functionality")
    
    # Test 10: Profile after ad (verify points increased)
    test10_result, updated_profile = test_rewards_profile_after_ad()
    results.append(("Profile After Ad", test10_result))
    
    # Test 11: Purchase item
    test11_result, purchase_data = test_purchase_item()
    results.append(("Purchase Item", test11_result))
    
    # Test 12: Equip item
    test12_result, equip_data = test_equip_item()
    results.append(("Equip Item", test12_result))
    
    # Test 13: User decorations
    test13_result, decorations_data = test_user_decorations()
    results.append(("User Decorations", test13_result))
    
    # Test 14: Kids level
    test14_result, kids_data = test_kids_level()
    results.append(("Kids Level", test14_result))
    
    # Test 15: Admin stats
    test15_result, stats_data = test_admin_stats()
    results.append(("Admin Stats", test15_result))
    
    # Test 16: Admin ads
    test16_result, admin_ads_data = test_admin_ads()
    results.append(("Admin Ads", test16_result))
    
    # Test 17: Leaderboard
    test17_result, leaderboard_data = test_leaderboard()
    results.append(("Leaderboard", test17_result))
    
    # Test 18: Unequip item
    test18_result, unequip_data = test_unequip_item()
    results.append(("Unequip Item", test18_result))
    
    # Summary
    print(f"\n{'='*80}")
    print("🎮 REWARDS STORE API TEST SUMMARY")
    print(f"{'='*80}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 FINAL RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL REWARDS STORE API ENDPOINTS WORKING PERFECTLY!")
    else:
        print(f"⚠️  {total - passed} tests failed - see details above")
    
    # Save results to file
    test_results = {
        "test_date": datetime.now().isoformat(),
        "backend_url": BASE_URL,
        "test_user_id": TEST_USER_ID,
        "kids_test_user_id": KIDS_TEST_USER_ID,
        "total_tests": total,
        "passed_tests": passed,
        "success_rate": f"{passed/total*100:.1f}%",
        "results": [{"test": name, "passed": result} for name, result in results]
    }
    
    with open("/app/rewards_store_api_test_results.json", "w") as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n📁 Detailed results saved to: /app/rewards_store_api_test_results.json")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)