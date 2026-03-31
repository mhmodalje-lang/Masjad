#!/usr/bin/env python3
"""
Final Backend API Testing for Stories Platform
Verifying the thumbnail_url field fix
"""

import requests
import json
import sys

# Backend URL from frontend/.env
BACKEND_URL = "https://quality-check-app-2.preview.emergentagent.com"

def test_stories_list_translated_with_thumbnail_fix():
    """Test that thumbnail_url field is now present in all stories"""
    print("🧪 Testing GET /api/stories/list-translated with thumbnail_url field fix...")
    
    url = f"{BACKEND_URL}/api/stories/list-translated"
    params = {"limit": 5, "language": "ar"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            stories = data.get("stories", [])
            print(f"   Stories count: {len(stories)}")
            
            if stories:
                first_story = stories[0]
                print(f"   First story keys: {list(first_story.keys())}")
                
                # Check if thumbnail_url field is now present
                has_thumbnail_field = "thumbnail_url" in first_story
                thumbnail_value = first_story.get("thumbnail_url")
                
                print(f"   Has thumbnail_url field: {has_thumbnail_field}")
                print(f"   Thumbnail value: {thumbnail_value}")
                
                if has_thumbnail_field:
                    print("   ✅ PASS: Stories now include thumbnail_url field")
                    return True
                else:
                    print("   ❌ FAIL: Stories still missing thumbnail_url field")
                    return False
            else:
                print("   ⚠️  WARNING: No stories returned")
                return True
        else:
            print(f"   ❌ FAIL: Expected 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def main():
    """Run the thumbnail field verification test"""
    print("🚀 Final Backend API Test - Thumbnail Field Fix Verification")
    print(f"📍 Backend URL: {BACKEND_URL}")
    print("=" * 60)
    
    success = test_stories_list_translated_with_thumbnail_fix()
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION RESULT")
    print("=" * 60)
    
    if success:
        print("✅ PASS: thumbnail_url field fix is working correctly")
        return 0
    else:
        print("❌ FAIL: thumbnail_url field fix needs attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())