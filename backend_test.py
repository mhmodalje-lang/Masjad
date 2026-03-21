#!/usr/bin/env python3
"""
Backend API Testing for Salah Teaching Endpoints
Islamic Prayer App - Testing Agent
"""

import requests
import json
import time
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://islamic-prayer-44.preview.emergentagent.com"

# Expected position values for validation
EXPECTED_POSITIONS = {
    'qiyam_niyyah', 'takbir', 'qiyam_qiraa', 'qiyam_fatiha', 
    'ruku', 'itidal', 'sujud_1', 'juloos', 'sujud_2', 'tashahhud', 'tasleem'
}

# Required fields for each salah step
REQUIRED_FIELDS = {
    'step', 'position', 'title', 'description', 
    'dhikr_ar', 'dhikr_transliteration', 'body_position'
}

class SalahAPITester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_result(self, test_name: str, status: str, details: str, response_time: float = 0):
        """Log test result"""
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'response_time': f"{response_time:.3f}s" if response_time > 0 else "N/A"
        }
        self.results.append(result)
        self.total_tests += 1
        if status == "✅ PASSED":
            self.passed_tests += 1
        print(f"{test_name}: {status}")
        print(f"  Details: {details}")
        if response_time > 0:
            print(f"  Response Time: {response_time:.3f}s")
        print()

    def test_endpoint(self, endpoint: str, expected_status: int = 200) -> Dict[str, Any]:
        """Test a single endpoint and return response data"""
        url = f"{BACKEND_URL}{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code != expected_status:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code} (expected {expected_status})",
                    'response_time': response_time
                }
            
            try:
                data = response.json()
                return {
                    'success': True,
                    'data': data,
                    'response_time': response_time
                }
            except json.JSONDecodeError:
                return {
                    'success': False,
                    'error': "Invalid JSON response",
                    'response_time': response_time
                }
                
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return {
                'success': False,
                'error': f"Request failed: {str(e)}",
                'response_time': response_time
            }

    def validate_salah_step(self, step: Dict[str, Any], step_number: int) -> List[str]:
        """Validate a single salah step structure"""
        errors = []
        
        # Check required fields exist
        for field in REQUIRED_FIELDS:
            if field not in step:
                errors.append(f"Missing required field: {field}")
        
        # Check non-dhikr fields are not empty
        non_dhikr_fields = ['step', 'position', 'title', 'description', 'body_position']
        for field in non_dhikr_fields:
            if field in step and (not step[field] or step[field] == ""):
                errors.append(f"Empty value for field: {field}")
        
        # dhikr_ar and dhikr_transliteration can be empty for step 1 (intention)
        if step_number != 1:  # Not the intention step
            if 'dhikr_ar' in step and (not step['dhikr_ar'] or step['dhikr_ar'] == ""):
                errors.append(f"Empty dhikr_ar for step {step_number} (dhikr required for non-intention steps)")
            if 'dhikr_transliteration' in step and (not step['dhikr_transliteration'] or step['dhikr_transliteration'] == ""):
                errors.append(f"Empty dhikr_transliteration for step {step_number} (dhikr required for non-intention steps)")
        
        # Validate step number
        if 'step' in step:
            if not isinstance(step['step'], int):
                errors.append(f"Step number should be integer, got {type(step['step'])}")
            elif step['step'] != step_number:
                errors.append(f"Step number mismatch: expected {step_number}, got {step['step']}")
        
        # Validate position
        if 'position' in step:
            if step['position'] not in EXPECTED_POSITIONS:
                errors.append(f"Invalid position '{step['position']}', expected one of: {EXPECTED_POSITIONS}")
        
        # Validate string fields
        string_fields = ['title', 'description', 'dhikr_ar', 'dhikr_transliteration', 'body_position']
        for field in string_fields:
            if field in step and not isinstance(step[field], str):
                errors.append(f"Field '{field}' should be string, got {type(step[field])}")
        
        return errors

    def test_health_endpoint(self):
        """Test health check endpoint"""
        result = self.test_endpoint("/api/health")
        
        if not result['success']:
            self.log_result(
                "GET /api/health",
                "❌ FAILED",
                result['error'],
                result['response_time']
            )
            return
        
        data = result['data']
        
        # Validate health response structure
        if 'status' not in data:
            self.log_result(
                "GET /api/health",
                "❌ FAILED",
                "Missing 'status' field in health response",
                result['response_time']
            )
            return
        
        if data['status'] != 'healthy':
            self.log_result(
                "GET /api/health",
                "❌ FAILED",
                f"Health status is '{data['status']}', expected 'healthy'",
                result['response_time']
            )
            return
        
        self.log_result(
            "GET /api/health",
            "✅ PASSED",
            f"Health check successful, status: {data['status']}",
            result['response_time']
        )

    def test_salah_endpoint(self, locale: str):
        """Test salah endpoint for specific locale"""
        endpoint = f"/api/kids-learn/salah?locale={locale}"
        result = self.test_endpoint(endpoint)
        
        if not result['success']:
            self.log_result(
                f"GET {endpoint}",
                "❌ FAILED",
                result['error'],
                result['response_time']
            )
            return
        
        data = result['data']
        
        # Check if response has steps
        if 'steps' not in data:
            self.log_result(
                f"GET {endpoint}",
                "❌ FAILED",
                "Response missing 'steps' field",
                result['response_time']
            )
            return
        
        steps = data['steps']
        
        # Validate step count
        if len(steps) != 11:
            self.log_result(
                f"GET {endpoint}",
                "❌ FAILED",
                f"Expected 11 steps, got {len(steps)}",
                result['response_time']
            )
            return
        
        # Validate each step
        all_errors = []
        for i, step in enumerate(steps, 1):
            step_errors = self.validate_salah_step(step, i)
            if step_errors:
                all_errors.extend([f"Step {i}: {error}" for error in step_errors])
        
        if all_errors:
            self.log_result(
                f"GET {endpoint}",
                "❌ FAILED",
                f"Validation errors: {'; '.join(all_errors[:5])}{'...' if len(all_errors) > 5 else ''}",
                result['response_time']
            )
            return
        
        # Validate locale-specific content
        locale_errors = self.validate_locale_content(steps, locale)
        if locale_errors:
            self.log_result(
                f"GET {endpoint}",
                "❌ FAILED",
                f"Locale validation errors: {'; '.join(locale_errors[:3])}{'...' if len(locale_errors) > 3 else ''}",
                result['response_time']
            )
            return
        
        # Extract sample data for verification
        sample_step = steps[0]
        sample_details = f"11 steps returned, sample step 1: position='{sample_step.get('position')}', title='{sample_step.get('title', '')[:30]}...'"
        
        self.log_result(
            f"GET {endpoint}",
            "✅ PASSED",
            sample_details,
            result['response_time']
        )

    def validate_locale_content(self, steps: List[Dict], locale: str) -> List[str]:
        """Validate locale-specific content"""
        errors = []
        
        for i, step in enumerate(steps, 1):
            if locale == 'ar':
                # For Arabic locale, check if Arabic content is present
                if 'title' in step and step['title']:
                    # Check if title contains Arabic characters
                    has_arabic = any('\u0600' <= char <= '\u06FF' for char in step['title'])
                    if not has_arabic:
                        errors.append(f"Step {i} title should contain Arabic text for Arabic locale")
                
                if 'description' in step and step['description']:
                    # Check if description contains Arabic characters
                    has_arabic = any('\u0600' <= char <= '\u06FF' for char in step['description'])
                    if not has_arabic:
                        errors.append(f"Step {i} description should contain Arabic text for Arabic locale")
            
            elif locale == 'en':
                # For English locale, check if content is in Latin script
                if 'title' in step and step['title']:
                    # Check if title is primarily Latin characters
                    has_arabic = any('\u0600' <= char <= '\u06FF' for char in step['title'])
                    if has_arabic:
                        errors.append(f"Step {i} title should be in English for English locale")
                
                if 'description' in step and step['description']:
                    # Check if description is primarily Latin characters
                    has_arabic = any('\u0600' <= char <= '\u06FF' for char in step['description'])
                    if has_arabic:
                        errors.append(f"Step {i} description should be in English for English locale")
            
            # dhikr_ar should always be in Arabic regardless of locale
            if 'dhikr_ar' in step and step['dhikr_ar']:
                has_arabic = any('\u0600' <= char <= '\u06FF' for char in step['dhikr_ar'])
                if not has_arabic:
                    errors.append(f"Step {i} dhikr_ar should contain Arabic text")
        
        return errors

    def run_all_tests(self):
        """Run all Salah API tests"""
        print("=" * 60)
        print("SALAH TEACHING API ENDPOINTS TESTING")
        print("=" * 60)
        print(f"Backend URL: {BACKEND_URL}")
        print()
        
        # Test health endpoint
        self.test_health_endpoint()
        
        # Test Arabic salah endpoint
        self.test_salah_endpoint('ar')
        
        # Test English salah endpoint
        self.test_salah_endpoint('en')
        
        # Print summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print()
        
        # Print detailed results
        for result in self.results:
            print(f"{result['test']}: {result['status']}")
            print(f"  {result['details']}")
            print(f"  Response Time: {result['response_time']}")
            print()
        
        return self.passed_tests == self.total_tests

if __name__ == "__main__":
    tester = SalahAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 ALL SALAH API TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED - CHECK DETAILS ABOVE")