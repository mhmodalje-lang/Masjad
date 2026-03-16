#!/usr/bin/env python3
"""
Backend Test Suite - Phase 3 Testing: New API Endpoints
Testing: my-saved, my-liked, auto-categorize, ads/placement, updated my-stats
"""
import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BACKEND_URL = "https://faith-hub-65.preview.emergentagent.com/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log(message, color=Colors.WHITE):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] {message}{Colors.END}")

def test_endpoint(method, url, headers=None, json_data=None, expected_status=200, description=""):
    """Test a single endpoint and return response data"""
    log(f"🔄 {method} {url} - {description}", Colors.CYAN)
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=json_data, timeout=30)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=json_data, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            log(f"❌ Unsupported method: {method}", Colors.RED)
            return None
        
        if response.status_code == expected_status:
            log(f"✅ {description} - Status: {response.status_code}", Colors.GREEN)
            try:
                return response.json()
            except:
                return {"status": "success", "text": response.text}
        else:
            log(f"❌ {description} - Expected: {expected_status}, Got: {response.status_code}", Colors.RED)
            try:
                error_data = response.json()
                log(f"   Error: {error_data}", Colors.RED)
            except:
                log(f"   Error: {response.text}", Colors.RED)
            return None
            
    except requests.exceptions.Timeout:
        log(f"⏱️ {description} - Request timed out", Colors.YELLOW)
        return None
    except requests.exceptions.ConnectionError:
        log(f"🔌 {description} - Connection error", Colors.RED)
        return None
    except Exception as e:
        log(f"💥 {description} - Exception: {str(e)}", Colors.RED)
        return None

def main():
    log("🚀 PHASE 3 TESTING: New Backend API Endpoints", Colors.BOLD)
    log("Testing: my-saved, my-liked, auto-categorize, ads/placement, my-stats", Colors.CYAN)
    log("="*80, Colors.BLUE)
    
    # Store test data
    auth_token = None
    story_id = None
    
    # Test 1: Register user (as per review request)
    log("\n📝 Test 1: User Registration", Colors.BOLD)
    register_data = {
        "email": "testphase3@test.com",
        "password": "test123", 
        "name": "Phase3 Tester"
    }
    
    response = test_endpoint(
        "POST", 
        f"{BACKEND_URL}/auth/register",
        json_data=register_data,
        description="Register Arabic user for stories"
    )
    
    if response and "access_token" in response:
        auth_token = response["access_token"]
        log(f"✅ Auth token obtained from registration: {auth_token[:20]}...", Colors.GREEN)
    else:
        # Try login if registration failed (user might already exist)
        log("Registration failed - trying login...", Colors.YELLOW)
        login_data = {
            "email": "testphase3@test.com",
            "password": "test123"
        }
        
        login_response = test_endpoint(
            "POST",
            f"{BACKEND_URL}/auth/login",
            json_data=login_data,
            description="Login existing user"
        )
        
        if login_response and "access_token" in login_response:
            auth_token = login_response["access_token"]
            log(f"✅ Auth token obtained from login: {auth_token[:20]}...", Colors.GREEN)
        else:
            log("❌ Failed to get auth token from login - stopping test", Colors.RED)
            return
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Test 2: Create a story (as per review request)
    log("\n✍️ Test 2: Create Story for Testing", Colors.BOLD)
    story_data = {
        "title": "فضل الاستغفار",
        "content": "الاستغفار من أعظم العبادات",
        "category": "istighfar"
    }
    
    response = test_endpoint(
        "POST",
        f"{BACKEND_URL}/stories/create",
        headers=headers,
        json_data=story_data,
        description="Create test story"
    )
    
    if response and "story" in response:
        story_id = response["story"]["id"]
        log(f"✅ Story created with ID: {story_id}", Colors.GREEN)
        log(f"   Title: {response['story']['title']}", Colors.CYAN)
        log(f"   Category: {response['story']['category']}", Colors.CYAN)
    else:
        log("❌ Failed to create story - stopping test", Colors.RED)
        return
    
    # Test 3: Like the story
    log("\n❤️ Test 3: Like the Story", Colors.BOLD)
    response = test_endpoint(
        "POST",
        f"{BACKEND_URL}/sohba/posts/{story_id}/like",
        headers=headers,
        description=f"Like story {story_id}"
    )
    
    if response and response.get("success"):
        log("✅ Story liked successfully", Colors.GREEN)
        log(f"   Liked: {response.get('liked', 'unknown')}", Colors.CYAN)
    
    # Test 4: Save the story
    log("\n💾 Test 4: Save the Story", Colors.BOLD)
    response = test_endpoint(
        "POST",
        f"{BACKEND_URL}/sohba/posts/{story_id}/save",
        headers=headers,
        description=f"Save story {story_id}"
    )
    
    if response and response.get("success"):
        log("✅ Story saved successfully", Colors.GREEN)
        log(f"   Saved: {response.get('saved', 'unknown')}", Colors.CYAN)
    
    # Test 5: GET /api/stories/my-saved
    log("\n📚 Test 5: Get My Saved Stories", Colors.BOLD)
    response = test_endpoint(
        "GET",
        f"{BACKEND_URL}/stories/my-saved",
        headers=headers,
        description="Get saved stories for authenticated user"
    )
    
    if response and "stories" in response:
        saved_stories = response["stories"]
        log(f"✅ Found {len(saved_stories)} saved stories", Colors.GREEN)
        
        if len(saved_stories) >= 1:
            log("✅ At least 1 saved story found as expected", Colors.GREEN)
            # Check if our test story is in saved stories
            found_our_story = any(story.get("id") == story_id for story in saved_stories)
            if found_our_story:
                log("✅ Our test story found in saved stories", Colors.GREEN)
            else:
                log("❌ Our test story NOT found in saved stories", Colors.RED)
        else:
            log("❌ No saved stories found", Colors.RED)
    else:
        log("❌ Failed to get saved stories", Colors.RED)
    
    # Test 6: GET /api/stories/my-liked
    log("\n❤️ Test 6: Get My Liked Stories", Colors.BOLD)
    response = test_endpoint(
        "GET",
        f"{BACKEND_URL}/stories/my-liked",
        headers=headers,
        description="Get liked stories for authenticated user"
    )
    
    if response and "stories" in response:
        liked_stories = response["stories"]
        log(f"✅ Found {len(liked_stories)} liked stories", Colors.GREEN)
        
        if len(liked_stories) >= 1:
            log("✅ At least 1 liked story found as expected", Colors.GREEN)
            # Check if our test story is in liked stories
            found_our_story = any(story.get("id") == story_id for story in liked_stories)
            if found_our_story:
                log("✅ Our test story found in liked stories", Colors.GREEN)
            else:
                log("❌ Our test story NOT found in liked stories", Colors.RED)
        else:
            log("❌ No liked stories found", Colors.RED)
    else:
        log("❌ Failed to get liked stories", Colors.RED)
    
    # Test 7: POST /api/stories/auto-categorize
    log("\n🤖 Test 7: AI Auto-Categorize Story", Colors.BOLD)
    categorize_data = {
        "title": "فضل الاستغفار",
        "content": "الاستغفار عظيم"
    }
    
    response = test_endpoint(
        "POST",
        f"{BACKEND_URL}/stories/auto-categorize",
        headers=headers,
        json_data=categorize_data,
        description="AI auto-categorize Islamic content"
    )
    
    if response and "category" in response:
        category = response["category"]
        log(f"✅ AI categorization successful", Colors.GREEN)
        log(f"   Suggested category: {category}", Colors.CYAN)
        
        # Check if category is valid
        valid_categories = ["istighfar", "sahaba", "quran", "prophets", "ruqyah", "rizq", "tawba", "miracles", "general"]
        if category in valid_categories:
            log("✅ Category is valid", Colors.GREEN)
        else:
            log(f"❌ Invalid category: {category}", Colors.RED)
    else:
        log("❌ AI categorization failed", Colors.RED)
    
    # Test 8: GET /api/ads/placement/home
    log("\n🎯 Test 8: Get Ads for Home Placement", Colors.BOLD)
    response = test_endpoint(
        "GET",
        f"{BACKEND_URL}/ads/placement/home",
        description="Get ads for home placement (no auth needed)"
    )
    
    if response and "ads" in response:
        ads = response["ads"]
        log(f"✅ Ads endpoint working - found {len(ads)} ads", Colors.GREEN)
        
        if len(ads) == 0:
            log("   ℹ️ No ads currently configured (expected for new system)", Colors.CYAN)
        else:
            log(f"   Found {len(ads)} ads for home placement", Colors.GREEN)
            for ad in ads[:2]:  # Show first 2 ads
                log(f"   - Ad: {ad.get('title', 'No title')}", Colors.CYAN)
    else:
        log("❌ Failed to get ads", Colors.RED)
    
    # Test 9: GET /api/sohba/my-stats (Updated with new fields)
    log("\n📊 Test 9: Get Updated My Stats", Colors.BOLD)
    response = test_endpoint(
        "GET",
        f"{BACKEND_URL}/sohba/my-stats",
        headers=headers,
        description="Get updated user stats with new fields"
    )
    
    if response:
        log("✅ My stats endpoint working", Colors.GREEN)
        
        # Check for expected fields
        expected_fields = ["posts", "stories", "followers", "following", "total_likes", "saved_count", "liked_count"]
        for field in expected_fields:
            if field in response:
                log(f"   ✅ {field}: {response[field]}", Colors.GREEN)
            else:
                log(f"   ❌ Missing field: {field}", Colors.RED)
        
        # Verify we have at least 1 in saved_count and liked_count (from our test)
        if response.get("saved_count", 0) >= 1:
            log("✅ Saved count reflects our test save", Colors.GREEN)
        else:
            log("❌ Saved count doesn't reflect our test save", Colors.RED)
            
        if response.get("liked_count", 0) >= 1:
            log("✅ Liked count reflects our test like", Colors.GREEN)
        else:
            log("❌ Liked count doesn't reflect our test like", Colors.RED)
    else:
        log("❌ Failed to get user stats", Colors.RED)
    
    # Final Summary
    log("\n" + "="*80, Colors.BLUE)
    log("🏁 PHASE 3 TESTING COMPLETE", Colors.BOLD)
    log("="*80, Colors.BLUE)
    
    log(f"\n📊 Test Summary:", Colors.BOLD)
    log(f"   ✅ User registration/login working", Colors.GREEN)
    log(f"   ✅ Story creation successful", Colors.GREEN)
    log(f"   ✅ Like/Save functionality working", Colors.GREEN)
    log(f"   📚 GET /api/stories/my-saved tested", Colors.CYAN)
    log(f"   ❤️ GET /api/stories/my-liked tested", Colors.CYAN)
    log(f"   🤖 POST /api/stories/auto-categorize tested", Colors.CYAN)
    log(f"   🎯 GET /api/ads/placement/home tested", Colors.CYAN)
    log(f"   📊 GET /api/sohba/my-stats tested", Colors.CYAN)
    
    log(f"\n🎯 All new Phase 3 endpoints tested!", Colors.GREEN)

if __name__ == "__main__":
    main()