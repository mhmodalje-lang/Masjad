#!/usr/bin/env python3
"""
V2026 Architecture Overhaul - Backend API Testing
=================================================
Tests the critical endpoints for the Islamic app's V2026 rebuild:
1. NEW Global Verse Endpoint (Single & Bulk)
2. Existing endpoint compatibility
3. Explanation text validation (must be concise, not 10-page Ibn Kathir)
"""

import asyncio
import httpx
import json
from datetime import datetime

# Backend URL from frontend/.env
BASE_URL = "https://quran-rebuild-v2026.preview.emergentagent.com/api"

class TestResults:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def add_result(self, test_name, passed, details, error=None):
        self.results.append({
            "test": test_name,
            "passed": passed,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY: {self.passed} PASSED, {self.failed} FAILED")
        print(f"{'='*60}")
        for result in self.results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"{status} {result['test']}")
            if result["details"]:
                print(f"    Details: {result['details']}")
            if result["error"]:
                print(f"    Error: {result['error']}")
        print(f"{'='*60}")

async def test_health_endpoint():
    """Test basic health check endpoint"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{BASE_URL}/health")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    return True, f"Health check passed: {data}"
                else:
                    return False, f"Health check failed: {data}"
            else:
                return False, f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Exception: {str(e)}"

async def test_global_verse_single(language, expected_translation_source, expected_explanation_source):
    """Test NEW Global Verse Endpoint for single verse"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            url = f"{BASE_URL}/quran/v4/global-verse/1/1"
            params = {"language": language}
            response = await client.get(url, params=params)
            
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}: {response.text}"
            
            data = response.json()
            
            # Validate required fields
            required_fields = ["success", "verse_key", "arabic_text", "translation", 
                             "explanation", "explanation_source", "surah_name", 
                             "surah_name_translated", "audio_url"]
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return False, f"Missing required fields: {missing_fields}"
            
            # Validate content
            if not data.get("arabic_text"):
                return False, "Arabic text is empty"
            
            if not data.get("translation") and language != "ar":
                return False, f"Translation is empty for language {language}"
            
            if not data.get("explanation"):
                return False, "Explanation is empty"
            
            # CRITICAL: Check explanation length (must be concise, not 10-page Ibn Kathir)
            explanation = data.get("explanation", "")
            explanation_words = len(explanation.split())
            if explanation_words > 200:  # More than 200 words is too long
                return False, f"Explanation too long ({explanation_words} words). Must be concise, not Ibn Kathir-style"
            
            # Validate verse key
            if data.get("verse_key") != "1:1":
                return False, f"Wrong verse key: {data.get('verse_key')}"
            
            # Validate audio URL
            audio_url = data.get("audio_url", "")
            if not audio_url or "everyayah.com" not in audio_url:
                return False, f"Invalid audio URL: {audio_url}"
            
            details = {
                "language": language,
                "translation_length": len(data.get("translation", "")),
                "explanation_length": len(explanation),
                "explanation_words": explanation_words,
                "explanation_source": data.get("explanation_source"),
                "surah_name": data.get("surah_name"),
                "surah_name_translated": data.get("surah_name_translated"),
                "cached": data.get("cached", False)
            }
            
            return True, f"Global verse endpoint working for {language}: {details}"
            
    except Exception as e:
        return False, f"Exception: {str(e)}"

async def test_global_verse_bulk():
    """Test NEW Global Verse Endpoint for bulk verses"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            url = f"{BASE_URL}/quran/v4/global-verse/bulk/1"
            params = {"language": "fr", "from_ayah": 1, "to_ayah": 7}
            response = await client.get(url, params=params)
            
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}: {response.text}"
            
            data = response.json()
            
            # Validate structure
            if not data.get("success"):
                return False, "Success field is false"
            
            verses = data.get("verses", [])
            if len(verses) != 7:
                return False, f"Expected 7 verses, got {len(verses)}"
            
            # Validate each verse
            for i, verse in enumerate(verses, 1):
                if verse.get("verse_key") != f"1:{i}":
                    return False, f"Wrong verse key for verse {i}: {verse.get('verse_key')}"
                
                if not verse.get("arabic_text"):
                    return False, f"Missing Arabic text for verse {i}"
                
                if not verse.get("translation"):
                    return False, f"Missing French translation for verse {i}"
                
                if not verse.get("audio_url"):
                    return False, f"Missing audio URL for verse {i}"
            
            details = {
                "surah_id": data.get("surah_id"),
                "language": data.get("language"),
                "total_verses": data.get("total"),
                "first_verse_translation_length": len(verses[0].get("translation", "")),
                "last_verse_translation_length": len(verses[-1].get("translation", ""))
            }
            
            return True, f"Bulk verses endpoint working: {details}"
            
    except Exception as e:
        return False, f"Exception: {str(e)}"

async def test_existing_tafsir_endpoint():
    """Test existing tafsir endpoint compatibility"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            url = f"{BASE_URL}/quran/v4/tafsir/1:1"
            params = {"language": "fr"}
            response = await client.get(url, params=params)
            
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}: {response.text}"
            
            data = response.json()
            
            # Validate required fields
            if not data.get("success"):
                return False, "Success field is false"
            
            if data.get("translation_pending") is True:
                return False, "Translation pending flag is true (should be false)"
            
            if not data.get("text"):
                return False, "Tafsir text is empty"
            
            details = {
                "verse_key": data.get("verse_key"),
                "language": data.get("language"),
                "tafsir_name": data.get("tafsir_name"),
                "text_length": len(data.get("text", "")),
                "cached": data.get("cached", False)
            }
            
            return True, f"Existing tafsir endpoint working: {details}"
            
    except Exception as e:
        return False, f"Exception: {str(e)}"

async def test_existing_daily_hadith_endpoint():
    """Test existing daily hadith endpoint compatibility"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            url = f"{BASE_URL}/daily-hadith"
            params = {"language": "fr"}
            response = await client.get(url, params=params)
            
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}: {response.text}"
            
            data = response.json()
            
            # Validate required fields
            if not data.get("success"):
                return False, "Success field is false"
            
            hadith = data.get("hadith", {})
            if not hadith:
                return False, "Hadith data is missing"
            
            if hadith.get("translation_pending") is True:
                return False, "Translation pending flag is true (should be false)"
            
            if not hadith.get("text"):
                return False, "Hadith text is empty"
            
            details = {
                "hadith_number": hadith.get("number"),
                "translation_language": hadith.get("translation_language"),
                "text_length": len(hadith.get("text", "")),
                "source": hadith.get("source"),
                "date": data.get("date")
            }
            
            return True, f"Daily hadith endpoint working: {details}"
            
    except Exception as e:
        return False, f"Exception: {str(e)}"

async def main():
    """Run all tests"""
    print("🕌 V2026 Architecture Overhaul - Backend API Testing")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print("=" * 60)
    
    results = TestResults()
    
    # Test 1: Health Check
    print("Testing health endpoint...")
    passed, details = await test_health_endpoint()
    results.add_result("Health Check", passed, details)
    
    # Test 2: Global Verse - English
    print("Testing global verse endpoint (English)...")
    passed, details = await test_global_verse_single("en", "Saheeh International", "Abdel Haleem")
    results.add_result("Global Verse - English", passed, details)
    
    # Test 3: Global Verse - French
    print("Testing global verse endpoint (French)...")
    passed, details = await test_global_verse_single("fr", "Hamidullah", "Montada")
    results.add_result("Global Verse - French", passed, details)
    
    # Test 4: Global Verse - German
    print("Testing global verse endpoint (German)...")
    passed, details = await test_global_verse_single("de", "Bubenheim", "Abu Reda")
    results.add_result("Global Verse - German", passed, details)
    
    # Test 5: Global Verse - Russian
    print("Testing global verse endpoint (Russian)...")
    passed, details = await test_global_verse_single("ru", "Abu Adel", "As-Sa'di")
    results.add_result("Global Verse - Russian", passed, details)
    
    # Test 6: Global Verse - Turkish
    print("Testing global verse endpoint (Turkish)...")
    passed, details = await test_global_verse_single("tr", "Diyanet", "Elmalılı")
    results.add_result("Global Verse - Turkish", passed, details)
    
    # Test 7: Global Verse - Greek
    print("Testing global verse endpoint (Greek)...")
    passed, details = await test_global_verse_single("el", "QuranEnc", "Rowwad")
    results.add_result("Global Verse - Greek", passed, details)
    
    # Test 8: Global Verse Bulk
    print("Testing global verse bulk endpoint...")
    passed, details = await test_global_verse_bulk()
    results.add_result("Global Verse - Bulk (French)", passed, details)
    
    # Test 9: Existing Tafsir Endpoint
    print("Testing existing tafsir endpoint...")
    passed, details = await test_existing_tafsir_endpoint()
    results.add_result("Existing Tafsir Endpoint", passed, details)
    
    # Test 10: Existing Daily Hadith Endpoint
    print("Testing existing daily hadith endpoint...")
    passed, details = await test_existing_daily_hadith_endpoint()
    results.add_result("Existing Daily Hadith Endpoint", passed, details)
    
    # Print results
    results.print_summary()
    
    # Save results to file
    with open("/app/test_results_backend.json", "w") as f:
        json.dump({
            "test_run": datetime.now().isoformat(),
            "base_url": BASE_URL,
            "summary": {
                "total_tests": len(results.results),
                "passed": results.passed,
                "failed": results.failed,
                "success_rate": f"{(results.passed / len(results.results) * 100):.1f}%"
            },
            "results": results.results
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: /app/test_results_backend.json")
    
    return results.failed == 0

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)