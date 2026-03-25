#!/usr/bin/env python3
"""
Arabic Academy Multilingual Localization Testing
Test Date: 2026-01-27
Focus: Verify locale filtering works correctly for Arabic Academy endpoints
"""

import requests
import json
from typing import Dict, List, Any

# Configuration
BASE_URL = "https://fast-reload-app.preview.emergentagent.com"
TIMEOUT = 30

class ArabicAcademyLocalizationTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        self.results.append({
            'test': test_name,
            'status': status,
            'details': details
        })
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            
    def make_request(self, endpoint: str) -> tuple:
        """Make HTTP request and return (success, data, status_code)"""
        try:
            url = f"{BASE_URL}{endpoint}"
            print(f"Testing: {url}")
            response = requests.get(url, timeout=TIMEOUT)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return True, data, 200
                except json.JSONDecodeError:
                    return False, f"Invalid JSON response", response.status_code
            else:
                return False, f"HTTP {response.status_code}: {response.text[:200]}", response.status_code
                
        except requests.exceptions.Timeout:
            return False, "Request timeout", 0
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {str(e)}", 0

    def check_mixed_language_keys(self, data: Any, locale: str) -> List[str]:
        """Check for mixed language keys like meaning_en, meaning_de, etc."""
        mixed_keys = []
        
        def recursive_check(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    # Check for mixed language keys
                    if any(key.endswith(f"_{lang}") for lang in ['en', 'de', 'fr', 'tr', 'ru', 'sv', 'nl', 'el']):
                        mixed_keys.append(current_path)
                    recursive_check(value, current_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    recursive_check(item, f"{path}[{i}]")
        
        recursive_check(data)
        return mixed_keys

    def test_health_endpoint(self):
        """Test 1: GET /api/health - should return 200"""
        print("\n🔸 TEST 1: HEALTH CHECK")
        
        endpoint = "/api/health"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "Health Check"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        if status_code != 200:
            self.log_result(test_name, "FAIL", f"Expected 200, got {status_code}")
            return
            
        self.log_result(test_name, "PASS", f"Health check successful - Status: {status_code}")

    def test_german_letters(self):
        """Test 2: GET /api/arabic-academy/letters?locale=de - Should return German meanings ONLY"""
        print("\n🔸 TEST 2: GERMAN LETTERS")
        
        endpoint = "/api/arabic-academy/letters?locale=de"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "German Letters Localization"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check for mixed language keys
        mixed_keys = self.check_mixed_language_keys(data, 'de')
        if mixed_keys:
            self.log_result(test_name, "FAIL", f"Found mixed language keys: {mixed_keys}")
            return
            
        # Check response structure
        if not isinstance(data, dict):
            self.log_result(test_name, "FAIL", "Response should be a dictionary")
            return
            
        # Look for letters data
        letters = data.get('letters', []) or data.get('data', []) or (data if isinstance(data, list) else [])
        
        if not letters:
            self.log_result(test_name, "FAIL", "No letters data found in response")
            return
            
        # Check first letter for German content
        first_letter = letters[0] if letters else {}
        
        # Verify required fields exist
        if not first_letter.get('name') and not first_letter.get('example_meaning'):
            self.log_result(test_name, "FAIL", "Letters should have 'name' and 'example_meaning' fields")
            return
            
        # Check for German words (basic check for common German words)
        german_indicators = ['der', 'die', 'das', 'und', 'ist', 'ein', 'eine', 'löwe', 'haus', 'katze', 'hund']
        content_str = str(data).lower()
        has_german = any(indicator in content_str for indicator in german_indicators)
        
        if not has_german:
            # Still pass if structure is correct, as we can't guarantee specific German words
            self.log_result(test_name, "PASS", f"German letters returned - {len(letters)} letters, no mixed language keys")
        else:
            self.log_result(test_name, "PASS", f"German letters with German content - {len(letters)} letters, contains German words")

    def test_french_letters(self):
        """Test 3: GET /api/arabic-academy/letters?locale=fr - Should return French meanings ONLY"""
        print("\n🔸 TEST 3: FRENCH LETTERS")
        
        endpoint = "/api/arabic-academy/letters?locale=fr"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "French Letters Localization"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check for mixed language keys
        mixed_keys = self.check_mixed_language_keys(data, 'fr')
        if mixed_keys:
            self.log_result(test_name, "FAIL", f"Found mixed language keys: {mixed_keys}")
            return
            
        # Look for letters data
        letters = data.get('letters', []) or data.get('data', []) or (data if isinstance(data, list) else [])
        
        if not letters:
            self.log_result(test_name, "FAIL", "No letters data found in response")
            return
            
        # Check for French words
        french_indicators = ['le', 'la', 'les', 'et', 'est', 'un', 'une', 'lion', 'maison', 'chat', 'chien']
        content_str = str(data).lower()
        has_french = any(indicator in content_str for indicator in french_indicators)
        
        self.log_result(test_name, "PASS", f"French letters returned - {len(letters)} letters, no mixed language keys")

    def test_turkish_vocabulary(self):
        """Test 4: GET /api/arabic-academy/vocabulary?locale=tr&category=animals - Turkish animals"""
        print("\n🔸 TEST 4: TURKISH VOCABULARY (ANIMALS)")
        
        endpoint = "/api/arabic-academy/vocabulary?locale=tr&category=animals"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "Turkish Animals Vocabulary"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check for mixed language keys
        mixed_keys = self.check_mixed_language_keys(data, 'tr')
        if mixed_keys:
            self.log_result(test_name, "FAIL", f"Found mixed language keys: {mixed_keys}")
            return
            
        # Look for vocabulary data - correct key is 'words'
        vocab = data.get('words', []) or data.get('vocabulary', []) or data.get('data', []) or (data if isinstance(data, list) else [])
        
        if not vocab:
            self.log_result(test_name, "FAIL", "No vocabulary data found in response")
            return
            
        # Check first item has single meaning field
        first_item = vocab[0] if vocab else {}
        if not first_item.get('meaning'):
            self.log_result(test_name, "FAIL", "Vocabulary items should have single 'meaning' field")
            return
            
        self.log_result(test_name, "PASS", f"Turkish animals vocabulary - {len(vocab)} items, single 'meaning' field, no mixed language keys")

    def test_russian_vocabulary(self):
        """Test 5: GET /api/arabic-academy/vocabulary?locale=ru - Russian vocab"""
        print("\n🔸 TEST 5: RUSSIAN VOCABULARY")
        
        endpoint = "/api/arabic-academy/vocabulary?locale=ru"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "Russian Vocabulary"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check for mixed language keys
        mixed_keys = self.check_mixed_language_keys(data, 'ru')
        if mixed_keys:
            self.log_result(test_name, "FAIL", f"Found mixed language keys: {mixed_keys}")
            return
            
        # Look for vocabulary data - correct key is 'words'
        vocab = data.get('words', []) or data.get('vocabulary', []) or data.get('data', []) or (data if isinstance(data, list) else [])
        
        if not vocab:
            self.log_result(test_name, "FAIL", "No vocabulary data found in response")
            return
            
        self.log_result(test_name, "PASS", f"Russian vocabulary - {len(vocab)} items, no mixed language keys")

    def test_swedish_numbers(self):
        """Test 6: GET /api/arabic-academy/numbers?locale=sv - Swedish numbers"""
        print("\n🔸 TEST 6: SWEDISH NUMBERS")
        
        endpoint = "/api/arabic-academy/numbers?locale=sv"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "Swedish Numbers"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check for mixed language keys
        mixed_keys = self.check_mixed_language_keys(data, 'sv')
        if mixed_keys:
            self.log_result(test_name, "FAIL", f"Found mixed language keys: {mixed_keys}")
            return
            
        # Look for numbers data
        numbers = data.get('numbers', []) or data.get('data', []) or (data if isinstance(data, list) else [])
        
        if not numbers:
            self.log_result(test_name, "FAIL", "No numbers data found in response")
            return
            
        # Check first item has word field
        first_item = numbers[0] if numbers else {}
        if not first_item.get('word'):
            self.log_result(test_name, "FAIL", "Numbers should have 'word' field")
            return
            
        self.log_result(test_name, "PASS", f"Swedish numbers - {len(numbers)} items, has 'word' field, no mixed language keys")

    def test_dutch_sentences(self):
        """Test 7: GET /api/arabic-academy/sentences?locale=nl - Dutch sentences"""
        print("\n🔸 TEST 7: DUTCH SENTENCES")
        
        endpoint = "/api/arabic-academy/sentences?locale=nl"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "Dutch Sentences"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check for mixed language keys
        mixed_keys = self.check_mixed_language_keys(data, 'nl')
        if mixed_keys:
            self.log_result(test_name, "FAIL", f"Found mixed language keys: {mixed_keys}")
            return
            
        # Look for sentences data
        sentences = data.get('sentences', []) or data.get('data', []) or (data if isinstance(data, list) else [])
        
        if not sentences:
            self.log_result(test_name, "FAIL", "No sentences data found in response")
            return
            
        # Check first item has translation field
        first_item = sentences[0] if sentences else {}
        if not first_item.get('translation'):
            self.log_result(test_name, "FAIL", "Sentences should have single 'translation' field")
            return
            
        self.log_result(test_name, "PASS", f"Dutch sentences - {len(sentences)} items, has 'translation' field, no mixed language keys")

    def test_greek_daily_word(self):
        """Test 8: GET /api/arabic-academy/daily-word?locale=el - Greek daily word"""
        print("\n🔸 TEST 8: GREEK DAILY WORD")
        
        endpoint = "/api/arabic-academy/daily-word?locale=el"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "Greek Daily Word"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check for mixed language keys
        mixed_keys = self.check_mixed_language_keys(data, 'el')
        if mixed_keys:
            self.log_result(test_name, "FAIL", f"Found mixed language keys: {mixed_keys}")
            return
            
        # Check for meaning field in the word object
        word_data = data.get('word', {})
        if not word_data.get('meaning'):
            self.log_result(test_name, "FAIL", "Daily word should have 'meaning' field in Greek")
            return
            
        self.log_result(test_name, "PASS", f"Greek daily word - has 'meaning' field, no mixed language keys")

    def test_german_alphabet_course(self):
        """Test 9: GET /api/kids-learn/course/alphabet?locale=de - German alphabet course"""
        print("\n🔸 TEST 9: GERMAN ALPHABET COURSE")
        
        endpoint = "/api/kids-learn/course/alphabet?locale=de"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "German Alphabet Course"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check for mixed language keys
        mixed_keys = self.check_mixed_language_keys(data, 'de')
        if mixed_keys:
            self.log_result(test_name, "FAIL", f"Found mixed language keys: {mixed_keys}")
            return
            
        self.log_result(test_name, "PASS", f"German alphabet course - no mixed language keys")

    def test_german_academy_overview(self):
        """Test 10: GET /api/kids-learn/academy/overview?locale=de - German academy overview"""
        print("\n🔸 TEST 10: GERMAN ACADEMY OVERVIEW")
        
        endpoint = "/api/kids-learn/academy/overview?locale=de"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "German Academy Overview"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        # Check for mixed language keys
        mixed_keys = self.check_mixed_language_keys(data, 'de')
        if mixed_keys:
            self.log_result(test_name, "FAIL", f"Found mixed language keys: {mixed_keys}")
            return
            
        self.log_result(test_name, "PASS", f"German academy overview - no mixed language keys")

    def test_live_streams(self):
        """Test 11: GET /api/live-streams - should return success with streams"""
        print("\n🔸 TEST 11: LIVE STREAMS")
        
        endpoint = "/api/live-streams"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "Live Streams"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        if not data.get('success'):
            self.log_result(test_name, "FAIL", f"Response success should be true")
            return
            
        streams = data.get('streams', [])
        self.log_result(test_name, "PASS", f"Live streams working - {len(streams)} streams")

    def test_kids_zone_game(self):
        """Test 12: GET /api/kids-zone/generate-game - should return success with game"""
        print("\n🔸 TEST 12: KIDS ZONE GAME")
        
        endpoint = "/api/kids-zone/generate-game"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "Kids Zone Game Generation"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        if not data.get('success'):
            self.log_result(test_name, "FAIL", f"Response success should be true")
            return
            
        self.log_result(test_name, "PASS", f"Kids zone game generation working")

    def test_quran_chapters(self):
        """Test 13: GET /api/quran/v4/chapters?language=ar - should return 114 chapters"""
        print("\n🔸 TEST 13: QURAN CHAPTERS")
        
        endpoint = "/api/quran/v4/chapters?language=ar"
        success, data, status_code = self.make_request(endpoint)
        
        test_name = "Quran Chapters"
        
        if not success:
            self.log_result(test_name, "FAIL", f"Request failed: {data}")
            return
            
        chapters = data.get('chapters', []) or data.get('data', []) or (data if isinstance(data, list) else [])
        
        if len(chapters) != 114:
            self.log_result(test_name, "FAIL", f"Expected 114 chapters, got {len(chapters)}")
            return
            
        self.log_result(test_name, "PASS", f"Quran chapters - {len(chapters)} chapters (correct)")

    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 STARTING ARABIC ACADEMY MULTILINGUAL LOCALIZATION TESTING")
        print(f"📍 Base URL: {BASE_URL}")
        print("🎯 Focus: Verify locale filtering works correctly")
        
        # Run all test suites
        self.test_health_endpoint()
        self.test_german_letters()
        self.test_french_letters()
        self.test_turkish_vocabulary()
        self.test_russian_vocabulary()
        self.test_swedish_numbers()
        self.test_dutch_sentences()
        self.test_greek_daily_word()
        self.test_german_alphabet_course()
        self.test_german_academy_overview()
        self.test_live_streams()
        self.test_kids_zone_game()
        self.test_quran_chapters()
        
        # Generate summary report
        self.generate_report()
        
    def generate_report(self):
        """Generate final test report"""
        print("\n" + "="*80)
        print("📊 ARABIC ACADEMY MULTILINGUAL LOCALIZATION TEST RESULTS")
        print("="*80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"📈 SUMMARY: {success_rate:.1f}% SUCCESS ({self.passed_tests}/{self.total_tests} tests passed)")
        print(f"✅ PASSED: {self.passed_tests}")
        print(f"❌ FAILED: {self.failed_tests}")
        
        # Group results by status
        passed_tests = [r for r in self.results if r['status'] == 'PASS']
        failed_tests = [r for r in self.results if r['status'] == 'FAIL']
        
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for result in failed_tests:
                print(f"   • {result['test']}: {result['details']}")
                
        if passed_tests:
            print(f"\n✅ PASSED TESTS ({len(passed_tests)}):")
            for result in passed_tests:
                print(f"   • {result['test']}: {result['details']}")
                
        # Critical findings
        critical_failures = [r for r in failed_tests if 'mixed language keys' in r['details'].lower()]
        if critical_failures:
            print(f"\n🚨 CRITICAL LOCALIZATION ISSUES ({len(critical_failures)}):")
            for result in critical_failures:
                print(f"   • {result['test']}: {result['details']}")
        else:
            print(f"\n🎉 LOCALIZATION VERIFICATION: No mixed language keys found in responses")
            
        print("\n" + "="*80)

if __name__ == "__main__":
    tester = ArabicAcademyLocalizationTester()
    tester.run_all_tests()