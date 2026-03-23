#!/usr/bin/env python3
"""
Extended Kids Learn API Test - All 9 Languages
==============================================
Tests translation functionality across all 9 supported languages
"""

import requests
import json
from datetime import datetime

BACKEND_URL = "https://quran-authentic-1.preview.emergentagent.com"
ALL_LANGUAGES = ["ar", "en", "de", "fr", "ru", "tr", "sv", "nl", "el"]

def test_all_languages():
    """Test key endpoints with all 9 languages"""
    print("🌍 Testing All 9 Languages Translation Support")
    print("=" * 60)
    
    results = {}
    
    # Test curriculum overview with all languages
    print("📚 Testing Curriculum Overview...")
    for lang in ALL_LANGUAGES:
        try:
            response = requests.get(f"{BACKEND_URL}/api/kids-learn/curriculum", 
                                  params={"locale": lang}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("stages"):
                    stage_title = data["stages"][0]["title"]
                    results[f"curriculum_{lang}"] = {
                        "status": "✅ PASS",
                        "sample_title": stage_title,
                        "stages_count": len(data["stages"])
                    }
                    print(f"  {lang}: ✅ {len(data['stages'])} stages - '{stage_title}'")
                else:
                    results[f"curriculum_{lang}"] = {"status": "❌ FAIL", "error": "Invalid response structure"}
                    print(f"  {lang}: ❌ Invalid response")
            else:
                results[f"curriculum_{lang}"] = {"status": "❌ FAIL", "error": f"HTTP {response.status_code}"}
                print(f"  {lang}: ❌ HTTP {response.status_code}")
        except Exception as e:
            results[f"curriculum_{lang}"] = {"status": "❌ FAIL", "error": str(e)}
            print(f"  {lang}: ❌ {str(e)}")
    
    # Test duas with all languages
    print("\n🤲 Testing Duas...")
    for lang in ALL_LANGUAGES:
        try:
            response = requests.get(f"{BACKEND_URL}/api/kids-learn/duas", 
                                  params={"locale": lang}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("duas"):
                    dua_title = data["duas"][0].get("title", "No title")
                    results[f"duas_{lang}"] = {
                        "status": "✅ PASS",
                        "sample_title": dua_title,
                        "duas_count": len(data["duas"])
                    }
                    print(f"  {lang}: ✅ {len(data['duas'])} duas - '{dua_title}'")
                else:
                    results[f"duas_{lang}"] = {"status": "❌ FAIL", "error": "Invalid response structure"}
                    print(f"  {lang}: ❌ Invalid response")
            else:
                results[f"duas_{lang}"] = {"status": "❌ FAIL", "error": f"HTTP {response.status_code}"}
                print(f"  {lang}: ❌ HTTP {response.status_code}")
        except Exception as e:
            results[f"duas_{lang}"] = {"status": "❌ FAIL", "error": str(e)}
            print(f"  {lang}: ❌ {str(e)}")
    
    # Test prophets with all languages
    print("\n👨‍🦳 Testing Prophets...")
    for lang in ALL_LANGUAGES:
        try:
            response = requests.get(f"{BACKEND_URL}/api/kids-learn/prophets-full", 
                                  params={"locale": lang}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("prophets"):
                    prophet_name = data["prophets"][0].get("name", "No name")
                    results[f"prophets_{lang}"] = {
                        "status": "✅ PASS",
                        "sample_name": prophet_name,
                        "prophets_count": len(data["prophets"])
                    }
                    print(f"  {lang}: ✅ {len(data['prophets'])} prophets - '{prophet_name}'")
                else:
                    results[f"prophets_{lang}"] = {"status": "❌ FAIL", "error": "Invalid response structure"}
                    print(f"  {lang}: ❌ Invalid response")
            else:
                results[f"prophets_{lang}"] = {"status": "❌ FAIL", "error": f"HTTP {response.status_code}"}
                print(f"  {lang}: ❌ HTTP {response.status_code}")
        except Exception as e:
            results[f"prophets_{lang}"] = {"status": "❌ FAIL", "error": str(e)}
            print(f"  {lang}: ❌ {str(e)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TRANSLATION TEST SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if "✅" in r["status"])
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
    
    # Save results
    with open("/app/kids_learn_translation_test_results.json", "w") as f:
        json.dump({
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": round(passed_tests/total_tests*100, 1),
                "test_date": datetime.now().isoformat(),
                "languages_tested": ALL_LANGUAGES
            },
            "results": results
        }, f, indent=2)
    
    print(f"\n📄 Results saved to: /app/kids_learn_translation_test_results.json")
    
    return failed_tests == 0

if __name__ == "__main__":
    test_all_languages()