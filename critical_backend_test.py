#!/usr/bin/env python3
"""
Critical Backend API Testing - Quick Verification
Tests the 5 specific endpoints mentioned in the review request
"""

import asyncio
import httpx
import json
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://arabic-academy-dev.preview.emergentagent.com/api"

async def test_endpoint(client, url, description, expected_criteria):
    """Test a single endpoint and return results"""
    try:
        print(f"\n🔍 Testing: {description}")
        print(f"URL: {url}")
        
        response = await client.get(url)
        status_code = response.status_code
        
        if status_code == 200:
            data = response.json()
            print(f"✅ Status: {status_code}")
            
            # Validate expected criteria
            validation_passed = True
            validation_messages = []
            
            for criteria, check_func in expected_criteria.items():
                try:
                    result = check_func(data)
                    if result:
                        validation_messages.append(f"✅ {criteria}: Valid")
                    else:
                        validation_messages.append(f"❌ {criteria}: Invalid")
                        validation_passed = False
                except Exception as e:
                    validation_messages.append(f"❌ {criteria}: Error - {str(e)}")
                    validation_passed = False
            
            for msg in validation_messages:
                print(msg)
            
            # Show sample data structure
            if isinstance(data, dict) and len(data) > 0:
                sample_keys = list(data.keys())[:5]
                print(f"📊 Response keys: {sample_keys}")
                
                # Show sample data for key fields
                if 'chapters' in data and len(data['chapters']) > 0:
                    first_chapter = data['chapters'][0]
                    print(f"📖 Sample chapter: {first_chapter.get('name_simple', 'N/A')} - {first_chapter.get('translated_name', {}).get('name', 'N/A')}")
                elif 'verses' in data and len(data['verses']) > 0:
                    first_verse = data['verses'][0]
                    print(f"📜 Sample verse: {first_verse.get('verse_number', 'N/A')} - {first_verse.get('translations', [{}])[0].get('text', 'N/A')[:50]}...")
                elif 'search' in data and 'results' in data['search']:
                    results_count = len(data['search']['results'])
                    print(f"🔍 Search results: {results_count} found")
                elif 'collections' in data and len(data['collections']) > 0:
                    first_collection = data['collections'][0]
                    print(f"📚 Sample collection: {first_collection.get('name', 'N/A')}")
            
            return validation_passed, f"✅ {description} - {'PASSED' if validation_passed else 'FAILED'}"
        else:
            print(f"❌ Status: {status_code}")
            try:
                error_data = response.json()
                print(f"❌ Error: {error_data}")
            except:
                print(f"❌ Error text: {response.text[:200]}")
            return False, f"❌ {description} - Status {status_code}"
            
    except httpx.TimeoutException:
        print(f"❌ Timeout after 30 seconds")
        return False, f"❌ {description} - Timeout"
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False, f"❌ {description} - Exception: {str(e)}"

async def main():
    """Run the 5 critical API tests from review request"""
    
    print("=" * 80)
    print("🚨 CRITICAL BACKEND API TESTING - Quick Verification")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"🕒 Test Started: {datetime.now().isoformat()}")
    print("=" * 80)
    
    # The 5 critical test cases from review request
    test_cases = [
        {
            "url": f"{BACKEND_URL}/quran/v4/chapters?language=ru",
            "description": "GET /api/quran/v4/chapters?language=ru - Should return 114 surahs with Russian names",
            "criteria": {
                "114 chapters": lambda data: len(data.get('chapters', [])) == 114,
                "Has Russian names": lambda data: any('translated_name' in chapter and chapter['translated_name'].get('language_name') == 'russian' for chapter in data.get('chapters', [])),
                "Valid structure": lambda data: 'chapters' in data
            }
        },
        {
            "url": f"{BACKEND_URL}/quran/v4/verses/by_chapter/1?language=ru",
            "description": "GET /api/quran/v4/verses/by_chapter/1?language=ru - Should return Al-Fatiha verses with Russian translation",
            "criteria": {
                "Has verses": lambda data: len(data.get('verses', [])) > 0,
                "Russian translations": lambda data: any('translations' in verse and len(verse['translations']) > 0 for verse in data.get('verses', [])),
                "Valid structure": lambda data: 'verses' in data
            }
        },
        {
            "url": f"{BACKEND_URL}/quran/v4/chapters?language=de",
            "description": "GET /api/quran/v4/chapters?language=de - Should return surahs with German names",
            "criteria": {
                "114 chapters": lambda data: len(data.get('chapters', [])) == 114,
                "Has German names": lambda data: any('translated_name' in chapter and chapter['translated_name'].get('language_name') == 'german' for chapter in data.get('chapters', [])),
                "Valid structure": lambda data: 'chapters' in data
            }
        },
        {
            "url": f"{BACKEND_URL}/hadith/collections",
            "description": "GET /api/hadith/collections - Should return hadith collections",
            "criteria": {
                "Has collections": lambda data: len(data.get('data', [])) > 0,
                "Valid collection structure": lambda data: all('name' in collection for collection in data.get('data', [])),
                "Valid structure": lambda data: 'data' in data
            }
        },
        {
            "url": f"{BACKEND_URL}/quran/v4/search?q=الله&language=ar",
            "description": "GET /api/quran/v4/search?q=الله&language=ar - Should return search results in Arabic",
            "criteria": {
                "Has search results": lambda data: 'search' in data and 'results' in data['search'],
                "Results not empty": lambda data: len(data.get('search', {}).get('results', [])) > 0,
                "Valid structure": lambda data: 'search' in data
            }
        }
    ]
    
    results = []
    passed = 0
    failed = 0
    
    # Set timeout and configure client
    timeout = httpx.Timeout(30.0)
    
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        for test_case in test_cases:
            success, message = await test_endpoint(
                client, 
                test_case["url"], 
                test_case["description"], 
                test_case["criteria"]
            )
            results.append(message)
            if success:
                passed += 1
            else:
                failed += 1
            
            # Small delay between tests
            await asyncio.sleep(1.0)
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 CRITICAL TEST SUMMARY")
    print("=" * 80)
    
    for result in results:
        print(result)
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"✅ Passed: {passed}/5")
    print(f"❌ Failed: {failed}/5")
    print(f"📈 Success Rate: {(passed / 5 * 100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL 5 CRITICAL TESTS PASSED! Backend API is working correctly.")
    else:
        print(f"\n⚠️  {failed} critical test(s) failed. Please check the issues above.")
    
    print(f"🕒 Test Completed: {datetime.now().isoformat()}")
    print("=" * 80)
    
    return passed, failed, results

if __name__ == "__main__":
    asyncio.run(main())