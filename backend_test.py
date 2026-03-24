#!/usr/bin/env python3
"""
Digital Shield & Mixed Language Fix Testing
Test all Digital Shield endpoints for the Islamic app
"""

import requests
import json
import re
from datetime import datetime

# Base URL from frontend/.env
BASE_URL = "https://hadith-cards.preview.emergentagent.com/api"

# All 9 supported languages
LANGUAGES = ["ar", "en", "fr", "de", "tr", "ru", "sv", "nl", "el"]

# Expected themes for Digital Shield
EXPECTED_THEMES = ["deepfakes", "privacy", "social_media", "misinformation", "ethics", "safety"]

def has_arabic_text(text):
    """Check if text contains Arabic characters (Unicode range \u0600-\u06FF)"""
    if not text:
        return False
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    return bool(arabic_pattern.search(text))

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("✅ Health endpoint: PASS")
                return True
            else:
                print(f"❌ Health endpoint: FAIL - Status not healthy: {data}")
                return False
        else:
            print(f"❌ Health endpoint: FAIL - Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint: FAIL - Error: {e}")
        return False

def test_digital_shield_all_lessons():
    """Test Digital Shield - All Lessons for all 9 languages"""
    print("\n🔍 Testing Digital Shield - All Lessons (9 languages)...")
    results = []
    
    for lang in LANGUAGES:
        try:
            url = f"{BASE_URL}/kids-learn/digital-shield?locale={lang}&theme=all"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check basic structure
                if not data.get("success"):
                    print(f"❌ {lang}: FAIL - success not true")
                    results.append(False)
                    continue
                
                lessons = data.get("lessons", [])
                if len(lessons) != 30:
                    print(f"❌ {lang}: FAIL - Expected 30 lessons, got {len(lessons)}")
                    results.append(False)
                    continue
                
                # Check each lesson structure
                valid_lessons = True
                arabic_violations = []
                
                for lesson in lessons:
                    # Check required fields
                    required_fields = ["id", "theme", "icon", "title", "content", "key_lesson"]
                    for field in required_fields:
                        if field not in lesson:
                            print(f"❌ {lang}: FAIL - Missing field '{field}' in lesson {lesson.get('id', 'unknown')}")
                            valid_lessons = False
                            break
                    
                    if not valid_lessons:
                        break
                    
                    # Check for Arabic text in non-Arabic locales
                    if lang != "ar":
                        for field in ["title", "content", "key_lesson"]:
                            text = lesson.get(field, "")
                            if has_arabic_text(text):
                                # Allow Arabic in content if it's a Quran/Hadith quote (contains specific patterns)
                                if field == "content" and any(pattern in text for pattern in ["قال تعالى", "قال النبي", "ﷺ", "رضي الله عنه"]):
                                    continue
                                arabic_violations.append(f"Lesson {lesson['id']} - {field}: {text[:50]}...")
                
                if not valid_lessons:
                    results.append(False)
                    continue
                
                if arabic_violations:
                    print(f"❌ {lang}: FAIL - Arabic text found in non-Arabic locale:")
                    for violation in arabic_violations[:3]:  # Show first 3 violations
                        print(f"   {violation}")
                    results.append(False)
                    continue
                
                print(f"✅ {lang}: PASS - 30 lessons, all fields present, no Arabic violations")
                results.append(True)
                
            else:
                print(f"❌ {lang}: FAIL - Status code: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"❌ {lang}: FAIL - Error: {e}")
            results.append(False)
    
    return all(results)

def test_digital_shield_theme_filtering():
    """Test Digital Shield - Theme Filtering"""
    print("\n🔍 Testing Digital Shield - Theme Filtering...")
    results = []
    
    for theme in EXPECTED_THEMES:
        try:
            url = f"{BASE_URL}/kids-learn/digital-shield?locale=en&theme={theme}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get("success"):
                    print(f"❌ Theme {theme}: FAIL - success not true")
                    results.append(False)
                    continue
                
                lessons = data.get("lessons", [])
                if len(lessons) != 5:
                    print(f"❌ Theme {theme}: FAIL - Expected 5 lessons, got {len(lessons)}")
                    results.append(False)
                    continue
                
                # Check that all lessons have the correct theme
                wrong_theme_lessons = [l for l in lessons if l.get("theme") != theme]
                if wrong_theme_lessons:
                    print(f"❌ Theme {theme}: FAIL - Found lessons with wrong theme: {[l.get('id') for l in wrong_theme_lessons]}")
                    results.append(False)
                    continue
                
                print(f"✅ Theme {theme}: PASS - 5 lessons, all correct theme")
                results.append(True)
                
            else:
                print(f"❌ Theme {theme}: FAIL - Status code: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"❌ Theme {theme}: FAIL - Error: {e}")
            results.append(False)
    
    return all(results)

def test_digital_shield_today_lesson():
    """Test Digital Shield - Today's Lesson"""
    print("\n🔍 Testing Digital Shield - Today's Lesson...")
    results = []
    
    # Test with English
    try:
        url = f"{BASE_URL}/kids-learn/digital-shield/today?locale=en"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if not data.get("success"):
                print("❌ Today's lesson (en): FAIL - success not true")
                results.append(False)
            else:
                lesson = data.get("lesson", {})
                lesson_number = data.get("lesson_number")
                total_lessons = data.get("total_lessons")
                
                # Check structure
                required_fields = ["id", "theme", "icon", "title", "content", "key_lesson"]
                missing_fields = [f for f in required_fields if f not in lesson]
                
                if missing_fields:
                    print(f"❌ Today's lesson (en): FAIL - Missing fields: {missing_fields}")
                    results.append(False)
                elif total_lessons != 30:
                    print(f"❌ Today's lesson (en): FAIL - Expected total_lessons=30, got {total_lessons}")
                    results.append(False)
                elif not (1 <= lesson_number <= 30):
                    print(f"❌ Today's lesson (en): FAIL - lesson_number {lesson_number} not in range 1-30")
                    results.append(False)
                else:
                    print(f"✅ Today's lesson (en): PASS - Lesson {lesson_number}/30, all fields present")
                    results.append(True)
        else:
            print(f"❌ Today's lesson (en): FAIL - Status code: {response.status_code}")
            results.append(False)
            
    except Exception as e:
        print(f"❌ Today's lesson (en): FAIL - Error: {e}")
        results.append(False)
    
    # Test with Swedish to verify translation
    try:
        url = f"{BASE_URL}/kids-learn/digital-shield/today?locale=sv"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if not data.get("success"):
                print("❌ Today's lesson (sv): FAIL - success not true")
                results.append(False)
            else:
                lesson = data.get("lesson", {})
                
                # Check for Swedish translation (should not contain Arabic except in quotes)
                arabic_violations = []
                for field in ["title", "content", "key_lesson"]:
                    text = lesson.get(field, "")
                    if has_arabic_text(text):
                        # Allow Arabic in content if it's a Quran/Hadith quote
                        if field == "content" and any(pattern in text for pattern in ["قال تعالى", "قال النبي", "ﷺ"]):
                            continue
                        arabic_violations.append(f"{field}: {text[:50]}...")
                
                if arabic_violations:
                    print(f"❌ Today's lesson (sv): FAIL - Arabic text found:")
                    for violation in arabic_violations:
                        print(f"   {violation}")
                    results.append(False)
                else:
                    print("✅ Today's lesson (sv): PASS - Swedish translation, no Arabic violations")
                    results.append(True)
        else:
            print(f"❌ Today's lesson (sv): FAIL - Status code: {response.status_code}")
            results.append(False)
            
    except Exception as e:
        print(f"❌ Today's lesson (sv): FAIL - Error: {e}")
        results.append(False)
    
    return all(results)

def test_digital_shield_themes_list():
    """Test Digital Shield - Themes List"""
    print("\n🔍 Testing Digital Shield - Themes List...")
    
    try:
        url = f"{BASE_URL}/kids-learn/digital-shield/themes?locale=en"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if not data.get("success"):
                print("❌ Themes list: FAIL - success not true")
                return False
            
            themes = data.get("themes", [])
            if len(themes) != 6:
                print(f"❌ Themes list: FAIL - Expected 6 themes, got {len(themes)}")
                return False
            
            # Check that all expected themes are present
            theme_ids = [t.get("id") for t in themes]
            missing_themes = [t for t in EXPECTED_THEMES if t not in theme_ids]
            
            if missing_themes:
                print(f"❌ Themes list: FAIL - Missing themes: {missing_themes}")
                return False
            
            # Check theme structure
            for theme in themes:
                if not all(field in theme for field in ["id", "count", "icon"]):
                    print(f"❌ Themes list: FAIL - Theme {theme.get('id')} missing required fields")
                    return False
                
                if theme.get("count") != 5:
                    print(f"❌ Themes list: FAIL - Theme {theme.get('id')} has {theme.get('count')} lessons, expected 5")
                    return False
            
            print("✅ Themes list: PASS - 6 themes, all with 5 lessons each")
            return True
            
        else:
            print(f"❌ Themes list: FAIL - Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Themes list: FAIL - Error: {e}")
        return False

def main():
    """Run all Digital Shield tests"""
    print("🛡️ DIGITAL SHIELD & MIXED LANGUAGE FIX - COMPREHENSIVE TESTING")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Time: {datetime.now().isoformat()}")
    print("=" * 70)
    
    test_results = []
    
    # Run all tests
    test_results.append(test_health_endpoint())
    test_results.append(test_digital_shield_all_lessons())
    test_results.append(test_digital_shield_theme_filtering())
    test_results.append(test_digital_shield_today_lesson())
    test_results.append(test_digital_shield_themes_list())
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(test_results)
    total = len(test_results)
    
    test_names = [
        "Health Endpoint",
        "Digital Shield - All Lessons (9 languages)",
        "Digital Shield - Theme Filtering (6 themes)",
        "Digital Shield - Today's Lesson",
        "Digital Shield - Themes List"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {name}: {status}")
    
    print("=" * 70)
    print(f"OVERALL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Digital Shield is working correctly.")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)