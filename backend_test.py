#!/usr/bin/env python3
"""
Noor Academy Translation System Testing
Tests all Academy endpoints for proper multilingual localization
"""

import requests
import json
import sys
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = "https://content-moderation-266.preview.emergentagent.com"

class TranslationTester:
    def __init__(self):
        self.results = []
        self.failed_tests = []
        
    def log_result(self, test_name: str, success: bool, details: str):
        """Log test result"""
        status = "✅" if success else "❌"
        result = f"{status} {test_name}: {details}"
        print(result)
        self.results.append(result)
        if not success:
            self.failed_tests.append(test_name)
    
    def is_english_content(self, text: str) -> bool:
        """Check if content appears to be in English"""
        if not isinstance(text, str):
            return False
        
        # Common English words that shouldn't appear in other languages
        english_indicators = [
            "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by",
            "from", "about", "into", "through", "during", "before", "after", "above", "below",
            "up", "down", "out", "off", "over", "under", "again", "further", "then", "once",
            "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
            "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
            "own", "same", "so", "than", "too", "very", "can", "will", "just", "should",
            "now", "Allah", "Prophet", "Islam", "Muslim", "Quran", "prayer", "faith",
            "belief", "worship", "mosque", "pilgrimage", "fasting", "charity"
        ]
        
        text_lower = text.lower()
        english_word_count = sum(1 for word in english_indicators if f" {word} " in f" {text_lower} ")
        
        # If more than 2 English words found, likely English content
        return english_word_count > 2
    
    def has_translation_dict_structure(self, obj: Any) -> bool:
        """Check if object has translation dictionary structure like {ar: ..., en: ...}"""
        if not isinstance(obj, dict):
            return False
        
        # Check for language code keys
        lang_codes = ['ar', 'en', 'de', 'fr', 'tr', 'ru', 'sv', 'nl', 'el']
        dict_keys = set(obj.keys())
        lang_keys_found = dict_keys.intersection(lang_codes)
        
        return len(lang_keys_found) >= 2
    
    def check_content_translation(self, content: Any, locale: str, field_name: str) -> tuple[bool, str]:
        """Check if content is properly translated"""
        if content is None:
            return True, f"{field_name} is None (acceptable)"
        
        if isinstance(content, dict):
            if self.has_translation_dict_structure(content):
                return False, f"{field_name} contains raw translation dict: {list(content.keys())}"
        
        if isinstance(content, str):
            if locale != 'en' and self.is_english_content(content):
                return False, f"{field_name} appears to be in English despite locale={locale}"
        
        if isinstance(content, list):
            for i, item in enumerate(content):
                if isinstance(item, dict) and self.has_translation_dict_structure(item):
                    return False, f"{field_name}[{i}] contains raw translation dict"
                if isinstance(item, str) and locale != 'en' and self.is_english_content(item):
                    return False, f"{field_name}[{i}] appears to be in English despite locale={locale}"
        
        return True, f"{field_name} properly translated"
    
    def test_lesson_endpoint(self, endpoint: str, locale: str, expected_language: str) -> bool:
        """Test a lesson endpoint for proper translation"""
        url = f"{BACKEND_URL}{endpoint}"
        
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                self.log_result(f"{endpoint} ({locale})", False, 
                              f"HTTP {response.status_code}: {response.text[:200]}")
                return False
            
            data = response.json()
            
            if not data.get('success'):
                self.log_result(f"{endpoint} ({locale})", False, 
                              f"API returned success=false: {data.get('message', 'No message')}")
                return False
            
            # Handle different response structures (lesson vs adab)
            lesson = data.get('lesson', {}) or data.get('adab', {})
            if not lesson:
                self.log_result(f"{endpoint} ({locale})", False, "No lesson/adab data in response")
                return False
            
            # Check lesson content fields
            issues = []
            
            # Check lesson.content (main content)
            if 'content' in lesson:
                success, msg = self.check_content_translation(lesson['content'], locale, 'lesson.content')
                if not success:
                    issues.append(msg)
            
            # Check lesson.quiz
            if 'quiz' in lesson and lesson['quiz']:
                quiz = lesson['quiz']
                
                # Check quiz question
                if 'question' in quiz:
                    success, msg = self.check_content_translation(quiz['question'], locale, 'lesson.quiz.question')
                    if not success:
                        issues.append(msg)
                
                # Check quiz options
                if 'options' in quiz and isinstance(quiz['options'], list):
                    for i, option in enumerate(quiz['options']):
                        success, msg = self.check_content_translation(option, locale, f'lesson.quiz.options[{i}]')
                        if not success:
                            issues.append(msg)
                
                # Check correct answer
                if 'correct_answer' in quiz:
                    success, msg = self.check_content_translation(quiz['correct_answer'], locale, 'lesson.quiz.correct_answer')
                    if not success:
                        issues.append(msg)
            
            # Check lesson.rules (for adab endpoint)
            if 'rules' in lesson and isinstance(lesson['rules'], list):
                for i, rule in enumerate(lesson['rules']):
                    success, msg = self.check_content_translation(rule, locale, f'lesson.rules[{i}]')
                    if not success:
                        issues.append(msg)
            
            if issues:
                self.log_result(f"{endpoint} ({locale})", False, 
                              f"Translation issues: {'; '.join(issues)}")
                return False
            else:
                # Show sample content to verify translation
                sample_content = ""
                if 'content' in lesson and isinstance(lesson['content'], str):
                    sample_content = f"Content: '{lesson['content'][:100]}...'"
                elif 'quiz' in lesson and lesson['quiz'] and 'question' in lesson['quiz']:
                    sample_content = f"Quiz: '{lesson['quiz']['question'][:100]}...'"
                elif 'rules' in lesson and lesson['rules'] and len(lesson['rules']) > 0:
                    sample_content = f"Rules: '{lesson['rules'][0][:100]}...'"
                
                self.log_result(f"{endpoint} ({locale})", True, 
                              f"{expected_language} content verified. {sample_content}")
                return True
                
        except requests.exceptions.RequestException as e:
            self.log_result(f"{endpoint} ({locale})", False, f"Request failed: {str(e)}")
            return False
        except json.JSONDecodeError as e:
            self.log_result(f"{endpoint} ({locale})", False, f"Invalid JSON response: {str(e)}")
            return False
        except Exception as e:
            self.log_result(f"{endpoint} ({locale})", False, f"Unexpected error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all translation tests"""
        print("🧪 Testing Noor Academy Translation System")
        print("=" * 60)
        
        # Test cases from review request
        test_cases = [
            ("/api/kids-learn/academy/aqeedah/lesson/1?locale=de", "de", "German"),
            ("/api/kids-learn/academy/fiqh/lesson/1?locale=fr", "fr", "French"),
            ("/api/kids-learn/academy/seerah/lesson/1?locale=tr", "tr", "Turkish"),
            ("/api/kids-learn/academy/nooraniya/lesson/1?locale=ru", "ru", "Russian"),
            ("/api/kids-learn/academy/adab/1?locale=sv", "sv", "Swedish"),
            ("/api/kids-learn/academy/aqeedah/lesson/5?locale=el", "el", "Greek"),
            ("/api/kids-learn/academy/fiqh/lesson/3?locale=nl", "nl", "Dutch"),
        ]
        
        success_count = 0
        total_count = len(test_cases)
        
        for endpoint, locale, language in test_cases:
            if self.test_lesson_endpoint(endpoint, locale, language):
                success_count += 1
        
        print("\n" + "=" * 60)
        print(f"📊 TRANSLATION TEST SUMMARY")
        print(f"✅ Passed: {success_count}/{total_count}")
        print(f"❌ Failed: {len(self.failed_tests)}")
        
        if self.failed_tests:
            print(f"\n🚨 FAILED TESTS:")
            for test in self.failed_tests:
                print(f"   - {test}")
        
        return success_count == total_count

def main():
    """Main test execution"""
    tester = TranslationTester()
    
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"🎯 Testing Academy Translation Endpoints")
    print()
    
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 ALL TRANSLATION TESTS PASSED!")
        sys.exit(0)
    else:
        print("\n💥 SOME TRANSLATION TESTS FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()